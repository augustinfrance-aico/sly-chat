"""
TITAN AI Client — Unified AI interface
Cascade: 6 Groq models (free, separate quotas) > Gemini (free)
Each model has its own rate limit — if one is exhausted, next one kicks in.
"""

import os
import logging
from pathlib import Path
from dotenv import load_dotenv

log = logging.getLogger("titan")

# Force load .env from the correct absolute path
_env_file = Path(__file__).resolve().parent.parent.parent / ".env"
if _env_file.exists():
    load_dotenv(_env_file, override=True)

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Groq models — ordered by quality, each has separate daily token quota
GROQ_MODELS = [
    "llama-3.3-70b-versatile",
    "meta-llama/llama-4-maverick-17b-128e-instruct",
    "meta-llama/llama-4-scout-17b-16e-instruct",
    "moonshotai/kimi-k2-instruct",
    "qwen/qwen3-32b",
    "llama-3.1-8b-instant",
]

_groq_client = None
_gemini_client = None

if GROQ_API_KEY:
    try:
        from groq import Groq
        _groq_client = Groq(api_key=GROQ_API_KEY)
        log.info(f"AI Client: Groq OK ({len(GROQ_MODELS)} models cascade)")
    except Exception as e:
        log.warning(f"Groq init failed: {e}")

if GEMINI_API_KEY:
    try:
        from google import genai
        _gemini_client = genai.Client(api_key=GEMINI_API_KEY)
        log.info("AI Client: Gemini OK (fallback)")
    except Exception as e:
        log.warning(f"Gemini init failed: {e}")


def _dedup_sentences(text: str) -> str:
    """Remove duplicate or near-duplicate sentences from AI response."""
    import re
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    seen = []
    result = []
    for s in sentences:
        normalized = re.sub(r'\s+', ' ', s).strip().lower()
        if normalized and normalized not in seen:
            seen.append(normalized)
            result.append(s)
    return ' '.join(result)


def chat(system: str, user_message: str, max_tokens: int = 2048) -> str:
    """Send a message to AI. Cascades through 6 Groq models then Gemini."""

    # === GROQ CASCADE (FREE — 6 models with separate quotas) ===
    if _groq_client:
        for model in GROQ_MODELS:
            try:
                response = _groq_client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system},
                        {"role": "user", "content": user_message},
                    ],
                    max_tokens=max_tokens,
                    temperature=0.7,
                )
                text = response.choices[0].message.content or ""
                # qwen3 returns <think>...</think> tags — strip them
                if "<think>" in text:
                    import re
                    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()
                if text:
                    log.info(f"AI: {model} OK")
                    return _dedup_sentences(text)
            except Exception as e:
                log.warning(f"AI {model}: {e}")
                continue

    # === GEMINI (FREE FALLBACK) ===
    if _gemini_client:
        try:
            response = _gemini_client.models.generate_content(
                model="gemini-2.0-flash",
                contents=user_message,
                config={
                    "system_instruction": system,
                    "max_output_tokens": max_tokens,
                    "temperature": 0.7,
                },
            )
            return _dedup_sentences(response.text)
        except Exception as e:
            log.warning(f"AI Gemini: {e}")

    return "Tous les providers IA sont temporairement satures. Reessaie dans quelques minutes."
