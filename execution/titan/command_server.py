"""
TITAN-COMMAND Server — Mini serveur local pour alimenter le dashboard.
Sert les données JSON de TITAN en temps réel + API pour la console + LLM chat.

Lancement : python -m execution.titan.command_server
Puis ouvrir : http://localhost:7777

API Endpoints:
  GET  /api/all           — Toutes les données en un call
  GET  /api/stats         — Dashboard stats
  GET  /api/conversations — Historique conversations
  GET  /api/gamification  — XP, level, streak
  GET  /api/health        — Santé systèmes
  GET  /api/system        — CPU, RAM, disk
  GET  /api/directives    — Liste des directives .md
  GET  /api/directive?name=X — Contenu d'une directive
  GET  /api/extensions    — État des extensions/modules
  GET  /api/modules       — Liste des modules TITAN avec statut
  GET  /api/memory        — Contenu titan_memory.json (lecture)
  GET  /api/evolution     — Données evolution.json complètes
  GET  /api/pokedex       — Agents formatés pour le Pokédex (agents, types, forms)
  GET  /api/bosses        — Boss fights et trainer data
  GET  /api/agents        — Liste des 25 agents avec pôle, rôle, emoji
  GET  /api/ticker        — News HN pour ticker (cache 5 min)
  POST /api/memory        — Sauvegarder key-value {key, value, category}
  POST /api/chat          — Chat avec le LLM (Ollama/Groq/Gemini)
  POST /api/extension     — Activer/désactiver une extension
  POST /api/anneal        — Déclencher self-annealing
"""

import json
import logging
import os
import re
import shutil
import subprocess
import time
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from socketserver import ThreadingMixIn
from urllib.parse import urlparse, parse_qs

# Paths
ROOT = Path(__file__).resolve().parent.parent.parent
TITAN_DIR = ROOT / "execution" / "titan"
MEMORY_DIR = TITAN_DIR / "memory"
PORTFOLIOS_DIR = ROOT / "portfolios"
DIRECTIVES_DIR = ROOT / "directives"
PERSONNALITES_DIR = ROOT / "personnalites"
EXTENSIONS_FILE = MEMORY_DIR / "extensions.json"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [CMD-SRV] %(message)s")
log = logging.getLogger("titan.command")

PORT = 7777
MAX_MESSAGE_LENGTH = 32_000  # chars max pour /api/chat
MAX_KEY_LENGTH = 256
MAX_VALUE_LENGTH = 10_000

# ============================================================
# CACHE SIMPLE — TTL en secondes
# Format : { path_key: (data, timestamp_float) }
# ============================================================
_cache: dict = {}
_CACHE_TTL_DEFAULT = 10      # 10 sec pour fichiers JSON (stats, gamification, etc.)
_CACHE_TTL_TICKER = 300      # 5 min pour le ticker HN


def _cache_get(key: str, ttl: float = _CACHE_TTL_DEFAULT):
    """Retourne la donnée si le cache est frais, sinon None."""
    entry = _cache.get(key)
    if entry is None:
        return None
    data, ts = entry
    if time.monotonic() - ts < ttl:
        return data
    return None


def _cache_set(key: str, data):
    """Stocke dans le cache avec timestamp courant."""
    _cache[key] = (data, time.monotonic())


def _cache_invalidate(key: str):
    """Supprime une entrée du cache."""
    _cache.pop(key, None)


