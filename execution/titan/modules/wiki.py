"""
TITAN Wikipedia Module
Instant knowledge from Wikipedia.
"""

import requests


class TitanWiki:
    """Access human knowledge instantly."""

    def search(self, query: str, lang: str = "fr") -> str:
        """Search Wikipedia and get a summary."""
        try:
            url = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{query}"
            resp = requests.get(url, timeout=10)

            if resp.status_code == 200:
                data = resp.json()
                title = data.get("title", query)
                extract = data.get("extract", "Pas de resume.")
                page_url = data.get("content_urls", {}).get("desktop", {}).get("page", "")

                return (
                    f"📚 WIKIPEDIA: {title}\n"
                    f"{'=' * 25}\n\n"
                    f"{extract[:1500]}\n\n"
                    f"🔗 {page_url}"
                )
            elif resp.status_code == 404:
                return self._search_suggestions(query, lang)
            else:
                return f"Erreur Wikipedia ({resp.status_code})"
        except Exception as e:
            return f"Erreur: {e}"

    def _search_suggestions(self, query: str, lang: str) -> str:
        """Search for suggestions when exact page not found."""
        try:
            url = f"https://{lang}.wikipedia.org/w/api.php"
            params = {"action": "opensearch", "search": query, "limit": 5, "format": "json"}
            resp = requests.get(url, params=params, timeout=10)
            data = resp.json()

            if len(data) > 1 and data[1]:
                lines = [f"🔍 '{query}' non trouve. Suggestions:\n"]
                for title in data[1]:
                    lines.append(f"  • {title}")
                return "\n".join(lines)
            return f"Aucun resultat pour '{query}'."
        except Exception:
            return f"Aucun resultat pour '{query}'."

    def random_article(self, lang: str = "fr") -> str:
        """Get a random Wikipedia article."""
        try:
            url = f"https://{lang}.wikipedia.org/api/rest_v1/page/random/summary"
            resp = requests.get(url, timeout=10)
            data = resp.json()
            title = data.get("title", "?")
            extract = data.get("extract", "")
            return (
                f"🎲 ARTICLE ALEATOIRE\n\n"
                f"📖 {title}\n"
                f"{extract[:1000]}"
            )
        except Exception:
            return "Impossible de charger un article aleatoire."

    def today_featured(self, lang: str = "en") -> str:
        """Get today's featured article."""
        try:
            from datetime import datetime
            now = datetime.now()
            url = f"https://{lang}.wikipedia.org/api/rest_v1/feed/featured/{now.year}/{now.month:02d}/{now.day:02d}"
            resp = requests.get(url, timeout=10)
            data = resp.json()
            tfa = data.get("tfa", {})
            title = tfa.get("title", "?")
            extract = tfa.get("extract", "Pas disponible.")
            return (
                f"⭐ ARTICLE DU JOUR\n\n"
                f"📖 {title}\n"
                f"{extract[:1200]}"
            )
        except Exception:
            return "Article du jour indisponible."
