"""
TITAN Calendar & Tasks Module
Personal task manager and daily planner.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path

from ..config import TITAN_NAME


TASKS_FILE = Path(__file__).parent.parent / "memory" / "tasks.json"
HABITS_FILE = Path(__file__).parent.parent / "memory" / "habits.json"


def _load(filepath: Path) -> dict:
    if filepath.exists():
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def _save(filepath: Path, data: dict):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


class TitanCalendar:
    """Titan's personal planner."""

    def __init__(self):
        pass

    # === TASKS ===

    def add_task(self, task: str, priority: str = "normal", due: str = None) -> str:
        """Add a task."""
        data = _load(TASKS_FILE)
        if "tasks" not in data:
            data["tasks"] = []

        task_obj = {
            "id": len(data["tasks"]) + 1,
            "task": task,
            "priority": priority,  # low, normal, high, urgent
            "due": due,
            "status": "todo",
            "created": datetime.now().isoformat(),
        }

        data["tasks"].append(task_obj)
        _save(TASKS_FILE, data)

        emoji = {"low": "⬜", "normal": "🔵", "high": "🟠", "urgent": "🔴"}.get(priority, "🔵")
        due_str = f" (deadline: {due})" if due else ""
        return f"{emoji} Tache ajoutee: {task}{due_str}"

    def complete_task(self, task_id: int) -> str:
        """Mark a task as done."""
        data = _load(TASKS_FILE)
        tasks = data.get("tasks", [])

        for t in tasks:
            if t["id"] == task_id:
                t["status"] = "done"
                t["completed_at"] = datetime.now().isoformat()
                _save(TASKS_FILE, data)
                return f"Done: {t['task']}"

        return f"Tache #{task_id} pas trouvee."

    def delete_task(self, task_id: int) -> str:
        """Delete a task."""
        data = _load(TASKS_FILE)
        tasks = data.get("tasks", [])

        data["tasks"] = [t for t in tasks if t["id"] != task_id]
        _save(TASKS_FILE, data)
        return f"Tache #{task_id} supprimee."

    def list_tasks(self, show_done: bool = False) -> str:
        """List all tasks."""
        data = _load(TASKS_FILE)
        tasks = data.get("tasks", [])

        if not show_done:
            tasks = [t for t in tasks if t["status"] != "done"]

        if not tasks:
            return "Aucune tache en cours. Profite, boss."

        priority_order = {"urgent": 0, "high": 1, "normal": 2, "low": 3}
        tasks.sort(key=lambda t: priority_order.get(t.get("priority", "normal"), 2))

        lines = [f"📋 TACHES ({len(tasks)})\n"]
        for t in tasks:
            emoji = {"low": "⬜", "normal": "🔵", "high": "🟠", "urgent": "🔴"}.get(t.get("priority"), "🔵")
            status = "✅" if t["status"] == "done" else emoji
            due = f" [{t['due']}]" if t.get("due") else ""
            lines.append(f"{status} #{t['id']} {t['task']}{due}")

        return "\n".join(lines)

    # === DAILY PLANNER ===

    def get_today_plan(self) -> str:
        """Get today's plan: tasks + reminders."""
        today = datetime.now().strftime("%Y-%m-%d")
        today_name = datetime.now().strftime("%A %d %B")

        data = _load(TASKS_FILE)
        tasks = [t for t in data.get("tasks", []) if t["status"] != "done"]

        urgent = [t for t in tasks if t.get("priority") == "urgent"]
        high = [t for t in tasks if t.get("priority") == "high"]
        normal = [t for t in tasks if t.get("priority") in ["normal", None]]
        due_today = [t for t in tasks if t.get("due") == today]

        lines = [f"📅 PLAN DU JOUR — {today_name}\n"]

        if due_today:
            lines.append("⏰ DUE AUJOURD'HUI:")
            for t in due_today:
                lines.append(f"  🔴 {t['task']}")
            lines.append("")

        if urgent:
            lines.append("🔴 URGENT:")
            for t in urgent:
                lines.append(f"  • {t['task']}")
            lines.append("")

        if high:
            lines.append("🟠 IMPORTANT:")
            for t in high:
                lines.append(f"  • {t['task']}")
            lines.append("")

        if normal:
            lines.append("🔵 NORMAL:")
            for t in normal[:5]:
                lines.append(f"  • {t['task']}")
            if len(normal) > 5:
                lines.append(f"  + {len(normal) - 5} autres...")

        if not any([urgent, high, normal, due_today]):
            lines.append("Rien de prevu. Journee libre ou tu veux qu'on planifie ?")

        return "\n".join(lines)

    # === HABITS ===

    def add_habit(self, habit: str) -> str:
        """Track a daily habit."""
        data = _load(HABITS_FILE)
        if "habits" not in data:
            data["habits"] = {}

        data["habits"][habit.lower()] = {
            "name": habit,
            "streak": 0,
            "total": 0,
            "last_done": None,
            "created": datetime.now().isoformat(),
        }

        _save(HABITS_FILE, data)
        return f"Habitude ajoutee: {habit}"

    def check_habit(self, habit: str) -> str:
        """Mark a habit as done today."""
        data = _load(HABITS_FILE)
        habits = data.get("habits", {})
        h = habits.get(habit.lower())

        if not h:
            return f"Habitude '{habit}' pas trouvee."

        today = datetime.now().strftime("%Y-%m-%d")
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

        if h["last_done"] == today:
            return f"Deja fait aujourd'hui: {h['name']} (streak: {h['streak']})"

        h["total"] += 1
        if h["last_done"] == yesterday:
            h["streak"] += 1
        else:
            h["streak"] = 1
        h["last_done"] = today

        _save(HABITS_FILE, data)

        fire = "🔥" * min(h["streak"], 5)
        return f"Done: {h['name']} — Streak: {h['streak']} jours {fire}"

    def list_habits(self) -> str:
        """List all habits with streaks."""
        data = _load(HABITS_FILE)
        habits = data.get("habits", {})

        if not habits:
            return "Aucune habitude trackee."

        today = datetime.now().strftime("%Y-%m-%d")
        lines = ["🎯 HABITUDES\n"]

        for key, h in habits.items():
            done_today = "✅" if h.get("last_done") == today else "⬜"
            fire = "🔥" * min(h.get("streak", 0), 3) if h.get("streak", 0) > 0 else ""
            lines.append(f"{done_today} {h['name']} — streak: {h.get('streak', 0)} {fire}")

        return "\n".join(lines)

    # === POMODORO ===

    def pomodoro_start(self, task: str = "focus") -> str:
        """Start a 25-min pomodoro."""
        end_time = (datetime.now() + timedelta(minutes=25)).strftime("%H:%M")
        return f"🍅 Pomodoro demarre: {task}\nFin a {end_time}\nConcentre-toi boss, pas de distraction."

    def pomodoro_break(self) -> str:
        """5-min break."""
        end_time = (datetime.now() + timedelta(minutes=5)).strftime("%H:%M")
        return f"☕ Pause 5 min. Reprends a {end_time}."
