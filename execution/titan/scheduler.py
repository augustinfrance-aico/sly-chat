"""
SLY Scheduler
Automated tasks that run on schedule — the Building works while you sleep.

Features:
- Daily morning brief (8h00)
- Streak reminders (evening)
- Nightshift configurable (/nightshift via Telegram)
"""

import asyncio
import json
import logging
from datetime import datetime, time as dtime, timezone, timedelta
from pathlib import Path
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
from .modules.liquefactor import ContentLiquefactor

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
        self.liquefactor = ContentLiquefactor()

        # Lazy-loaded modules for nightshift
        self._upwork = None
        self._perplexity = None

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
        self.last_breaking_check = None   # Timestamp dernier check breaking news
        self.last_youtube_check = None     # Timestamp dernier check YouTube
        self.last_liquefactor_digest = None  # Date dernier digest Liquefactor

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

    # === CONTENT LIQUEFACTOR — Breaking news, YouTube monitoring, digest HTML ===

    async def breaking_news_check(self):
        """Check for breaking AI news every 15 min (8h-23h). Silent if nothing."""
        now = _now_paris()
        if not (8 <= now.hour <= 23):
            return
        # Throttle: 15 min minimum between checks
        if self.last_breaking_check:
            elapsed = (now - self.last_breaking_check).total_seconds()
            if elapsed < 900:  # 15 min
                return
        self.last_breaking_check = now
        try:
            result = await asyncio.to_thread(self.liquefactor.check_breaking_news)
            if result:
                log.info(f"BREAKING NEWS detected: {result.get('title', '?')}")
            # Silent if nothing — liquefactor handles Telegram internally
        except Exception as e:
            log.error(f"Breaking news check error: {e}")

    async def youtube_channel_check(self):
        """Check monitored YouTube channels every 30 min for new videos."""
        now = _now_paris()
        # Throttle: 30 min minimum between checks
        if self.last_youtube_check:
            elapsed = (now - self.last_youtube_check).total_seconds()
            if elapsed < 1800:  # 30 min
                return
        self.last_youtube_check = now
        try:
            new_videos = await asyncio.to_thread(self.liquefactor.check_youtube_channels)
            if new_videos:
                log.info(f"New YouTube videos detected: {len(new_videos)}")
                for vid in new_videos:
                    url = vid.get("url", "")
                    if url:
                        log.info(f"Auto-reviewing: {vid.get('title', url)}")
                        try:
                            await asyncio.to_thread(self.liquefactor.generate_review, url)
                        except Exception as e:
                            log.error(f"Auto-review error for {url}: {e}")
        except Exception as e:
            log.error(f"YouTube channel check error: {e}")

    async def liquefactor_afternoon_digest(self):
        """Generate HTML AI digest page at 14h — replaces text-only aggregator."""
        now = _now_paris()
        if now.hour == 14 and now.minute < 5:
            today = now.strftime("%Y-%m-%d")
            if self.last_liquefactor_digest == today:
                return
            self.last_liquefactor_digest = today
            log.info("Generating Liquefactor daily digest (HTML page)...")
            try:
                result = await asyncio.to_thread(self.liquefactor.generate_daily_digest)
                if result:
                    log.info(f"Liquefactor digest deployed: {result.get('url', '?')}")
                else:
                    log.warning("Liquefactor digest: no result returned.")
            except Exception as e:
                log.error(f"Liquefactor digest error: {e}")

    # === NIGHTSHIFT — Configurable via /nightshift on Telegram ===

    NIGHTSHIFT_FILE = Path(__file__).parent / "memory" / "nightshift.json"

    # Available task types and their handlers
    NIGHTSHIFT_CATALOG = {
        "upwork_scan": {
            "label": "Scan Upwork leads",
            "emoji": "💼",
            "hour": 3,
        },
        "market_intel": {
            "label": "Veille marché IA/freelance",
            "emoji": "📡",
            "hour": 3,
        },
        "health_check": {
            "label": "Health check système",
            "emoji": "🔧",
            "hour": 5,
        },
        "api_status": {
            "label": "Status API (quotas/latence)",
            "emoji": "📊",
            "hour": 5,
        },
        "kdp_niches": {
            "label": "Scan niches KDP Amazon",
            "emoji": "📚",
            "hour": 3,
        },
        "news_digest": {
            "label": "Digest news IA overnight",
            "emoji": "📰",
            "hour": 4,
        },
        "memory_backup": {
            "label": "Backup mémoire SLY",
            "emoji": "💾",
            "hour": 4,
        },
        "rdlab_scan": {
            "label": "Scan R&D Lab papers",
            "emoji": "🔬",
            "hour": 3,
        },
    }

    def _load_nightshift(self) -> dict:
        """Load nightshift config from JSON."""
        try:
            with open(self.NIGHTSHIFT_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"enabled": False, "tasks": [], "history": []}

    def _save_nightshift(self, data: dict):
        """Save nightshift config to JSON."""
        try:
            with open(self.NIGHTSHIFT_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            log.error(f"Nightshift save error: {e}")

    async def _run_nightshift_task(self, task_id: str) -> str:
        """Execute a single nightshift task. Returns result text."""
        if task_id == "upwork_scan":
            try:
                if self._upwork is None:
                    from .modules.upwork import TitanUpwork
                    self._upwork = TitanUpwork()
                jobs = await self._upwork.get_relevant_jobs()
                return jobs[:800] if jobs else "Aucun job pertinent cette nuit."
            except Exception as e:
                return f"Erreur: {e}"

        elif task_id == "market_intel":
            try:
                if self._perplexity is None:
                    from .modules.perplexity import TitanPerplexity
                    self._perplexity = TitanPerplexity()
                result = await self._perplexity.search("AI automation freelance trends this week")
                return result[:800] if result else "Pas de tendance notable."
            except Exception as e:
                return f"Erreur: {e}"

        elif task_id == "health_check":
            try:
                report = self.auto_healer.health_check()
                status = "NOMINAL" if "NOMINAL" in report else "ATTENTION"
                return f"Systemes: {status}"
            except Exception as e:
                return f"Check failed: {e}"

        elif task_id == "api_status":
            try:
                from .ai_client import _model_stats
                if _model_stats:
                    lines = []
                    for model, stats in list(_model_stats.items())[:5]:
                        rate = stats.get("successes", 0) / max(stats.get("calls", 1), 1) * 100
                        lines.append(f"  {model}: {rate:.0f}% ({stats.get('calls', 0)} calls)")
                    return "\n".join(lines) if lines else "Aucune donnee API."
                return "Aucune donnee API."
            except Exception:
                return "Stats API indisponibles."

        elif task_id == "kdp_niches":
            try:
                if self._perplexity is None:
                    from .modules.perplexity import TitanPerplexity
                    self._perplexity = TitanPerplexity()
                result = await self._perplexity.search("Amazon KDP low content book niches trending 2026")
                return result[:800] if result else "Pas de niche detectee."
            except Exception as e:
                return f"Erreur: {e}"

        elif task_id == "news_digest":
            try:
                news = await self.news.get_ai_summary()
                return news[:800] if news else "Pas de news overnight."
            except Exception as e:
                return f"Erreur: {e}"

        elif task_id == "memory_backup":
            try:
                import shutil
                mem_dir = Path(__file__).parent / "memory"
                backup_count = 0
                for f in mem_dir.glob("*.json"):
                    shutil.copy2(f, f.with_suffix(".json.bak"))
                    backup_count += 1
                return f"{backup_count} fichiers backupes."
            except Exception as e:
                return f"Backup failed: {e}"

        elif task_id == "rdlab_scan":
            try:
                digest = await self.rdlab_digestor.generate_daily_digest()
                return digest[:800] if digest else "Pas de papers notables."
            except Exception as e:
                return f"Erreur: {e}"

        return "Tache inconnue."

    async def nightshift_run(self):
        """Execute all configured nightshift tasks at their scheduled hours."""
        config = self._load_nightshift()
        if not config.get("enabled"):
            return

        now = _now_paris()
        tasks = config.get("tasks", [])
        if not tasks:
            return

        # Group tasks by hour
        tasks_this_hour = []
        for task_id in tasks:
            meta = self.NIGHTSHIFT_CATALOG.get(task_id, {})
            task_hour = meta.get("hour", 3)
            if now.hour == task_hour and now.minute < 5:
                tasks_this_hour.append(task_id)

        if not tasks_this_hour:
            return

        today = now.strftime("%Y-%m-%d")
        # Check if already ran this hour today
        history_key = f"{today}-{now.hour}"
        history = config.get("history", [])
        if history_key in history:
            return

        # Mark as done
        history.append(history_key)
        # Keep only last 30 entries
        config["history"] = history[-30:]
        self._save_nightshift(config)

        log.info(f"Nightshift: running {len(tasks_this_hour)} tasks at {now.hour}h...")

        sections = [
            f"{'=' * 28}",
            f"  🌙 NIGHTSHIFT — {now.hour}h00",
            f"  {now.strftime('%A %d %B %Y')}",
            f"{'=' * 28}\n",
        ]

        for task_id in tasks_this_hour:
            meta = self.NIGHTSHIFT_CATALOG.get(task_id, {})
            emoji = meta.get("emoji", "⚙️")
            label = meta.get("label", task_id)
            try:
                result = await self._run_nightshift_task(task_id)
                sections.append(f"{emoji} {label}\n{result}\n")
            except Exception as e:
                sections.append(f"{emoji} {label}\nErreur: {e}\n")

        sections.append("Le Building a bosse pendant que tu dormais. 🏢")
        self.send_telegram("\n".join(sections))
        log.info(f"Nightshift {now.hour}h done.")

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
                await self.nightshift_run()            # NIGHTSHIFT — taches configurables via /nightshift
                await self.daily_health_check()        # 6h — santé système
                await self.rdlab_daily_digest()        # 7h30 — R&D Lab papers
                await self.smart_morning_digest()      # 8h — digest du matin
                await self.breaking_news_check()       # Toutes les 15 min (8h-23h) — breaking news IA
                await self.youtube_channel_check()     # Toutes les 30 min — monitoring YouTube
                await self.rdlab_scout_alert()         # 12h — alertes innovations (silent si rien)
                await self.liquefactor_afternoon_digest()  # 14h — digest HTML Liquefactor (remplace aggregator texte)
                await self.afternoon_digest()          # 14h — agrégateur texte (backup si Liquefactor échoue)
                await self.evening_reminder()          # 21h — rappel habitudes
                await self.evening_journal_prompt()    # 21h30 — journal du soir
                await self.rdlab_horizon_monthly()     # 1er du mois 9h — forecast
            except Exception as e:
                log.error(f"Scheduler error: {e}")

            await asyncio.sleep(60)

    def stop(self):
        self.running = False
        log.info("Scheduler stopped.")
