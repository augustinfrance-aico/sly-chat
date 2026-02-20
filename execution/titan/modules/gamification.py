"""
TITAN Gamification Module
Level up your life — XP, achievements, streaks, daily challenges.
Turn productivity into a game.
"""

import json
import os
import random
from datetime import datetime, timedelta
from typing import Optional

GAMIFICATION_DIR = os.path.join(os.path.dirname(__file__), "..", "memory")
GAMIFICATION_FILE = os.path.join(GAMIFICATION_DIR, "gamification.json")

# === XP TABLE ===
LEVEL_TABLE = {
    1: 0,
    2: 100,
    3: 250,
    4: 500,
    5: 800,
    6: 1200,
    7: 1700,
    8: 2500,
    9: 3500,
    10: 5000,
    11: 7000,
    12: 9500,
    13: 12500,
    14: 16000,
    15: 20000,
    16: 25000,
    17: 31000,
    18: 38000,
    19: 46000,
    20: 55000,
    21: 65000,
    22: 77000,
    23: 90000,
    24: 105000,
    25: 125000,
}

LEVEL_TITLES = {
    1: "Recrue",
    2: "Apprenti",
    3: "Initié",
    4: "Opérateur",
    5: "Agent",
    6: "Agent Confirmé",
    7: "Spécialiste",
    8: "Expert",
    9: "Vétéran",
    10: "Maître",
    11: "Élite",
    12: "Champion",
    13: "Légende",
    14: "Titan Bronze",
    15: "Titan Argent",
    16: "Titan Or",
    17: "Titan Platine",
    18: "Titan Diamant",
    19: "Titan Mythique",
    20: "Titan Légendaire",
    21: "Demi-Dieu",
    22: "Dieu",
    23: "Titan Suprême",
    24: "Architecte",
    25: "TITAN ULTIME",
}

# === XP REWARDS ===
XP_ACTIONS = {
    "message": 5,
    "command": 10,
    "task_complete": 25,
    "habit_done": 30,
    "pomodoro": 40,
    "news_check": 10,
    "market_check": 10,
    "search": 15,
    "workflow_create": 50,
    "email_write": 20,
    "code_generate": 25,
    "translate": 15,
    "proposal": 35,
    "memory_save": 10,
    "daily_brief": 20,
    "streak_bonus": 50,
    "first_of_day": 25,
    "night_owl": 15,      # Usage after midnight
    "early_bird": 20,     # Usage before 7am
    "marathon": 100,      # 10+ interactions in a day
}

