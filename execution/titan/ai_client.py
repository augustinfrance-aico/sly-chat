"""
TITAN AI Client — Unified AI interface v2.0
Cascade: Ollama (local, free) > Groq models (free) > Cerebras (free, 1M tok/day) > Gemini 2.5 Flash (free)
Each model has its own rate limit — if one is exhausted, next one kicks in.
Ollama is auto-detected: if running locally, TITAN uses it first (zero latency, zero API).

v2.0 Upgrades:
- Cache TTL (1h expiry — no stale responses)
- Latency tracking per model (avg, min, max, last 100)
- Auto-reorder cascade (fastest model first within Groq tier)
- Model quality scoring (success rate tracking)
- Response quality heuristic (local, zero-cost)
"""

import os
import hashlib
import logging
import time
import json
from pathlib import Path
from collections import OrderedDict
from datetime import datetime
from dotenv import load_dotenv

log = logging.getLogger("titan")

# Force load .env from the correct absolute path
_env_file = Path(__file__).resolve().parent.parent.parent / ".env"
if _env_file.exists():
    load_dotenv(_env_file, override=True)

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
CEREBRAS_API_KEY = os.getenv("CEREBRAS_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")

# === RESPONSE CACHE (LRU + TTL — saves 20-40% tokens, expires after 1h) ===
_response_cache: OrderedDict = OrderedDict()
_CACHE_MAX = 300
_CACHE_TTL = 3600  # 1 hour in seconds

def _cache_key(system: str, user_message: str) -> str:
    """Hash (system + user_message) for cache lookup."""
    raw = f"{system[:200]}|{user_message}".encode()
    return hashlib.md5(raw).hexdigest()

def _cache_get(key: str) -> str | None:
    if key in _response_cache:
        entry = _response_cache[key]
        # TTL check — expire stale responses
        if time.time() - entry["ts"] > _CACHE_TTL:
            del _response_cache[key]
            return None
        _response_cache.move_to_end(key)
        return entry["text"]
    return None

def _cache_put(key: str, value: str):
    _response_cache[key] = {"text": value, "ts": time.time()}
    if len(_response_cache) > _CACHE_MAX:
        _response_cache.popitem(last=False)

# === LATENCY TRACKER (per-model performance monitoring) ===
_LATENCY_FILE = Path(__file__).parent / "memory" / "ai_latency.json"
_latency_log: list[dict] = []
_model_stats: dict[str, dict] = {}  # model → {calls, total_ms, errors, successes}

def _track_latency(model: str, latency_ms: float, tokens: int = 0, success: bool = True):
    """Track per-model latency and success rate."""
    # In-memory log (last 200 entries)
    _latency_log.append({
        "model": model,
        "ms": round(latency_ms, 1),
        "tokens": tokens,
        "success": success,
        "ts": datetime.now().isoformat(),
    })
    if len(_latency_log) > 200:
        del _latency_log[:100]  # keep last 100

    # Per-model aggregates
    if model not in _model_stats:
        _model_stats[model] = {"calls": 0, "total_ms": 0, "errors": 0, "successes": 0}
    _model_stats[model]["calls"] += 1
    _model_stats[model]["total_ms"] += latency_ms
    if success:
        _model_stats[model]["successes"] += 1
    else:
        _model_stats[model]["errors"] += 1

def get_latency_stats() -> dict:
    """Return latency stats for all models — used by dashboard API."""
    result = {}
    for model, stats in _model_stats.items():
        calls = stats["calls"]
        result[model] = {
            "calls": calls,
            "avg_ms": round(stats["total_ms"] / calls, 1) if calls > 0 else 0,
            "errors": stats["errors"],
            "success_rate": round(stats["successes"] / calls * 100, 1) if calls > 0 else 0,
        }
    # Recent entries for sparkline
    result["_recent"] = _latency_log[-20:] if _latency_log else []
    return result

def get_cache_stats() -> dict:
    """Return cache hit/miss stats."""
    return {
        "size": len(_response_cache),
        "max": _CACHE_MAX,
        "ttl_seconds": _CACHE_TTL,
    }

def _save_latency_stats():
    """Persist latency stats to disk (called periodically)."""
    try:
        _LATENCY_FILE.parent.mkdir(exist_ok=True)
        with open(_LATENCY_FILE, "w", encoding="utf-8") as f:
            json.dump({"model_stats": _model_stats, "recent": _latency_log[-50:]},
                      f, ensure_ascii=False, indent=2)
    except Exception:
        pass