# ============================================================
# AGENTS DU BUILDING — données pour /api/agents
# ============================================================
_AGENTS_LIST = [
    # OMEGA-CORE
    {"name": "OMEGA",     "pole": "CORE",  "role": "Vision 360°, arbitrage",          "emoji": "🌀", "gov": True},
    # PÔLE R — RECON
    {"name": "MURPHY",    "pole": "RECON", "role": "Structure, priorisation",          "emoji": "🏗️", "gov": True},
    {"name": "ORACLE",    "pole": "RECON", "role": "Prédiction, timing",               "emoji": "🔮", "gov": True},
    {"name": "MAYA",      "pole": "RECON", "role": "Scanner niches",                   "emoji": "🗺️", "gov": False},
    {"name": "GHOST",     "pole": "RECON", "role": "Veille concurrentielle",           "emoji": "👻", "gov": False},
    {"name": "NASH",      "pole": "RECON", "role": "Data, pricing",                    "emoji": "📊", "gov": False},
    {"name": "CYPHER",    "pole": "RECON", "role": "KPIs, benchmarks",                 "emoji": "🔢", "gov": False},
    {"name": "RICK",      "pole": "RECON", "role": "Angles disruptifs",                "emoji": "⚡", "gov": False},
    # PÔLE F — FORGE
    {"name": "NIKOLA",    "pole": "FORGE", "role": "Architecture technique",           "emoji": "⚙️", "gov": True},
    {"name": "PHILOMÈNE", "pole": "FORGE", "role": "Qualité rédactionnelle",           "emoji": "✒️", "gov": True},
    {"name": "FORGE",     "pole": "FORGE", "role": "Exécution brute",                  "emoji": "🔨", "gov": False},
    {"name": "BASQUIAT",  "pole": "FORGE", "role": "Créatif, visuels",                 "emoji": "🎨", "gov": False},
    {"name": "ZARA",      "pole": "FORGE", "role": "Contenu social",                   "emoji": "📱", "gov": False},
    {"name": "MURRAY",    "pole": "FORGE", "role": "Long-form, newsletters",           "emoji": "📝", "gov": False},
    {"name": "LEON",      "pole": "FORGE", "role": "Scripts vidéo",                    "emoji": "🎬", "gov": False},
    {"name": "BALOO",     "pole": "FORGE", "role": "Vulgarisation",                    "emoji": "🐻", "gov": False},
    # PÔLE D — DEPLOY
    {"name": "BAGHEERA",  "pole": "DEPLOY","role": "Orchestration",                    "emoji": "🐆", "gov": True},
    {"name": "SPARTAN",   "pole": "DEPLOY","role": "Discipline, cadence",              "emoji": "🛡️", "gov": True},
    {"name": "BELFORT",   "pole": "DEPLOY","role": "Vente, closing",                   "emoji": "💼", "gov": False},
    {"name": "STANLEY",   "pole": "DEPLOY","role": "Growth, deals",                    "emoji": "📈", "gov": False},
    {"name": "SLY",       "pole": "DEPLOY","role": "Acquisition low-cost",             "emoji": "🦊", "gov": False},
    {"name": "VITO",      "pole": "DEPLOY","role": "Relations long terme",             "emoji": "🤝", "gov": False},
    {"name": "BENTLEY",   "pole": "DEPLOY","role": "Premium, positionnement",          "emoji": "💎", "gov": False},
    {"name": "GRIMALDI",  "pole": "DEPLOY","role": "Audit coûts, financement",         "emoji": "💰", "gov": False},
    {"name": "X-O1",      "pole": "DEPLOY","role": "Stabilité système, audit setup",   "emoji": "🤖", "gov": False},
    {"name": "ZEN",       "pole": "DEPLOY","role": "Contrôle qualité, recul",          "emoji": "🧘", "gov": False},
]


# ============================================================
# TICKER — fetch HN RSS côté serveur (évite CORS)
# ============================================================
_TICKER_FALLBACK = [
    {"title": "TITAN-COMMAND en ligne", "url": "#", "source": "TITAN"},
    {"title": "Empire AICO — Boucle R→F→D active", "url": "#", "source": "TITAN"},
    {"title": "Agents du Building opérationnels", "url": "#", "source": "TITAN"},
    {"title": "Cascade Groq — Zéro coût confirmé", "url": "#", "source": "TITAN"},
    {"title": "Mille Ruisseaux — flux continus", "url": "#", "source": "TITAN"},
]


