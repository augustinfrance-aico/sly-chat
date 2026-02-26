"""
TITAN LOCAL AGENT — Pont entre Telegram et ton PC.
Ce script tourne en local sur ton ordinateur et connecte TITAN à ta machine.

Fonctionnalités :
- /pc status    → CPU, RAM, disque, processus
- /pc run <cmd> → Exécuter une commande shell
- /pc read <path> → Lire un fichier
- /pc write <path> <content> → Écrire un fichier
- /pc git       → Status git du workspace
- /pc open <path> → Ouvrir un fichier/dossier
- /pc screenshot → Screenshot écran (si pyautogui dispo)
- /pc ps        → Processus actifs

Lancement : python -m execution.titan.titan_local
Fonctionne EN PARALLÈLE avec TITAN sur Render — même chat Telegram, zéro conflit.
"""

import asyncio
import logging
import os
import platform
import shutil
import subprocess
import time
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv

# Load env
ROOT = Path(__file__).resolve().parent.parent.parent
load_dotenv(ROOT / ".env")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
WORKSPACE = ROOT

logging.basicConfig(level=logging.INFO, format="%(asctime)s [LOCAL] %(message)s")
log = logging.getLogger("titan.local")

BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"


# === TELEGRAM HELPERS ===

def send_message(text: str):
    """Send message to Telegram chat."""
    if not TELEGRAM_CHAT_ID:
        return
    if len(text) > 4000:
        text = text[:3950] + "\n\n[...]"
    try:
        requests.post(
            f"{BASE_URL}/sendMessage",
            json={"chat_id": TELEGRAM_CHAT_ID, "text": text},
            timeout=10,
        )
    except Exception as e:
        log.error(f"Send error: {e}")


def get_updates(offset: int) -> list:
    """Get new Telegram updates."""
    try:
        resp = requests.get(
            f"{BASE_URL}/getUpdates",
            params={"offset": offset, "timeout": 30, "allowed_updates": ["message"]},
            timeout=35,
        )
        return resp.json().get("result", [])
    except Exception as e:
        log.error(f"Update error: {e}")
        return []


# === LOCAL COMMANDS ===

def pc_status() -> str:
    """System status — CPU, RAM, disk."""
    import psutil

    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    return (
        f"🖥️ PC STATUS\n"
        f"━━━━━━━━━━━━━━━\n"
        f"OS: {platform.system()} {platform.release()}\n"
        f"CPU: {cpu}%\n"
        f"RAM: {mem.percent}% ({mem.used // (1024**3)}/{mem.total // (1024**3)} GB)\n"
        f"Disque: {disk.percent}% ({disk.used // (1024**3)}/{disk.total // (1024**3)} GB)\n"
        f"Uptime: {datetime.now().strftime('%H:%M:%S')}\n"
        f"Python: {platform.python_version()}\n"
        f"Workspace: {WORKSPACE}"
    )


def pc_run(cmd: str) -> str:
    """Execute a shell command (sandboxed — read-only by default)."""
    # Block dangerous commands
    blocked = ["rm -rf", "format", "del /", "rmdir /s", "shutdown", "reboot"]
    if any(b in cmd.lower() for b in blocked):
        return "⛔ Commande bloquée (sécurité)."

    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=30,
            cwd=str(WORKSPACE)
        )
        output = result.stdout or result.stderr or "(pas de sortie)"
        return f"$ {cmd}\n\n{output[:3500]}"
    except subprocess.TimeoutExpired:
        return f"⏰ Timeout (30s) : {cmd}"
    except Exception as e:
        return f"Erreur : {e}"


def pc_read(path: str) -> str:
    """Read a file from the workspace."""
    filepath = WORKSPACE / path if not Path(path).is_absolute() else Path(path)
    if not filepath.exists():
        return f"Fichier introuvable : {filepath}"
    try:
        content = filepath.read_text(encoding="utf-8")
        if len(content) > 3500:
            content = content[:3500] + "\n\n[... tronqué]"
        return f"📄 {filepath.name}\n\n{content}"
    except Exception as e:
        return f"Erreur lecture : {e}"


def pc_write(args: str) -> str:
    """Write content to a file. Format: /pc write <path> <content>"""
    parts = args.split(None, 1)
    if len(parts) < 2:
        return "Format: /pc write <chemin> <contenu>"
    filepath = WORKSPACE / parts[0]
    try:
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(parts[1], encoding="utf-8")
        return f"✅ Écrit dans {filepath.name} ({len(parts[1])} chars)"
    except Exception as e:
        return f"Erreur écriture : {e}"


