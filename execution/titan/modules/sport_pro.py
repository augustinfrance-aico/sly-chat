"""
TITAN Sport Pro Module
Advanced sport tracking, programs, performance analysis, nutrition.
For someone who trains seriously.
"""

import json
import random
from datetime import datetime, timedelta
from pathlib import Path

from ..config import MEMORY_DIR
from ..ai_client import chat as ai_chat


class TitanSportPro:
    """Coach sportif personnel. Pas de repos."""

    SPORT_FILE = MEMORY_DIR / "sport_log.json"

    PROGRAMS = {
        "badminton": {
            "warmup": ["Jogging léger 5min", "Montées de genoux", "Talons-fesses", "Rotations épaules", "Shadow badminton 3min"],
            "drills": ["Clear fond de court x20", "Smash depuis mi-court x15", "Jeu de jambes en étoile x10", "Service court x20", "Drive croisé x15", "Amortis filet x20"],
            "conditioning": ["Suicide runs x5", "Squats sautés x15", "Fentes marchées x20", "Gainage 60s x3", "Burpees x10"],
            "tips": [
                "Grip: relâché en attente, serré au frappe",
                "Toujours revenir au centre après chaque coup",
                "Anticipe la trajectoire, pas le mouvement adverse",
                "Le jeu de jambes > la force du bras",
            ],
        },
        "musculation": {
            "push": ["Développé couché 4x8", "Développé militaire 3x10", "Dips 3x12", "Écarté haltères 3x12", "Triceps pushdown 3x15"],
            "pull": ["Tractions 4x8", "Rowing barre 4x8", "Tirage vertical 3x10", "Curl biceps 3x12", "Face pulls 3x15"],
            "legs": ["Squats 4x8", "Presse 3x10", "Fentes 3x12/jambe", "Leg curl 3x12", "Mollets 4x15", "Hip thrust 3x10"],
            "tips": [
                "Progressive overload: augmente poids OU reps chaque semaine",
                "1.6-2g de protéines par kg de poids de corps",
                "Le repos est aussi important que l'entraînement",
                "Forme > Ego. Baisse le poids si la forme se dégrade.",
            ],
        },
        "running": {
            "debutant": ["Lundi: 20min footing lent", "Mercredi: 25min footing", "Samedi: 30min footing"],
            "intermediaire": ["Lundi: 40min footing", "Mercredi: 30min fractionné (5x400m)", "Vendredi: 30min tempo run", "Dimanche: 50min sortie longue"],
            "avance": ["Lundi: 50min footing", "Mardi: Fractionné (8x400m)", "Jeudi: Tempo 40min", "Samedi: Sortie longue 1h15", "Dimanche: Footing récup 30min"],
            "tips": [
                "80% des runs en endurance fondamentale (tu peux parler)",
                "Augmente max 10% de volume par semaine",
                "Hydratation: bois AVANT d'avoir soif",
                "Cadence idéale: 170-180 pas/min",
            ],
        },
    }

    NUTRITION = {
        "pre_workout": [
            "Banane + beurre de cacahuète (30min avant)",
            "Flocons d'avoine + miel (1h avant)",
            "Toast + confiture (45min avant)",
            "Yaourt grec + fruits (1h avant)",
        ],
        "post_workout": [
            "Shake protéiné + banane (dans les 30min)",
            "Poulet + riz + légumes",
            "Oeufs + avocat + pain complet",
            "Saumon + patate douce + brocolis",
        ],
        "supplements": [
            ("Créatine", "5g/jour", "Force et récupération musculaire"),
            ("Whey Protéine", "25-30g post-workout", "Synthèse protéique"),
            ("Omega-3", "2-3g/jour", "Anti-inflammatoire, récupération"),
            ("Vitamine D", "2000 UI/jour", "Immunité, os, énergie"),
            ("Magnésium", "300-400mg/soir", "Récupération, sommeil, crampes"),
        ],
    }

    def __init__(self):
        pass

    def _load_log(self) -> dict:
        if self.SPORT_FILE.exists():
            return json.loads(self.SPORT_FILE.read_text(encoding="utf-8"))
        return {"sessions": [], "goals": [], "records": {}}

    def _save_log(self, data: dict):
        self.SPORT_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    def log_session(self, sport: str, duration: str = "60", notes: str = "") -> str:
        """Log a training session."""
        data = self._load_log()
        session = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "sport": sport,
            "duration_min": int(duration),
            "notes": notes,
        }
        data["sessions"].append(session)
        self._save_log(data)

        # Count sessions this week
        week_start = datetime.now() - timedelta(days=datetime.now().weekday())
        week_sessions = [s for s in data["sessions"] if s["date"] >= week_start.strftime("%Y-%m-%d")]

        return (
            f"💪 SESSION ENREGISTRÉE\n\n"
            f"🏋️ {sport}\n"
            f"⏱️ {duration} min\n"
            f"{f'📝 {notes}' if notes else ''}\n\n"
            f"📊 Cette semaine: {len(week_sessions)} sessions"
        )

    def stats(self) -> str:
        """Get training stats."""
        data = self._load_log()
        sessions = data.get("sessions", [])

        if not sessions:
            return "Aucune session enregistrée. Utilise /sportlog [sport] [durée] pour logger."

        # This week
        week_start = (datetime.now() - timedelta(days=datetime.now().weekday())).strftime("%Y-%m-%d")
        week = [s for s in sessions if s["date"] >= week_start]

        # This month
        month_start = datetime.now().strftime("%Y-%m-01")
        month = [s for s in sessions if s["date"] >= month_start]

        # Sports breakdown
        sports = {}
        for s in sessions:
            sp = s.get("sport", "?")
            if sp not in sports:
                sports[sp] = 0
            sports[sp] += 1

        total_time = sum(s.get("duration_min", 0) for s in sessions)
        week_time = sum(s.get("duration_min", 0) for s in week)

        lines = ["📊 STATS SPORT\n"]
        lines.append(f"📅 Cette semaine: {len(week)} sessions ({week_time}min)")
        lines.append(f"📅 Ce mois: {len(month)} sessions")
        lines.append(f"📅 Total: {len(sessions)} sessions ({total_time}min)")

        lines.append(f"\n🏆 PAR SPORT:")
        for sp, count in sorted(sports.items(), key=lambda x: x[1], reverse=True):
            lines.append(f"  • {sp}: {count} sessions")

        # Streak
        dates = sorted(set(s["date"][:10] for s in sessions), reverse=True)
        streak = 0
        check = datetime.now().strftime("%Y-%m-%d")
        for d in dates:
            if d == check:
                streak += 1
                check = (datetime.strptime(check, "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")
            else:
                break

        lines.append(f"\n🔥 Streak actuel: {streak} jour(s)")
        return "\n".join(lines)

    def program(self, sport: str = "badminton") -> str:
        """Get a training program."""
        sport_key = sport.lower().strip()
        prog = self.PROGRAMS.get(sport_key)

        if not prog:
            return f"Sport '{sport}' pas trouvé. Dispo: {', '.join(self.PROGRAMS.keys())}"

        lines = [f"🏋️ PROGRAMME {sport_key.upper()}\n"]

        for section, exercises in prog.items():
            if section == "tips":
                lines.append(f"\n💡 CONSEILS:")
                for tip in exercises:
                    lines.append(f"  • {tip}")
            else:
                lines.append(f"\n📋 {section.upper().replace('_', ' ')}:")
                for ex in exercises:
                    lines.append(f"  • {ex}")

        return "\n".join(lines)

    def nutrition_advice(self, timing: str = "post_workout") -> str:
        """Get nutrition advice."""
        lines = ["🥗 NUTRITION SPORTIVE\n"]

        if timing in ("pre", "pre_workout", "avant"):
            lines.append("🍌 AVANT L'ENTRAÎNEMENT:\n")
            for meal in self.NUTRITION["pre_workout"]:
                lines.append(f"  • {meal}")
        elif timing in ("post", "post_workout", "après", "apres"):
            lines.append("🍗 APRÈS L'ENTRAÎNEMENT:\n")
            for meal in self.NUTRITION["post_workout"]:
                lines.append(f"  • {meal}")
        elif timing in ("supplements", "supps", "complements"):
            lines.append("💊 SUPPLÉMENTS RECOMMANDÉS:\n")
            for name, dose, effect in self.NUTRITION["supplements"]:
                lines.append(f"  • {name}: {dose}")
                lines.append(f"    → {effect}")
        else:
            # All
            lines.append("🍌 AVANT:\n")
            for meal in self.NUTRITION["pre_workout"][:2]:
                lines.append(f"  • {meal}")
            lines.append("\n🍗 APRÈS:\n")
            for meal in self.NUTRITION["post_workout"][:2]:
                lines.append(f"  • {meal}")
            lines.append("\n💊 SUPPLÉMENTS TOP 3:\n")
            for name, dose, effect in self.NUTRITION["supplements"][:3]:
                lines.append(f"  • {name}: {dose} — {effect}")

        return "\n".join(lines)

    async def custom_program(self, request: str) -> str:
        """AI-generated custom training program."""
        return ai_chat("Expert assistant.", f"""Crée un programme d'entraînement personnalisé: "{request}" """, 1500)

    def motivation_sport(self) -> str:
        """Sport motivation quote."""
        quotes = [
            ("🏆", "La douleur d'aujourd'hui sera ta force de demain.", "Arnold Schwarzenegger"),
            ("💪", "Ce n'est pas la taille du chien dans le combat, c'est la taille du combat dans le chien.", "Mark Twain"),
            ("🔥", "Je déteste chaque minute d'entraînement. Mais je me dis: n'abandonne pas. Souffre maintenant et vis le reste de ta vie en champion.", "Muhammad Ali"),
            ("⚡", "L'excellence n'est pas un acte mais une habitude.", "Aristote"),
            ("🎯", "Tu ne peux pas mettre de limite à quoi que ce soit. Plus tu rêves, plus tu vas loin.", "Michael Phelps"),
            ("💥", "Ton corps peut supporter presque tout. C'est ton esprit que tu dois convaincre.", "Anonyme"),
            ("🏅", "La différence entre l'ordinaire et l'extraordinaire, c'est le petit extra.", "Jimmy Johnson"),
        ]
        emoji, quote, author = random.choice(quotes)
        return f"{emoji} MOTIVATION SPORT\n\n« {quote} »\n\n— {author}"
