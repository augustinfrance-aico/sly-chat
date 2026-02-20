"""
TITAN TaskMaster Module
Proactive task management, reminders, accountability.
Like having 10 billion people working for you.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path

from ..config import MEMORY_DIR
from ..ai_client import chat as ai_chat


class TitanTaskMaster:
    """Ton gestionnaire de tâches qui ne te lâche JAMAIS."""

    TASKS_FILE = MEMORY_DIR / "tasks.json"

    PRIORITIES = {"urgent": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}

    def __init__(self):
        pass

    def _load_tasks(self) -> dict:
        if self.TASKS_FILE.exists():
            return json.loads(self.TASKS_FILE.read_text(encoding="utf-8"))
        return {"tasks": [], "completed": [], "recurring": []}

    def _save_tasks(self, data: dict):
        self.TASKS_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    def add(self, title: str, priority: str = "medium", due: str = "", category: str = "general") -> str:
        """Add a task."""
        data = self._load_tasks()
        task = {
            "id": len(data["tasks"]) + len(data["completed"]) + 1,
            "title": title,
            "priority": priority.lower(),
            "category": category,
            "due": due if due else (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
            "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "status": "pending",
        }
        data["tasks"].append(task)
        self._save_tasks(data)

        emoji = self.PRIORITIES.get(priority.lower(), "🟡")
        return (
            f"✅ TÂCHE AJOUTÉE\n\n"
            f"{emoji} {title}\n"
            f"📂 {category} | ⏰ {task['due']}\n"
            f"ID: #{task['id']}"
        )

    def list_tasks(self, filter_cat: str = "") -> str:
        """List all pending tasks."""
        data = self._load_tasks()
        tasks = data.get("tasks", [])

        if filter_cat:
            tasks = [t for t in tasks if t.get("category", "").lower() == filter_cat.lower()]

        if not tasks:
            return "🎉 Aucune tâche en cours. Profite ou crée-toi des objectifs!"

        # Sort by priority then due date
        priority_order = {"urgent": 0, "high": 1, "medium": 2, "low": 3}
        tasks.sort(key=lambda t: (priority_order.get(t.get("priority", "medium"), 2), t.get("due", "")))

        lines = ["📋 MES TÂCHES\n"]

        # Check for overdue
        today = datetime.now().strftime("%Y-%m-%d")
        overdue = [t for t in tasks if t.get("due", "") < today]
        if overdue:
            lines.append("⚠️ EN RETARD:")
            for t in overdue:
                emoji = self.PRIORITIES.get(t.get("priority", "medium"), "🟡")
                lines.append(f"  {emoji} #{t['id']} {t['title']} (DUE: {t['due']})")
            lines.append("")

        # Today
        today_tasks = [t for t in tasks if t.get("due", "") == today]
        if today_tasks:
            lines.append("📅 AUJOURD'HUI:")
            for t in today_tasks:
                emoji = self.PRIORITIES.get(t.get("priority", "medium"), "🟡")
                lines.append(f"  {emoji} #{t['id']} {t['title']}")
            lines.append("")

        # Upcoming
        upcoming = [t for t in tasks if t.get("due", "") > today]
        if upcoming:
            lines.append("📆 À VENIR:")
            for t in upcoming[:10]:
                emoji = self.PRIORITIES.get(t.get("priority", "medium"), "🟡")
                lines.append(f"  {emoji} #{t['id']} {t['title']} ({t['due']})")

        lines.append(f"\n📊 Total: {len(tasks)} tâches | {len(overdue)} en retard")
        return "\n".join(lines)

    def done(self, task_id: str) -> str:
        """Mark a task as done."""
        data = self._load_tasks()
        task_id_int = int(task_id)

        for i, task in enumerate(data["tasks"]):
            if task["id"] == task_id_int:
                task["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                task["status"] = "completed"
                data["completed"].append(task)
                data["tasks"].pop(i)
                self._save_tasks(data)

                remaining = len(data["tasks"])
                return (
                    f"✅ TÂCHE COMPLÉTÉE\n\n"
                    f"🎯 {task['title']}\n\n"
                    f"📊 Reste: {remaining} tâche(s)"
                )

        return f"Tâche #{task_id} non trouvée."

    def delete(self, task_id: str) -> str:
        """Delete a task."""
        data = self._load_tasks()
        task_id_int = int(task_id)

        for i, task in enumerate(data["tasks"]):
            if task["id"] == task_id_int:
                data["tasks"].pop(i)
                self._save_tasks(data)
                return f"🗑️ Tâche #{task_id} supprimée: {task['title']}"

        return f"Tâche #{task_id} non trouvée."

    def proactive_check(self) -> str:
        """Proactive task reminder — what needs attention NOW."""
        data = self._load_tasks()
        tasks = data.get("tasks", [])

        if not tasks:
            return ""  # Nothing to report

        today = datetime.now().strftime("%Y-%m-%d")
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

        overdue = [t for t in tasks if t.get("due", "") < today]
        today_tasks = [t for t in tasks if t.get("due", "") == today]
        tomorrow_tasks = [t for t in tasks if t.get("due", "") == tomorrow]
        urgent = [t for t in tasks if t.get("priority") == "urgent"]

        lines = []

        if overdue:
            lines.append(f"⚠️ {len(overdue)} tâche(s) EN RETARD!")
            for t in overdue[:3]:
                lines.append(f"  🔴 {t['title']} (due: {t['due']})")

        if urgent:
            lines.append(f"🚨 {len(urgent)} tâche(s) URGENTE(S)")
            for t in urgent[:3]:
                lines.append(f"  🔴 {t['title']}")

        if today_tasks:
            lines.append(f"📅 {len(today_tasks)} tâche(s) pour AUJOURD'HUI")
            for t in today_tasks[:3]:
                emoji = self.PRIORITIES.get(t.get("priority", "medium"), "🟡")
                lines.append(f"  {emoji} {t['title']}")

        if tomorrow_tasks:
            lines.append(f"📆 {len(tomorrow_tasks)} tâche(s) pour DEMAIN")

        if not lines:
            return ""

        return "🤖 RAPPEL TITAN\n\n" + "\n".join(lines)

    def weekly_summary(self) -> str:
        """Weekly productivity summary."""
        data = self._load_tasks()
        completed = data.get("completed", [])
        pending = data.get("tasks", [])

        week_start = (datetime.now() - timedelta(days=datetime.now().weekday())).strftime("%Y-%m-%d")
        week_completed = [t for t in completed if t.get("completed_at", "")[:10] >= week_start]

        lines = ["📊 BILAN HEBDOMADAIRE\n"]
        lines.append(f"✅ Complétées cette semaine: {len(week_completed)}")
        lines.append(f"📋 En cours: {len(pending)}")

        if week_completed:
            lines.append(f"\n🏆 FAIT CETTE SEMAINE:")
            for t in week_completed[:10]:
                lines.append(f"  ✅ {t['title']}")

        # Categories breakdown
        cats = {}
        for t in week_completed:
            cat = t.get("category", "general")
            cats[cat] = cats.get(cat, 0) + 1

        if cats:
            lines.append(f"\n📂 PAR CATÉGORIE:")
            for cat, count in sorted(cats.items(), key=lambda x: x[1], reverse=True):
                lines.append(f"  • {cat}: {count}")

        # Productivity score
        total = len(week_completed) + len(pending)
        if total > 0:
            score = (len(week_completed) / total) * 100
            lines.append(f"\n📈 Score productivité: {score:.0f}%")

        return "\n".join(lines)

    async def plan_day(self) -> str:
        """AI-generated daily plan based on pending tasks."""
        data = self._load_tasks()
        tasks = data.get("tasks", [])

        if not tasks:
            return "Aucune tâche. Ajoute des tâches avec /taskadd [titre]"

        tasks_text = "\n".join([
            f"- [{t.get('priority', 'medium')}] {t['title']} (due: {t.get('due', '?')}, cat: {t.get('category', 'general')})"
            for t in tasks[:15]
        ])

        return ai_chat("Expert assistant.", f"""Voici mes taches en cours:\n\n{tasks_text}\n\nCree un plan de journee optimal. Organise par blocs de temps, priorite aux taches urgentes.""", 1000)
