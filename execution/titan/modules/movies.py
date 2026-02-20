"""
TITAN Movies Module v2
Movie recommendations with Rotten Tomatoes scores, top lists, AI reco.
Uses free APIs + smart scraping + AI intelligence.
"""

import random
import re
import requests

from ..ai_client import chat as ai_chat


class TitanMovies:
    """Le cinéma c'est la vie."""

    # Curated top lists — the real stuff
    TOP_FILMS = {
        "all_time": [
            ("The Shawshank Redemption", 1994, "9.3", "97%"),
            ("The Godfather", 1972, "9.2", "97%"),
            ("The Dark Knight", 2008, "9.0", "94%"),
            ("Pulp Fiction", 1994, "8.9", "92%"),
            ("Schindler's List", 1993, "9.0", "97%"),
            ("Fight Club", 1999, "8.8", "79%"),
            ("Inception", 2010, "8.8", "87%"),
            ("The Matrix", 1999, "8.7", "83%"),
            ("Goodfellas", 1990, "8.7", "96%"),
            ("Interstellar", 2014, "8.7", "73%"),
            ("Parasite", 2019, "8.5", "99%"),
            ("Whiplash", 2014, "8.5", "94%"),
            ("The Prestige", 2006, "8.5", "76%"),
            ("Memento", 2000, "8.4", "93%"),
            ("Django Unchained", 2012, "8.4", "87%"),
        ],
        "2024_2025": [
            ("Oppenheimer", 2023, "8.5", "93%"),
            ("Dune: Part Two", 2024, "8.6", "92%"),
            ("The Brutalist", 2024, "8.0", "93%"),
            ("Anora", 2024, "7.8", "95%"),
            ("Conclave", 2024, "7.7", "92%"),
            ("The Substance", 2024, "7.3", "89%"),
            ("Emilia Pérez", 2024, "7.0", "78%"),
            ("A Complete Unknown", 2024, "7.5", "87%"),
            ("Nosferatu", 2024, "7.2", "85%"),
            ("Civil War", 2024, "7.0", "82%"),
        ],
        "french": [
            ("Intouchables", 2011, "8.5", "76%"),
            ("La Haine", 1995, "8.1", "100%"),
            ("Amélie", 2001, "8.3", "90%"),
            ("Le Fabuleux Destin d'Amélie Poulain", 2001, "8.3", "90%"),
            ("Un Prophète", 2009, "7.9", "97%"),
            ("Les Choristes", 2004, "7.8", "69%"),
            ("Le Dîner de Cons", 1998, "7.7", "71%"),
            ("Anatomie d'une Chute", 2023, "7.7", "96%"),
            ("Le Bureau des Légendes", 2015, "8.6", "100%"),
            ("Lupin", 2021, "7.5", "98%"),
        ],
        "series": [
            ("Breaking Bad", 2008, "9.5", "96%"),
            ("The Wire", 2002, "9.3", "94%"),
            ("Chernobyl", 2019, "9.4", "96%"),
            ("Band of Brothers", 2001, "9.4", "97%"),
            ("The Sopranos", 1999, "9.2", "92%"),
            ("True Detective S1", 2014, "9.0", "78%"),
            ("Severance", 2022, "8.7", "97%"),
            ("Shogun", 2024, "8.7", "99%"),
            ("The Bear", 2022, "8.6", "96%"),
            ("Dark", 2017, "8.8", "95%"),
        ],
    }

    MOOD_MAP = {
        "chill": ["The Grand Budapest Hotel", "Amélie", "Chef", "The Secret Life of Walter Mitty", "About Time", "Midnight in Paris", "The Intern", "Julie & Julia"],
        "intense": ["Sicario", "No Country for Old Men", "Se7en", "Zodiac", "Heat", "Prisoners", "Wind River", "Hell or High Water"],
        "mindblown": ["Inception", "Interstellar", "The Prestige", "Arrival", "Ex Machina", "Annihilation", "Dark", "Severance", "Mr. Robot"],
        "funny": ["The Big Lebowski", "Superbad", "The Hangover", "Borat", "Step Brothers", "Airplane!", "OSS 117", "Le Dîner de Cons"],
        "sad": ["Schindler's List", "The Green Mile", "Hachi", "Eternal Sunshine", "Manchester by the Sea", "Grave of the Fireflies"],
        "date": ["La La Land", "About Time", "Crazy Stupid Love", "500 Days of Summer", "Before Sunrise", "The Notebook", "Amélie"],
        "solo": ["Into the Wild", "Drive", "Blade Runner 2049", "Lost in Translation", "Her", "The Revenant", "Cast Away"],
        "peur": ["Hereditary", "Get Out", "The Shining", "Midsommar", "It Follows", "The Witch", "A Quiet Place"],
        "french": ["Intouchables", "La Haine", "Un Prophète", "Les Choristes", "Le Grand Bain", "Anatomie d'une Chute", "Le Bureau des Légendes"],
        "anime": ["Spirited Away", "Your Name", "Attack on Titan", "Death Note", "Demon Slayer", "Jujutsu Kaisen", "Vinland Saga", "Cowboy Bebop"],
    }

    def __init__(self):
        pass

    def trending(self) -> str:
        """Get trending movies/shows."""
        try:
            resp = requests.get("https://api.tvmaze.com/schedule", timeout=10)
            shows = resp.json()[:10]
            lines = ["🎬 TRENDING AUJOURD'HUI\n"]
            seen = set()
            for s in shows:
                show = s.get("show", {})
                name = show.get("name", "?")
                if name in seen:
                    continue
                seen.add(name)
                rating = show.get("rating", {}).get("average", "N/A")
                genres = ", ".join(show.get("genres", [])[:2])
                star = "⭐" if rating and rating != "N/A" and rating > 7 else "🎥"
                lines.append(f"  {star} {name} ({genres}) — {rating}/10")
            return "\n".join(lines)
        except Exception as e:
            return f"Erreur trending: {e}"

    def search(self, query: str) -> str:
        """Search for a movie/show with Rotten Tomatoes-style info."""
        try:
            resp = requests.get(f"https://api.tvmaze.com/search/shows?q={query}", timeout=10)
            results = resp.json()[:5]

            if not results:
                return f"Aucun résultat pour '{query}'."

            lines = [f"🔍 RÉSULTATS: {query}\n"]
            for r in results:
                show = r.get("show", {})
                name = show.get("name", "?")
                year = show.get("premiered", "?")[:4] if show.get("premiered") else "?"
                rating = show.get("rating", {}).get("average", "N/A")
                genres = ", ".join(show.get("genres", [])[:3])
                summary = show.get("summary", "")
                if summary:
                    summary = re.sub(r"<[^>]+>", "", summary)[:150]

                # Rotten Tomatoes link
                rt_slug = name.lower().replace(" ", "_").replace("'", "").replace(":", "")
                rt_link = f"https://www.rottentomatoes.com/search?search={name.replace(' ', '+')}"

                lines.append(f"🎬 {name} ({year})")
                lines.append(f"   Genres: {genres} | Note: {rating}/10")
                lines.append(f"   🍅 Rotten Tomatoes: {rt_link}")
                if summary:
                    lines.append(f"   {summary}...")
                lines.append("")

            return "\n".join(lines)
        except Exception as e:
            return f"Erreur: {e}"

    def top(self, category: str = "all_time") -> str:
        """Get top movies/series list."""
        cat = category.lower().replace(" ", "_")
        films = self.TOP_FILMS.get(cat, self.TOP_FILMS["all_time"])

        cat_names = {
            "all_time": "TOP FILMS DE TOUS LES TEMPS",
            "2024_2025": "MEILLEURS FILMS 2024-2025",
            "french": "TOP FILMS/SÉRIES FRANÇAIS",
            "series": "TOP SÉRIES DE TOUS LES TEMPS",
        }
        title = cat_names.get(cat, f"TOP {cat.upper()}")

        lines = [f"🏆 {title}\n"]
        for i, (name, year, imdb, rt) in enumerate(films, 1):
            lines.append(f"  {i}. {name} ({year})")
            lines.append(f"     IMDb: {imdb}/10 | 🍅 RT: {rt}")

        lines.append(f"\nDisponible: all_time, 2024_2025, french, series")
        lines.append(f"Usage: /movietop [catégorie]")
        return "\n".join(lines)

    def recommend(self, mood: str = "random") -> str:
        """Recommend based on mood."""
        mood_key = mood.lower().strip()

        if mood_key in self.MOOD_MAP:
            picks = self.MOOD_MAP[mood_key]
        else:
            mood_key = "random"
            picks = random.choice(list(self.MOOD_MAP.values()))

        selected = random.sample(picks, min(3, len(picks)))

        lines = [f"🎬 RECOMMANDATIONS ({mood_key.upper()})\n"]
        for pick in selected:
            rt_link = f"https://www.rottentomatoes.com/search?search={pick.replace(' ', '+')}"
            lines.append(f"  👉 {pick}")
            lines.append(f"     🍅 {rt_link}")

        lines.append(f"\nMoods dispo: {', '.join(self.MOOD_MAP.keys())}")
        lines.append(f"Usage: /moviereco [mood]")
        return "\n".join(lines)

    def random_movie(self) -> str:
        """Suggest a random gem."""
        all_films = []
        for cat_films in self.TOP_FILMS.values():
            all_films.extend(cat_films)
        for mood_films in self.MOOD_MAP.values():
            all_films.extend([(f, None, None, None) for f in mood_films])

        pick = random.choice(all_films)
        if isinstance(pick, tuple) and len(pick) == 4:
            name, year, imdb, rt = pick
            return (
                f"🎲 FILM RANDOM\n\n"
                f"👉 {name} ({year or '?'})\n"
                f"IMDb: {imdb or '?'}/10 | 🍅 RT: {rt or '?'}\n\n"
                f"🍅 https://www.rottentomatoes.com/search?search={name.replace(' ', '+')}"
            )
        else:
            name = pick[0] if isinstance(pick, tuple) else pick
            return (
                f"🎲 FILM RANDOM\n\n"
                f"👉 {name}\n\n"
                f"🍅 https://www.rottentomatoes.com/search?search={name.replace(' ', '+')}"
            )

    def rt_search(self, movie: str) -> str:
        """Direct Rotten Tomatoes search link."""
        rt_url = f"https://www.rottentomatoes.com/search?search={movie.replace(' ', '+')}"
        return (
            f"🍅 ROTTEN TOMATOES\n\n"
            f"Film: {movie}\n"
            f"Lien direct: {rt_url}\n\n"
            f"(Rotten Tomatoes montre le score critique + audience)"
        )

    async def ai_recommend(self, preferences: str) -> str:
        """AI-powered movie recommendations based on user preferences."""
        return ai_chat("Expert assistant.", f"""En tant qu'expert cinéma avec une connaissance encyclopédique, recommande des films/séries basés sur ces préférences: "{preferences}" """, 1500)

    def whats_on(self) -> str:
        """What's on streaming platforms now."""
        lines = ["📺 OÙ REGARDER QUOI\n"]
        lines.append("🔗 Liens rapides pour voir les nouveautés:\n")

        platforms = [
            ("Netflix", "https://www.netflix.com/browse/new-arrivals"),
            ("Prime Video", "https://www.primevideo.com/"),
            ("Disney+", "https://www.disneyplus.com/"),
            ("Canal+", "https://www.canalplus.com/"),
            ("Apple TV+", "https://tv.apple.com/"),
            ("Crunchyroll", "https://www.crunchyroll.com/fr"),
        ]

        for name, url in platforms:
            lines.append(f"  📱 {name}: {url}")

        lines.append(f"\n💡 Utilise JustWatch.com pour savoir où un film est dispo:")
        lines.append(f"   https://www.justwatch.com/fr")
        return "\n".join(lines)
