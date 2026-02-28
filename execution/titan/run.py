"""
████████╗██╗████████╗ █████╗ ███╗   ██╗
╚══██╔══╝██║╚══██╔══╝██╔══██╗████╗  ██║
   ██║   ██║   ██║   ███████║██╔██╗ ██║
   ██║   ██║   ██║   ██╔══██║██║╚██╗██║
   ██║   ██║   ██║   ██║  ██║██║ ╚████║
   ╚═╝   ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝

TITAN — Personal AI Agent
Launch: python -m titan.run

This starts:
1. Telegram Bot (responds to messages)
2. Scheduler (morning brief, digest, journal)
3. All modules (news, web, finance, upwork, n8n)
"""

import asyncio
import logging
import os
import sys
import threading
from datetime import datetime

from .telegram_bot import TitanTelegram
from .scheduler import TitanScheduler
from .config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger("titan")


BANNER = """
╔══════════════════════════════════════╗
║  T.I.T.A.N. v4.0 — NEURAL ENGINE   ║
║  53 modules | 250+ commandes        ║
║  Module Registry + Smart Context    ║
║  Cache TTL + Latency Tracking       ║
║  Owner: Augustin — AICO Empire      ║
╚══════════════════════════════════════╝
"""


def check_config():
    """Verify all required config is present."""
    errors = []

    if not TELEGRAM_BOT_TOKEN:
        errors.append("TELEGRAM_BOT_TOKEN manquant dans .env")
    if not TELEGRAM_CHAT_ID:
        errors.append("TELEGRAM_CHAT_ID manquant dans .env (optionnel mais recommandé)")

    return errors


async def main():
    """Launch Titan."""
    print(BANNER)

    # Config check
    errors = check_config()
    if errors:
        for e in errors:
            log.warning(f"⚠️  {e}")

    # At least one AI provider is needed (Groq free preferred)
    groq_key = os.getenv("GROQ_API_KEY", "")
    gemini_key = os.getenv("GEMINI_API_KEY", "")
    if not groq_key and not gemini_key:
        log.error("Aucune API IA configuree. Ajoute GROQ_API_KEY ou GEMINI_API_KEY dans .env")
        sys.exit(1)

    if not TELEGRAM_BOT_TOKEN:
        log.error("TELEGRAM_BOT_TOKEN est requis. Crée un bot via @BotFather sur Telegram.")
        sys.exit(1)

    log.info(f"Démarrage de Titan — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Initialize Module Registry (auto-catalog all modules)
    try:
        from .module_registry import registry
        registry.auto_register_from_catalog()
        log.info(f"Module Registry: {len(registry.MODULE_CATALOG)} modules catalogués")
    except Exception as e:
        log.warning(f"Module Registry init failed: {e}")

    # Start command_server in background thread (serves dashboard HTML)
    try:
        from .command_server import run as run_command_server
        cmd_thread = threading.Thread(target=run_command_server, daemon=True, name="command-server")
        cmd_thread.start()
        log.info("TITAN-COMMAND server started in background thread")
    except Exception as e:
        log.warning(f"Command server failed to start: {e} — dashboard will not be available")

    # Create instances
    bot = TitanTelegram()
    scheduler = TitanScheduler()

    # Run both concurrently
    try:
        await asyncio.gather(
            bot.run(),
            scheduler.run(),
        )
    except KeyboardInterrupt:
        log.info("Arrêt demandé...")
        bot.stop()
        scheduler.stop()
    except Exception as e:
        log.error(f"Erreur fatale: {e}")
        bot.stop()
        scheduler.stop()


if __name__ == "__main__":
    asyncio.run(main())
