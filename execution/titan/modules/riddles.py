"""
TITAN Riddles & Trivia Module
Brain teasers, riddles, trivia questions.
"""

import random
import requests


class TitanRiddles:
    """Train ton cerveau."""

    RIDDLES = [
        {"q": "Je suis toujours devant toi mais je ne peux pas etre vu. Qui suis-je ?", "a": "Le futur"},
        {"q": "Plus je seche, plus je suis mouillee. Qui suis-je ?", "a": "Une serviette"},
        {"q": "J'ai des villes mais pas de maisons, des forets mais pas d'arbres, de l'eau mais pas de poissons. Qui suis-je ?", "a": "Une carte"},
        {"q": "Qu'est-ce qui a un coeur qui ne bat pas ?", "a": "Un artichaut"},
        {"q": "Je peux voyager autour du monde en restant dans un coin. Qui suis-je ?", "a": "Un timbre"},
        {"q": "Plus on me tire, plus je suis courte. Qui suis-je ?", "a": "Une cigarette"},
        {"q": "Je monte et je descends sans bouger. Qui suis-je ?", "a": "La temperature"},
        {"q": "On me prend sans me voler. Qui suis-je ?", "a": "Une photo"},
        {"q": "J'ai 13 coeurs mais pas d'organes. Qui suis-je ?", "a": "Un jeu de cartes"},
        {"q": "Je suis plein de trous mais je retiens l'eau. Qui suis-je ?", "a": "Une eponge"},
    ]

    TECH_TRIVIA = [
        {"q": "En quelle annee le premier iPhone est sorti ?", "a": "2007", "options": ["2005", "2007", "2008", "2010"]},
        {"q": "Quel langage de programmation a ete cree par Guido van Rossum ?", "a": "Python", "options": ["Java", "Python", "Ruby", "C++"]},
        {"q": "Combien de bits dans un octet ?", "a": "8", "options": ["4", "8", "16", "32"]},
        {"q": "Quel est le vrai nom de Bitcoin ?", "a": "Satoshi Nakamoto (pseudonyme du createur)", "options": ["Le createur est anonyme"]},
        {"q": "Quel est le site le plus visite au monde ?", "a": "Google", "options": ["Google", "YouTube", "Facebook", "Wikipedia"]},
        {"q": "En quelle annee a ete fonde Amazon ?", "a": "1994", "options": ["1994", "1998", "2000", "1996"]},
        {"q": "Quel est le premier langage de programmation de haut niveau ?", "a": "FORTRAN (1957)", "options": ["FORTRAN", "COBOL", "BASIC", "C"]},
        {"q": "Combien de lignes de code dans le noyau Linux ?", "a": "~30 millions", "options": ["1 million", "10 millions", "30 millions", "100 millions"]},
    ]

    def riddle(self) -> str:
        """Get a random riddle."""
        r = random.choice(self.RIDDLES)
        return (
            f"🧩 ENIGME\n\n"
            f"{r['q']}\n\n"
            f"(reponds /answer pour la solution)"
        )

    def riddle_answer(self) -> str:
        """This returns a random answer — in practice, track state."""
        r = random.choice(self.RIDDLES)
        return f"💡 Reponse: {r['a']}"

    def trivia(self) -> str:
        """Get a tech trivia question."""
        t = random.choice(self.TECH_TRIVIA)
        return (
            f"🎯 TRIVIA TECH\n\n"
            f"{t['q']}\n\n"
            f"Reponse: {t['a']}"
        )

    def trivia_api(self) -> str:
        """Get trivia from Open Trivia DB."""
        try:
            resp = requests.get("https://opentdb.com/api.php?amount=1&type=multiple", timeout=5)
            data = resp.json()["results"][0]
            import html
            question = html.unescape(data["question"])
            answer = html.unescape(data["correct_answer"])
            category = data["category"]
            difficulty = data["difficulty"]

            return (
                f"🎯 TRIVIA ({category})\n"
                f"Difficulte: {difficulty}\n\n"
                f"{question}\n\n"
                f"💡 Reponse: {answer}"
            )
        except Exception:
            return self.trivia()

    def would_you_rather(self) -> str:
        """Would you rather game."""
        scenarios = [
            ("Pouvoir voler", "Etre invisible"),
            ("Avoir 10M EUR mais ne jamais voyager", "Voyager partout mais etre fauche"),
            ("Savoir parler toutes les langues", "Savoir jouer de tous les instruments"),
            ("Revivre le passe", "Voir le futur"),
            ("Travailler 4h/jour pour 3000 EUR/mois", "Travailler 10h/jour pour 15000 EUR/mois"),
            ("Etre le meilleur dev du monde", "Etre le meilleur commercial du monde"),
            ("N'avoir jamais besoin de dormir", "N'avoir jamais besoin de manger"),
        ]
        a, b = random.choice(scenarios)
        return f"🤔 TU PREFERAIS...\n\nA) {a}\nB) {b}"

    def math_challenge(self) -> str:
        """Quick math challenge."""
        ops = [
            (lambda: (a := random.randint(10, 99), b := random.randint(10, 99), f"{a} + {b}", a + b)),
            (lambda: (a := random.randint(10, 99), b := random.randint(2, 20), f"{a} x {b}", a * b)),
            (lambda: (a := random.randint(100, 999), b := random.randint(10, 99), f"{a} - {b}", a - b)),
        ]

        gen = random.choice(ops)()
        expr = gen[2]
        answer = gen[3]

        return f"🧮 CALCUL RAPIDE\n\n{expr} = ?\n\nReponse: {answer}"
