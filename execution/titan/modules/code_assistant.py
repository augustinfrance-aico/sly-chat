"""
TITAN Code Assistant
Generate code, debug, explain, review — from Telegram.
"""

from ..ai_client import chat as ai_chat


class TitanCode:
    """Titan writes and debugs code."""

    def __init__(self):
        pass

    async def generate(self, description: str, language: str = "python") -> str:
        """Generate code from description."""
        return ai_chat("Expert assistant.", f"""Genere du code {language} pour: {description}""", 2048)

    async def debug(self, code: str, error: str = "") -> str:
        """Debug code and fix issues."""
        return ai_chat("Expert assistant.", f"""Debug ce code:\n\n{code}\n\nErreur: {error}""", 2048)

    async def explain(self, code: str) -> str:
        """Explain code in simple terms."""
        return ai_chat("Expert assistant.", f"""Explique ce code simplement (comme a un junior):\n\n{code}""", 1024)

    async def review(self, code: str) -> str:
        """Review code quality."""
        return ai_chat("Expert assistant.", f"""Review ce code:\n\n{code}""", 1024)

    async def convert(self, code: str, from_lang: str, to_lang: str) -> str:
        """Convert code from one language to another."""
        return ai_chat("Expert assistant.", f"""Convertis ce code de {from_lang} vers {to_lang}:\n\n{code}""", 2048)

    async def regex(self, description: str) -> str:
        """Generate regex from description."""
        return ai_chat("Expert assistant.", f"""Genere une regex pour: {description}""", 512)

    async def sql(self, description: str, db_type: str = "PostgreSQL") -> str:
        """Generate SQL query from description."""
        return ai_chat("Expert assistant.", f"""Genere une requete SQL ({db_type}) pour: {description}""", 1024)
