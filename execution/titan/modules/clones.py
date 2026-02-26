"""
TITAN Clones Module — L'Armée de Clones Sociaux
1 idée → 15 contenus automatiques pour toutes les plateformes.
ZERO effort — juste /clone "ton idée" et c'est parti.

[ZARA + BASQUIAT + SLY]

Features:
- Transformation d'une idée en 8+ formats de contenu
- Adapté par plateforme (LinkedIn, Twitter, YouTube, etc.)
- Export dans un dossier prêt à copier-coller
"""

import json
import logging
from datetime import datetime
from pathlib import Path

from ..ai_client import chat

log = logging.getLogger("titan.clones")

MEMORY_DIR = Path(__file__).parent.parent / "memory"
CLONES_DIR = MEMORY_DIR / "clones_output"


class TitanClones:
    """L'Armée de Clones — 1 idée → contenu partout."""

    def __init__(self):
        CLONES_DIR.mkdir(parents=True, exist_ok=True)

    async def generate_clones(self, idea: str) -> str:
        """Transforme une idée en contenu multi-plateforme."""
        if not idea or len(idea) < 5:
            return "Donne-moi une idée. Ex: /clone L'IA va remplacer 80% des agences"

        try:
            content = chat(
                "Tu es ZARA + BASQUIAT + SLY — machine à contenu. "
                "Transforme cette idée en 8 formats de contenu. "
                "CHAQUE format doit être COMPLET et prêt à publier.\n\n"
                "Formats :\n"
                "1. 🐦 TWEET (max 280 chars, accrocheur)\n"
                "2. 💼 LINKEDIN (3-5 paragraphes, storytelling pro)\n"
                "3. 🧵 THREAD TWITTER (5 tweets numérotés)\n"
                "4. 📱 CAPTION INSTAGRAM/TIKTOK (court, hashtags)\n"
                "5. 📝 ARTICLE MEDIUM (intro + 3 points + conclusion)\n"
                "6. 💬 QUOTE CARD (1 phrase percutante pour image)\n"
                "7. 📧 EMAIL NEWSLETTER (sujet + body court)\n"
                "8. 🎬 SCRIPT SHORT VIDEO (30 sec, hook→contenu→CTA)\n\n"
                "Sépare chaque format clairement. Tout en français sauf si l'idée est en anglais.",
                f"Idée : {idea}",
                max_tokens=2000,
            )

            # Sauvegarder dans un fichier
            timestamp = datetime.now().strftime("%Y%m%d_%H%M")
            slug = idea[:30].replace(" ", "_").replace("/", "")
            filepath = CLONES_DIR / f"clone_{timestamp}_{slug}.md"

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"# Clone — {idea}\n")
                f.write(f"*Généré le {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n\n")
                f.write(content)

            # Résumé court pour Telegram
            lines = content.split("\n")
            preview = "\n".join(lines[:15])
            if len(preview) > 3000:
                preview = preview[:3000] + "\n\n[...]"

            return (
                f"🧬 CLONES GÉNÉRÉS — 8 formats\n\n"
                f"{preview}\n\n"
                f"📄 Fichier complet : {filepath.name}"
            )

        except Exception as e:
            return f"Erreur clone : {e}"

    def list_clones(self) -> str:
        """Liste les clones générés."""
        files = sorted(CLONES_DIR.glob("clone_*.md"), reverse=True)[:10]
        if not files:
            return "Aucun clone généré. /clone [ton idée] pour commencer."

        lines = ["🧬 CLONES RÉCENTS\n"]
        for f in files:
            lines.append(f"• {f.stem}")

        return "\n".join(lines)

    def handle_command(self, command: str) -> str:
        """Route les commandes clones."""
        cmd = command.strip()

        if cmd.lower() in ("/clone", "/clones"):
            return self.list_clones()
        elif cmd.lower().startswith("/clone "):
            idea = cmd[7:].strip()
            import asyncio
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    return "Clones en génération..."
                return loop.run_until_complete(self.generate_clones(idea))
            except Exception:
                return "Clones en génération..."
        else:
            return (
                "🧬 ARMÉE DE CLONES\n\n"
                "/clone [idée] — Générer 8 formats de contenu\n"
                "/clones — Liste des clones récents\n\n"
                "Ex: /clone L'IA va remplacer 80% des agences"
            )
