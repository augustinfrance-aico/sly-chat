"""
TITAN Mega-Prompt — Le Building dans une boîte
Génère un mega-prompt transportable qui reconstruit l'esprit du Building
dans N'IMPORTE quel LLM (GPT, Gemini, Claude, local).

[OMEGA + PHILOMÈNE + RICK]

Features:
- Lecture auto des fichiers du Building
- Compression en 1 prompt optimisé
- Export clipboard-ready
- Versions par LLM cible
"""

import logging
from datetime import datetime
from pathlib import Path

from ..ai_client import chat

log = logging.getLogger("titan.mega_prompt")

ROOT_DIR = Path(__file__).parent.parent.parent.parent
MEMORY_DIR = Path(__file__).parent.parent / "memory"
MEGA_PROMPT_DIR = MEMORY_DIR / "mega_prompts"


class TitanMegaPrompt:
    """Le Méga-Prompt — l'empire transportable."""

    def __init__(self):
        MEGA_PROMPT_DIR.mkdir(parents=True, exist_ok=True)

    def _read_building_essence(self) -> str:
        """Lit l'essence du Building depuis les fichiers clés."""
        essence_parts = []

        # Fichiers à lire pour capturer l'essence
        key_files = [
            ROOT_DIR / "CLAUDE.md",
            ROOT_DIR / "directives" / "TRI_POLE.md",
            ROOT_DIR / "personnalites" / "CASTING.md",
            ROOT_DIR / "directives" / "ROUTING.md",
        ]

        for filepath in key_files:
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                # Garder les 2000 premiers chars de chaque
                essence_parts.append(f"[{filepath.name}]\n{content[:2000]}")
            except Exception:
                continue

        return "\n\n---\n\n".join(essence_parts)

    def generate(self, target_llm: str = "universal") -> str:
        """Génère le mega-prompt."""
        essence = self._read_building_essence()

        system = (
            "Tu es OMEGA + PHILOMÈNE + RICK — les 3 meilleurs agents fusionnés. "
            "Ta mission : comprimer TOUT le Building (25 agents, 3 pôles, toutes les règles) "
            "en UN SEUL prompt qui peut être collé dans n'importe quel LLM. "
            "Le prompt généré doit :\n"
            "1. Recréer la personnalité complète du Building\n"
            "2. Inclure les 25 agents avec leurs rôles\n"
            "3. Inclure le Tri-Pôle (R→F→D)\n"
            "4. Inclure le style (direct, pas de blabla, humour, Augus = Suzerain)\n"
            "5. Faire max 3000 tokens\n"
            "6. Être auto-suffisant (aucune référence à des fichiers externes)\n\n"
            f"LLM cible : {target_llm}"
        )

        try:
            mega = chat(system, f"Essence du Building :\n{essence}", max_tokens=2000)
        except Exception as e:
            return f"Erreur génération : {e}"

        # Sauvegarder
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        filepath = MEGA_PROMPT_DIR / f"mega_{target_llm}_{timestamp}.md"
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"# MEGA-PROMPT BUILDING — {target_llm.upper()}\n")
            f.write(f"*Généré le {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n\n")
            f.write(mega)

        preview = mega[:3000] if len(mega) > 3000 else mega

        return (
            f"🧠 MEGA-PROMPT GÉNÉRÉ ({target_llm})\n\n"
            f"{preview}\n\n"
            f"📄 Fichier : {filepath.name}\n"
            f"Colle ça dans n'importe quel LLM — le Building renaît."
        )

    def list_prompts(self) -> str:
        """Liste les mega-prompts générés."""
        files = sorted(MEGA_PROMPT_DIR.glob("mega_*.md"), reverse=True)[:5]
        if not files:
            return "Aucun mega-prompt. /megaprompt pour en générer un."

        lines = ["🧠 MEGA-PROMPTS\n"]
        for f in files:
            lines.append(f"• {f.stem}")
        return "\n".join(lines)

    def handle_command(self, command: str) -> str:
        """Route les commandes mega-prompt."""
        cmd = command.lower().strip()

        if cmd in ("/megaprompt", "/mega"):
            return self.generate("universal")
        elif cmd.startswith("/megaprompt "):
            target = cmd.replace("/megaprompt ", "").strip()
            return self.generate(target)
        elif cmd == "/mega list":
            return self.list_prompts()
        else:
            return (
                "🧠 MEGA-PROMPT\n\n"
                "/megaprompt — Prompt universel\n"
                "/megaprompt gpt — Optimisé GPT\n"
                "/megaprompt gemini — Optimisé Gemini\n"
                "/mega list — Liste des prompts générés"
            )
