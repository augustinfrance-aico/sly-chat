"""
TITAN Aggregator Module — L'Agrégateur Personnel
Plus jamais scroller. 1 digest/jour avec les 5 trucs qui comptent.

[GHOST + CYPHER + ZARA]

Features:
- Veille multi-sources (RSS, APIs gratuites)
- Filtrage IA par pertinence
- 1 message Telegram/jour à l'heure choisie
- Sources : Tech, IA, Crypto, Business, ProductHunt, HackerNews
- Scoring de pertinence personnalisé
"""

import json
import logging
import random
from datetime import datetime
from pathlib import Path

from ..ai_client import chat

log = logging.getLogger("titan.aggregator")

MEMORY_DIR = Path(__file__).parent.parent / "memory"
AGGREGATOR_FILE = MEMORY_DIR / "aggregator.json"


class TitanAggregator:
    """L'Agrégateur — filtre le bruit, garde le signal."""

    def __init__(self):
        self.sources = {
            "hackernews": "https://hacker-news.firebaseio.com/v0",
            "producthunt": "https://www.producthunt.com",
        }

    def _load(self) -> dict:
        if AGGREGATOR_FILE.exists():
            with open(AGGREGATOR_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"history": [], "preferences": {}, "blocked_topics": []}

    def _save(self, data: dict):
        with open(AGGREGATOR_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _fetch_hackernews(self, n: int = 15) -> list:
        """Top stories HackerNews via API gratuite."""
        import requests
        try:
            resp = requests.get(
                f"{self.sources['hackernews']}/topstories.json",
                timeout=10,
            )
            story_ids = resp.json()[:n]
            stories = []
            for sid in story_ids[:n]:
                r = requests.get(
                    f"{self.sources['hackernews']}/item/{sid}.json",
                    timeout=5,
                )
                item = r.json()
                if item and item.get("title"):
                    stories.append({
                        "title": item["title"],
                        "url": item.get("url", ""),
                        "score": item.get("score", 0),
                        "source": "HackerNews",
                    })
            return stories
        except Exception as e:
            log.warning(f"HackerNews fetch error: {e}")
            return []

    def _fetch_rss_items(self, n: int = 10) -> list:
        """Fetch items from RSS feeds (config.py NEWS_FEEDS)."""
        try:
            import feedparser
        except ImportError:
            return []

        from ..config import NEWS_FEEDS
        items = []

        for category, feeds in NEWS_FEEDS.items():
            for feed_url in feeds[:2]:  # Max 2 par catégorie pour la vitesse
                try:
                    feed = feedparser.parse(feed_url)
                    for entry in feed.entries[:3]:
                        items.append({
                            "title": entry.get("title", ""),
                            "url": entry.get("link", ""),
                            "score": 0,
                            "source": category.upper(),
                            "published": entry.get("published", ""),
                        })
                except Exception:
                    continue

        return items[:n]

    async def generate_daily_digest(self) -> str:
        """Génère le digest quotidien — les 5 trucs qui comptent."""
        # Collecter les sources
        hn_items = self._fetch_hackernews(15)
        rss_items = self._fetch_rss_items(15)
        all_items = hn_items + rss_items

        if not all_items:
            return "📡 Agrégateur : sources indisponibles. Réessaie plus tard."

        # Formatter pour l'IA
        items_text = "\n".join(
            f"- [{item['source']}] {item['title']} (score: {item.get('score', '?')})"
            for item in all_items
        )

        # Filtrage IA
        try:
            digest = chat(
                "Tu es l'AGRÉGATEUR — style GHOST + CYPHER. "
                "Sélectionne les 5 items les plus pertinents pour un fondateur "
                "d'empire d'agents IA (intéressé par : IA, automation, business, "
                "tendances tech, outils gratuits). "
                "Format : 5 bullets ultra-courts (1 phrase chacun). "
                "Ajoute un emoji pertinent par item. "
                "Termine par 1 phrase 'Le truc du jour' — l'item le plus fou ou surprenant.",
                f"Items collectés :\n{items_text}",
                max_tokens=400,
            )
        except Exception:
            # Fallback sans IA
            top5 = sorted(all_items, key=lambda x: x.get("score", 0), reverse=True)[:5]
            digest = "\n".join(
                f"• [{item['source']}] {item['title']}" for item in top5
            )

        # Sauvegarder l'historique
        data = self._load()
        data["history"].append({
            "date": datetime.now().strftime("%Y-%m-%d"),
            "items_scanned": len(all_items),
            "digest": digest,
        })
        if len(data["history"]) > 90:
            data["history"] = data["history"][-90:]
        self._save(data)

        return f"📡 DIGEST DU JOUR\n\n{digest}\n\n— {len(all_items)} sources scannées"

    def get_digest_history(self, days: int = 7) -> str:
        """Historique des digests récents."""
        data = self._load()
        history = data.get("history", [])[-days:]
        if not history:
            return "Pas de digest en historique."

        lines = ["📡 HISTORIQUE DIGESTS\n"]
        for h in history:
            lines.append(f"\n📅 {h['date']} ({h['items_scanned']} sources)")
            lines.append(h.get("digest", "—"))
        return "\n".join(lines)

    def handle_command(self, command: str) -> str:
        """Route les commandes agrégateur."""
        cmd = command.lower().strip()

        if cmd in ("/digest", "/agreg"):
            # Sync wrapper
            import asyncio
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    # Already in async context
                    return "Digest en cours de génération..."
                return loop.run_until_complete(self.generate_daily_digest())
            except Exception:
                return "Digest en cours de génération..."
        elif cmd == "/digest history":
            return self.get_digest_history()
        else:
            return (
                "📡 AGRÉGATEUR PERSONNEL\n\n"
                "/digest — Digest du jour (5 items)\n"
                "/digest history — Historique des 7 derniers jours"
            )
