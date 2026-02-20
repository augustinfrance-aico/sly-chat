"""
TITAN Startup Module
Business name generator, pitch deck, business model canvas, competitor analysis.
"""

import random

from ..ai_client import chat as ai_chat


class TitanStartup:
    """Build your empire."""

    def __init__(self):
        pass

    def name_generator(self, keywords: str) -> str:
        """Generate startup names."""
        parts = keywords.split()
        prefixes = ["", "Go", "Neo", "Flux", "Hyper", "Aero", "Vox", "Zen", "Pixel", "Byte"]
        suffixes = ["", "ly", "ify", "io", "Hub", "Lab", "AI", "X", "Pro", "Cloud"]

        names = set()
        for word in parts:
            for pre in random.sample(prefixes, 5):
                for suf in random.sample(suffixes, 5):
                    name = f"{pre}{word.capitalize()}{suf}"
                    if 4 < len(name) < 15:
                        names.add(name)

        selected = random.sample(list(names), min(15, len(names)))
        lines = [f"NOMS DE STARTUP ({keywords})\n"]
        for n in selected:
            lines.append(f"  * {n}")
        return "\n".join(lines)

    async def elevator_pitch(self, idea: str) -> str:
        """Generate an elevator pitch."""
        return ai_chat("Expert assistant.", f"""Cree un elevator pitch de 30 secondes pour: "{idea}" """, 500)

    async def business_model(self, idea: str) -> str:
        """Generate a Business Model Canvas."""
        return ai_chat("Expert assistant.", f"""Cree un Business Model Canvas pour: "{idea}" """, 2000)

    async def competitor_analysis(self, market: str) -> str:
        """Analyze competitors in a market."""
        return ai_chat("Expert assistant.", f"""Analyse les concurrents dans le marche: "{market}" """, 1500)

    async def pricing_strategy(self, product: str) -> str:
        """Suggest pricing strategies."""
        return ai_chat("Expert assistant.", f"""Propose 3 strategies de pricing pour: "{product}" """, 1000)
