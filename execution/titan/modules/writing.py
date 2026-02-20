"""
TITAN Writing Module
Creative writing assistant — stories, scripts, copywriting, blog posts.
"""

from ..ai_client import chat as ai_chat


class TitanWriting:
    """Ecriture pro en un message."""

    def __init__(self):
        pass

    async def blog_post(self, topic: str) -> str:
        """Generate a blog post."""
        return ai_chat("Expert assistant.", f"""Ecris un article de blog sur: "{topic}" """, 2000)

    async def copywriting(self, product: str, audience: str = "general") -> str:
        """Generate marketing copy."""
        return ai_chat("Expert assistant.", f"""Ecris du copywriting pour: "{product}" (audience: {audience})""", 1000)

    async def story(self, premise: str) -> str:
        """Generate a short story."""
        return ai_chat("Expert assistant.", f"""Ecris une histoire courte basee sur: "{premise}" """, 2000)

    async def summarize(self, text: str) -> str:
        """Summarize any text."""
        return ai_chat("Expert assistant.", f"""Resume ce texte en 3-5 points cles:\n\n{text}""", 500)

    async def paraphrase(self, text: str) -> str:
        """Paraphrase text."""
        return ai_chat("Expert assistant.", f"""Reformule ce texte de 3 facons differentes:\n\n{text}""", 1000)

    async def slogan(self, brand: str, values: str = "") -> str:
        """Generate brand slogans."""
        return ai_chat("Expert assistant.", f"""Genere 10 slogans pour la marque "{brand}". Valeurs: {values}""", 500)
