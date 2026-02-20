"""
TITAN Dashboard Module
Visual stats and analytics — see your productivity at a glance.
"""

import json
import os
from datetime import datetime, timedelta
from typing import Optional

MEMORY_DIR = os.path.join(os.path.dirname(__file__), "..", "memory")
DASHBOARD_FILE = os.path.join(MEMORY_DIR, "dashboard_stats.json")


class TitanDashboard:
    """Your command center — analytics and stats."""

    def __init__(self):
        os.makedirs(MEMORY_DIR, exist_ok=True)
        self.data = self._load()

    def _load(self) -> dict:
        if os.path.exists(DASHBOARD_FILE):
            try:
                with open(DASHBOARD_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass

        return {
            "weekly_activity": {},
            "module_usage": {},
            "command_history": [],
            "response_times": [],
            "daily_logs": {},
        }

    def _save(self):
        try:
            with open(DASHBOARD_FILE, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
        except Exception:
            pass

    def log_interaction(self, module: str, command: str = None, response_time: float = None):
        """Log an interaction for analytics."""
        today = datetime.now().strftime("%Y-%m-%d")
        hour = datetime.now().strftime("%H")

        # Weekly activity
        if today not in self.data["weekly_activity"]:
            self.data["weekly_activity"][today] = {"total": 0, "hours": {}}
        self.data["weekly_activity"][today]["total"] += 1
        self.data["weekly_activity"][today]["hours"][hour] = \
            self.data["weekly_activity"][today]["hours"].get(hour, 0) + 1

        # Module usage
        self.data["module_usage"][module] = self.data["module_usage"].get(module, 0) + 1

        # Command history (keep last 100)
        if command:
            self.data["command_history"].append({
                "cmd": command[:50],
                "module": module,
                "time": datetime.now().strftime("%H:%M"),
                "date": today,
            })
            self.data["command_history"] = self.data["command_history"][-100:]

        # Response times
        if response_time:
            self.data["response_times"].append(response_time)
            self.data["response_times"] = self.data["response_times"][-50:]

        # Clean old data (keep 30 days)
        cutoff = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        self.data["weekly_activity"] = {
            k: v for k, v in self.data["weekly_activity"].items() if k >= cutoff
        }

        self._save()

    def _bar_chart(self, data: dict, max_width: int = 15) -> list:
        """Generate a horizontal bar chart."""
        if not data:
            return ["  (pas de données)"]

        max_val = max(data.values()) if data.values() else 1
        lines = []

        for label, value in sorted(data.items(), key=lambda x: x[1], reverse=True):
            bar_len = int((value / max_val) * max_width)
            bar = "█" * bar_len + "░" * (max_width - bar_len)
            lines.append(f"  {label:<12} [{bar}] {value}")

        return lines

    def _sparkline(self, values: list) -> str:
        """Generate a sparkline from values."""
        if not values:
            return "▁▁▁▁▁▁▁"

        chars = "▁▂▃▄▅▆▇█"
        min_val = min(values)
        max_val = max(values)
        rng = max_val - min_val if max_val != min_val else 1

        return "".join(
            chars[min(int((v - min_val) / rng * 7), 7)] for v in values
        )

    def get_overview(self) -> str:
        """Main dashboard view."""
        today = datetime.now().strftime("%Y-%m-%d")

        # Today's stats
        today_data = self.data["weekly_activity"].get(today, {"total": 0, "hours": {}})
        today_total = today_data["total"]

        # Week stats
        week_totals = []
        week_labels = []
        for i in range(6, -1, -1):
            day = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            day_label = (datetime.now() - timedelta(days=i)).strftime("%a")
            count = self.data["weekly_activity"].get(day, {}).get("total", 0)
            week_totals.append(count)
            week_labels.append(day_label)

        week_total = sum(week_totals)
        sparkline = self._sparkline(week_totals)

        # Activity by hour (today)
        peak_hour = None
        if today_data["hours"]:
            peak_hour = max(today_data["hours"], key=today_data["hours"].get)

        # Module usage
        top_modules = dict(
            sorted(self.data["module_usage"].items(), key=lambda x: x[1], reverse=True)[:5]
        )

        # Average response time
        avg_time = None
        if self.data["response_times"]:
            avg_time = sum(self.data["response_times"]) / len(self.data["response_times"])

        lines = [
            f"╔═══════════════════════════════╗",
            f"║   📊 DASHBOARD TITAN            ║",
            f"║   {datetime.now().strftime('%d/%m/%Y %H:%M')}             ║",
            f"╠═══════════════════════════════╣",
            f"║",
            f"║  📅 AUJOURD'HUI",
            f"║  Interactions: {today_total}",
        ]

        if peak_hour:
            lines.append(f"║  Heure de pointe: {peak_hour}h")

        lines.extend([
            f"║",
            f"║  📈 SEMAINE ({week_total} total)",
            f"║  {' '.join(week_labels)}",
            f"║  {sparkline}",
            f"║  {' '.join(str(t).rjust(3) for t in week_totals)}",
            f"║",
            f"║  🔧 TOP MODULES",
        ])

        for module, count in top_modules.items():
            lines.append(f"║  • {module}: {count}")

        if avg_time:
            lines.append(f"║")
            lines.append(f"║  ⚡ Temps moyen: {avg_time:.1f}s")

        lines.extend([
            f"║",
            f"╚═══════════════════════════════╝",
        ])

        return "\n".join(lines)

    def get_weekly_report(self) -> str:
        """Detailed weekly report."""
        lines = [
            f"📊 RAPPORT HEBDOMADAIRE",
            f"Semaine du {(datetime.now() - timedelta(days=6)).strftime('%d/%m')} au {datetime.now().strftime('%d/%m/%Y')}",
            f"{'=' * 35}\n",
        ]

        # Daily breakdown
        lines.append("📅 ACTIVITÉ PAR JOUR\n")
        total = 0
        for i in range(6, -1, -1):
            day = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            day_name = (datetime.now() - timedelta(days=i)).strftime("%A")
            count = self.data["weekly_activity"].get(day, {}).get("total", 0)
            total += count
            bar = "█" * min(count, 20) + "░" * max(0, 20 - count)
            lines.append(f"  {day_name[:3]} [{bar}] {count}")

        lines.append(f"\n  Total: {total} interactions")
        avg = total / 7
        lines.append(f"  Moyenne: {avg:.0f}/jour")

        # Module breakdown
        lines.append(f"\n🔧 MODULES UTILISÉS\n")
        lines.extend(self._bar_chart(self.data["module_usage"]))

        # Most recent commands
        recent = self.data["command_history"][-10:]
        if recent:
            lines.append(f"\n📜 DERNIÈRES COMMANDES\n")
            for cmd in reversed(recent):
                lines.append(f"  [{cmd['time']}] {cmd['cmd']} ({cmd['module']})")

        return "\n".join(lines)

    def get_heatmap(self) -> str:
        """Activity heatmap by hour."""
        lines = [
            f"🗺 HEATMAP D'ACTIVITÉ\n",
            f"Heures les plus actives (30 derniers jours)\n",
        ]

        # Aggregate hours across all days
        hour_totals = {}
        for day_data in self.data["weekly_activity"].values():
            for hour, count in day_data.get("hours", {}).items():
                hour_totals[hour] = hour_totals.get(hour, 0) + count

        if not hour_totals:
            lines.append("  Pas encore de données.")
            return "\n".join(lines)

        max_val = max(hour_totals.values())
        blocks = " ░▒▓█"

        # Display 24h grid
        for h in range(24):
            h_str = f"{h:02d}"
            count = hour_totals.get(h_str, 0)
            intensity = int((count / max_val) * 4) if max_val > 0 else 0
            block = blocks[intensity]
            bar = block * 10
            lines.append(f"  {h_str}h [{bar}] {count}")

        return "\n".join(lines)
