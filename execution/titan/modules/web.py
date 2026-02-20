"""
TITAN Web Module
Web search and research capabilities.
Titan can search the internet and synthesize information.
"""

import json
import re
from datetime import datetime
from typing import Optional

import requests

from ..config import GOOGLE_SEARCH_KEY, GOOGLE_SEARCH_CX
from ..ai_client import chat as ai_chat


class TitanWeb:
    """Titan's connection to the internet."""

    def __init__(self):
        pass

    async def search(self, query: str, num_results: int = 5) -> str:
        """Search the web and return synthesized results."""

        # Try Google Custom Search API
        results = self._google_search(query, num_results)

        if not results:
            # Fallback: use Claude's knowledge
            return await self._claude_answer(query)

        # Format results
        context = "\n".join([
            f"Source: {r['title']}\nURL: {r['link']}\nExtrait: {r['snippet']}\n"
            for r in results
        ])

        # Synthesize with Claude
        return ai_chat("Expert assistant.", f"""Voici les resultats de recherche pour: "{query}"\n\n{context}\n\nSynthetise en une reponse concise et utile.""", 1024)

    def _google_search(self, query: str, num: int = 5) -> list:
        """Search using Google Custom Search API."""
        if not GOOGLE_SEARCH_KEY or not GOOGLE_SEARCH_CX:
            return []

        try:
            url = "https://www.googleapis.com/customsearch/v1"
            params = {
                "key": GOOGLE_SEARCH_KEY,
                "cx": GOOGLE_SEARCH_CX,
                "q": query,
                "num": min(num, 10),
            }
            resp = requests.get(url, params=params, timeout=10)
            data = resp.json()

            results = []
            for item in data.get("items", []):
                results.append({
                    "title": item.get("title", ""),
                    "link": item.get("link", ""),
                    "snippet": item.get("snippet", ""),
                })

            return results

        except Exception:
            return []

    async def _claude_answer(self, query: str) -> str:
        """Fallback: answer from Claude's knowledge."""
        return ai_chat("Expert assistant.", f"""Reponds a cette question de maniere concise et informative: {query}""", 1024)

    async def get_url_summary(self, url: str) -> str:
        """Fetch a URL and summarize its content."""
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (compatible; TitanBot/1.0)"
            }
            resp = requests.get(url, headers=headers, timeout=15)
            text = resp.text[:5000]

            # Clean HTML roughly
            text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL)
            text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
            text = re.sub(r'<[^>]+>', ' ', text)
            text = re.sub(r'\s+', ' ', text).strip()

            if not text:
                return "Page vide ou impossible à lire."

            return ai_chat("Expert assistant.", f"Résume le contenu principal de cette page en 3-5 bullet points:\n\n{text[:3000]}", 512)

        except Exception as e:
            return f"Impossible de lire l'URL: {e}"

    async def translate(self, text: str, target_lang: str = "fr") -> str:
        """Translate text to target language."""
        lang_names = {
            "fr": "français", "en": "anglais", "es": "espagnol",
            "de": "allemand", "it": "italien", "pt": "portugais",
        }
        lang_name = lang_names.get(target_lang, target_lang)

        return ai_chat("Expert assistant.", f"Traduis ce texte en {lang_name}. Donne uniquement la traduction, rien d'autre.\n\n{text}", 1024)
