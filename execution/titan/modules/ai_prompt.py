"""
TITAN AI Prompt Generator
Generate perfect prompts for AI tools (Midjourney, DALL-E, Stable Diffusion, ChatGPT).
"""

from ..ai_client import chat as ai_chat


class TitanAIPrompt:
    """Master the art of prompting."""

    def __init__(self):
        pass

    async def midjourney(self, concept: str) -> str:
        """Generate a Midjourney prompt."""
        return ai_chat("Expert assistant.", f"""Genere un prompt Midjourney professionnel pour: "{concept}" """, 500)

    async def dalle(self, concept: str) -> str:
        """Generate a DALL-E prompt."""
        return ai_chat("Expert assistant.", f"""Genere un prompt DALL-E optimise pour: "{concept}" """, 500)

    async def stable_diffusion(self, concept: str) -> str:
        """Generate a Stable Diffusion prompt with negative prompt."""
        return ai_chat("Expert assistant.", f"""Genere un prompt Stable Diffusion pour: "{concept}" """, 500)

    async def chatgpt_prompt(self, task: str) -> str:
        """Generate an optimized ChatGPT/Claude prompt."""
        return ai_chat("Expert assistant.", f"""Genere un prompt systeme optimise pour ChatGPT/Claude pour cette tache: "{task}" """, 1000)

    async def improve_prompt(self, original: str) -> str:
        """Improve an existing prompt."""
        return ai_chat("Expert assistant.", f"""Ameliore ce prompt pour le rendre plus efficace:\n\n{original}""", 1000)
