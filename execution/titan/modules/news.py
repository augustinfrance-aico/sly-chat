"""
TITAN News Module
Real-time news aggregation from multiple sources.
Tech, AI, Business, Crypto, France.
"""

import feedparser
import json
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional


from ..config import NEWS_FEEDS
from ..ai_client import chat as ai_chat


CACHE_FILE = Path(__file__).parent.parent / "memory" / "news_cache.json"


class TitanNews:
    """Titan's eyes on the world."""

    def __init__(self):
        self.cache = self._load_cache()

    def _load_cache(self) -> dict:
        if CACHE_FILE.exists():
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"articles": [], "last_fetch": None}

    def _save_cache(self):
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(self.cache, f, ensure_ascii=False, indent=2)

    def _article_id(self, title: str) -> str:
        return hashlib.md5(title.encode()).hexdigest()[:12]

    async def fetch_news(self, categories: list = None, max_per_feed: int = 5) -> list:
        """Fetch latest news from RSS feeds."""
        if categories is None:
            categories = list(NEWS_FEEDS.keys())

        articles = []
        seen_ids = set()

        for category in categories:
            feeds = NEWS_FEEDS.get(category, [])
            for feed_url in feeds:
                try:
                    feed = feedparser.parse(feed_url)
                    for entry in feed.entries[:max_per_feed]:
                        title = entry.get("title", "")
                        art_id = self._article_id(title)

                        if art_id in seen_ids:
                            continue
                        seen_ids.add(art_id)

                        published = entry.get("published", "")
                        summary = entry.get("summary", entry.get("description", ""))
                        # Clean HTML tags
                        summary = summary.replace("<p>", "").replace("</p>", " ")
                        summary = summary[:300]

                        articles.append({
                            "id": art_id,
                            "title": title,
                            "summary": summary,
                            "link": entry.get("link", ""),
                            "published": published,
                            "category": category,
                            "source": feed.feed.get("title", feed_url),
                        })
                except Exception:
                    continue

        # Sort by date (newest first)
        articles.sort(key=lambda x: x.get("published", ""), reverse=True)

        # Cache
        self.cache["articles"] = articles[:100]
        self.cache["last_fetch"] = datetime.now().isoformat()
        self._save_cache()

        return articles

    async def get_brief(self, categories: list = None, max_articles: int = 10) -> str:
        """Get a formatted news brief."""
        articles = await self.fetch_news(categories)

        if not articles:
            return "Aucune actualité récupérée. Vérifie la connexion."

        top = articles[:max_articles]

        # Format for Telegram
        lines = [f"📰 TOP {len(top)} ACTUS — {datetime.now().strftime('%d/%m %H:%M')}\n"]

        for i, art in enumerate(top, 1):
            emoji = {
                "tech": "💻", "ai": "🤖", "business": "📈",
                "crypto": "🪙", "france": "🇫🇷"
            }.get(art["category"], "📌")

            lines.append(f"{emoji} {art['title']}")
            if art.get("summary"):
                short = art["summary"][:120]
                lines.append(f"   └ {short}...")
            lines.append("")

        return "\n".join(lines)

    async def get_ai_summary(self, max_articles: int = 15) -> str:
        """Get a Claude-powered intelligent summary of the news."""
        articles = await self.fetch_news()

        if not articles:
            return "Pas de news à résumer."

        top = articles[:max_articles]
        articles_text = "\n".join([
            f"- [{a['category'].upper()}] {a['title']}: {a.get('summary', '')[:200]}"
            for a in top
        ])

        return ai_chat(
            "Expert assistant.",
            f"""Resume ces actualites en un brief de 5-6 bullet points percutants.
Sois concis, informatif, et ajoute un mini commentaire sarcastique si pertinent.

{articles_text}""",
            1024,
        )

    async def search_news(self, query: str) -> str:
        """Search through cached news."""
        if not self.cache.get("articles"):
            await self.fetch_news()

        query_lower = query.lower()
        results = [
            a for a in self.cache["articles"]
            if query_lower in a["title"].lower() or query_lower in a.get("summary", "").lower()
        ]

        if not results:
            return f"Rien trouvé dans les news pour '{query}'."

        lines = [f"🔍 {len(results)} résultat(s) pour '{query}':\n"]
        for art in results[:5]:
            lines.append(f"• {art['title']}")
            lines.append(f"  {art['link']}\n")

        return "\n".join(lines)
