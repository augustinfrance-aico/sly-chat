"""
TITAN Library — La Bibliothèque d'Augus
Compile automatiquement les meilleures idées, décisions, citations.
ZERO effort — tout est extrait des conversations existantes.

[PHILOMÈNE + MURRAY + BALOO]

Features:
- Extraction auto des meilleures phrases/idées des conversations
- Classement par catégorie (idée, décision, citation, leçon)
- Export en livre markdown
- FLEMMARD-approved : 0 input requis
"""

import json
import logging
from datetime import datetime
from pathlib import Path

from ..ai_client import chat

log = logging.getLogger("titan.library")

MEMORY_DIR = Path(__file__).parent.parent / "memory"
LIBRARY_FILE = MEMORY_DIR / "library.json"


class TitanLibrary:
    """La Bibliothèque — mémoire dorée d'Augus."""

    def __init__(self):
        pass

    def _load(self) -> dict:
        if LIBRARY_FILE.exists():
            with open(LIBRARY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"entries": [], "categories": {}}

    def _save(self, data: dict):
        with open(LIBRARY_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def auto_extract(self, user_msg: str, titan_reply: str):
        """Appelé après chaque conversation — extrait les pépites SILENCIEUSEMENT."""
        # Filtre rapide — pas d'extraction sur les trucs courts/triviaux
        if len(user_msg) < 30 and len(titan_reply) < 100:
            return

        # Mots-clés qui indiquent un contenu intéressant
        triggers = [
            "idée", "décision", "stratégie", "empire", "toujours", "jamais",
            "règle", "principe", "important", "building", "vision", "objectif",
            "j'ai compris", "j'ai réalisé", "le truc c'est", "en fait",
            "idea", "decision", "strategy", "rule",
        ]

        combined = (user_msg + " " + titan_reply).lower()
        if not any(t in combined for t in triggers):
            return

        # Extraction IA — rapide
        try:
            extraction = chat(
                "Tu es PHILOMÈNE — archiviste. "
                "Lis cet échange et extrais 0 ou 1 pépite (idée, décision, citation, leçon). "
                "Si rien d'intéressant, réponds exactement : RIEN. "
                "Si pépite trouvée, format : CATÉGORIE|texte court de la pépite. "
                "Catégories : idée, décision, citation, leçon. "
                "Max 1 ligne.",
                f"User: {user_msg}\nTitan: {titan_reply}",
                max_tokens=100,
            )

            if "RIEN" in extraction.upper() or "|" not in extraction:
                return

            parts = extraction.split("|", 1)
            if len(parts) != 2:
                return

            category = parts[0].strip().lower()
            content = parts[1].strip()

            if len(content) < 10:
                return

            data = self._load()
            data["entries"].append({
                "content": content,
                "category": category,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "source": user_msg[:100],
            })

            # Max 500 entrées
            if len(data["entries"]) > 500:
                data["entries"] = data["entries"][-500:]

            self._save(data)
            log.info(f"[LIBRARY] Pépite extraite : [{category}] {content[:60]}")

        except Exception as e:
            log.debug(f"Library extraction error: {e}")

    def get_random_gem(self) -> str:
        """Retourne une pépite au hasard — pour les rappels."""
        import random
        data = self._load()
        entries = data.get("entries", [])
        if not entries:
            return ""
        gem = random.choice(entries)
        return f"💎 [{gem['category']}] {gem['content']} — {gem['date']}"

    def get_all(self, category: str = None) -> str:
        """Liste toutes les pépites."""
        data = self._load()
        entries = data.get("entries", [])

        if category:
            entries = [e for e in entries if e.get("category") == category]

        if not entries:
            return "📚 Bibliothèque vide. Continue de parler à TITAN, les pépites s'accumulent."

        lines = [f"📚 BIBLIOTHÈQUE D'AUGUS ({len(entries)} pépites)\n"]
        for e in entries[-20:]:  # Dernières 20
            lines.append(f"💎 [{e['category']}] {e['content']}")

        return "\n".join(lines)

    def export_markdown(self) -> str:
        """Exporte la bibliothèque en markdown."""
        data = self._load()
        entries = data.get("entries", [])

        if not entries:
            return "Bibliothèque vide."

        # Grouper par catégorie
        by_cat = {}
        for e in entries:
            cat = e.get("category", "autre")
            by_cat.setdefault(cat, []).append(e)

        lines = ["# Bibliothèque d'Augus\n", f"*{len(entries)} pépites collectées*\n\n---\n"]

        for cat, items in sorted(by_cat.items()):
            lines.append(f"\n## {cat.title()} ({len(items)})\n")
            for item in items:
                lines.append(f"- {item['content']} *({item['date']})*")

        filepath = MEMORY_DIR / "journal_exports" / f"library_{datetime.now().strftime('%Y%m%d')}.md"
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        return f"📄 Bibliothèque exportée → {filepath.name}"

    def handle_command(self, command: str) -> str:
        """Route les commandes bibliothèque."""
        cmd = command.lower().strip()

        if cmd in ("/library", "/biblio"):
            return self.get_all()
        elif cmd == "/library random":
            gem = self.get_random_gem()
            return gem or "Bibliothèque vide pour l'instant."
        elif cmd.startswith("/library "):
            cat = cmd.replace("/library ", "").strip()
            return self.get_all(category=cat)
        elif cmd == "/library export":
            return self.export_markdown()
        else:
            return (
                "📚 BIBLIOTHÈQUE D'AUGUS\n\n"
                "/library — Toutes les pépites\n"
                "/library random — Une pépite au hasard\n"
                "/library idée — Filtre par catégorie\n"
                "/library export — Export markdown\n\n"
                "La bibliothèque se remplit automatiquement."
            )
