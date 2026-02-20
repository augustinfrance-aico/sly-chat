"""
TITAN Horoscope Module
Daily horoscope and zodiac info — for fun.
"""

import random
from datetime import datetime


class TitanHoroscope:
    """Les astres parlent... ou pas."""

    SIGNS = {
        "belier": {"emoji": "♈", "en": "aries", "dates": "21 mars - 19 avril", "element": "Feu"},
        "taureau": {"emoji": "♉", "en": "taurus", "dates": "20 avril - 20 mai", "element": "Terre"},
        "gemeaux": {"emoji": "♊", "en": "gemini", "dates": "21 mai - 20 juin", "element": "Air"},
        "cancer": {"emoji": "♋", "en": "cancer", "dates": "21 juin - 22 juillet", "element": "Eau"},
        "lion": {"emoji": "♌", "en": "leo", "dates": "23 juillet - 22 aout", "element": "Feu"},
        "vierge": {"emoji": "♍", "en": "virgo", "dates": "23 aout - 22 septembre", "element": "Terre"},
        "balance": {"emoji": "♎", "en": "libra", "dates": "23 septembre - 22 octobre", "element": "Air"},
        "scorpion": {"emoji": "♏", "en": "scorpio", "dates": "23 octobre - 21 novembre", "element": "Eau"},
        "sagittaire": {"emoji": "♐", "en": "sagittarius", "dates": "22 novembre - 21 decembre", "element": "Feu"},
        "capricorne": {"emoji": "♑", "en": "capricorn", "dates": "22 decembre - 19 janvier", "element": "Terre"},
        "verseau": {"emoji": "♒", "en": "aquarius", "dates": "20 janvier - 18 fevrier", "element": "Air"},
        "poissons": {"emoji": "♓", "en": "pisces", "dates": "19 fevrier - 20 mars", "element": "Eau"},
    }

    PREDICTIONS = {
        "travail": [
            "Une opportunite inattendue se presente. Saisis-la.",
            "Journee productive. Tes efforts seront recompenses.",
            "Un contact professionnel va te surprendre positivement.",
            "Reste concentre sur tes objectifs, les distractions guettent.",
            "C'est le moment de lancer ce projet que tu repousses.",
            "Une collaboration fructueuse s'annonce.",
            "Ton travail acharne commence a porter ses fruits.",
        ],
        "finance": [
            "Bon moment pour investir dans tes competences.",
            "Un revenu supplementaire pourrait arriver bientot.",
            "Prudence avec les depenses impulsives aujourd'hui.",
            "Les astres favorisent les negociations financieres.",
            "Un client ou partenaire lucratif pourrait apparaitre.",
        ],
        "sante": [
            "Prends soin de toi. Une pause s'impose.",
            "L'energie est au rendez-vous, profites-en.",
            "Attention au stress, pense a respirer.",
            "Journee ideale pour le sport ou la meditation.",
            "Ecoute ton corps, il sait ce dont il a besoin.",
        ],
        "mood": [
            "🟢 Excellente journee en perspective !",
            "🟡 Journee correcte, quelques surprises.",
            "🟢 Les energies sont alignees en ta faveur.",
            "🟡 Patience est de mise aujourd'hui.",
            "🟢 Tout roule ! Profite de cette vague positive.",
            "🟡 Quelques defis, mais rien que tu ne puisses gerer.",
        ],
    }

    def daily(self, sign: str) -> str:
        """Get daily horoscope for a sign."""
        sign_lower = sign.lower().strip()
        info = self.SIGNS.get(sign_lower)

        if not info:
            available = ", ".join(self.SIGNS.keys())
            return f"Signe inconnu. Disponibles: {available}"

        # Seed based on date + sign for consistency within a day
        seed = int(datetime.now().strftime("%Y%m%d")) + hash(sign_lower)
        rng = random.Random(seed)

        travail = rng.choice(self.PREDICTIONS["travail"])
        finance = rng.choice(self.PREDICTIONS["finance"])
        sante = rng.choice(self.PREDICTIONS["sante"])
        mood = rng.choice(self.PREDICTIONS["mood"])
        lucky_number = rng.randint(1, 99)
        lucky_color = rng.choice(["Rouge", "Bleu", "Vert", "Or", "Violet", "Blanc", "Noir"])

        return (
            f"{info['emoji']} HOROSCOPE — {sign.upper()}\n"
            f"{'=' * 25}\n"
            f"({info['dates']} | Element: {info['element']})\n\n"
            f"💼 Travail: {travail}\n\n"
            f"💰 Finance: {finance}\n\n"
            f"❤️ Sante: {sante}\n\n"
            f"{mood}\n\n"
            f"🔢 Numero chanceux: {lucky_number}\n"
            f"🎨 Couleur du jour: {lucky_color}"
        )

    def compatibility(self, sign1: str, sign2: str) -> str:
        """Check zodiac compatibility."""
        s1 = self.SIGNS.get(sign1.lower().strip())
        s2 = self.SIGNS.get(sign2.lower().strip())

        if not s1 or not s2:
            return "Signe(s) inconnu(s)."

        # Simple element-based compatibility
        compat_map = {
            ("Feu", "Feu"): 85, ("Feu", "Air"): 90, ("Feu", "Terre"): 50, ("Feu", "Eau"): 40,
            ("Air", "Air"): 80, ("Air", "Terre"): 45, ("Air", "Eau"): 55,
            ("Terre", "Terre"): 85, ("Terre", "Eau"): 90,
            ("Eau", "Eau"): 75,
        }

        pair = (s1["element"], s2["element"])
        score = compat_map.get(pair) or compat_map.get((pair[1], pair[0])) or 60

        bar = "█" * (score // 10) + "░" * (10 - score // 10)
        return (
            f"💕 COMPATIBILITE\n\n"
            f"{s1['emoji']} {sign1.capitalize()} x {s2['emoji']} {sign2.capitalize()}\n"
            f"[{bar}] {score}%\n\n"
            f"Elements: {s1['element']} + {s2['element']}"
        )
