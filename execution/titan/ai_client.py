"""
TITAN AI Client — Unified AI interface
Cascade: Ollama (local, free) > 6 Groq models (free, separate quotas) > Gemini (free)
Each model has its own rate limit — if one is exhausted, next one kicks in.
Ollama is auto-detected: if running locally, TITAN uses it first (zero latency, zero API).
Includes response cache (LRU) to save tokens on repeated questions.
"""

import os
import hashlib
import logging
from pathlib import Path
from collections import OrderedDict
from dotenv import load_dotenv

log = logging.getLogger("titan")

# Force load .env from the correct absolute path
_env_file = Path(__file__).resolve().parent.parent.parent / ".env"
if _env_file.exists():
    load_dotenv(_env_file, override=True)

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")

# === RESPONSE CACHE (LRU — saves 20-40% tokens on repeated questions) ===
_response_cache: OrderedDict = OrderedDict()
_CACHE_MAX = 200

def _cache_key(system: str, user_message: str) -> str:
    """Hash (system + user_message) for cache lookup."""
    raw = f"{system[:200]}|{user_message}".encode()
    return hashlib.md5(raw).hexdigest()

def _cache_get(key: str) -> str | None:
    if key in _response_cache:
        _response_cache.move_to_end(key)
        return _response_cache[key]
    return None

def _cache_put(key: str, value: str):
    _response_cache[key] = value
    if len(_response_cache) > _CACHE_MAX:
        _response_cache.popitem(last=False)

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
_ollama_available = False

# === OLLAMA (LOCAL — zero cost, zero latency) ===
try:
    import httpx
    _ollama_check = httpx.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=2)
    if _ollama_check.status_code == 200:
        _ollama_available = True
        _ollama_models = [m["name"] for m in _ollama_check.json().get("models", [])]
        # Auto-select best available model
        if OLLAMA_MODEL not in _ollama_models and _ollama_models:
            OLLAMA_MODEL = _ollama_models[0]
        log.info(f"AI Client: Ollama OK (local — {OLLAMA_MODEL})")
except Exception:
    # Ollama not running or httpx not installed — no problem, skip
    pass

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


def _strip_questions(text: str) -> str:
    """Remove ALL question sentences from AI response — hard filter, no trust in model."""
    import re
    # Split on sentence-ending punctuation, keeping delimiters
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    # Also split on newlines
    expanded = []
    for s in sentences:
        expanded.extend(line.strip() for line in s.split('\n') if line.strip())
    # Keep only non-question sentences
    filtered = [s for s in expanded if not s.endswith('?')]
    if not filtered:
        # Everything was a question — strip the ? and return first sentence
        first = expanded[0] if expanded else text
        return re.sub(r'\?+$', '.', first)
    return ' '.join(filtered)


def chat(system: str, user_message: str, max_tokens: int = 2048) -> str:
    """Send a message to AI. Cascades through 6 Groq models then Gemini.
    Includes LRU cache to avoid burning tokens on repeated questions."""

    # === CACHE CHECK ===
    ck = _cache_key(system, user_message)
    cached = _cache_get(ck)
    if cached:
        log.info("AI: cache hit (0 tokens)")
        return cached

    # === OLLAMA (LOCAL — zero cost, zero latency, offline) ===
    if _ollama_available:
        try:
            import httpx
            resp = httpx.post(
                f"{OLLAMA_BASE_URL}/api/chat",
                json={
                    "model": OLLAMA_MODEL,
                    "messages": [
                        {"role": "system", "content": system},
                        {"role": "user", "content": user_message},
                    ],
                    "stream": False,
                    "options": {"num_predict": max_tokens, "temperature": 0.7},
                },
                timeout=60,
            )
            if resp.status_code == 200:
                text = resp.json().get("message", {}).get("content", "")
                if text:
                    log.info(f"AI: Ollama/{OLLAMA_MODEL} OK ({len(text)} chars)")
                    result = _strip_questions(_dedup_sentences(text))
                    _cache_put(ck, result)
                    return result
        except Exception as e:
            log.warning(f"AI Ollama: {e}")

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
                    log.info(f"AI: {model} OK ({len(text)} chars)")
                    result = _strip_questions(_dedup_sentences(text))
                    _cache_put(ck, result)
                    return result
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
            log.info(f"AI: gemini-2.0-flash OK ({len(response.text)} chars)")
            result = _strip_questions(_dedup_sentences(response.text))
            _cache_put(ck, result)
            return result
        except Exception as e:
            log.warning(f"AI Gemini: {e}")

    return "Tous les providers IA sont temporairement satures. Reessaie dans quelques minutes."


def ollama_status() -> str:
    """Return Ollama status — available models, current model, local or not."""
    global _ollama_available, OLLAMA_MODEL
    try:
        import httpx
        resp = httpx.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=3)
        if resp.status_code == 200:
            models = [m["name"] for m in resp.json().get("models", [])]
            _ollama_available = True
            active = f"✅ Actif : {OLLAMA_MODEL}" if OLLAMA_MODEL in models else "⚠️ Modèle configuré non trouvé"
            return (
                f"🦙 OLLAMA LOCAL\n"
                f"━━━━━━━━━━━━━━━\n"
                f"{active}\n"
                f"Modèles installés : {', '.join(models) if models else 'Aucun'}\n"
                f"URL : {OLLAMA_BASE_URL}\n"
                f"Cascade : Ollama → Groq (6) → Gemini"
            )
        return "❌ Ollama — serveur ne répond pas."
    except Exception:
        _ollama_available = False
        return "❌ Ollama non détecté. Lance 'ollama serve' pour activer le mode local."


def ollama_set_model(model_name: str) -> str:
    """Switch the active Ollama model."""
    global OLLAMA_MODEL, _ollama_available
    try:
        import httpx
        resp = httpx.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=3)
        if resp.status_code == 200:
            models = [m["name"] for m in resp.json().get("models", [])]
            if model_name in models:
                OLLAMA_MODEL = model_name
                _ollama_available = True
                return f"✅ Modèle Ollama → {model_name}"
            # Check partial match
            matches = [m for m in models if model_name in m]
            if matches:
                OLLAMA_MODEL = matches[0]
                _ollama_available = True
                return f"✅ Modèle Ollama → {matches[0]}"
            return f"❌ Modèle '{model_name}' non trouvé. Dispo : {', '.join(models)}"
    except Exception:
        return "❌ Ollama non disponible."
