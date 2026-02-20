"""
TITAN Bible Module
Daily verses, book exploration, wisdom, devotion.
Uses free Bible API.
"""

import random
import requests

from ..ai_client import chat as ai_chat


class TitanBible:
    """La Parole au quotidien."""

    POPULAR_VERSES = [
        ("Philippiens 4:13", "Je puis tout par celui qui me fortifie."),
        ("Psaumes 23:1", "L'Éternel est mon berger: je ne manquerai de rien."),
        ("Proverbes 3:5-6", "Confie-toi en l'Éternel de tout ton cœur, et ne t'appuie pas sur ta sagesse."),
        ("Romains 8:28", "Toutes choses concourent au bien de ceux qui aiment Dieu."),
        ("Josué 1:9", "Fortifie-toi et prends courage. Ne t'effraie point, car l'Éternel ton Dieu est avec toi partout où tu iras."),
        ("Jérémie 29:11", "Car je connais les projets que j'ai formés sur vous, dit l'Éternel, projets de paix et non de malheur, afin de vous donner un avenir et de l'espérance."),
        ("Psaumes 46:10", "Arrêtez, et sachez que je suis Dieu."),
        ("Matthieu 6:33", "Cherchez premièrement le royaume et la justice de Dieu; et toutes ces choses vous seront données par-dessus."),
        ("Esaïe 40:31", "Ceux qui se confient en l'Éternel renouvellent leur force. Ils prennent le vol comme les aigles."),
        ("Psaumes 119:105", "Ta parole est une lampe à mes pieds, et une lumière sur mon sentier."),
        ("Jean 3:16", "Car Dieu a tant aimé le monde qu'il a donné son Fils unique, afin que quiconque croit en lui ne périsse point, mais qu'il ait la vie éternelle."),
        ("Romains 12:2", "Ne vous conformez pas au siècle présent, mais soyez transformés par le renouvellement de l'intelligence."),
        ("2 Timothée 1:7", "Car ce n'est pas un esprit de timidité que Dieu nous a donné, mais un esprit de force, d'amour et de sagesse."),
        ("Psaumes 37:4", "Fais de l'Éternel tes délices, et il te donnera ce que ton cœur désire."),
        ("Proverbes 16:3", "Recommande à l'Éternel tes œuvres, et tes projets réussiront."),
        ("Matthieu 7:7", "Demandez, et l'on vous donnera; cherchez, et vous trouverez; frappez, et l'on vous ouvrira."),
        ("Psaumes 91:1-2", "Celui qui demeure sous l'abri du Très Haut repose à l'ombre du Tout Puissant."),
        ("Colossiens 3:23", "Tout ce que vous faites, faites-le de bon cœur, comme pour le Seigneur et non pour des hommes."),
        ("Proverbes 27:17", "Comme le fer aiguise le fer, ainsi un homme excite la colère d'un homme."),
        ("Galates 6:9", "Ne nous lassons pas de faire le bien; car nous moissonnerons au temps convenable, si nous ne nous relâchons pas."),
    ]

    # Thematic verses for specific situations
    THEMES = {
        "force": [
            ("Philippiens 4:13", "Je puis tout par celui qui me fortifie."),
            ("Esaïe 41:10", "Ne crains rien, car je suis avec toi; ne promène pas des regards inquiets."),
            ("2 Timothée 1:7", "Car ce n'est pas un esprit de timidité que Dieu nous a donné."),
        ],
        "paix": [
            ("Jean 14:27", "Je vous laisse la paix, je vous donne ma paix."),
            ("Philippiens 4:6-7", "Ne vous inquiétez de rien; mais en toute chose faites connaître vos besoins à Dieu par des prières."),
            ("Psaumes 46:10", "Arrêtez, et sachez que je suis Dieu."),
        ],
        "sagesse": [
            ("Proverbes 3:5-6", "Confie-toi en l'Éternel de tout ton cœur."),
            ("Jacques 1:5", "Si quelqu'un d'entre vous manque de sagesse, qu'il la demande à Dieu."),
            ("Proverbes 4:7", "Voici le commencement de la sagesse: acquiers la sagesse."),
        ],
        "business": [
            ("Proverbes 16:3", "Recommande à l'Éternel tes œuvres, et tes projets réussiront."),
            ("Colossiens 3:23", "Tout ce que vous faites, faites-le de bon cœur, comme pour le Seigneur."),
            ("Proverbes 22:29", "Si tu vois un homme habile dans son travail, il se tient devant les rois."),
        ],
        "perseverance": [
            ("Galates 6:9", "Ne nous lassons pas de faire le bien."),
            ("Jacques 1:12", "Heureux l'homme qui supporte patiemment la tentation."),
            ("Romains 5:3-4", "La tribulation produit la persévérance, la persévérance la victoire dans l'épreuve."),
        ],
        "confiance": [
            ("Jérémie 29:11", "Car je connais les projets que j'ai formés sur vous."),
            ("Psaumes 37:5", "Recommande ton sort à l'Éternel, mets en lui ta confiance, et il agira."),
            ("Proverbes 3:5", "Confie-toi en l'Éternel de tout ton cœur."),
        ],
    }

    BOOKS_INFO = {
        "genese": "Genèse — La création, Abraham, Isaac, Jacob, Joseph. Le commencement de tout.",
        "exode": "Exode — Moïse, les 10 plaies, la traversée de la mer Rouge, les 10 commandements.",
        "psaumes": "Psaumes — 150 chants de louange, prière et méditation. Le cœur de la Bible.",
        "proverbes": "Proverbes — Sagesse pratique pour la vie quotidienne. Business + vie.",
        "ecclesiaste": "Ecclésiaste — La quête du sens de la vie. Vanité des vanités.",
        "matthieu": "Matthieu — La vie de Jésus racontée pour les Juifs. Le Sermon sur la Montagne.",
        "jean": "Jean — L'évangile le plus spirituel. 'Au commencement était la Parole.'",
        "romains": "Romains — La théologie de Paul. Justification par la foi.",
        "apocalypse": "Apocalypse — La fin des temps. Visions de Jean sur l'île de Patmos.",
    }

    def __init__(self):
        pass

    def verse_of_day(self) -> str:
        """Get an inspiring verse of the day."""
        ref, text = random.choice(self.POPULAR_VERSES)
        return (
            f"📖 VERSET DU JOUR\n\n"
            f"« {text} »\n\n"
            f"— {ref}"
        )

    def verse_theme(self, theme: str = "force") -> str:
        """Get verses by theme."""
        theme_key = theme.lower().strip()
        if theme_key in self.THEMES:
            verses = self.THEMES[theme_key]
        else:
            return (
                f"Thème '{theme}' non trouvé.\n"
                f"Thèmes dispo: {', '.join(self.THEMES.keys())}\n"
                f"Usage: /bibletheme [thème]"
            )

        lines = [f"📖 VERSETS — {theme_key.upper()}\n"]
        for ref, text in verses:
            lines.append(f"  « {text} »")
            lines.append(f"  — {ref}\n")

        return "\n".join(lines)

    def book_info(self, book: str = "proverbes") -> str:
        """Get info about a Bible book."""
        book_key = book.lower().strip()
        info = self.BOOKS_INFO.get(book_key, None)

        if info:
            return f"📚 {info}"

        lines = ["📚 LIVRES DISPONIBLES\n"]
        for b, desc in self.BOOKS_INFO.items():
            lines.append(f"  📖 {desc}")
        lines.append(f"\nUsage: /biblebook [livre]")
        return "\n".join(lines)

    def proverb(self) -> str:
        """Get a random Proverb (the business-friendly book)."""
        proverbs = [
            ("11:14", "Quand la direction manque, le peuple tombe; le salut est dans le grand nombre de conseillers."),
            ("13:11", "La richesse mal acquise diminue, mais celui qui amasse peu à peu l'augmente."),
            ("14:23", "Tout travail procure l'abondance, mais les paroles en l'air ne mènent qu'à la disette."),
            ("15:22", "Les projets échouent, faute d'une assemblée qui délibère; mais ils réussissent quand il y a de nombreux conseillers."),
            ("16:9", "Le cœur de l'homme médite sa voie, mais c'est l'Éternel qui dirige ses pas."),
            ("21:5", "Les projets de l'homme diligent ne mènent qu'à l'abondance."),
            ("22:1", "La réputation est préférable à de grandes richesses, et la grâce vaut mieux que l'argent et l'or."),
            ("24:16", "Car sept fois le juste tombe, et il se relève."),
            ("27:23", "Connais bien chacune de tes brebis, donne tes soins à tes troupeaux."),
            ("28:19", "Celui qui cultive son champ est rassasié de pain, mais celui qui poursuit des choses vaines est rassasié de pauvreté."),
        ]
        ref, text = random.choice(proverbs)
        return (
            f"📜 PROVERBE {ref}\n\n"
            f"« {text} »\n\n"
            f"— Proverbes {ref}"
        )

    async def devotion(self, topic: str = "") -> str:
        """AI-generated daily devotion."""
        ref, text = random.choice(self.POPULAR_VERSES)

        prompt = f"""Écris une courte dévotion quotidienne (5-7 phrases) basée sur ce verset:

"{text}" — {ref}

{f'Thème souhaité: {topic}' if topic else ''}

Structure:
1. Le verset
2. Explication simple et moderne (pas de jargon religieux lourd)
3. Application concrète dans la vie de tous les jours (business, relations, ambitions)
4. Une prière courte (2 phrases)

Ton: inspirant, moderne, concret. Comme un mentor spirituel qui parle à un entrepreneur.
En français."""

        return ai_chat("Expert assistant.", prompt, 800)

    def search_verse(self, keyword: str) -> str:
        """Search verses by keyword."""
        keyword_lower = keyword.lower()
        results = []

        for ref, text in self.POPULAR_VERSES:
            if keyword_lower in text.lower() or keyword_lower in ref.lower():
                results.append((ref, text))

        for theme_verses in self.THEMES.values():
            for ref, text in theme_verses:
                if keyword_lower in text.lower() or keyword_lower in ref.lower():
                    if (ref, text) not in results:
                        results.append((ref, text))

        if not results:
            return f"Aucun verset trouvé pour '{keyword}'. Essaie un autre mot-clé."

        lines = [f"🔍 VERSETS — '{keyword}'\n"]
        for ref, text in results[:5]:
            lines.append(f"  « {text} »")
            lines.append(f"  — {ref}\n")

        return "\n".join(lines)
