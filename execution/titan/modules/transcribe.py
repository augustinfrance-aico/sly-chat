"""
Transcribe Module — YouTube video → structured text transcript.
Pipeline: yt-dlp (audio download) → Groq Whisper (transcription) → cleanup.

Usage:
    from execution.titan.modules.transcribe import transcribe_youtube
    result = await transcribe_youtube("https://www.youtube.com/watch?v=xxx")
    # result = {"transcript": "...", "duration_sec": 360, "title": "...", "video_id": "..."}

Endpoint: POST /api/transcribe  (command_server.py)
Called by: n8n workflow "Content Liquefactor"
"""

import asyncio
import json
import logging
import os
import re
import subprocess
import tempfile
from pathlib import Path

log = logging.getLogger("titan.transcribe")

# Resolve ffmpeg path — prefer venv Scripts, then system PATH
_VENV_SCRIPTS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), ".venv", "Scripts")
FFMPEG_PATH = os.path.join(_VENV_SCRIPTS, "ffmpeg.exe") if os.path.exists(os.path.join(_VENV_SCRIPTS, "ffmpeg.exe")) else "ffmpeg"

# Max audio duration: 8 hours (Groq free tier = 8h/day total)
MAX_DURATION_SEC = 28800
# Max file size for Groq Whisper: 25MB
MAX_FILE_SIZE_MB = 25
# Chunk size for splitting long audio (15 min chunks — stays under 25MB at 64kbps mono)
CHUNK_DURATION_SEC = 900


def _extract_video_id(url: str) -> str | None:
    """Extract YouTube video ID from various URL formats."""
    patterns = [
        r'(?:v=|/v/|youtu\.be/)([a-zA-Z0-9_-]{11})',
        r'(?:embed/)([a-zA-Z0-9_-]{11})',
        r'(?:shorts/)([a-zA-Z0-9_-]{11})',
    ]
    for p in patterns:
        m = re.search(p, url)
        if m:
            return m.group(1)
    return None


def _download_audio(url: str, output_dir: str) -> dict:
    """Download audio from YouTube using yt-dlp. Returns metadata dict."""
    video_id = _extract_video_id(url)
    if not video_id:
        raise ValueError(f"URL YouTube invalide: {url}")

    output_path = os.path.join(output_dir, f"{video_id}.mp3")

    ffmpeg_dir = os.path.dirname(FFMPEG_PATH) if FFMPEG_PATH != "ffmpeg" else None
    cmd = [
        "yt-dlp",
        "-x",                           # Extract audio only
        "--audio-format", "mp3",         # Convert to mp3
        "--audio-quality", "9",          # Low quality (speech only, smaller file)
        "--no-playlist",                 # Single video only
        "-o", output_path,
        "--print-json",                  # Output metadata as JSON
        "--no-simulate",                 # Actually download
    ]
    if ffmpeg_dir:
        cmd.extend(["--ffmpeg-location", ffmpeg_dir])
    cmd.append(url)

    log.info(f"Downloading audio: {video_id}")
    result = subprocess.run(
        cmd, capture_output=True, text=True, timeout=1200,  # 20 min timeout for long videos
        env={**os.environ, "PYTHONIOENCODING": "utf-8"}
    )

    if result.returncode != 0:
        err = result.stderr[:500] if result.stderr else "Unknown error"
        raise RuntimeError(f"yt-dlp failed: {err}")

    # Parse metadata from stdout (last JSON line)
    metadata = {}
    for line in result.stdout.strip().split("\n"):
        line = line.strip()
        if line.startswith("{"):
            try:
                metadata = json.loads(line)
            except json.JSONDecodeError:
                pass

    title = metadata.get("title", video_id)
    duration = metadata.get("duration", 0)

    if duration > MAX_DURATION_SEC:
        raise ValueError(f"Video trop longue: {duration}s (max {MAX_DURATION_SEC}s = {MAX_DURATION_SEC // 3600}h)")

    # Find the actual output file (yt-dlp may add extension)
    actual_path = output_path
    if not os.path.exists(actual_path):
        # Try common variations
        for ext in [".mp3", ".m4a", ".opus", ".webm"]:
            candidate = os.path.join(output_dir, f"{video_id}{ext}")
            if os.path.exists(candidate):
                actual_path = candidate
                break

    if not os.path.exists(actual_path):
        raise FileNotFoundError(f"Audio file not found after download: {output_path}")

    file_size_mb = os.path.getsize(actual_path) / (1024 * 1024)
    log.info(f"Downloaded: {title} ({duration}s, {file_size_mb:.1f}MB)")

    return {
        "path": actual_path,
        "title": title,
        "duration": duration,
        "video_id": video_id,
        "file_size_mb": file_size_mb,
    }