# === ACHIEVEMENTS ===
ACHIEVEMENTS = {
    # Communication
    "first_words": {
        "name": "🗣 Premiers Mots",
        "desc": "Envoie ton premier message à Titan",
        "condition": "messages >= 1",
        "xp_reward": 50,
    },
    "chatterbox": {
        "name": "💬 Bavard",
        "desc": "Envoie 100 messages",
        "condition": "messages >= 100",
        "xp_reward": 200,
    },
    "storyteller": {
        "name": "📖 Conteur",
        "desc": "Envoie 500 messages",
        "condition": "messages >= 500",
        "xp_reward": 500,
    },
    # Productivity
    "task_starter": {
        "name": "✅ Première Tâche",
        "desc": "Complète ta première tâche",
        "condition": "tasks_completed >= 1",
        "xp_reward": 50,
    },
    "task_machine": {
        "name": "⚡ Machine à Tâches",
        "desc": "Complète 50 tâches",
        "condition": "tasks_completed >= 50",
        "xp_reward": 300,
    },
    "task_legend": {
        "name": "🏆 Légende Productive",
        "desc": "Complète 200 tâches",
        "condition": "tasks_completed >= 200",
        "xp_reward": 1000,
    },
    # Streaks
    "streak_3": {
        "name": "🔥 Flamme",
        "desc": "3 jours de suite d'utilisation",
        "condition": "streak >= 3",
        "xp_reward": 100,
    },
    "streak_7": {
        "name": "🔥🔥 Semaine de Feu",
        "desc": "7 jours consécutifs",
        "condition": "streak >= 7",
        "xp_reward": 250,
    },
    "streak_30": {
        "name": "🔥🔥🔥 Mois Infernal",
        "desc": "30 jours consécutifs",
        "condition": "streak >= 30",
        "xp_reward": 1000,
    },
    "streak_100": {
        "name": "💎 Diamant",
        "desc": "100 jours consécutifs !",
        "condition": "streak >= 100",
        "xp_reward": 5000,
    },
    # Exploration
    "explorer": {
        "name": "🧭 Explorateur",
        "desc": "Utilise 5 modules différents",
        "condition": "modules_used >= 5",
        "xp_reward": 150,
    },
    "master_explorer": {
        "name": "🗺 Maître Explorateur",
        "desc": "Utilise tous les modules",
        "condition": "modules_used >= 10",
        "xp_reward": 500,
    },
    # Finance
    "crypto_watcher": {
        "name": "🪙 Crypto Watcher",
        "desc": "Consulte le marché 10 fois",
        "condition": "market_checks >= 10",
        "xp_reward": 100,
    },
    "wolf_of_wall_street": {
        "name": "🐺 Loup de Wall Street",
        "desc": "Consulte le marché 100 fois",
        "condition": "market_checks >= 100",
        "xp_reward": 500,
    },
    # Automation
    "first_workflow": {
        "name": "⚙️ Automaticien",
        "desc": "Crée ton premier workflow n8n",
        "condition": "workflows_created >= 1",
        "xp_reward": 100,
    },
    "automation_king": {
        "name": "👑 Roi de l'Automation",
        "desc": "Crée 10 workflows",
        "condition": "workflows_created >= 10",
        "xp_reward": 500,
    },
    # Special
    "night_owl": {
        "name": "🦉 Hibou",
        "desc": "Utilise Titan après minuit",
        "condition": "night_sessions >= 1",
        "xp_reward": 50,
    },
    "early_bird": {
        "name": "🐦 Lève-tôt",
        "desc": "Utilise Titan avant 7h",
        "condition": "early_sessions >= 1",
        "xp_reward": 50,
    },
    "marathon_runner": {
        "name": "🏃 Marathonien",
        "desc": "10+ interactions en une journée",
        "condition": "max_daily >= 10",
        "xp_reward": 150,
    },
    "centurion": {
        "name": "💯 Centurion",
        "desc": "50+ interactions en une journée",
        "condition": "max_daily >= 50",
        "xp_reward": 500,
    },
    # Levels
    "level_5": {
        "name": "⭐ Agent",
        "desc": "Atteins le niveau 5",
        "condition": "level >= 5",
        "xp_reward": 200,
    },
    "level_10": {
        "name": "⭐⭐ Maître",
        "desc": "Atteins le niveau 10",
        "condition": "level >= 10",
        "xp_reward": 500,
    },
    "level_20": {
        "name": "⭐⭐⭐ Titan Légendaire",
        "desc": "Atteins le niveau 20",
        "condition": "level >= 20",
        "xp_reward": 2000,
    },
    "level_25": {
        "name": "👑 TITAN ULTIME",
        "desc": "Atteins le niveau maximum !",
        "condition": "level >= 25",
        "xp_reward": 10000,
    },
}

# === DAILY CHALLENGES ===
DAILY_CHALLENGES = [
    {"name": "Productif", "desc": "Complète 3 tâches aujourd'hui", "xp": 75, "check": "daily_tasks >= 3"},
    {"name": "Curieux", "desc": "Fais 3 recherches aujourd'hui", "xp": 50, "check": "daily_searches >= 3"},
    {"name": "Informé", "desc": "Consulte les news et le marché", "xp": 40, "check": "daily_news >= 1 and daily_market >= 1"},
    {"name": "Communiquant", "desc": "Écris un email ou un message pro", "xp": 60, "check": "daily_emails >= 1"},
    {"name": "Codeur", "desc": "Génère ou debug du code", "xp": 60, "check": "daily_code >= 1"},
    {"name": "Polyglotte", "desc": "Traduis quelque chose", "xp": 40, "check": "daily_translate >= 1"},
    {"name": "Automaticien", "desc": "Crée un workflow", "xp": 80, "check": "daily_workflows >= 1"},
    {"name": "Mémorisant", "desc": "Sauvegarde quelque chose en mémoire", "xp": 30, "check": "daily_memories >= 1"},
    {"name": "Marathonien", "desc": "Envoie 20 messages aujourd'hui", "xp": 60, "check": "daily_messages >= 20"},
    {"name": "Multitâche", "desc": "Utilise 4 modules différents", "xp": 70, "check": "daily_modules >= 4"},
]


