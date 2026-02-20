"""
TITAN Motivation Module
Daily motivation, quotes, affirmations, and mindset tools.
"""

import random
import requests
from datetime import datetime


class TitanMotivation:
    """Stay motivated, stay hungry."""

    AFFIRMATIONS = [
        "Tu es capable de tout ce que tu decides d'accomplir.",
        "Chaque jour est une nouvelle opportunite de devenir meilleur.",
        "Le succes n'est pas final, l'echec n'est pas fatal. C'est le courage de continuer qui compte.",
        "Tu ne perds jamais. Soit tu gagnes, soit tu apprends.",
        "Travaille en silence. Laisse le succes faire du bruit.",
        "La discipline bat le talent quand le talent ne travaille pas.",
        "Pendant que tu dors, quelqu'un travaille. Pendant que tu travailles, quelqu'un progresse.",
        "1% de mieux chaque jour = 37x meilleur en un an.",
        "L'impossible n'est qu'une opinion, pas un fait.",
        "Le meilleur moment pour commencer c'etait hier. Le deuxieme meilleur moment c'est maintenant.",
    ]

    STOIC_QUOTES = [
        "Ce qui te trouble, ce ne sont pas les choses, mais tes jugements sur les choses. — Epictete",
        "Tu as le pouvoir sur ton esprit, pas sur les evenements. Realise cela, et tu trouveras la force. — Marc Aurele",
        "La richesse ne consiste pas a avoir de grandes possessions, mais a avoir peu de besoins. — Epictete",
        "Ce n'est pas parce que les choses sont difficiles que nous n'osons pas ; c'est parce que nous n'osons pas qu'elles sont difficiles. — Seneque",
        "Le bonheur de ta vie depend de la qualite de tes pensees. — Marc Aurele",
    ]

    HUSTLE_QUOTES = [
        "Don't watch the clock; do what it does. Keep going. — Sam Levenson",
        "The only way to do great work is to love what you do. — Steve Jobs",
        "Move fast and break things. Unless you are breaking stuff, you are not moving fast enough. — Zuckerberg",
        "Stay hungry, stay foolish. — Steve Jobs",
        "I have not failed. I've just found 10,000 ways that won't work. — Edison",
        "Success usually comes to those who are too busy to be looking for it. — Thoreau",
        "Your time is limited, don't waste it living someone else's life. — Steve Jobs",
    ]

    def quote(self) -> str:
        """Get a random motivational quote."""
        try:
            resp = requests.get("https://zenquotes.io/api/random", timeout=5)
            data = resp.json()[0]
            return f"💡 CITATION\n\n\"{data['q']}\"\n— {data['a']}"
        except Exception:
            q = random.choice(self.HUSTLE_QUOTES)
            return f"💡 CITATION\n\n{q}"

    def affirmation(self) -> str:
        """Daily affirmation."""
        aff = random.choice(self.AFFIRMATIONS)
        return f"✨ AFFIRMATION DU JOUR\n\n{aff}"

    def stoic(self) -> str:
        """Stoic wisdom."""
        q = random.choice(self.STOIC_QUOTES)
        return f"🏛 SAGESSE STOIQUE\n\n{q}"

    def hustle(self) -> str:
        """Hustle motivation."""
        q = random.choice(self.HUSTLE_QUOTES)
        return f"🔥 HUSTLE MODE\n\n{q}"

    def morning_motivation(self) -> str:
        """Complete morning motivation package."""
        now = datetime.now()
        day_num = now.timetuple().tm_yday
        days_left = 365 - day_num

        return (
            f"☀️ MOTIVATION MATINALE\n"
            f"{'=' * 25}\n\n"
            f"Jour {day_num}/365 — {days_left} jours restants cette annee.\n\n"
            f"💡 {random.choice(self.HUSTLE_QUOTES)}\n\n"
            f"✨ {random.choice(self.AFFIRMATIONS)}\n\n"
            f"🎯 Rappel: chaque minute que tu investis aujourd'hui\n"
            f"te rapproche de la version de toi que tu veux devenir.\n\n"
            f"Let's go boss. 💪"
        )

    def pomodoro_motivation(self) -> str:
        """Quick motivation for focus sessions."""
        msgs = [
            "25 minutes de focus absolu. Tu peux tout faire en 25 min.",
            "Deep work mode. Pas de notifs, pas de distractions. GO.",
            "Un pomodoro a la fois. C'est comme ca qu'on construit des empires.",
            "Focus. Execute. Repeat. Tu es une machine.",
            "25 min qui peuvent changer ta journee. Montre ce que tu vaux.",
        ]
        return f"🍅 {random.choice(msgs)}"

    def weekly_reflection(self) -> str:
        """Weekly reflection prompts."""
        prompts = [
            "Quelle a ete ta plus grande victoire cette semaine ?",
            "Qu'est-ce que tu aurais pu faire mieux ?",
            "Qu'est-ce que tu as appris de nouveau ?",
            "Es-tu plus proche de tes objectifs qu'il y a 7 jours ?",
            "Quelle habitude veux-tu renforcer la semaine prochaine ?",
        ]
        lines = ["📝 REFLEXION HEBDOMADAIRE\n"]
        for i, p in enumerate(prompts, 1):
            lines.append(f"  {i}. {p}")
        return "\n".join(lines)
