"""
TITAN Portfolio Generator
Generate beautiful HTML portfolio pages from a brief.
Dark mode, modern, ready to show clients.
"""

from pathlib import Path

from ..ai_client import chat as ai_chat

OUTPUT_DIR = Path(__file__).parent.parent.parent  # execution/


class TitanPortfolio:
    """Titan builds portfolio pages."""

    def __init__(self):
        pass

    async def generate(self, brief: str, filename: str = "portfolio_titan.html") -> str:
        """Generate a complete HTML portfolio page."""
        html = ai_chat("Expert assistant.", f"""Genere une page HTML portfolio complete et moderne.

Brief: {brief}

Style: dark mode, responsive, animations CSS. Sections: hero, description, tech stack, resultats.
Reponds UNIQUEMENT avec le HTML, rien d'autre.""", 4096)

        # Extract HTML if wrapped in code block
        if "```html" in html:
            html = html.split("```html")[1].split("```")[0]
        elif "```" in html:
            html = html.split("```")[1].split("```")[0]

        # Save file
        filepath = OUTPUT_DIR / filename
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)

        return f"Portfolio genere: {filepath}\nOuvre-le dans ton navigateur pour voir le resultat."

    async def generate_proposal(self, client_name: str, project_brief: str, filename: str = None) -> str:
        """Generate a client-specific proposal page."""
        if not filename:
            slug = client_name.lower().replace(" ", "_").replace("'", "")
            filename = f"proposal_{slug}.html"

        html = ai_chat("Expert assistant.", f"""Genere une page HTML de proposition commerciale pour un client.

Client: {client_name}
Projet: {project_brief}

Style: dark mode, professionnel. Sections: intro, solution, pricing, CTA.
Reponds UNIQUEMENT avec le HTML, rien d'autre.""", 4096)

        if "```html" in html:
            html = html.split("```html")[1].split("```")[0]
        elif "```" in html:
            html = html.split("```")[1].split("```")[0]

        filepath = OUTPUT_DIR / filename
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)

        return f"Proposition generee: {filepath}"
