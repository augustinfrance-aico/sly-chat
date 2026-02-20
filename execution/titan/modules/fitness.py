"""
TITAN Fitness Module
Workout generator, calorie tracker, BMI calculator, exercise library.
"""

import random
from datetime import datetime


class TitanFitness:
    """Train hard, stay sharp."""

    WORKOUTS = {
        "push": [
            "Pompes classiques — 4x15",
            "Pompes diamant — 3x12",
            "Dips sur chaise — 3x12",
            "Pike push-ups — 3x10",
            "Pompes declines — 3x12",
        ],
        "pull": [
            "Tractions pronation — 4x8",
            "Tractions supination — 3x10",
            "Rowing inverse (table) — 3x12",
            "Curl biceps (sac a dos leste) — 3x12",
            "Superman hold — 3x30s",
        ],
        "legs": [
            "Squats — 4x20",
            "Fentes avant — 3x12/jambe",
            "Pistol squats (assiste) — 3x8/jambe",
            "Wall sit — 3x45s",
            "Calf raises — 4x20",
            "Jump squats — 3x15",
        ],
        "core": [
            "Planche — 3x60s",
            "Crunchs — 4x20",
            "Mountain climbers — 3x30s",
            "Russian twists — 3x20",
            "Leg raises — 3x15",
            "Planche laterale — 3x30s/cote",
        ],
        "cardio": [
            "Burpees — 3x10",
            "Jumping jacks — 3x30s",
            "High knees — 3x30s",
            "Box jumps (escalier) — 3x12",
            "Sprint sur place — 4x20s",
        ],
    }

    def workout(self, muscle_group: str = "full") -> str:
        """Generate a workout."""
        if muscle_group.lower() == "full":
            exercises = []
            for group in self.WORKOUTS.values():
                exercises.extend(random.sample(group, min(2, len(group))))
            random.shuffle(exercises)
        elif muscle_group.lower() in self.WORKOUTS:
            exercises = self.WORKOUTS[muscle_group.lower()]
        else:
            available = ", ".join(self.WORKOUTS.keys())
            return f"Groupes: {available}, full"

        lines = [
            f"💪 WORKOUT — {muscle_group.upper()}",
            f"{'=' * 25}\n",
        ]
        for i, ex in enumerate(exercises, 1):
            lines.append(f"  {i}. {ex}")

        lines.append(f"\n⏱ Repos: 60s entre les series")
        lines.append(f"🔥 Total: ~{len(exercises) * 5} minutes")
        return "\n".join(lines)

    def bmi(self, weight_kg: float, height_cm: float) -> str:
        """Calculate BMI."""
        height_m = height_cm / 100
        bmi_val = weight_kg / (height_m ** 2)

        if bmi_val < 18.5:
            cat = "Sous-poids"
            emoji = "🔵"
        elif bmi_val < 25:
            cat = "Normal"
            emoji = "🟢"
        elif bmi_val < 30:
            cat = "Surpoids"
            emoji = "🟡"
        else:
            cat = "Obese"
            emoji = "🔴"

        return (
            f"📊 IMC (BMI)\n\n"
            f"Poids: {weight_kg} kg\n"
            f"Taille: {height_cm} cm\n"
            f"IMC: {bmi_val:.1f}\n"
            f"{emoji} Categorie: {cat}"
        )

    def calories(self, weight_kg: float, height_cm: float, age: int, gender: str = "m", activity: str = "moderate") -> str:
        """Calculate daily calorie needs (Mifflin-St Jeor)."""
        if gender.lower() in ("m", "homme", "male"):
            bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
        else:
            bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161

        multipliers = {
            "sedentary": 1.2, "light": 1.375, "moderate": 1.55,
            "active": 1.725, "very_active": 1.9,
        }
        mult = multipliers.get(activity.lower(), 1.55)
        tdee = bmr * mult

        return (
            f"🔥 CALORIES QUOTIDIENNES\n\n"
            f"BMR: {bmr:.0f} kcal\n"
            f"TDEE ({activity}): {tdee:.0f} kcal\n\n"
            f"🟢 Maintien: {tdee:.0f} kcal\n"
            f"📉 Perte: {tdee - 500:.0f} kcal (-500)\n"
            f"📈 Prise: {tdee + 300:.0f} kcal (+300)"
        )

    def stretch(self) -> str:
        """Quick stretching routine."""
        stretches = [
            "Etirement du cou — 30s chaque cote",
            "Epaules en cercle — 15 rotations",
            "Etirement pectoraux (porte) — 30s",
            "Toucher les orteils — 30s",
            "Etirement quadriceps — 30s/jambe",
            "Fente basse — 30s/cote",
            "Chat/Vache — 10 repetitions",
            "Torsion assise — 30s/cote",
        ]
        lines = ["🧘 STRETCHING RAPIDE (5 min)\n"]
        for i, s in enumerate(stretches, 1):
            lines.append(f"  {i}. {s}")
        return "\n".join(lines)

    def challenge_7min(self) -> str:
        """The scientific 7-minute workout."""
        exercises = [
            ("Jumping jacks", "30s"),
            ("Wall sit", "30s"),
            ("Pompes", "30s"),
            ("Crunchs", "30s"),
            ("Step-up chaise", "30s"),
            ("Squats", "30s"),
            ("Dips chaise", "30s"),
            ("Planche", "30s"),
            ("High knees", "30s"),
            ("Fentes", "30s"),
            ("Pompes rotation", "30s"),
            ("Planche laterale", "30s"),
        ]
        lines = ["⚡ 7-MINUTE WORKOUT\n"]
        for i, (ex, dur) in enumerate(exercises, 1):
            lines.append(f"  {i:2d}. {ex} — {dur}")
        lines.append("\n10s de repos entre chaque exercice")
        return "\n".join(lines)
