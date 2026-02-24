"""
TITAN Scheduler
Automated tasks that run on schedule — Titan works while you sleep.

Features:
- Daily morning brief (8h00)
- Crypto alerts (significant price changes)
- Streak reminders (evening)
- Gamification daily reset
"""

import asyncio
import logging
from datetime import datetime, time as dtime
from typing import Callable

import requests

from .config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from .modules.news import TitanNews
from .modules.finance import TitanFinance
from .modules.calendar import TitanCalendar
from .modules.gamification import TitanGamification

log = logging.getLogger("titan.scheduler")


class TitanScheduler:
    """Background scheduler for automated tasks."""

    def __init__(self):
        self.tasks = []
        self.running = False
        self.base_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

        # Modules
        self.news = TitanNews()
        self.finance = TitanFinance()
        self.calendar = TitanCalendar()
        self.gamification = TitanGamification()

        # State
        self.last_brief_date = None
        self.last_crypto_check = None
        self.last_evening_reminder = None
        self.crypto_prices_cache = {}

    def send_telegram(self, text: str):
        """Send a message to Telegram. Truncate if too long."""
        if not TELEGRAM_CHAT_ID:
            return
        try:
            if len(text) > 4000:
                text = text[:3950] + "\n\n[...]"
            requests.post(
                f"{self.base_url}/sendMessage",
                json={"chat_id": TELEGRAM_CHAT_ID, "text": text},
                timeout=10,
            )
        except Exception as e:
            log.error(f"Telegram send error: {e}")

    async def morning_brief(self):
        """Send the daily morning brief at 8:00 AM."""
        now = datetime.now()

        if now.hour == 8 and now.minute < 5:
            today = now.strftime("%Y-%m-%d")
            if self.last_brief_date == today:
                return

            self.last_brief_date = today
            log.info("Generating morning brief...")

            sections = [
                f"{'=' * 28}",
                f"  BRIEF MATINAL TITAN",
                f"  {now.strftime('%A %d %B %Y')}",
                f"{'=' * 28}\n",
            ]

            # News
            try:
                news = await self.news.get_ai_summary()
                sections.append(f"📰 ACTUALITES\n{news}\n")
            except Exception as e:
                sections.append(f"📰 News indisponibles: {e}\n")

            # Crypto
            try:
                crypto = await self.finance.get_crypto_brief()
                sections.append(f"{crypto}\n")
            except Exception as e:
                sections.append(f"🪙 Crypto indisponible: {e}\n")

            # Stocks
            try:
                stocks = await self.finance.get_stocks_brief()
                sections.append(f"{stocks}\n")
            except Exception:
                pass

            # Tasks for today
            try:
                tasks = self.calendar.list_tasks()
                if tasks and "Aucune" not in tasks:
                    sections.append(f"✅ TACHES\n{tasks}\n")
            except Exception:
                pass

            # Habits
            try:
                habits = self.calendar.list_habits()
                if habits and "Aucune" not in habits:
                    sections.append(f"🔄 HABITUDES\n{habits}\n")
            except Exception:
                pass

            sections.append("Bonne journee. 💪")

            self.send_telegram("\n".join(sections))
            log.info("Morning brief sent.")

    async def crypto_alerts(self):
        """Check for significant crypto price changes."""
        now = datetime.now()

        if self.last_crypto_check and (now - self.last_crypto_check).seconds < 1800:
            return

        self.last_crypto_check = now

        try:
            prices = self.finance.get_crypto_prices()
            if "error" in prices:
                return

            alerts = []
            for symbol, data in prices.items():
                change = abs(data.get("change_24h", 0))

                if change > 5:
                    direction = "📈" if data["change_24h"] > 0 else "📉"
                    alerts.append(
                        f"{direction} {symbol}: {data['change_24h']:+.1f}% "
                        f"(${data['usd']:,.0f})"
                    )

            if alerts:
                msg = "🚨 ALERTE CRYPTO\n\n" + "\n".join(alerts)
                self.send_telegram(msg)
                log.info(f"Crypto alert sent: {len(alerts)} alerts")

        except Exception as e:
            log.error(f"Crypto alert error: {e}")

    async def evening_reminder(self):
        """Send an evening reminder about streak and habits at 21:00."""
        now = datetime.now()

        if now.hour == 21 and now.minute < 5:
            today = now.strftime("%Y-%m-%d")
            if self.last_evening_reminder == today:
                return

            self.last_evening_reminder = today

            sections = ["🌙 RAPPEL DU SOIR\n"]

            # Unchecked habits
            try:
                habits = self.calendar.list_habits()
                if habits and "Aucune" not in habits:
                    sections.append(f"\n🔄 HABITUDES\n{habits}")
            except Exception:
                pass

            sections.append("\nBonne soiree. 🌙")
            self.send_telegram("\n".join(sections))
            log.info("Evening reminder sent.")

    async def run(self):
        """Main scheduler loop."""
        self.running = True
        log.info("Scheduler started.")

        while self.running:
            try:
                await self.morning_brief()
                await self.crypto_alerts()
                await self.evening_reminder()
            except Exception as e:
                log.error(f"Scheduler error: {e}")

            await asyncio.sleep(60)

    def stop(self):
        self.running = False
        log.info("Scheduler stopped.")
