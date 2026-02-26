"""
TITAN Film Building — Script cinématique du Building
Génère un script vidéo 3-5 min racontant l'histoire de l'empire.

[LEON + BASQUIAT + MURRAY]

Features:
- Script narratif cinématique
- Direction artistique incluse
- Découpage en scènes
- Export markdown prêt pour production
"""

import logging
from datetime import datetime
from pathlib import Path

from ..ai_client import chat

log = logging.getLogger("titan.film")

MEMORY_DIR = Path(__file__).parent.parent / "memory"
FILM_DIR = MEMORY_DIR / "film_scripts"


class TitanFilm:
    """Le Film du Building — script cinématique."""

    def __init__(self):
        FILM_DIR.mkdir(parents=True, exist_ok=True)

    def generate_script(self, style: str = "epic") -> str:
        """Génère un script vidéo complet."""
        styles = {
            "epic": "Ton épique, cinématique, musique Hans Zimmer dans la tête. Narration à la Morgan Freeman.",
            "street": "Ton street, direct, comme un documentaire Netflix sur une startup. Brut et vrai.",
            "minimal": "Ton minimal, Apple keynote vibes. Chaque mot compte. Silences puissants.",
            "funny": "Ton humoristique, self-aware, le fondateur qui se moque de lui-même avec classe.",
        }

        tone = styles.get(style, styles["epic"])

        try:
            script = chat(
                f"Tu es LEON + BASQUIAT + MURRAY — trio cinématique. "
                f"Écris un script vidéo de 3-5 minutes sur LE BUILDING — "
                f"un empire de 25 agents IA créé par Augus, un seul homme. "
                f"L'histoire : un fondateur non-technique construit un empire d'agents autonomes "
                f"(TITAN bot Telegram, 53 modules, cascade IA 6 modèles, coût total 0€). "
                f"25 agents de personnalité, 3 pôles (RECON, FORGE, DEPLOY), "
                f"tout tourne tout seul.\n\n"
                f"Style : {tone}\n\n"
                f"Format :\n"
                f"[SCÈNE X — TITRE] (durée)\n"
                f"NARRATION : texte\n"
                f"VISUEL : description de ce qu'on voit\n"
                f"MUSIQUE : ambiance\n\n"
                f"5-8 scènes. Hook puissant dans les 5 premières secondes.",
                "Génère le script complet.",
                max_tokens=2000,
            )
        except Exception as e:
            return f"Erreur script : {e}"

        # Sauvegarder
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        filepath = FILM_DIR / f"script_{style}_{timestamp}.md"
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"# LE BUILDING — Script ({style})\n")
            f.write(f"*{datetime.now().strftime('%Y-%m-%d %H:%M')}*\n\n")
            f.write(script)

        preview = script[:3000] if len(script) > 3000 else script

        return (
            f"🎬 SCRIPT GÉNÉRÉ — style {style}\n\n"
            f"{preview}\n\n"
            f"📄 Fichier : {filepath.name}"
        )

    def handle_command(self, command: str) -> str:
        """Route les commandes film."""
        cmd = command.lower().strip()

        if cmd in ("/film", "/script"):
            return self.generate_script("epic")
        elif cmd.startswith("/film "):
            style = cmd.replace("/film ", "").strip()
            return self.generate_script(style)
        else:
            return (
                "🎬 FILM DU BUILDING\n\n"
                "/film — Script épique (défaut)\n"
                "/film street — Style documentaire\n"
                "/film minimal — Style Apple\n"
                "/film funny — Style humoristique"
            )