def _fetch_ticker() -> list:
    """Fetch HN newest RSS, parse XML, retourne liste de dicts."""
    cached = _cache_get("ticker", _CACHE_TTL_TICKER)
    if cached is not None:
        return cached

    try:
        url = "https://hnrss.org/newest?count=8"
        req = urllib.request.Request(url, headers={"User-Agent": "TITAN-COMMAND/2.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
        root = ET.fromstring(raw)
        items = []
        for item in root.findall(".//item"):
            title_el = item.find("title")
            link_el = item.find("link")
            if title_el is not None and link_el is not None:
                title = (title_el.text or "").strip()
                link = (link_el.text or "#").strip()
                if title:
                    items.append({"title": title, "url": link, "source": "HackerNews"})
        if items:
            _cache_set("ticker", items)
            return items
    except Exception as e:
        log.warning(f"Ticker fetch error: {e} — fallback statique")

    _cache_set("ticker", _TICKER_FALLBACK)
    return _TICKER_FALLBACK


# ============================================================
# HELPERS
# ============================================================

def _read_body(handler) -> dict:
    """Read JSON body from POST request. Returns {} on any error."""
    try:
        length = int(handler.headers.get("Content-Length", 0))
    except (ValueError, TypeError):
        log.warning("Invalid Content-Length header")
        return {}
    if length <= 0:
        return {}
    if length > 1_000_000:  # 1MB max
        log.warning(f"Request body too large: {length} bytes")
        return {}
    try:
        raw = handler.rfile.read(length)
        return json.loads(raw.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        log.warning(f"Invalid JSON body: {e}")
        return {}
    except Exception as e:
        log.error(f"Error reading request body: {e}")
        return {}


def _get_extensions() -> dict:
    """Get extensions state from file or defaults."""
    defaults = {
        "journal":         {"name": "Journal du soir",        "icon": "📓", "desc": "3 questions Zen chaque soir",                "enabled": True,  "category": "vie"},
        "coach":           {"name": "Coach silencieux",        "icon": "🧠", "desc": "Nudge 1x/jour basé sur tes patterns",        "enabled": True,  "category": "vie"},
        "library":         {"name": "Library auto",            "icon": "📚", "desc": "Extraction automatique de gems",             "enabled": True,  "category": "systeme"},
        "auto_healer":     {"name": "Auto-Healer",             "icon": "🏥", "desc": "Détection et réparation auto des erreurs",   "enabled": True,  "category": "systeme"},
        "morning_digest":  {"name": "Morning Digest",          "icon": "☀️", "desc": "5 bullets IA chaque matin à 8h",             "enabled": True,  "category": "info"},
        "aggregator":      {"name": "Aggregator",              "icon": "🗞️", "desc": "HackerNews + RSS digest à 14h",              "enabled": True,  "category": "info"},
        "film":            {"name": "Film Building",           "icon": "🎬", "desc": "Scripts cinéma de l'empire",                 "enabled": True,  "category": "creatif"},
        "clones":          {"name": "Content Clones",          "icon": "🧬", "desc": "1 idée → 8 formats",                         "enabled": True,  "category": "creatif"},
        "portfolio_live":  {"name": "Portfolio Live",          "icon": "📊", "desc": "Auto-génération HTML portfolio",             "enabled": True,  "category": "deploy"},
        "empire_visual":   {"name": "Empire Visual",           "icon": "🎨", "desc": "Branding & identité visuelle",               "enabled": True,  "category": "creatif"},
        "mega_prompt":     {"name": "Mega-Prompt",             "icon": "💊", "desc": "Export Building vers tout LLM",              "enabled": True,  "category": "systeme"},
        "ollama":          {"name": "Ollama Local",            "icon": "🦙", "desc": "LLM local gratuit, zéro API",                "enabled": True,  "category": "systeme"},
        "gamification":    {"name": "Gamification",            "icon": "🎮", "desc": "XP, niveaux, achievements",                  "enabled": True,  "category": "vie"},
        "finance":         {"name": "Finance",                  "icon": "💰", "desc": "Module désactivé",                         "enabled": False, "category": "info"},
        "news":            {"name": "News IA",                 "icon": "📰", "desc": "Synthèse IA des actualités",                 "enabled": True,  "category": "info"},
        "upwork":          {"name": "Upwork Pipeline",         "icon": "💼", "desc": "Veille et pitch Upwork",                     "enabled": True,  "category": "deploy"},
        "voice":           {"name": "Vocaux",                  "icon": "🎤", "desc": "Transcription et traitement vocaux",         "enabled": True,  "category": "vie"},
        "president":       {"name": "Jacques (Président)",     "icon": "🎩", "desc": "Directeur stratégique interne",              "enabled": True,  "category": "systeme"},
    }
    try:
        if EXTENSIONS_FILE.exists():
            saved = json.loads(EXTENSIONS_FILE.read_text(encoding="utf-8"))
            for k, v in saved.items():
                if k in defaults:
                    defaults[k]["enabled"] = v.get("enabled", True)
            return defaults
    except Exception as e:
        log.error(f"Error loading extensions: {e}")
    return defaults


def _save_extensions(exts: dict):
    """Save extensions state."""
    EXTENSIONS_FILE.write_text(json.dumps(exts, ensure_ascii=False, indent=2), encoding="utf-8")


def _chat_llm(message: str, system: str = "") -> str:
    """Send a message to available LLM — Ollama first, then Groq, then Gemini."""
    if not system:
        system = (
            "Tu es TITAN, l'assistant IA d'Augustin. Tu réponds en français, "
            "de manière directe et concise. Tu es dans l'interface TITAN-COMMAND."
        )

    # Try Ollama first
    try:
        import httpx
        resp = httpx.post(
            "http://localhost:11434/api/chat",
            json={
                "model": os.getenv("OLLAMA_MODEL", "llama3.1:8b"),
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": message},
                ],
                "stream": False,
                "options": {"num_predict": 1024, "temperature": 0.7},
            },
            timeout=15,
        )
        if resp.status_code == 200:
            text = resp.json().get("message", {}).get("content", "")
            if text:
                return f"[🦙 Ollama] {text}"
    except Exception as e:
        log.error(f"Ollama LLM error: {e}")

    # Try Groq
    try:
        from dotenv import load_dotenv
        load_dotenv(ROOT / ".env")
        api_key = os.getenv("GROQ_API_KEY", "")
        if api_key:
            from groq import Groq
            client = Groq(api_key=api_key)
            models = ["llama-3.3-70b-versatile", "meta-llama/llama-4-maverick-17b-128e-instruct", "llama-3.1-8b-instant"]
            for model in models:
                try:
                    r = client.chat.completions.create(
                        model=model,
                        messages=[{"role": "system", "content": system}, {"role": "user", "content": message}],
                        max_tokens=1024,
                        temperature=0.7,
                    )
                    text = r.choices[0].message.content or ""
                    if text:
                        return f"[⚡ Groq/{model.split('/')[-1]}] {text}"
                except Exception as e:
                    log.error(f"Groq model {model} error: {e}")
                    continue
    except Exception as e:
        log.error(f"Groq LLM error: {e}")

    # Try Gemini
    try:
        from dotenv import load_dotenv
        load_dotenv(ROOT / ".env")
        api_key = os.getenv("GEMINI_API_KEY", "")
        if api_key:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-2.0-flash")
            r = model.generate_content(f"System: {system}\n\nUser: {message}")
            return f"[💎 Gemini] {r.text}"
    except Exception as e:
        log.error(f"Gemini LLM error: {e}")

    return "[❌] Aucun LLM disponible. Lance Ollama (ollama serve) ou vérifie tes clés API dans .env."


# ============================================================
# HANDLER
# ============================================================

class CommandHandler(SimpleHTTPRequestHandler):
    """Serve TITAN-COMMAND dashboard + API endpoints."""

    def do_GET(self):
        _t0 = time.monotonic()
        parsed = urlparse(self.path)
        path = parsed.path
        params = parse_qs(parsed.query)

        # === API ENDPOINTS ===
        if path == "/api/stats":
            self._json_response(self._read_json_cached("dashboard_stats.json"))
        elif path == "/api/conversations":
            self._json_response(self._read_json_cached("conversations.json"))
        elif path == "/api/gamification":
            self._json_response(self._read_json_cached("gamification.json"))
        elif path == "/api/memory":
            self._json_response(self._read_json("titan_memory.json"))
        elif path == "/api/contacts":
            self._json_response(self._read_json("contacts.json"))
        elif path == "/api/news":
            self._json_response(self._read_json("news_cache.json"))
        elif path == "/api/profile":
            self._json_response(self._read_json("personal_profile.json"))
        elif path == "/api/auto_facts":
            self._json_response(self._read_json("auto_facts.json"))
        elif path == "/api/health":
            self._json_response(self._health_check())
        elif path == "/api/system":
            self._json_response(self._system_info())
        elif path == "/api/directives":
            self._json_response(self._list_directives())
        elif path == "/api/directive":
            name = params.get("name", [""])[0]
            self._json_response(self._read_directive(name))
        elif path == "/api/modules":
            self._json_response(self._get_modules())
        elif path == "/api/extensions":
            self._json_response(_get_extensions())
        elif path == "/api/agents":
            self._json_response({"agents": _AGENTS_LIST, "total": len(_AGENTS_LIST)})
        elif path == "/api/ticker":
            self._json_response({"items": _fetch_ticker()})
        elif path == "/api/memory/search":
            query = params.get("q", [""])[0]
            if query:
                try:
                    from execution.titan.modules.memory import search_memory
                    results = search_memory(query)
                    self._json_response({"results": results})
                except Exception as e:
                    log.error(f"memory/search error: {e}")
                    self._json_response({"results": [], "error": str(e)})
            else:
                self._json_response({"results": []})
        elif path == "/api/memory/list":
            category = params.get("category", [None])[0]
            if category and not re.match(r'^[a-zA-Z0-9_-]{1,50}$', category):
                category = None
            try:
                from execution.titan.modules.memory import list_memories
                results = list_memories(category)
                self._json_response({"results": results})
            except Exception as e:
                log.error(f"memory/list error: {e}")
                self._json_response({"results": [], "error": str(e)})
        elif path == "/api/memory/facts":
            try:
                from execution.titan.modules.memory import get_auto_facts
                facts = get_auto_facts(50)
                self._json_response({"facts": facts})
            except Exception as e:
                log.error(f"memory/facts error: {e}")
                self._json_response({"facts": [], "error": str(e)})
        elif path == "/api/evolution":
            self._json_response(self._read_json_cached("evolution.json", from_memory_dir=False, filepath=MEMORY_DIR / "evolution.json"))
        elif path == "/api/pokedex":
            data = self._read_json_cached("evolution.json", from_memory_dir=False, filepath=MEMORY_DIR / "evolution.json")
            if "error" in data:
                self._json_response({"agents": {}, "types": {}, "forms": {}})
            else:
                self._json_response({
                    "agents": data.get("agents", {}),
                    "types":  data.get("system", {}).get("types", {}),
                    "forms":  data.get("system", {}).get("forms", {}),
                })
        elif path == "/api/bosses":
            data = self._read_json_cached("evolution.json", from_memory_dir=False, filepath=MEMORY_DIR / "evolution.json")
            if "error" in data:
                self._json_response({"bosses": {}, "trainer": {}})
            else:
                self._json_response({"bosses": data.get("bosses", {}), "trainer": data.get("trainer", {})})
        elif path == "/api/claude/status":
            try:
                result = subprocess.run(
                    ["claude", "--version"],
                    capture_output=True, text=True, timeout=5, encoding="utf-8",
                )
                self._json_response({"available": True, "version": result.stdout.strip()})
            except Exception:
                self._json_response({"available": False, "version": None})
        elif path == "/api/all":
            self._json_response({
                "stats":         self._read_json_cached("dashboard_stats.json"),
                "gamification":  self._read_json_cached("gamification.json"),
                "conversations": self._read_json_cached("conversations.json"),
                "profile":       self._read_json("personal_profile.json"),
                "health":        self._health_check(),
                "system":        self._system_info(),
                "extensions":    _get_extensions(),
                "timestamp":     datetime.now().isoformat(),
            })
        elif path == "/" or path == "/index.html":
            self._serve_file(PORTFOLIOS_DIR / "titan_command.html")
        elif path.startswith("/api/"):
            log.warning(f"404 Unknown API endpoint: {path}")
            self._json_response({"error": f"Unknown endpoint: {path}"}, 404)
        else:
            safe_path = self._safe_static_path(path)
            if safe_path and safe_path.exists() and safe_path.is_file():
                self._serve_file(safe_path)
            else:
                self._json_response({"error": "Not found"}, 404)

        self._log_request(path, _t0)

    def do_POST(self):
        _t0 = time.monotonic()
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/chat":
            body = _read_body(self)
            message = body.get("message", "")
            system = body.get("system", "")
            if not message:
                log.warning("POST /api/chat — message manquant")
                self._json_response({"error": "message required"}, 400)
                self._log_request(path, _t0)
                return
            if len(message) > MAX_MESSAGE_LENGTH:
                self._json_response({"error": f"Message trop long (max {MAX_MESSAGE_LENGTH} chars)"}, 400)
                self._log_request(path, _t0)
                return
            log.info(f"Chat: {message[:80]}")
            response = _chat_llm(message, system)
            self._json_response({"response": response})

        elif path == "/api/extension":
            body = _read_body(self)
            ext_id = body.get("id", "")
            enabled = body.get("enabled", True)
            exts = _get_extensions()
            if ext_id in exts:
                exts[ext_id]["enabled"] = enabled
                _save_extensions(exts)
                self._json_response({"ok": True, "id": ext_id, "enabled": enabled})
            else:
                self._json_response({"error": f"Extension '{ext_id}' not found"}, 404)

        elif path == "/api/memory":
            body = _read_body(self)
            key = body.get("key", "")
            value = body.get("value", "")
            category = body.get("category", "general")
            if not key or not value:
                log.warning("POST /api/memory — key ou value manquant")
                self._json_response({"error": "key and value required"}, 400)
                self._log_request(path, _t0)
                return
            if len(key) > MAX_KEY_LENGTH:
                self._json_response({"error": f"key trop longue (max {MAX_KEY_LENGTH})"}, 400)
                self._log_request(path, _t0)
                return
            if len(str(value)) > MAX_VALUE_LENGTH:
                self._json_response({"error": f"value trop longue (max {MAX_VALUE_LENGTH})"}, 400)
                self._log_request(path, _t0)
                return
            if not re.match(r'^[a-zA-Z0-9_-]{1,50}$', str(category)):
                category = "general"
            try:
                from execution.titan.modules.memory import remember
                result = remember(key, value, category)
                # Invalider le cache mémoire
                _cache_invalidate("titan_memory.json")
                self._json_response({"ok": True, "result": result})
            except Exception as e:
                log.error(f"Memory save error: {e}")
                self._json_response({"error": str(e)}, 500)

        elif path == "/api/anneal":
            body = _read_body(self)
            log.info("Self-annealing triggered from TITAN-COMMAND")
            report = self._run_annealing()
            # Invalider tout le cache après annealing (fichiers potentiellement modifiés)
            _cache.clear()
            self._json_response(report)

        elif path == "/api/claude":
            body = _read_body(self)
            message = body.get("message", "").strip()
            if not message:
                self._json_response({"error": "Message vide", "status": "error"}, 400)
                self._log_request(path, _t0)
                return
            if len(message) > 5000:
                self._json_response({"error": "Message trop long (max 5000)", "status": "error"}, 400)
                self._log_request(path, _t0)
                return
            workdir = body.get("workdir", str(ROOT))
            try:
                log.info(f"Claude CLI: {message[:80]}...")
                result = subprocess.run(
                    ["claude", "--print", "--output-format", "text", message],
                    capture_output=True, text=True, timeout=120,
                    cwd=workdir, encoding="utf-8",
                )
                response_text = result.stdout.strip()
                if result.returncode != 0 and not response_text:
                    response_text = result.stderr.strip() or "Erreur Claude Code (pas de sortie)"
                self._json_response({"response": response_text, "model": "claude-code-local", "status": "ok"})
                log.info(f"Claude CLI response: {len(response_text)} chars")
            except subprocess.TimeoutExpired:
                self._json_response({"error": "Timeout — Claude Code a mis plus de 120s", "status": "timeout"})
            except FileNotFoundError:
                self._json_response({"error": "Claude CLI non trouve. npm install -g @anthropic-ai/claude-code", "status": "error"})
            except Exception as e:
                log.error(f"Claude CLI error: {e}")
                self._json_response({"error": str(e), "status": "error"}, 500)

        else:
            self._json_response({"error": f"Unknown POST endpoint: {path}"}, 404)

        self._log_request(path, _t0)

    def do_OPTIONS(self):
        """Handle CORS preflight."""
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    # ----------------------------------------------------------
    # LECTURE JSON — avec et sans cache
    # ----------------------------------------------------------

    def _read_json(self, filename: str) -> dict:
        """Lecture directe sans cache."""
        filepath = MEMORY_DIR / filename
        try:
            if filepath.exists():
                return json.loads(filepath.read_text(encoding="utf-8"))
            return {"error": f"{filename} not found"}
        except json.JSONDecodeError:
            return {"error": f"{filename} corrupted"}
        except Exception as e:
            return {"error": str(e)}

    def _read_json_cached(self, cache_key: str, from_memory_dir: bool = True, filepath: Path = None) -> dict:
        """Lecture JSON avec cache TTL 10 secondes."""
        cached = _cache_get(cache_key)
        if cached is not None:
            return cached

        if filepath is None and from_memory_dir:
            filepath = MEMORY_DIR / cache_key

        if filepath is None:
            return {"error": "filepath not specified"}

        try:
            if filepath.exists():
                data = json.loads(filepath.read_text(encoding="utf-8"))
                _cache_set(cache_key, data)
                return data
            return {"error": f"{filepath.name} not found"}
        except json.JSONDecodeError:
            return {"error": f"{filepath.name} corrupted"}
        except Exception as e:
            return {"error": str(e)}

    # ----------------------------------------------------------
    # LOGGING AMÉLIORÉ — temps de réponse en ms
    # ----------------------------------------------------------

    def _log_request(self, path: str, t0: float):
        """Log la requête avec le temps de réponse en ms."""
        if "/api/" in path:
            elapsed_ms = int((time.monotonic() - t0) * 1000)
            method = self.command if hasattr(self, "command") else "GET"
            log.info(f"{method} {path} — {elapsed_ms}ms")

    def log_message(self, format, *args):
        """Override SimpleHTTPRequestHandler default — on gère nous-mêmes dans _log_request."""
        pass  # Silenced — logging via _log_request

    # ----------------------------------------------------------
    # HEALTH / SYSTEM / MODULES
    # ----------------------------------------------------------

    def _health_check(self):
        checks = {}
        for f in MEMORY_DIR.glob("*.json"):
            try:
                json.loads(f.read_text(encoding="utf-8"))
                checks[f.stem] = {"status": "ok", "size": f.stat().st_size}
            except Exception as e:
                checks[f.stem] = {"status": "error", "error": str(e)}
        try:
            import httpx
            r = httpx.get("http://localhost:11434/api/tags", timeout=2)
            models = [m["name"] for m in r.json().get("models", [])]
            checks["ollama"] = {"status": "ok", "models": models}
        except Exception as e:
            log.error(f"Ollama health check error: {e}")
            checks["ollama"] = {"status": "offline"}
        return checks

    def _system_info(self):
        try:
            import psutil
            cpu = psutil.cpu_percent(interval=None)
            mem = psutil.virtual_memory()
            if os.name == "nt":
                drive = os.path.splitdrive(str(TITAN_DIR))[0] + "\\"
            else:
                drive = "/"
            try:
                disk = psutil.disk_usage(drive)
                disk_data = {
                    "disk_percent": disk.percent,
                    "disk_used_gb": round(disk.used / (1024**3), 1),
                    "disk_total_gb": round(disk.total / (1024**3), 1),
                }
            except OSError as e:
                log.warning(f"disk_usage error pour {drive}: {e}")
                disk_data = {"disk_percent": 0, "disk_used_gb": 0, "disk_total_gb": 0}
            return {
                "cpu_percent": cpu,
                "ram_percent": mem.percent,
                "ram_used_gb": round(mem.used / (1024**3), 1),
                "ram_total_gb": round(mem.total / (1024**3), 1),
                **disk_data,
                "timestamp": datetime.now().isoformat(),
            }
        except ImportError:
            return {"error": "psutil not installed", "timestamp": datetime.now().isoformat()}
        except Exception as e:
            log.error(f"system_info error: {e}")
            return {"error": str(e), "timestamp": datetime.now().isoformat()}

    def _list_directives(self):
        """List all directive .md files."""
        dirs = []
        for d in sorted(DIRECTIVES_DIR.glob("*.md")):
            dirs.append({"name": d.stem, "file": d.name, "size": d.stat().st_size, "category": "directive"})
        for p in sorted(PERSONNALITES_DIR.glob("*.md")):
            dirs.append({"name": p.stem, "file": p.name, "size": p.stat().st_size, "category": "personnalite"})
        claude_md = ROOT / "CLAUDE.md"
        if claude_md.exists():
            dirs.append({"name": "CLAUDE", "file": "CLAUDE.md", "size": claude_md.stat().st_size, "category": "core"})
        return dirs

    def _read_directive(self, name: str) -> dict:
        """Read a specific directive or personality file."""
        if not name:
            return {"error": "name parameter required"}
        if not re.match(r'^[a-zA-Z0-9_-]{1,100}$', name):
            return {"error": "Nom invalide"}
        allowed_dirs = [DIRECTIVES_DIR, PERSONNALITES_DIR, ROOT]
        root_resolved = ROOT.resolve()
        for d in allowed_dirs:
            filepath = d / f"{name}.md"
            try:
                filepath.resolve().relative_to(root_resolved)
            except ValueError:
                log.warning(f"Path traversal bloqué dans directive: {filepath}")
                continue
            if filepath.exists():
                try:
                    content = filepath.read_text(encoding="utf-8")
                    rel_path = str(filepath.relative_to(ROOT)).replace("\\", "/")
                    return {"name": name, "content": content, "path": rel_path}
                except (OSError, PermissionError) as e:
                    log.error(f"Erreur lecture directive {name}: {e}")
                    return {"error": str(e)}
        return {"error": f"Directive '{name}' not found"}

    def _get_modules(self) -> list:
        """Return list of known TITAN modules with status."""
        return [
            {"name": "brain",        "status": "active", "desc": "Intelligence centrale"},
            {"name": "president",    "status": "active", "desc": "Directeur du Building"},
            {"name": "voice",        "status": "active", "desc": "Transcription vocaux"},
            {"name": "finance",      "status": "active", "desc": "Crypto & marchés"},
            {"name": "news",         "status": "active", "desc": "Actualités"},
            {"name": "gamification", "status": "active", "desc": "XP & niveaux"},
            {"name": "calendar",     "status": "active", "desc": "Tâches & habitudes"},
            {"name": "journal",      "status": "active", "desc": "Journal du soir"},
            {"name": "upwork",       "status": "active", "desc": "Jobs Upwork"},
            {"name": "aggregator",   "status": "active", "desc": "Digest quotidien"},
            {"name": "library",      "status": "active", "desc": "Bibliothèque"},
            {"name": "auto_healer",  "status": "active", "desc": "Auto-réparation"},
        ]

    # ----------------------------------------------------------
    # SELF-ANNEALING
    # ----------------------------------------------------------

    def _run_annealing(self) -> dict:
        """Run self-annealing: check and repair TITAN systems."""
        report = {"timestamp": datetime.now().isoformat(), "checks": [], "fixes": [], "status": "nominal"}

        for f in MEMORY_DIR.glob("*.json"):
            if "_backup_" in f.stem:
                continue
            try:
                json.loads(f.read_text(encoding="utf-8"))
                report["checks"].append({"file": f.name, "status": "ok"})
            except json.JSONDecodeError as je:
                log.warning(f"JSON corrompu détecté : {f.name} — {je}")
                backup_ok = False
                try:
                    backup = f.parent / f"{f.stem}_backup_{int(datetime.now().timestamp())}.json"
                    shutil.copy2(str(f), str(backup))
                    log.info(f"Backup créé : {backup.name}")
                    backup_ok = True
                except Exception as e:
                    log.error(f"Backup échoué pour {f.name}: {e}")
                try:
                    f.write_text("{}", encoding="utf-8")
                    report["fixes"].append({"file": f.name, "action": "reset to {}", "backup": backup_ok, "status": "fixed"})
                    report["status"] = "repaired"
                except Exception as e:
                    log.error(f"Reset échoué pour {f.name}: {e}")
                    report["fixes"].append({"file": f.name, "action": "fix failed", "error": str(e)})
                    report["status"] = "degraded"
            except OSError as e:
                log.error(f"Lecture impossible {f.name}: {e}")
                report["checks"].append({"file": f.name, "status": "error", "error": str(e)})

        if not EXTENSIONS_FILE.exists():
            _save_extensions(_get_extensions())
            report["fixes"].append({"file": "extensions.json", "action": "created default", "status": "fixed"})

        try:
            import httpx
            httpx.get("http://localhost:11434/api/tags", timeout=2)
            report["checks"].append({"service": "ollama", "status": "ok"})
        except Exception as e:
            log.warning(f"Ollama offline lors de l'annealing: {e}")
            report["checks"].append({"service": "ollama", "status": "offline"})

        return report

    # ----------------------------------------------------------
    # RESPONSE HELPERS
    # ----------------------------------------------------------

    def _json_response(self, data, status: int = 200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False, default=str).encode("utf-8"))

    def _safe_static_path(self, url_path: str):
        """Résout un path URL vers un fichier dans PORTFOLIOS_DIR.
        Bloque tout path traversal. Retourne None si non sécurisé."""
        try:
            clean = url_path.lstrip("/").replace("\\", "/")
            resolved = (PORTFOLIOS_DIR / clean).resolve()
            resolved.relative_to(PORTFOLIOS_DIR.resolve())
            return resolved
        except (ValueError, OSError):
            log.warning(f"Path traversal bloqué : {url_path}")
            return None

    def _serve_file(self, filepath: Path):
        """Sert un fichier statique avec gestion d'erreur."""
        ext = filepath.suffix.lower()
        content_types = {
            ".html":  "text/html; charset=utf-8",
            ".js":    "application/javascript; charset=utf-8",
            ".css":   "text/css; charset=utf-8",
            ".json":  "application/json; charset=utf-8",
            ".png":   "image/png",
            ".jpg":   "image/jpeg",
            ".jpeg":  "image/jpeg",
            ".svg":   "image/svg+xml",
            ".ico":   "image/x-icon",
        }
        try:
            data = filepath.read_bytes()
        except (OSError, PermissionError) as e:
            log.error(f"Erreur lecture fichier {filepath}: {e}")
            self._json_response({"error": "File read error"}, 500)
            return
        self.send_response(200)
        self.send_header("Content-Type", content_types.get(ext, "application/octet-stream"))
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(data)


# ============================================================
# SERVEUR
# ============================================================

class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    """Serveur HTTP multi-threadé — chaque requête dans son propre thread."""
    daemon_threads = True


def run():
    server = ThreadingHTTPServer(("0.0.0.0", PORT), CommandHandler)
    import socket
    local_ip = "localhost"
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(1)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
    except Exception:
        pass
    finally:
        if s:
            s.close()
    log.info("=" * 50)
    log.info("  TITAN-COMMAND SERVER v3 — ONLINE")
    log.info(f"  Dashboard : http://localhost:{PORT}")
    log.info(f"  Mobile    : http://{local_ip}:{PORT}")
    log.info(f"  API       : http://localhost:{PORT}/api/all")
    log.info(f"  Agents    : http://localhost:{PORT}/api/agents")
    log.info(f"  Ticker    : http://localhost:{PORT}/api/ticker")
    log.info(f"  Memory    : {MEMORY_DIR}")
    log.info("=" * 50)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        log.info("Server stopped.")
        server.server_close()


if __name__ == "__main__":
    run()
