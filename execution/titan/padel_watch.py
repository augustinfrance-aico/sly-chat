"""
PadelShot Sniper — Réservation automatique à l'ouverture des créneaux.
Se connecte à 23:59, attend minuit, réserve le premier créneau dispo.

Usage:
  python execution/titan/padel_watch.py          # Mode scheduler (boucle infinie)
  python execution/titan/padel_watch.py scan      # Scan unique
  python execution/titan/padel_watch.py snipe     # Snipe immédiat (prochain créneau)
"""
import asyncio
import io
import logging
import sys
import os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(message)s",
    datefmt="%H:%M:%S",
)


async def main():
    from execution.titan.modules.padel_sniper import PadelSniper

    mode = sys.argv[1] if len(sys.argv) > 1 else "scheduler"
    sniper = PadelSniper()

    if mode == "scan":
        print(await sniper.run_once())

    elif mode == "snipe":
        print("🏸 SNIPE MODE — reservation immediate du prochain creneau")
        await sniper.snipe()

    else:
        print("🏸 PadelShot Sniper — Mode scheduler")
        print("   Cibles: Ven/Sam/Dim 16h-18h @ Craponne")
        print("   Snipe: minuit J-16 | Scan: 1x/jour 12h30")
        print("   Mode discret: 1 piste/creneau, delais entre requetes")
        print(f"   Alertes: Telegram ({os.getenv('TELEGRAM_CHAT_ID', '?')})")
        print()
        await sniper.run_scheduler()


if __name__ == "__main__":
    asyncio.run(main())