class TitanGamification:
    """Turn your life into a game. Every action counts."""

    def __init__(self):
        os.makedirs(GAMIFICATION_DIR, exist_ok=True)
        self.data = self._load()

    def _load(self) -> dict:
        """Load gamification data."""
        if os.path.exists(GAMIFICATION_FILE):
            try:
                with open(GAMIFICATION_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass

        return {
            "xp": 0,
            "level": 1,
            "title": "Recrue",
            "achievements": [],
            "streak": 0,
            "last_active_date": None,
            "stats": {
                "messages": 0,
                "commands": 0,
                "tasks_completed": 0,
                "market_checks": 0,
                "workflows_created": 0,
                "night_sessions": 0,
                "early_sessions": 0,
                "max_daily": 0,
                "modules_used_list": [],
                "modules_used": 0,
                "total_days": 0,
            },
            "daily": {
                "date": None,
                "messages": 0,
                "tasks": 0,
                "searches": 0,
                "news": 0,
                "market": 0,
                "emails": 0,
                "code": 0,
                "translate": 0,
                "workflows": 0,
                "memories": 0,
                "modules": [],
                "challenge": None,
                "challenge_done": False,
            },
        }

    def _save(self):
        """Save gamification data."""
        try:
            with open(GAMIFICATION_FILE, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
        except Exception:
            pass

    def _check_daily_reset(self):
        """Reset daily counters if it's a new day."""
        today = datetime.now().strftime("%Y-%m-%d")
        if self.data["daily"]["date"] != today:
            # Update streak
            yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
            if self.data["last_active_date"] == yesterday:
                self.data["streak"] += 1
            elif self.data["last_active_date"] != today:
                self.data["streak"] = 1

            # Track max daily
            prev_daily_msgs = self.data["daily"]["messages"]
            if prev_daily_msgs > self.data["stats"]["max_daily"]:
                self.data["stats"]["max_daily"] = prev_daily_msgs

            # Reset daily
            self.data["daily"] = {
                "date": today,
                "messages": 0,
                "tasks": 0,
                "searches": 0,
                "news": 0,
                "market": 0,
                "emails": 0,
                "code": 0,
                "translate": 0,
                "workflows": 0,
                "memories": 0,
                "modules": [],
                "challenge": None,
                "challenge_done": False,
            }

            # Pick daily challenge
            self.data["daily"]["challenge"] = random.choice(DAILY_CHALLENGES)

            self.data["last_active_date"] = today
            self.data["stats"]["total_days"] += 1

    def _progress_bar(self, current: int, total: int, length: int = 15) -> str:
        """Generate a text progress bar."""
        if total == 0:
            return "█" * length
        filled = int(length * current / total)
        bar = "█" * filled + "░" * (length - filled)
        return bar

    def _get_level_for_xp(self, xp: int) -> int:
        """Get the level for a given XP amount."""
        level = 1
        for lvl, required in sorted(LEVEL_TABLE.items()):
            if xp >= required:
                level = lvl
        return level

    def _xp_for_next_level(self) -> tuple:
        """Get current XP progress and requirement for next level."""
        current_level = self.data["level"]
        if current_level >= 25:
            return self.data["xp"], self.data["xp"], True

        current_threshold = LEVEL_TABLE.get(current_level, 0)
        next_threshold = LEVEL_TABLE.get(current_level + 1, 999999)

        progress = self.data["xp"] - current_threshold
        needed = next_threshold - current_threshold

        return progress, needed, False

    # === PUBLIC API ===

    def add_xp(self, action: str, module: str = None) -> dict:
        """Add XP for an action. Returns level-up info if applicable."""
        self._check_daily_reset()

        xp_gained = XP_ACTIONS.get(action, 5)
        old_level = self.data["level"]

        # Streak bonus
        if self.data["streak"] >= 7:
            xp_gained = int(xp_gained * 1.5)
        elif self.data["streak"] >= 3:
            xp_gained = int(xp_gained * 1.2)

        self.data["xp"] += xp_gained
        new_level = self._get_level_for_xp(self.data["xp"])

        # Update stats
        self.data["stats"]["messages"] += 1
        if action == "command":
            self.data["stats"]["commands"] += 1
        self.data["daily"]["messages"] += 1

        # Track module usage
        if module and module not in self.data["stats"]["modules_used_list"]:
            self.data["stats"]["modules_used_list"].append(module)
            self.data["stats"]["modules_used"] = len(self.data["stats"]["modules_used_list"])
        if module and module not in self.data["daily"]["modules"]:
            self.data["daily"]["modules"].append(module)

        # Time-based bonuses
        hour = datetime.now().hour
        if hour >= 0 and hour < 5:
            self.data["stats"]["night_sessions"] += 1
        if hour >= 5 and hour < 7:
            self.data["stats"]["early_sessions"] += 1

        # Check first of day bonus
        if self.data["daily"]["messages"] == 1:
            self.data["xp"] += XP_ACTIONS["first_of_day"]
            xp_gained += XP_ACTIONS["first_of_day"]

        result = {
            "xp_gained": xp_gained,
            "total_xp": self.data["xp"],
            "level": new_level,
            "leveled_up": new_level > old_level,
            "new_achievements": [],
        }

        # Level up
        if new_level > old_level:
            self.data["level"] = new_level
            self.data["title"] = LEVEL_TITLES.get(new_level, f"Niveau {new_level}")
            result["new_title"] = self.data["title"]

        # Check achievements
        result["new_achievements"] = self._check_achievements()

        self._save()
        return result

    def track_action(self, action_type: str):
        """Track a specific action for daily challenges and stats."""
        self._check_daily_reset()

        mapping = {
            "task_complete": ("tasks_completed", "tasks"),
            "search": (None, "searches"),
            "news_check": (None, "news"),
            "market_check": ("market_checks", "market"),
            "email_write": (None, "emails"),
            "code_generate": (None, "code"),
            "translate": (None, "translate"),
            "workflow_create": ("workflows_created", "workflows"),
            "memory_save": (None, "memories"),
        }

        stat_key, daily_key = mapping.get(action_type, (None, None))

        if stat_key:
            self.data["stats"][stat_key] = self.data["stats"].get(stat_key, 0) + 1
        if daily_key:
            self.data["daily"][daily_key] = self.data["daily"].get(daily_key, 0) + 1

        self._save()

    def _check_achievements(self) -> list:
        """Check and award new achievements."""
        new = []
        stats = self.data["stats"]
        stats["level"] = self.data["level"]
        stats["streak"] = self.data["streak"]
        stats["daily_modules"] = len(self.data["daily"].get("modules", []))

        for ach_id, ach in ACHIEVEMENTS.items():
            if ach_id in self.data["achievements"]:
                continue

            condition = ach["condition"]
            try:
                # Parse simple conditions like "messages >= 100"
                parts = condition.split()
                if len(parts) == 3:
                    key, op, val = parts
                    stat_val = stats.get(key, 0)
                    threshold = int(val)

                    if op == ">=" and stat_val >= threshold:
                        self.data["achievements"].append(ach_id)
                        self.data["xp"] += ach["xp_reward"]
                        new.append(ach)
            except Exception:
                continue

        return new

    def check_daily_challenge(self) -> Optional[dict]:
        """Check if daily challenge is completed."""
        self._check_daily_reset()
        challenge = self.data["daily"].get("challenge")
        if not challenge or self.data["daily"].get("challenge_done"):
            return None

        daily = self.data["daily"]
        check_vars = {
            "daily_tasks": daily.get("tasks", 0),
            "daily_searches": daily.get("searches", 0),
            "daily_news": daily.get("news", 0),
            "daily_market": daily.get("market", 0),
            "daily_emails": daily.get("emails", 0),
            "daily_code": daily.get("code", 0),
            "daily_translate": daily.get("translate", 0),
            "daily_workflows": daily.get("workflows", 0),
            "daily_memories": daily.get("memories", 0),
            "daily_messages": daily.get("messages", 0),
            "daily_modules": len(daily.get("modules", [])),
        }

        try:
            if eval(challenge["check"], {"__builtins__": {}}, check_vars):
                self.data["daily"]["challenge_done"] = True
                self.data["xp"] += challenge["xp"]
                self._save()
                return challenge
        except Exception:
            pass

        return None

    # === DISPLAY ===

    def get_profile(self) -> str:
        """Get the full gamified profile card."""
        self._check_daily_reset()

        progress, needed, maxed = self._xp_for_next_level()
        bar = self._progress_bar(progress, needed)

        streak_icon = "🔥" * min(self.data["streak"], 5) if self.data["streak"] > 0 else "❄️"

        lines = [
            f"╔══════════════════════════════╗",
            f"║  🏛 PROFIL TITAN               ║",
            f"╠══════════════════════════════╣",
            f"║",
            f"║  Niveau {self.data['level']} — {self.data['title']}",
            f"║  XP: {self.data['xp']:,}",
        ]

        if not maxed:
            lines.append(f"║  [{bar}] {progress}/{needed}")
        else:
            lines.append(f"║  [{bar}] MAX LEVEL !")

        lines.extend([
            f"║",
            f"║  {streak_icon} Streak: {self.data['streak']} jours",
            f"║  📊 Messages: {self.data['stats']['messages']:,}",
            f"║  ✅ Tâches: {self.data['stats']['tasks_completed']}",
            f"║  🏅 Achievements: {len(self.data['achievements'])}/{len(ACHIEVEMENTS)}",
            f"║  📅 Jours actifs: {self.data['stats']['total_days']}",
            f"║",
            f"╚══════════════════════════════╝",
        ])

        return "\n".join(lines)

    def get_achievements_display(self) -> str:
        """Display all achievements."""
        self._check_daily_reset()

        lines = ["🏅 ACHIEVEMENTS\n"]
        unlocked = self.data["achievements"]

        for ach_id, ach in ACHIEVEMENTS.items():
            if ach_id in unlocked:
                lines.append(f"  ✅ {ach['name']} — {ach['desc']} (+{ach['xp_reward']} XP)")
            else:
                lines.append(f"  🔒 {ach['name']} — {ach['desc']}")

        lines.append(f"\nDébloqués: {len(unlocked)}/{len(ACHIEVEMENTS)}")
        return "\n".join(lines)

    def get_daily_status(self) -> str:
        """Get daily challenge and stats."""
        self._check_daily_reset()

        daily = self.data["daily"]
        challenge = daily.get("challenge", {})

        lines = [
            f"📋 DÉFI DU JOUR\n",
        ]

        if challenge:
            status = "✅ COMPLÉTÉ !" if daily.get("challenge_done") else "⏳ En cours..."
            lines.append(f"  🎯 {challenge.get('name', '?')}: {challenge.get('desc', '?')}")
            lines.append(f"  Récompense: +{challenge.get('xp', 0)} XP")
            lines.append(f"  Status: {status}")
        else:
            lines.append("  Pas de défi aujourd'hui.")

        lines.extend([
            f"\n📊 STATS DU JOUR",
            f"  💬 Messages: {daily.get('messages', 0)}",
            f"  ✅ Tâches: {daily.get('tasks', 0)}",
            f"  🔍 Recherches: {daily.get('searches', 0)}",
            f"  📧 Emails: {daily.get('emails', 0)}",
            f"  💻 Code: {daily.get('code', 0)}",
            f"  🔥 Streak: {self.data['streak']} jours",
        ])

        return "\n".join(lines)

    def get_leaderboard_position(self) -> str:
        """Fun fake leaderboard to motivate."""
        level = self.data["level"]
        xp = self.data["xp"]

        # Generate fun "competitors"
        fake_users = [
            ("Tony Stark", 25, 130000),
            ("Elon M.", 23, 95000),
            ("Batman", 22, 80000),
            ("John Wick", 20, 58000),
            ("Neo", 18, 40000),
            ("Boss 👑", level, xp),
            ("Average Joe", max(1, level - 3), max(0, xp - 2000)),
        ]

        fake_users.sort(key=lambda x: x[2], reverse=True)

        lines = ["🏆 CLASSEMENT TITAN\n"]
        medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣"]

        for i, (name, lvl, xp_val) in enumerate(fake_users):
            medal = medals[i] if i < len(medals) else f"{i+1}."
            marker = " ◀️ TOI" if name == "Boss 👑" else ""
            lines.append(f"  {medal} {name} — Nv.{lvl} ({xp_val:,} XP){marker}")

        return "\n".join(lines)

    def format_xp_notification(self, result: dict) -> str:
        """Format an XP gain notification for inline display."""
        parts = [f"+{result['xp_gained']} XP"]

        if result.get("leveled_up"):
            parts.append(f"\n\n🎉 LEVEL UP ! Niveau {result['level']} — {result.get('new_title', '')}")

        for ach in result.get("new_achievements", []):
            parts.append(f"\n🏅 Achievement débloqué: {ach['name']}")

        return " ".join(parts) if not result.get("leveled_up") and not result.get("new_achievements") else "\n".join(parts)
