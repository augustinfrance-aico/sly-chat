"""
TITAN Scheduler
Automated tasks that run on schedule — Titan works while you sleep.

Features:
- Daily morning brief (8h00)
- Streak reminders (evening)
- Gamification daily reset
"""

import asyncio
import logging
from datetime import datetime, time as dtime, timezone, timedelta
from typing import Callable

import requests

# Timezone Paris (UTC+1 hiver, UTC+2 été)
PARIS_TZ = timezone(timedelta(hours=1))  # CET — ajuster à +2 en été si besoin


def _now_paris() -> datetime:
    """Heure actuelle en Europe/Paris."""
    return datetime.now(PARIS_TZ)

from .config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from .modules.news import TitanNews
from .modules.calendar import TitanCalendar
from .modules.gamification import TitanGamification
from .modules.morning_digest import TitanMorningDigest
from .modules.journal import TitanJournal
from .modules.auto_healer import TitanAutoHealer
from .modules.aggregator import TitanAggregator
from .modules.library import TitanLibrary
from .modules.rdlab_digestor import TitanRDLabDigestor
from .modules.rdlab_scout import TitanRDLabScout
from .modules.rdlab_horizon import TitanRDLabHorizon

log = logging.getLogger("titan.scheduler")


class TitanScheduler:
    """Background scheduler for automated tasks."""

    def __init__(self):
        self.tasks = []
        self.running = False
        self.base_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

        # Modules
        self.news = TitanNews()
        self.calendar = TitanCalendar()
        self.gamification = TitanGamification()
        self.morning_digest = TitanMorningDigest()
        self.journal = TitanJournal()
        self.auto_healer = TitanAutoHealer()
        self.aggregator = TitanAggregator()
        self.library = TitanLibrary()
        self.rdlab_digestor = TitanRDLabDigestor()
        self.rdlab_scout = TitanRDLabScout()
        self.rdlab_horizon = TitanRDLabHorizon()

        # State
        self.last_brief_date = None
        self.last_evening_reminder = None
        self.last_digest_date = None
        self.last_journal_prompt = None
        self.last_health_check = None
        self.last_aggregator_date = None
        self.last_rdlab_daily = None
        self.last_rdlab_scout_alert = None
        self.last_rdlab_horizon = None

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
        now = _now_paris()

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

    async def evening_reminder(self):
        """Send an evening reminder about streak and habits at 21:00."""
        now = _now_paris()

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

    async def smart_morning_digest(self):
        """Send the smart morning digest at 8:00 AM (replaces old brief)."""
        now = _now_paris()
        if now.hour == 8 and now.minute < 5:
            today = now.strftime("%Y-%m-%d")
            if self.last_digest_date == today:
                return
            self.last_digest_date = today
            log.info("Generating smart morning digest...")
            try:
                digest = await self.morning_digest.generate()
                self.send_telegram(digest)
                log.info("Smart morning digest sent.")
            except Exception as e:
                log.error(f"Morning digest error: {e}")

    async def evening_journal_prompt(self):
        """Send journal prompt at 21:30 — FLEMMARD approved (just 3 questions)."""
        now = _now_paris()
        if now.hour == 21 and 25 <= now.minute <= 35:
            today = now.strftime("%Y-%m-%d")
            if self.last_journal_prompt == today:
                return
            self.last_journal_prompt = today
            log.info("Sending journal prompt...")
            try:
                prompt = self.journal.start_evening_session()
                self.send_telegram(prompt)
                log.info("Journal prompt sent.")
            except Exception as e:
                log.error(f"Journal prompt error: {e}")

    async def daily_health_check(self):
        """Run auto-healer health check at 6:00 AM."""
        now = _now_paris()
        if now.hour == 6 and now.minute < 5:
            today = now.strftime("%Y-%m-%d")
            if self.last_health_check == today:
                return
            self.last_health_check = today
            log.info("Running daily health check...")
            try:
                report = self.auto_healer.health_check()
                # Only send if issues found
                if "NOMINAL" not in report:
                    self.send_telegram(report)
                log.info("Health check done.")
            except Exception as e:
                log.error(f"Health check error: {e}")

    async def afternoon_digest(self):
        """Send aggregator digest at 14:00."""
        now = _now_paris()
        if now.hour == 14 and now.minute < 5:
            today = now.strftime("%Y-%m-%d")
            if self.last_aggregator_date == today:
                return
            self.last_aggregator_date = today
            log.info("Generating afternoon digest...")
            try:
                digest = await self.aggregator.generate_daily_digest()
                self.send_telegram(digest)
                log.info("Afternoon digest sent.")
            except Exception as e:
                log.error(f"Aggregator error: {e}")

    async def rdlab_daily_digest(self):
        """Send R&D Lab daily digest at 7:30 AM (before morning digest)."""
        now = _now_paris()
        if now.hour == 7 and 25 <= now.minute <= 35:
            today = now.strftime("%Y-%m-%d")
            if self.last_rdlab_daily == today:
                return
            self.last_rdlab_daily = today
            log.info("Generating R&D Lab daily digest...")
            try:
                digest = await self.rdlab_digestor.generate_daily_digest()
                self.send_telegram(digest)
                log.info("R&D Lab daily digest sent.")
            except Exception as e:
                log.error(f"RDLab daily digest error: {e}")

    async def rdlab_scout_alert(self):
        """Check for explosive trends at 12:00 PM. Silent if nothing."""
        now = _now_paris()
        if now.hour == 12 and now.minute < 5:
            today = now.strftime("%Y-%m-%d")
            if self.last_rdlab_scout_alert == today:
                return
            self.last_rdlab_scout_alert = today
            log.info("Checking R&D Lab scout alerts...")
            try:
                alert = await self.rdlab_scout.check_alerts()
                if alert:
                    self.send_telegram(alert)
                    log.info("R&D Lab scout alert sent.")
                else:
                    log.info("R&D Lab scout: no explosive trends.")
            except Exception as e:
                log.error(f"RDLab scout alert error: {e}")

    async def rdlab_horizon_monthly(self):
        """Monthly horizon forecast on the 1st at 9:00 AM."""
        now = _now_paris()
        if now.day == 1 and now.hour == 9 and now.minute < 5:
            month_key = now.strftime("%Y-%m")
            if self.last_rdlab_horizon == month_key:
                return
            self.last_rdlab_horizon = month_key
            log.info("Generating R&D Lab horizon forecast...")
            try:
                forecast = await self.rdlab_horizon.generate_forecast()
                self.send_telegram(forecast)
                log.info("R&D Lab horizon forecast sent.")
            except Exception as e:
                log.error(f"RDLab horizon error: {e}")

    async def run(self):
        """Main scheduler loop."""
        self.running = True
        log.info("Scheduler started (with Building Life + R&D Lab modules).")

        # Boot delay — skip 2 min after deploy to avoid spam
        log.info("Scheduler boot delay: 120s (anti-spam on deploy)")
        await asyncio.sleep(120)
        log.info("Scheduler active.")

        while self.running:
            try:
                await self.daily_health_check()       # 6h — santé TITAN
                await self.rdlab_daily_digest()        # 7h30 — R&D Lab papers
                await self.smart_morning_digest()      # 8h — digest du matin
                # morning_brief supprimé — doublon avec smart_morning_digest
                await self.rdlab_scout_alert()         # 12h — alertes innovations (silent si rien)
                await self.afternoon_digest()          # 14h — agrégateur
                await self.evening_reminder()          # 21h — rappel habitudes
                await self.evening_journal_prompt()    # 21h30 — journal du soir
                await self.rdlab_horizon_monthly()     # 1er du mois 9h — forecast
            except Exception as e:
                log.error(f"Scheduler error: {e}")

            await asyncio.sleep(60)

    def stop(self):
        self.running = False
        log.info("Scheduler stopped.")