def _split_audio(audio_path: str, output_dir: str, chunk_sec: int = CHUNK_DURATION_SEC) -> list[str]:
    """Split audio file into chunks using ffmpeg. Returns list of chunk paths."""
    chunks = []
    # Get duration
    probe = subprocess.run(
        [FFMPEG_PATH, "-i", audio_path, "-f", "null", "-"],
        capture_output=True, text=True, timeout=60
    )
    # Extract duration from ffmpeg output
    duration_match = re.search(r"Duration: (\d+):(\d+):(\d+)", probe.stderr)
    if not duration_match:
        # Single chunk if can't determine duration
        return [audio_path]

    h, m, s = int(duration_match.group(1)), int(duration_match.group(2)), int(duration_match.group(3))
    total_sec = h * 3600 + m * 60 + s

    if total_sec <= chunk_sec + 30:  # Small margin
        return [audio_path]

    # Split into chunks
    for i, start in enumerate(range(0, total_sec, chunk_sec)):
        chunk_path = os.path.join(output_dir, f"chunk_{i:03d}.mp3")
        cmd = [
            FFMPEG_PATH, "-y",
            "-ss", str(start),
            "-i", audio_path,
            "-t", str(chunk_sec),
            "-acodec", "libmp3lame",
            "-ab", "64k",              # Low bitrate to stay under 25MB
            "-ar", "16000",            # 16kHz enough for speech
            "-ac", "1",                # Mono
            chunk_path,
        ]
        subprocess.run(cmd, capture_output=True, timeout=120)
        if os.path.exists(chunk_path) and os.path.getsize(chunk_path) > 0:
            chunks.append(chunk_path)

    return chunks if chunks else [audio_path]


def _transcribe_chunk_groq(audio_path: str, max_retries: int = 5) -> str:
    """Transcribe a single audio chunk using Groq Whisper API. Auto-retries on rate limit."""
    import time as _time

    api_key = os.getenv("GROQ_API_KEY", "")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY not configured")

    file_size = os.path.getsize(audio_path) / (1024 * 1024)
    if file_size > MAX_FILE_SIZE_MB:
        raise ValueError(f"Chunk trop gros: {file_size:.1f}MB (max {MAX_FILE_SIZE_MB}MB)")

    from groq import Groq
    client = Groq(api_key=api_key)

    for attempt in range(max_retries):
        try:
            with open(audio_path, "rb") as f:
                result = client.audio.transcriptions.create(
                    model="whisper-large-v3-turbo",
                    file=f,
                    language="en",
                    response_format="text",
                )
            return result if isinstance(result, str) else str(result)
        except Exception as e:
            err_str = str(e)
            if "429" in err_str or "rate_limit" in err_str:
                # Extract wait time from error message (e.g. "try again in 6m27.5s")
                wait_match = re.search(r"try again in (\d+)m([\d.]+)s", err_str)
                if wait_match:
                    wait_sec = int(wait_match.group(1)) * 60 + float(wait_match.group(2)) + 5
                else:
                    wait_sec = 120 * (attempt + 1)  # Escalating backoff
                log.warning(f"Rate limit hit, waiting {wait_sec:.0f}s before retry {attempt + 1}/{max_retries}")
                _time.sleep(wait_sec)
            else:
                raise
    raise RuntimeError(f"Groq transcription failed after {max_retries} retries (rate limit)")


async def transcribe_youtube(url: str) -> dict:
    """
    Full pipeline: YouTube URL → transcript text.
    Returns: {transcript, title, duration_sec, video_id, chunks_count}
    """
    with tempfile.TemporaryDirectory(prefix="sly_transcribe_") as tmpdir:
        # Step 1: Download audio
        meta = await asyncio.to_thread(_download_audio, url, tmpdir)

        # Step 2: Split if needed (long videos)
        chunks = await asyncio.to_thread(_split_audio, meta["path"], tmpdir)
        log.info(f"Audio split into {len(chunks)} chunk(s)")

        # Step 3: Transcribe each chunk
        transcripts = []
        for i, chunk_path in enumerate(chunks):
            log.info(f"Transcribing chunk {i + 1}/{len(chunks)}...")
            text = await asyncio.to_thread(_transcribe_chunk_groq, chunk_path)
            if text and text.strip():
                transcripts.append(text.strip())

        full_transcript = "\n\n".join(transcripts)

        if not full_transcript.strip():
            raise RuntimeError("Transcription vide — la video n'a peut-etre pas de contenu audio")

        return {
            "transcript": full_transcript,
            "title": meta["title"],
            "duration_sec": meta["duration"],
            "video_id": meta["video_id"],
            "chunks_count": len(chunks),
            "char_count": len(full_transcript),
        }


def transcribe_youtube_sync(url: str) -> dict:
    """Synchronous wrapper for transcribe_youtube."""
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(transcribe_youtube(url))
    finally:
        loop.close()
