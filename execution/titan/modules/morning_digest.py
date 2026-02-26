"""
TITAN Morning Digest — Le Digest du Matin
5 bullet points. 30 secondes de lecture. Aucune action requise.

[ORACLE + MAYA + BALOO]

Envoyé automatiquement à 8h via scheduler.
Remplace le brief matinal actuel avec un format plus court et plus utile.
FLEMMARD-approved : zéro input requis d'Augus.
"""

import json
import logging
from datetime import datetime
from pathlib import Path

from ..ai_client import chat

log = logging.getLogger("titan.morning_digest")

MEMORY_DIR = Path(__file__).parent.parent / "memory"
DIGEST_FILE = MEMORY_DIR / "morning_digests.json"


class TitanMorningDigest:
    """Digest du matin — 5 bullets, 30 sec, 0 effort."""

    def __init__(self):
        pass

    def _load(self) -> dict:
        if DIGEST_FILE.exists():
            with open(DIGEST_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"digests": []}

    def _save(self, data: dict):
        with open(DIGEST_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    async def generate(self) -> str:
        """Génère le digest matinal complet."""
        sections = []

        # 1. Tendances IA du jour
        ai_trend = self._get_ai_trend()

        # 2. Météo business
        biz_weather = self._get_business_weather()

        # Compiler avec IA
        raw_data = f"IA: {ai_trend}\nBusiness: {biz_weather}"

        try:
            digest = chat(
                "Tu es le DIGEST — style BALOO (vulgarisation). "
                "Compile ces données en 5 bullet points ULTRA COURTS. "
                "Format :\n"
                "☀️ [humeur du jour en 1 mot]\n"
                "• [bullet 1 — tendance IA]\n"
                "• [bullet 2 — opportunité business]\n"
                "• [bullet 3 — fait surprenant]\n"
                "• [bullet 4 — action recommandée pour la journée]\n\n"
                "MAX 1 ligne par bullet. Pas de blabla.",
                raw_data,
                max_tokens=300,
            )
        except Exception:
            digest = self._fallback_digest(ai_trend)

        # Sauvegarder
        data = self._load()
        data["digests"].append({
            "date": datetime.now().strftime("%Y-%m-%d"),
            "content": digest,
        })
        if len(data["digests"]) > 90:
            data["digests"] = data["digests"][-90:]
        self._save(data)

        now = datetime.now()
        header = f"☀️ DIGEST — {now.strftime('%A %d %B')}\n"
        return f"{header}\n{digest}"

    def _get_ai_trend(self) -> str:
        """Tendance IA du jour via RSS gratuit."""
        try:
            import feedparser
            feed = feedparser.parse("https://news.mit.edu/topic/mitartificial-intelligence2-rss.xml")
            if feed.entries:
                return feed.entries[0].get("title", "Pas de news IA")
            return "Sources IA indisponibles"
        except Exception:
            return "Sources IA indisponibles"

    def _get_crypto_snapshot(self) -> str:
        """Snapshot crypto rapide via API gratuite."""
        import requests
        try:
            resp = requests.get(
                "https://api.coingecko.com/api/v3/simple/price",
                params={"ids": "bitcoin,ethereum,solana", "vs_currencies": "usd", "include_24hr_change": "true"},
                timeout=10,
            )
            data = resp.json()
            parts = []
            for coin, info in data.items():
                price = info.get("usd", 0)
                change = info.get("usd_24h_change", 0)
                arrow = "📈" if change > 0 else "📉"
                parts.append(f"{coin.upper()}: ${price:,.0f} ({change:+.1f}%) {arrow}")
            return " | ".join(parts)
        except Exception:
            return "Crypto data indisponible"

    def _get_business_weather(self) -> str:
        """Météo business — sentiment général."""
        try:
            import feedparser
            feed = feedparser.parse("https://www.entrepreneur.com/latest.rss")
            if feed.entries:
                titles = [e.get("title", "") for e in feed.entries[:3]]
                return " | ".join(titles)
            return "Business news indisponibles"
        except Exception:
            return "Business news indisponibles"

    def _fallback_digest(self, ai: str) -> str:
        """Digest sans IA si le provider est down."""
        return (
            f"• IA : {ai[:80]}\n"
            f"• Le Building tourne. L'empire attend tes ordres."
        )

    def handle_command(self, command: str) -> str:
        """Commande manuelle du digest."""
        import asyncio
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                return "Digest en génération..."
            return loop.run_until_complete(self.generate())
        except Exception:
            return "Digest en génération..."
