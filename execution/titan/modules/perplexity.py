"""
TITAN Perplexity Module
Deep web search with source synthesis — like Perplexity AI, zero cost.
DuckDuckGo search → scrape top URLs → AI synthesis with citations.
"""

import logging
import re
import json
import time
from datetime import datetime
from pathlib import Path

import requests

from ..ai_client import chat as ai_chat

log = logging.getLogger("titan.perplexity")

HISTORY_FILE = Path(__file__).parent.parent / "memory" / "search_history.json"
MAX_HISTORY = 50


class TitanPerplexity:
    """Deep search agent — DuckDuckGo + scraping + AI synthesis."""

    def __init__(self):
        self._history = self._load_history()

    # === MAIN ENTRY POINT ===

    async def search(self, query: str, num_results: int = 5, scrape_top: int = 3) -> str:
        """Full Perplexity-style search: DDG → scrape → synthesize."""
        if not query.strip():
            return "Donne-moi un sujet de recherche."

        t0 = time.time()

        # Step 1: DuckDuckGo search
        results = self._web_search(query, num_results)
        if not results:
            return self._ai_fallback(query)

        # Step 2: Scrape top N URLs
        sources = []
        for r in results[:scrape_top]:
            content = self._scrape_url(r["url"])
            sources.append({
                "title": r["title"],
                "url": r["url"],
                "snippet": r["snippet"],
                "content": content,
            })

        # Step 3: AI synthesis with citations
        answer = self._synthesize(query, sources)

        # Step 4: Format with source links
        elapsed = round(time.time() - t0, 1)
        source_links = "\n".join(
            f"  [{i+1}] {s['title']}\n      {s['url']}"
            for i, s in enumerate(sources) if s["url"]
        )

        formatted = (
            f"🔍 RECHERCHE APPROFONDIE\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📝 {query}\n\n"
            f"{answer}\n\n"
            f"📚 SOURCES ({len(sources)})\n{source_links}\n\n"
            f"⏱ {elapsed}s"
        )

        self._save_to_history(query, sources, elapsed)
        return formatted

    # === DUCKDUCKGO SEARCH ===

    def _web_search(self, query: str, num_results: int = 5) -> list:
        """Search DuckDuckGo — free, no API key."""
        try:
            from ddgs import DDGS
            with DDGS() as ddgs:
                results = []
                for r in ddgs.text(query, max_results=num_results):
                    results.append({
                        "title": r.get("title", ""),
                        "url": r.get("href", ""),
                        "snippet": r.get("body", ""),
                    })
                return results
        except ImportError:
            log.error("ddgs not installed — pip install ddgs")
            return []
        except Exception as e:
            log.warning(f"DDG search error: {e}")
            return []

    # === URL SCRAPING ===

    def _scrape_url(self, url: str, max_chars: int = 3000) -> str:
        """Fetch URL and extract main text content. Regex-based, no BS4."""
        try:
            headers = {"User-Agent": "Mozilla/5.0 (compatible; TitanBot/2.0)"}
            resp = requests.get(url, headers=headers, timeout=8)
            resp.raise_for_status()
            html = resp.text[:50000]

            # Strip script/style/nav/header/footer blocks
            html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
            html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
            html = re.sub(r'<nav[^>]*>.*?</nav>', '', html, flags=re.DOTALL)
            html = re.sub(r'<header[^>]*>.*?</header>', '', html, flags=re.DOTALL)
            html = re.sub(r'<footer[^>]*>.*?</footer>', '', html, flags=re.DOTALL)
            # Strip all remaining tags
            text = re.sub(r'<[^>]+>', ' ', html)
            # Normalize whitespace
            text = re.sub(r'\s+', ' ', text).strip()
            # Decode HTML entities
            text = text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
            text = text.replace('&quot;', '"').replace('&#39;', "'")

            return text[:max_chars] if text else ""
        except Exception as e:
            log.debug(f"Scrape failed for {url}: {e}")
            return ""

    # === AI SYNTHESIS ===

    def _synthesize(self, query: str, sources: list) -> str:
        """Use ai_chat() to synthesize a cited answer from scraped sources."""
        context_parts = []
        for i, s in enumerate(sources):
            content = s.get("content", "") or s.get("snippet", "")
            if content:
                context_parts.append(f"[Source {i+1}] {s['title']}\n{content[:1500]}")

        if not context_parts:
            context_parts = [
                f"[Source {i+1}] {s['title']}: {s['snippet']}"
                for i, s in enumerate(sources) if s.get("snippet")
            ]

        context = "\n\n".join(context_parts)

        system_prompt = (
            "Tu es un moteur de recherche IA. Tu synthetises les sources web "
            "pour repondre a la question de l'utilisateur. "
            "Cite les sources avec [1], [2], etc. "
            "Reponse structuree, factuelle, 150-300 mots max. "
            "Pas de questions. Pas de fluff."
        )

        user_prompt = (
            f"Question: {query}\n\n"
            f"Sources web:\n{context}\n\n"
            f"Synthetise une reponse complete avec citations [1], [2], etc."
        )

        return ai_chat(system_prompt, user_prompt, max_tokens=1024)

    # === FALLBACK ===

    def _ai_fallback(self, query: str) -> str:
        """Pure AI answer when DuckDuckGo returns nothing."""
        answer = ai_chat(
            "Expert assistant. Reponds de maniere factuelle et structuree.",
            f"Reponds a cette question: {query}",
            max_tokens=1024
        )
        return (
            f"🔍 RECHERCHE\n━━━━━━━━━━━━\n"
            f"📝 {query}\n\n"
            f"{answer}\n\n"
            f"⚠️ Aucune source web — reponse basee sur connaissances IA."
        )

    # === SEARCH HISTORY ===

    def _load_history(self) -> list:
        try:
            if HISTORY_FILE.exists():
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception:
            pass
        return []

    def _save_to_history(self, query: str, sources: list, elapsed: float):
        self._history.append({
            "query": query,
            "sources": [{"title": s["title"], "url": s["url"]} for s in sources],
            "timestamp": datetime.now().isoformat(),
            "elapsed_s": elapsed,
        })
        if len(self._history) > MAX_HISTORY:
            self._history = self._history[-MAX_HISTORY:]
        try:
            HISTORY_FILE.parent.mkdir(exist_ok=True)
            with open(HISTORY_FILE, "w", encoding="utf-8") as f:
                json.dump(self._history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            log.warning(f"Search history save failed: {e}")

    def get_history(self, limit: int = 10) -> str:
        """Return recent search history formatted."""
        if not self._history:
            return "Aucune recherche en historique."
        recent = self._history[-limit:][::-1]
        lines = ["🔍 HISTORIQUE RECHERCHES\n━━━━━━━━━━━━━━━━━━━━━━━━"]
        for h in recent:
            ts = h.get("timestamp", "")[:16]
            n_src = len(h.get("sources", []))
            lines.append(f"  [{ts}] {h['query']} ({h.get('elapsed_s', '?')}s, {n_src} sources)")
        return "\n".join(lines)