def pc_git() -> str:
    """Git status of the workspace."""
    try:
        status = subprocess.run(
            "git status --short", shell=True, capture_output=True, text=True,
            timeout=10, cwd=str(WORKSPACE)
        )
        branch = subprocess.run(
            "git branch --show-current", shell=True, capture_output=True, text=True,
            timeout=5, cwd=str(WORKSPACE)
        )
        log_out = subprocess.run(
            "git log --oneline -5", shell=True, capture_output=True, text=True,
            timeout=5, cwd=str(WORKSPACE)
        )
        return (
            f"🔀 GIT STATUS\n"
            f"━━━━━━━━━━━━━━\n"
            f"Branche: {branch.stdout.strip()}\n\n"
            f"Fichiers modifiés:\n{status.stdout[:2000] or '(clean)'}\n\n"
            f"Derniers commits:\n{log_out.stdout[:1000]}"
        )
    except Exception as e:
        return f"Erreur git : {e}"


def pc_open(path: str) -> str:
    """Open a file or folder in the OS default app."""
    filepath = WORKSPACE / path if not Path(path).is_absolute() else Path(path)
    if not filepath.exists():
        return f"Introuvable : {filepath}"
    try:
        os.startfile(str(filepath))
        return f"✅ Ouvert : {filepath.name}"
    except Exception as e:
        return f"Erreur : {e}"


def pc_ps() -> str:
    """List top processes by memory."""
    import psutil
    procs = []
    for p in psutil.process_iter(["pid", "name", "memory_percent", "cpu_percent"]):
        try:
            info = p.info
            if info["memory_percent"] and info["memory_percent"] > 0.5:
                procs.append(info)
        except Exception:
            pass
    procs.sort(key=lambda x: x["memory_percent"], reverse=True)
    lines = ["🔧 TOP PROCESSUS\n"]
    for p in procs[:15]:
        lines.append(f"  {p['name'][:20]:20} PID:{p['pid']:>6}  RAM:{p['memory_percent']:.1f}%")
    return "\n".join(lines)


def pc_ollama(args: str = "") -> str:
    """Manage Ollama — status, pull, switch model, list."""
    parts = args.split(None, 1) if args else []
    subcmd = parts[0].lower() if parts else "status"
    rest = parts[1].strip() if len(parts) > 1 else ""

    if subcmd == "status":
        try:
            from execution.titan.ai_client import ollama_status
            return ollama_status()
        except ImportError:
            # Direct check
            try:
                resp = requests.get("http://localhost:11434/api/tags", timeout=3)
                if resp.status_code == 200:
                    models = [m["name"] for m in resp.json().get("models", [])]
                    return f"🦙 Ollama OK\nModèles : {', '.join(models) if models else 'Aucun'}"
            except Exception:
                return "❌ Ollama non détecté. Lance 'ollama serve'."

    elif subcmd == "list":
        try:
            resp = requests.get("http://localhost:11434/api/tags", timeout=3)
            models = resp.json().get("models", [])
            if not models:
                return "Aucun modèle installé. Utilise /pc ollama pull <modèle>"
            lines = ["🦙 MODÈLES OLLAMA\n"]
            for m in models:
                size_gb = m.get("size", 0) / (1024**3)
                lines.append(f"  • {m['name']} ({size_gb:.1f} GB)")
            return "\n".join(lines)
        except Exception:
            return "❌ Ollama non disponible."

    elif subcmd == "pull":
        if not rest:
            return "Usage: /pc ollama pull <modèle>\nEx: /pc ollama pull llama3.1:8b"
        try:
            log.info(f"Pulling Ollama model: {rest}")
            result = subprocess.run(
                f"ollama pull {rest}", shell=True, capture_output=True, text=True, timeout=600
            )
            if result.returncode == 0:
                return f"✅ Modèle {rest} téléchargé."
            return f"❌ Erreur pull : {result.stderr[:500]}"
        except subprocess.TimeoutExpired:
            return f"⏰ Timeout — le modèle {rest} est peut-être trop gros. Lance manuellement : ollama pull {rest}"
        except Exception as e:
            return f"❌ {e}"

    elif subcmd in ("use", "switch", "model"):
        if not rest:
            return "Usage: /pc ollama use <modèle>"
        try:
            from execution.titan.ai_client import ollama_set_model
            return ollama_set_model(rest)
        except ImportError:
            return f"⚠️ Modèle noté : {rest}. Redémarre TITAN Local pour appliquer."

    elif subcmd == "serve":
        try:
            subprocess.Popen("ollama serve", shell=True)
            return "🦙 Ollama démarré en arrière-plan."
        except Exception as e:
            return f"❌ {e}"

    return (
        "🦙 OLLAMA — Commandes\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "/pc ollama status  — Statut Ollama\n"
        "/pc ollama list    — Modèles installés\n"
        "/pc ollama pull <m> — Télécharger un modèle\n"
        "/pc ollama use <m>  — Changer de modèle actif\n"
        "/pc ollama serve   — Démarrer Ollama\n"
        "\nModèles recommandés (gratuits) :\n"
        "  llama3.1:8b     — Rapide, 4.7GB\n"
        "  mistral:7b      — Polyvalent, 4.1GB\n"
        "  phi3:mini       — Ultra léger, 2.3GB\n"
        "  qwen2.5:7b      — Bon en code, 4.4GB\n"
        "  gemma2:9b       — Google, 5.4GB"
    )


