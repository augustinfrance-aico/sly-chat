"""
TITAN Productivity Module
Eisenhower matrix, time blocking, SMART goals, weekly review.
"""

from datetime import datetime

from ..ai_client import chat as ai_chat


class TitanProductivity:
    """Work smarter, not harder."""

    def __init__(self):
        pass

    def eisenhower(self, tasks: str) -> str:
        """Sort tasks into Eisenhower matrix.
        tasks format: "task1, task2, task3"
        """
        task_list = [t.strip() for t in tasks.split(",")]
        lines = [
            f"📊 MATRICE EISENHOWER\n",
            f"{'=' * 35}\n",
            f"🔴 URGENT + IMPORTANT (faire maintenant):",
        ]

        # Simple heuristic: first tasks = urgent+important
        per_quadrant = max(1, len(task_list) // 4)
        q1 = task_list[:per_quadrant]
        q2 = task_list[per_quadrant:per_quadrant * 2]
        q3 = task_list[per_quadrant * 2:per_quadrant * 3]
        q4 = task_list[per_quadrant * 3:]

        for t in q1:
            lines.append(f"  • {t}")

        lines.append(f"\n🟡 IMPORTANT (planifier):")
        for t in q2:
            lines.append(f"  • {t}")

        lines.append(f"\n🟠 URGENT (deleguer):")
        for t in q3:
            lines.append(f"  • {t}")

        lines.append(f"\n⚪ NI L'UN NI L'AUTRE (eliminer):")
        for t in q4:
            lines.append(f"  • {t}")

        return "\n".join(lines)

    async def smart_goal(self, goal: str) -> str:
        """Convert a vague goal into SMART format."""
        return ai_chat("Expert assistant.", f"""Transforme cet objectif en objectif SMART: "{goal}" """, 1000)

    def time_block(self, tasks: str) -> str:
        """Create a time-blocked schedule.
        tasks: "task1:1h, task2:30m, task3:2h"
        """
        now = datetime.now().replace(hour=9, minute=0, second=0)
        items = [t.strip() for t in tasks.split(",")]

        lines = [f"⏰ TIME BLOCKING\n", f"{'=' * 25}\n"]
        current = now

        for item in items:
            parts = item.split(":")
            task = parts[0].strip()
            duration = parts[1].strip() if len(parts) > 1 else "1h"

            # Parse duration
            minutes = 60
            if "h" in duration:
                minutes = int(duration.replace("h", "").strip()) * 60
            elif "m" in duration:
                minutes = int(duration.replace("m", "").strip())

            end = current.replace(minute=current.minute + minutes)
            start_str = current.strftime("%H:%M")
            end_str = f"{(current.hour + minutes // 60):02d}:{(current.minute + minutes % 60):02d}"

            lines.append(f"  {start_str} - {end_str} | {task}")

            from datetime import timedelta
            current = current + timedelta(minutes=minutes)

            # Add break every 90 min
            if (current - now).seconds > 5400 and (current - now).seconds % 5400 < minutes * 60:
                break_end = current + timedelta(minutes=15)
                lines.append(f"  {current.strftime('%H:%M')} - {break_end.strftime('%H:%M')} | ☕ Pause")
                current = break_end

        return "\n".join(lines)

    def pareto(self, items: str) -> str:
        """Apply Pareto principle (80/20) to a list."""
        item_list = [t.strip() for t in items.split(",")]
        top_20 = max(1, len(item_list) // 5)

        lines = [
            f"📊 PRINCIPE DE PARETO (80/20)\n",
            f"Sur {len(item_list)} elements, concentre-toi sur ces {top_20}:\n",
            f"🔥 TOP {top_20} (20% qui gerent 80% des resultats):",
        ]
        for t in item_list[:top_20]:
            lines.append(f"  ⭐ {t}")

        lines.append(f"\n📋 Le reste ({len(item_list) - top_20} elements):")
        for t in item_list[top_20:]:
            lines.append(f"  • {t}")

        return "\n".join(lines)

    def rule_of_three(self) -> str:
        """The Rule of 3 — pick 3 things for today."""
        return (
            f"3️⃣ REGLE DES 3\n\n"
            f"Choisis les 3 choses les plus importantes a faire aujourd'hui:\n\n"
            f"1. ________________________________\n"
            f"2. ________________________________\n"
            f"3. ________________________________\n\n"
            f"Si tu ne fais QUE ces 3 choses, la journee est un succes.\n"
            f"Envoie /task pour les ajouter."
        )
