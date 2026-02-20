"""
TITAN Memes Module
Random memes, fun facts, and internet culture.
"""

import random
import requests


class TitanMemes:
    """Memes et fun — parce que la vie est trop courte."""

    def random_meme(self) -> str:
        """Get a random meme from Reddit."""
        try:
            resp = requests.get("https://meme-api.com/gimme", timeout=10)
            data = resp.json()
            title = data.get("title", "Meme")
            url = data.get("url", "")
            subreddit = data.get("subreddit", "")
            return f"😂 {title}\n📎 {url}\nr/{subreddit}"
        except Exception:
            return self._fallback_joke()

    def random_meme_sub(self, subreddit: str = "ProgrammerHumor") -> str:
        """Get a meme from a specific subreddit."""
        try:
            resp = requests.get(f"https://meme-api.com/gimme/{subreddit}", timeout=10)
            data = resp.json()
            return f"😂 {data.get('title', 'Meme')}\n📎 {data.get('url', '')}"
        except Exception:
            return "Subreddit indisponible."

    def fun_fact(self) -> str:
        """Random fun fact."""
        try:
            resp = requests.get("https://uselessfacts.jsph.pl/random.json?language=en", timeout=10)
            data = resp.json()
            return f"🧠 FUN FACT\n\n{data.get('text', 'No fact found')}"
        except Exception:
            facts = [
                "Le miel ne se perime jamais. On a trouve du miel comestible dans des tombes egyptiennes.",
                "Les poulpes ont 3 coeurs et le sang bleu.",
                "La Tour Eiffel peut grandir de 15 cm en ete a cause de la dilatation thermique.",
                "Un groupe de flamants roses s'appelle un 'flamboyance'.",
                "Les astronautes grandissent d'environ 5 cm dans l'espace.",
            ]
            return f"🧠 FUN FACT\n\n{random.choice(facts)}"

    def _fallback_joke(self) -> str:
        jokes = [
            "Pourquoi les plongeurs plongent-ils toujours en arriere ? Parce que sinon ils tomberaient dans le bateau.",
            "Qu'est-ce qu'un canif ? Un petit fien.",
            "Comment appelle-t-on un chat tombe dans un pot de peinture le jour de Noel ? Un chat peint de Noel.",
            "Un dev mass son code legacy... Il a trouve un TODO de 2003.",
        ]
        return f"😂 {random.choice(jokes)}"

    def number_fact(self, number: int) -> str:
        """Get a fact about a number."""
        try:
            resp = requests.get(f"http://numbersapi.com/{number}", timeout=5)
            return f"🔢 {number}: {resp.text}"
        except Exception:
            return f"Pas de fact pour {number}."

    def this_day(self) -> str:
        """What happened on this day in history."""
        try:
            from datetime import datetime
            today = datetime.now()
            resp = requests.get(f"http://numbersapi.com/{today.month}/{today.day}/date", timeout=5)
            return f"📅 CE JOUR DANS L'HISTOIRE\n\n{resp.text}"
        except Exception:
            return "Historique indisponible."

    def dad_joke(self) -> str:
        """Get a dad joke."""
        try:
            resp = requests.get("https://icanhazdadjoke.com/", headers={"Accept": "application/json"}, timeout=5)
            return f"👴 DAD JOKE\n\n{resp.json().get('joke', '...')}"
        except Exception:
            return self._fallback_joke()
