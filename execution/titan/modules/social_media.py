"""
TITAN Social Media Module
Generate posts, hashtags, bios, content calendars.
"""

from ..ai_client import chat as ai_chat


class TitanSocial:
    """Domine les reseaux sociaux."""

    def __init__(self):
        pass

    async def linkedin_post(self, topic: str) -> str:
        """Generate a viral LinkedIn post."""
        return ai_chat("Expert assistant.", f"""Ecris un post LinkedIn viral sur: "{topic}" """, 1000)

    async def twitter_thread(self, topic: str) -> str:
        """Generate a Twitter/X thread."""
        return ai_chat("Expert assistant.", f"""Ecris un thread Twitter/X de 7 tweets sur: "{topic}" """, 1500)

    async def instagram_caption(self, topic: str) -> str:
        """Generate an Instagram caption."""
        return ai_chat("Expert assistant.", f"""Ecris une caption Instagram pour: "{topic}" """, 500)

    async def hashtags(self, topic: str) -> str:
        """Generate relevant hashtags."""
        return ai_chat("Expert assistant.", f"""Genere 30 hashtags pertinents pour: "{topic}" """, 300)

    async def bio(self, platform: str, description: str) -> str:
        """Generate a social media bio."""
        return ai_chat("Expert assistant.", f"""Ecris une bio {platform} pour: "{description}" """, 300)

    async def content_calendar(self, niche: str, days: int = 7) -> str:
        """Generate a content calendar."""
        return ai_chat("Expert assistant.", f"""Cree un calendrier de contenu pour {days} jours pour la niche: "{niche}" """, 2000)