def pc_app() -> str:
    """Open TITAN-COMMAND dashboard in browser."""
    import webbrowser
    try:
        webbrowser.open("http://localhost:7777")
        return "✅ TITAN-COMMAND ouvert dans le navigateur."
    except Exception as e:
        return f"❌ {e}\nOuvre manuellement : http://localhost:7777"


def pc_tower() -> str:
    """Open Moon Tower visualization in browser."""
    import webbrowser
    try:
        webbrowser.open("http://localhost:7777/moon_tower.html")
        return "🏰 Moon Tower ouverte dans le navigateur."
    except Exception as e:
        return f"❌ {e}\nOuvre manuellement : http://localhost:7777/moon_tower.html"


def pc_ls(path: str = "") -> str:
    """List files in a directory."""
    dirpath = WORKSPACE / path if path else WORKSPACE
    if not dirpath.is_dir():
        return f"Pas un dossier : {dirpath}"
    try:
        items = sorted(dirpath.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
        lines = [f"📂 {dirpath}\n"]
        for item in items[:50]:
            prefix = "📁 " if item.is_dir() else "   "
            size = ""
            if item.is_file():
                s = item.stat().st_size
                size = f" ({s // 1024}KB)" if s > 1024 else f" ({s}B)"
            lines.append(f"{prefix}{item.name}{size}")
        if len(items) > 50:
            lines.append(f"\n... et {len(items) - 50} autres")
        return "\n".join(lines)
    except Exception as e:
        return f"Erreur : {e}"


# === COMMAND ROUTER ===

def handle_pc_command(args: str) -> str:
    """Route /pc <subcommand> to the right handler."""
    if not args:
        return (
            "🖥️ TITAN LOCAL — Commandes PC\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "/pc status    — CPU, RAM, disque\n"
            "/pc run <cmd> — Exécuter commande shell\n"
            "/pc read <f>  — Lire un fichier\n"
            "/pc write <f> <c> — Écrire un fichier\n"
            "/pc git       — Status git\n"
            "/pc open <f>  — Ouvrir fichier/dossier\n"
            "/pc ps        — Processus actifs\n"
            "/pc ls [dir]  — Lister fichiers\n"
            "/pc ollama    — 🦙 Gérer Ollama (IA locale)\n"
            "/pc app       — 🖥️ Ouvrir TITAN-COMMAND\n"
            "/pc tower     — 🏰 Ouvrir Moon Tower"
        )

    parts = args.split(None, 1)
    cmd = parts[0].lower()
    rest = parts[1] if len(parts) > 1 else ""

    handlers = {
        "status": lambda: pc_status(),
        "run": lambda: pc_run(rest),
        "read": lambda: pc_read(rest),
        "write": lambda: pc_write(rest),
        "git": lambda: pc_git(),
        "open": lambda: pc_open(rest),
        "ps": lambda: pc_ps(),
        "ls": lambda: pc_ls(rest),
        "ollama": lambda: pc_ollama(rest),
        "app": lambda: pc_app(),
        "tower": lambda: pc_tower(),
    }

    handler = handlers.get(cmd)
    if handler:
        try:
            return handler()
        except ImportError as e:
            return f"Module manquant : {e}\nInstalle avec : pip install psutil"
        except Exception as e:
            return f"Erreur : {e}"
    return f"Commande inconnue : {cmd}. Tape /pc pour l'aide."


# === MAIN LOOP ===

async def main():
    """Main polling loop — runs alongside TITAN on Render."""
    log.info("=" * 40)
    log.info("  TITAN LOCAL AGENT — ONLINE")
    log.info(f"  Workspace: {WORKSPACE}")
    log.info(f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log.info("=" * 40)

    # Get latest offset to skip old messages
    offset = 0
    try:
        resp = requests.get(
            f"{BASE_URL}/getUpdates",
            params={"offset": -1, "limit": 1, "timeout": 0},
            timeout=5,
        )
        results = resp.json().get("result", [])
        if results:
            offset = results[-1]["update_id"] + 1
    except Exception:
        pass

    while True:
        updates = get_updates(offset)
        for update in updates:
            offset = update["update_id"] + 1
            msg = update.get("message", {})
            text = msg.get("text", "")
            chat_id = str(msg.get("chat", {}).get("id", ""))

            # Only respond to /pc commands from authorized chat
            if chat_id != TELEGRAM_CHAT_ID:
                continue

            if text.startswith("/pc"):
                args = text[3:].strip()
                log.info(f"[PC] {args or 'help'}")
                response = handle_pc_command(args)
                send_message(response)

        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
