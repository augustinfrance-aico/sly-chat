"""
TITAN Culture Module
Knowledge, culture, daily learning, facts, history.
Always learning, always growing.
"""

import random

from ..ai_client import chat as ai_chat


class TitanCulture:
    """La culture c'est ce qui reste quand on a tout oublie."""

    CATEGORIES = [
        "science", "histoire", "philosophie", "psychologie", "economie",
        "geopolitique", "art", "technologie", "nature", "espace",
        "mathematiques", "medecine", "droit", "sociologie", "linguistique",
    ]

    DAILY_FACTS = [
        ("Science", "L'ADN humain est compose de 3.2 milliards de paires de bases. Si tu le deroulais, il ferait 2 metres de long."),
        ("Histoire", "L'Empire romain a dure 503 ans (27 av. J.-C. a 476 ap. J.-C.) en Occident, et 1480 ans si on compte Byzance."),
        ("Psychologie", "Le biais de confirmation nous fait chercher des infos qui confirment nos croyances et ignorer le reste."),
        ("Economie", "L'effet de levier: emprunter pour investir. Un rendement de 10% sur 100K empruntes = 10K sans avoir mis 100K."),
        ("Geopolitique", "Les 5 membres permanents du Conseil de Securite de l'ONU (USA, Russie, Chine, France, UK) ont un droit de veto."),
        ("Art", "La Joconde n'a pas de sourcils. Soit Leonard de Vinci les a peints trop fins, soit il ne les a jamais peints."),
        ("Maths", "Le nombre d'or (1.618...) apparait dans les coquillages, les galaxies, les fleurs, et le visage humain."),
        ("Droit", "En France, le Code Civil de 1804 (Code Napoleon) est toujours la base du droit civil francais."),
        ("Medecine", "Le cerveau humain consomme 20% de l'energie du corps alors qu'il ne represente que 2% de sa masse."),
        ("Nature", "Les arbres communiquent entre eux via un reseau souterrain de champignons appele le 'Wood Wide Web'."),
        ("Tech", "Le premier iPhone (2007) avait 128 Mo de RAM. Un smartphone moyen en 2025 en a 8 Go -- 62 fois plus."),
        ("Philosophie", "Socrate: 'Je sais que je ne sais rien.' -- L'humilite intellectuelle est le debut de la sagesse."),
        ("Linguistique", "Il y a environ 7000 langues dans le monde. Une disparait toutes les 2 semaines."),
        ("Architecture", "La Grande Pyramide de Gizeh a ete la plus haute structure humaine pendant 3800 ans (jusqu'en 1311)."),
        ("Musique", "Mozart a compose plus de 600 oeuvres. Il a commence a 5 ans et est mort a 35."),
        ("Espace", "La lumiere du Soleil met 8 minutes 20 secondes pour atteindre la Terre."),
        ("Chimie", "L'or est si malleable qu'une once (28g) peut etre etiree en un fil de 80 km."),
        ("Politique", "La France est la 5eme Republique. La premiere a dure de 1792 a 1804."),
        ("Innovation", "Le GPS a ete rendu gratuit pour le public en 2000 par Bill Clinton. Avant, l'erreur etait volontairement de 100m."),
        ("Stats", "50% de la richesse mondiale est detenue par 1% de la population."),
    ]

    MENTAL_MODELS = [
        ("Inversion", "Au lieu de 'comment reussir?', demande 'comment echouer a coup sur?' et fais l'inverse.", "Charlie Munger"),
        ("Premiere Principes", "Decompose tout probleme en elements fondamentaux et reconstruis a partir de zero.", "Elon Musk"),
        ("Pareto (80/20)", "80% des resultats viennent de 20% des efforts. Trouve les 20% qui comptent.", "Vilfredo Pareto"),
        ("Cercle de Competence", "Connaitre les limites de ce que tu sais est plus important que d'etendre ce que tu sais.", "Warren Buffett"),
        ("Skin in the Game", "Ne fais confiance qu'aux gens qui ont quelque chose a perdre dans leurs conseils.", "Nassim Taleb"),
        ("Effet Lindy", "Plus quelque chose a survecu longtemps, plus c'est probable qu'il survive encore longtemps.", "Nassim Taleb"),
        ("Second Order Thinking", "Ne regarde pas juste les consequences immediates. Demande: 'Et ensuite?'", "Howard Marks"),
        ("Occam's Razor", "L'explication la plus simple est generalement la bonne.", "Guillaume d'Ockham"),
        ("Hanlon's Razor", "N'attribue jamais a la malveillance ce qui s'explique par l'incompetence.", "Robert Hanlon"),
        ("Antifragilite", "Certaines choses deviennent plus fortes quand on les stresse. Sois antifragile.", "Nassim Taleb"),
    ]

    BOOKS_MUST_READ = [
        ("Thinking, Fast and Slow", "Daniel Kahneman", "Comment notre cerveau prend des decisions"),
        ("The 48 Laws of Power", "Robert Greene", "Les lois du pouvoir et de l'influence"),
        ("Atomic Habits", "James Clear", "Comment construire des habitudes qui changent ta vie"),
        ("Zero to One", "Peter Thiel", "Comment creer quelque chose de nouveau"),
        ("The Lean Startup", "Eric Ries", "Lancer un business avec methode"),
        ("Sapiens", "Yuval Noah Harari", "L'histoire de l'humanite en 500 pages"),
        ("Meditations", "Marc Aurele", "La philosophie stoicienne par un empereur romain"),
        ("The Art of War", "Sun Tzu", "Strategie militaire applicable au business"),
        ("Deep Work", "Cal Newport", "La concentration profonde comme superpouvoir"),
        ("Antifragile", "Nassim Taleb", "Comment prosperer dans le chaos"),
        ("Rich Dad Poor Dad", "Robert Kiyosaki", "Les bases de l'education financiere"),
        ("Start with Why", "Simon Sinek", "Pourquoi les grands leaders inspirent"),
        ("Man's Search for Meaning", "Viktor Frankl", "Trouver un sens dans la souffrance"),
        ("The Psychology of Money", "Morgan Housel", "La psychologie derriere l'argent"),
        ("Never Split the Difference", "Chris Voss", "L'art de la negociation par un ex-FBI"),
    ]

    def __init__(self):
        pass

    def fact_of_day(self) -> str:
        """Random knowledge fact."""
        cat, fact = random.choice(self.DAILY_FACTS)
        return f"{cat}\n\n{fact}"

    def mental_model(self) -> str:
        """Random mental model for better thinking."""
        name, explanation, author = random.choice(self.MENTAL_MODELS)
        return (
            f"MODELE MENTAL: {name.upper()}\n\n"
            f"{explanation}\n\n"
            f"-- {author}"
        )

    def book_reco(self) -> str:
        """Recommend a must-read book."""
        title, author, desc = random.choice(self.BOOKS_MUST_READ)
        return (
            f"LIVRE A LIRE\n\n"
            f"{title}\n"
            f"{author}\n"
            f"{desc}\n\n"
            f"https://www.amazon.fr/s?k={title.replace(' ', '+')}"
        )

    def book_list(self) -> str:
        """Full reading list."""
        lines = ["BIBLIOTHEQUE ESSENTIELLE\n"]
        for i, (title, author, desc) in enumerate(self.BOOKS_MUST_READ, 1):
            lines.append(f"  {i}. {title} -- {author}")
            lines.append(f"     {desc}")
        return "\n".join(lines)

    async def learn(self, topic: str) -> str:
        """Deep dive on any topic."""
        return ai_chat("Expert assistant.", f"""Explique-moi "{topic}" de maniere experte mais accessible.""", 1500)

    async def debate(self, topic: str) -> str:
        """Present both sides of a debate."""
        return ai_chat("Expert assistant.", f"""Presente les deux cotes du debat sur: "{topic}" """, 1500)

    def vocabulary(self) -> str:
        """Learn a powerful word."""
        words = [
            ("Serendipite", "Decouverte heureuse faite par hasard", "La penicilline a ete decouverte par serendipite."),
            ("Antifragile", "Qui se renforce face au stress et au chaos", "Les muscles sont antifragiles: le stress les rend plus forts."),
            ("Paradigme", "Modele de pensee dominant a une epoque", "Internet a change le paradigme de l'information."),
            ("Heuristique", "Raccourci mental pour prendre des decisions rapides", "Acheter la marque la plus connue est une heuristique."),
            ("Asymetrie", "Quand le gain potentiel est tres superieur au risque", "Un bon investissement a une asymetrie favorable."),
            ("Effet Dunning-Kruger", "Les incompetents surestiment leurs capacites", "Plus tu en sais, plus tu realises que tu ne sais rien."),
            ("Dissonance cognitive", "Inconfort quand tes actions contredisent tes croyances", "Fumer en sachant que c'est mauvais = dissonance cognitive."),
            ("Optionalite", "Avoir beaucoup d'options sans etre oblige d'en choisir une", "L'entrepreneur a de l'optionalite, le salarie moins."),
        ]
        word, definition, example = random.choice(words)
        return (
            f"MOT DU JOUR: {word.upper()}\n\n"
            f"Definition: {definition}\n"
            f"Exemple: {example}"
        )