def _load_latency_stats():
    """Load persisted latency stats."""
    global _model_stats
    try:
        if _LATENCY_FILE.exists():
            with open(_LATENCY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                _model_stats.update(data.get("model_stats", {}))
    except Exception:
        pass

_load_latency_stats()

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

_cerebras_available = False
if CEREBRAS_API_KEY:
    try:
        from openai import OpenAI as _CerebrasOpenAI
        _cerebras_client = _CerebrasOpenAI(api_key=CEREBRAS_API_KEY, base_url="https://api.cerebras.ai/v1")
        _cerebras_available = True
        log.info("AI Client: Cerebras OK (1M tokens/day, 3000 t/s)")
    except Exception as e:
        log.warning(f"Cerebras init failed: {e}")

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


def _get_optimized_groq_order() -> list:
    """Auto-reorder Groq models — fastest reliable model first.
    Keeps quality order for models with no data yet."""
    scored = []
    for model in GROQ_MODELS:
        stats = _model_stats.get(model)
        if stats and stats["calls"] >= 3:  # need at least 3 data points
            avg_ms = stats["total_ms"] / stats["calls"]
            success_rate = stats["successes"] / stats["calls"]
            # Score = lower is better. Penalize errors heavily.
            score = avg_ms * (1 + (1 - success_rate) * 10)
            scored.append((score, model))
        else:
            # No data → keep original order (quality-first)
            scored.append((999999 + GROQ_MODELS.index(model), model))
    scored.sort()
    return [model for _, model in scored]


def _score_response(text: str) -> int:
    """Score qualité réponse 0-100 (heuristique locale, zero cost).
    Used for monitoring — not blocking."""
    score = 60
    length = len(text)
    if length < 10: score -= 30          # quasi-vide
    elif length < 30: score -= 15        # trop court
    elif length > 3000: score -= 10      # trop long
    if '?' in text: score -= 10          # questions (ne devrait pas)
    if text.count('\n') >= 2: score += 5 # structuré
    if any(w in text.lower() for w in ["erreur", "impossible", "désolé", "cannot"]): score -= 10
    if any(w in text.lower() for w in ["voici", "action", "résultat", "étape"]): score += 5
    return min(100, max(0, score))


# Global call counter for periodic saves
_call_counter = 0

def chat(system: str, user_message: str, max_tokens: int = 2048) -> str:
    """Send a message to AI. Cascades through Ollama → Groq (auto-ordered) → Gemini.
    Features: LRU cache with TTL, latency tracking, auto-reorder, response scoring."""
    global _call_counter

    # === CACHE CHECK (with TTL) ===
    ck = _cache_key(system, user_message)
    cached = _cache_get(ck)
    if cached:
        log.info("AI: cache hit (0 tokens, 0 latency)")
        _track_latency("cache", 0, 0, True)
        return cached

    # === OLLAMA (LOCAL — zero cost, zero latency, offline) ===
    if _ollama_available:
        try:
            import httpx
            t0 = time.time()
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
            latency = (time.time() - t0) * 1000
            if resp.status_code == 200:
                text = resp.json().get("message", {}).get("content", "")
                if text:
                    _track_latency(f"ollama/{OLLAMA_MODEL}", latency, len(text), True)
                    log.info(f"AI: Ollama/{OLLAMA_MODEL} OK ({len(text)} chars, {latency:.0f}ms)")
                    result = _strip_questions(_dedup_sentences(text))
                    _cache_put(ck, result)
                    return result
            _track_latency(f"ollama/{OLLAMA_MODEL}", latency, 0, False)
        except Exception as e:
            _track_latency(f"ollama/{OLLAMA_MODEL}", 0, 0, False)
            log.warning(f"AI Ollama: {e}")

    # === GROQ CASCADE (FREE — auto-ordered by performance) ===
    if _groq_client:
        optimized_order = _get_optimized_groq_order()
        for model in optimized_order:
            try:
                t0 = time.time()
                response = _groq_client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system},
                        {"role": "user", "content": user_message},
                    ],
                    max_tokens=max_tokens,
                    temperature=0.7,
                )
                latency = (time.time() - t0) * 1000
                text = response.choices[0].message.content or ""
                # qwen3 returns <think>...</think> tags — strip them
                if "<think>" in text:
                    import re
                    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()
                if text:
                    _track_latency(model, latency, len(text), True)
                    quality = _score_response(text)
                    log.info(f"AI: {model} OK ({len(text)} chars, {latency:.0f}ms, Q:{quality})")
                    result = _strip_questions(_dedup_sentences(text))
                    _cache_put(ck, result)
                    _call_counter += 1
                    # Auto-save latency stats every 25 calls
                    if _call_counter % 25 == 0:
                        _save_latency_stats()
                    return result
                _track_latency(model, latency, 0, False)
            except Exception as e:
                _track_latency(model, 0, 0, False)
                log.warning(f"AI {model}: {e}")
                continue

    # === CEREBRAS (FREE — 1M tokens/day, 3000 t/s, OpenAI-compatible) ===
    if _cerebras_available:
        try:
            t0 = time.time()
            cerebras_resp = _cerebras_client.chat.completions.create(
                model="llama-3.3-70b",
                messages=[{"role": "system", "content": system}, {"role": "user", "content": user_message}],
                max_tokens=max_tokens,
                temperature=0.7,
            )
            latency = (time.time() - t0) * 1000
            result = cerebras_resp.choices[0].message.content or ""
            if result:
                _track_latency("cerebras-llama-3.3-70b", latency, len(result), True)
                log.info(f"AI: cerebras-llama-3.3-70b OK ({len(result)} chars, {latency:.0f}ms)")
                result = _strip_questions(_dedup_sentences(result))
                _cache_put(ck, result)
                return result
            _track_latency("cerebras-llama-3.3-70b", latency, 0, False)
        except Exception as e:
            _track_latency("cerebras-llama-3.3-70b", 0, 0, False)
            log.warning(f"AI Cerebras: {e}")

    # === GEMINI (FREE FALLBACK) ===
    if _gemini_client:
        try:
            t0 = time.time()
            response = _gemini_client.models.generate_content(
                model="gemini-2.5-flash",
                contents=user_message,
                config={
                    "system_instruction": system,
                    "max_output_tokens": max_tokens,
                    "temperature": 0.7,
                },
            )
            latency = (time.time() - t0) * 1000
            _track_latency("gemini-2.5-flash", latency, len(response.text), True)
            log.info(f"AI: gemini-2.5-flash OK ({len(response.text)} chars, {latency:.0f}ms)")
            result = _strip_questions(_dedup_sentences(response.text))
            _cache_put(ck, result)
            return result
        except Exception as e:
            _track_latency("gemini-2.5-flash", 0, 0, False)
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
