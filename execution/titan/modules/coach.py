"""
TITAN Coach Module — Le Coach Invisible
Détection de patterns, nudges subtils, anti-burnout.

[ZEN + SPARTAN + BALOO]

Features:
- Analyse le rythme de messages (flow / surcharge / inactivité)
- Nudges subtils intégrés aux réponses normales
- Détection de burnout / procrastination
- Stats de productivité (heures actives, patterns)
- Jamais envahissant — 1 nudge max par session
"""

import json
import logging
from datetime import datetime, timedelta
from pathlib import Path

log = logging.getLogger("titan.coach")

MEMORY_DIR = Path(__file__).parent.parent / "memory"
COACH_FILE = MEMORY_DIR / "coach.json"


class TitanCoach:
    """Le Coach Invisible — subtil, jamais envahissant."""

    def __init__(self):
        self._last_nudge_date = None
        self._session_messages = 0
        self._session_start = None

    def _load(self) -> dict:
        if COACH_FILE.exists():
            with open(COACH_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"activity_log": [], "nudges_sent": [], "patterns": {}}

    def _save(self, data: dict):
        with open(COACH_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def log_activity(self):
        """Log une interaction — appelé à chaque message reçu."""
        now = datetime.now()
        data = self._load()

        if not self._session_start:
            self._session_start = now

        self._session_messages += 1

        data["activity_log"].append({
            "timestamp": now.isoformat(),
            "hour": now.hour,
            "weekday": now.strftime("%A"),
        })

        # Garder les 30 derniers jours
        cutoff = (now - timedelta(days=30)).isoformat()
        data["activity_log"] = [
            a for a in data["activity_log"] if a["timestamp"] > cutoff
        ]

        self._save(data)

    def get_nudge(self) -> str:
        """Retourne un nudge contextuel (ou rien si pas pertinent).
        Max 1 nudge par jour. Subtil."""
        now = datetime.now()
        today = now.strftime("%Y-%m-%d")

        # Max 1 nudge/jour
        if self._last_nudge_date == today:
            return ""

        data = self._load()
        activity = data.get("activity_log", [])

        # Pas assez de données
        if len(activity) < 5:
            return ""

        nudge = ""

        # === DÉTECTION PATTERNS ===

        # 1. Travail tard (après 1h du matin)
        if now.hour >= 1 and now.hour <= 5:
            nudge = "🌙 Il est tard, Commandant. Le système tourne sans toi. Dors."

        # 2. Trop de messages en peu de temps (>20 en 1h = surcharge)
        recent_hour = [
            a for a in activity
            if a["timestamp"] > (now - timedelta(hours=1)).isoformat()
        ]
        if len(recent_hour) > 20 and not nudge:
            nudge = "⚡ 20+ messages en 1h. Tu carbures. Pense à respirer 5 min."

        # 3. Longue absence (>48h sans activité)
        if activity:
            last_ts = datetime.fromisoformat(activity[-1]["timestamp"])
            gap = (now - last_ts).total_seconds() / 3600
            if gap > 48 and not nudge:
                nudge = "👋 Content de te revoir. L'empire a attendu patiemment."

        # 4. Week-end travail
        if now.strftime("%A") in ("Saturday", "Sunday") and now.hour < 12 and not nudge:
            if len(recent_hour) > 5:
                nudge = "☀️ Week-end. Le Building peut tourner seul aujourd'hui."

        # 5. Session très longue (>3h d'affilée)
        if self._session_start:
            session_hours = (now - self._session_start).total_seconds() / 3600
            if session_hours > 3 and not nudge:
                nudge = "⏱️ 3h+ de session. Pause recommandée — Spartan approuve."

        if nudge:
            self._last_nudge_date = today
            data["nudges_sent"].append({
                "date": today,
                "nudge": nudge,
                "hour": now.hour,
            })
            if len(data["nudges_sent"]) > 90:
                data["nudges_sent"] = data["nudges_sent"][-90:]
            self._save(data)

        return nudge

    def get_stats(self) -> str:
        """Stats de productivité — quand tu bosses, combien, patterns."""
        data = self._load()
        activity = data.get("activity_log", [])

        if len(activity) < 10:
            return "📊 Pas assez de données (min 10 interactions)."

        # Heures les plus actives
        hours = {}
        days = {}
        for a in activity:
            h = a.get("hour", 0)
            d = a.get("weekday", "?")
            hours[h] = hours.get(h, 0) + 1
            days[d] = days.get(d, 0) + 1

        top_hours = sorted(hours.items(), key=lambda x: x[1], reverse=True)[:3]
        top_days = sorted(days.items(), key=lambda x: x[1], reverse=True)[:3]

        # Streak activité
        dates = sorted(set(
            a["timestamp"][:10] for a in activity
        ), reverse=True)
        streak = 1
        for i in range(len(dates) - 1):
            d1 = datetime.strptime(dates[i], "%Y-%m-%d")
            d2 = datetime.strptime(dates[i + 1], "%Y-%m-%d")
            if (d1 - d2).days == 1:
                streak += 1
            else:
                break

        hours_str = ", ".join(f"{h}h ({c}x)" for h, c in top_hours)
        days_str = ", ".join(f"{d} ({c}x)" for d, c in top_days)

        return (
            f"📊 COACH — STATS PRODUCTIVITÉ\n\n"
            f"🕐 Heures actives : {hours_str}\n"
            f"📅 Jours actifs : {days_str}\n"
            f"🔥 Streak : {streak} jours\n"
            f"💬 Interactions (30j) : {len(activity)}\n"
            f"📈 Moyenne : {len(activity) // max(len(dates), 1)}/jour"
        )

    def get_weekly_insight(self) -> str:
        """Insight hebdo du coach."""
        from ..ai_client import chat

        data = self._load()
        nudges = data.get("nudges_sent", [])[-7:]
        activity = data.get("activity_log", [])

        week_ago = (datetime.now() - timedelta(days=7)).isoformat()
        week_activity = [a for a in activity if a["timestamp"] > week_ago]

        if len(week_activity) < 5:
            return "Pas assez d'activité cette semaine pour un insight."

        hours = [a.get("hour", 0) for a in week_activity]
        avg_hour = sum(hours) / len(hours) if hours else 12

        try:
            insight = chat(
                "Tu es ZEN — coach discret. Analyse le rythme de travail. "
                "1 observation + 1 recommandation. 3 phrases max. Subtil, pas moralisateur.",
                f"Activité semaine : {len(week_activity)} interactions. "
                f"Heure moyenne : {avg_hour:.0f}h. "
                f"Nudges envoyés : {len(nudges)}. "
                f"Détails nudges : {json.dumps(nudges, ensure_ascii=False)}",
                max_tokens=200,
            )
            return f"🧘 INSIGHT HEBDO\n\n{insight}"
        except Exception:
            return f"🧘 Semaine : {len(week_activity)} interactions, heure moyenne {avg_hour:.0f}h."

    def handle_command(self, command: str) -> str:
        """Route les commandes coach."""
        cmd = command.lower().strip()

        if cmd in ("/coach", "/stats"):
            return self.get_stats()
        elif cmd == "/coach insight":
            return self.get_weekly_insight()
        else:
            return (
                "🧘 COACH INVISIBLE\n\n"
                "/coach — Stats productivité\n"
                "/coach insight — Insight hebdo\n\n"
                "Le coach envoie aussi des nudges subtils automatiquement."
            )
