"""
TITAN Empire Visual — Identité visuelle du Building
Génère les guidelines visuelles complètes de l'empire.

[BASQUIAT + LEON + ZARA]

Features:
- Palette de couleurs définie
- Guidelines typographiques
- Templates de posts
- Style guide complet
- Export markdown
"""

import logging
from datetime import datetime
from pathlib import Path

from ..ai_client import chat

log = logging.getLogger("titan.empire_visual")

MEMORY_DIR = Path(__file__).parent.parent / "memory"
VISUAL_DIR = MEMORY_DIR / "empire_visual"


# === IDENTITÉ VISUELLE DU BUILDING ===
BRAND = {
    "name": "BUILDING IA",
    "tagline": "Empire d'Agents Autonomes",
    "colors": {
        "primary": "#7B2FF7",       # Violet électrique
        "secondary": "#00D4FF",     # Cyan néon
        "accent": "#FF6B35",        # Orange feu
        "dark": "#0A0A0F",          # Noir profond
        "surface": "#12121A",       # Gris foncé
        "text": "#E0E0E0",          # Gris clair
        "muted": "#666666",         # Gris moyen
    },
    "fonts": {
        "heading": "Space Grotesk, Segoe UI, sans-serif",
        "body": "Inter, Segoe UI, sans-serif",
        "mono": "JetBrains Mono, Consolas, monospace",
    },
    "emojis": {
        "brand": "⚡",
        "success": "✅",
        "warning": "⚠️",
        "building": "🏗️",
        "agent": "🤖",
        "money": "💰",
        "fire": "🔥",
        "target": "🎯",
    },
    "tone": "Direct, technique mais accessible, humour sec, jamais corporate.",
}


class TitanEmpireVisual:
    """L'Empire Visuel — identité du Building."""

    def __init__(self):
        VISUAL_DIR.mkdir(parents=True, exist_ok=True)

    def get_brand_guide(self) -> str:
        """Retourne le guide de marque complet."""
        b = BRAND
        c = b["colors"]

        return (
            f"🎨 IDENTITÉ VISUELLE — {b['name']}\n"
            f"Tagline : {b['tagline']}\n\n"
            f"═══ COULEURS ═══\n"
            f"🟣 Primary : {c['primary']} (violet électrique)\n"
            f"🔵 Secondary : {c['secondary']} (cyan néon)\n"
            f"🟠 Accent : {c['accent']} (orange feu)\n"
            f"⬛ Dark : {c['dark']} (noir profond)\n"
            f"📝 Text : {c['text']} (gris clair)\n\n"
            f"═══ TYPO ═══\n"
            f"Titres : {b['fonts']['heading']}\n"
            f"Corps : {b['fonts']['body']}\n"
            f"Code : {b['fonts']['mono']}\n\n"
            f"═══ TON ═══\n"
            f"{b['tone']}\n\n"
            f"═══ EMOJIS OFFICIELS ═══\n"
            + "\n".join(f"{v} = {k}" for k, v in b["emojis"].items())
        )

    def generate_style_guide(self) -> str:
        """Génère un style guide complet en markdown."""
        try:
            guide = chat(
                "Tu es BASQUIAT — directeur artistique du Building IA. "
                "Génère un style guide complet pour la marque. "
                "Inclus : 1) Philosophie visuelle, 2) Do / Don't, "
                "3) Exemples de posts (LinkedIn, Twitter), "
                "4) Guidelines images/visuels, 5) Voice & tone guide. "
                "Style : premium mais accessible, tech mais humain.",
                f"Marque : {BRAND['name']}\n"
                f"Couleurs : {BRAND['colors']}\n"
                f"Ton : {BRAND['tone']}",
                max_tokens=1500,
            )
        except Exception as e:
            return f"Erreur : {e}"

        filepath = VISUAL_DIR / f"style_guide_{datetime.now().strftime('%Y%m%d')}.md"
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"# Style Guide — {BRAND['name']}\n\n{guide}")

        return f"🎨 STYLE GUIDE GÉNÉRÉ\n\n{guide[:2000]}\n\n📄 {filepath.name}"

    def generate_css_theme(self) -> str:
        """Génère le thème CSS officiel du Building."""
        c = BRAND["colors"]
        f = BRAND["fonts"]

        css = f"""/* BUILDING IA — Theme CSS Officiel */
/* Généré par BASQUIAT le {datetime.now().strftime('%Y-%m-%d')} */

:root {{
    --primary: {c['primary']};
    --secondary: {c['secondary']};
    --accent: {c['accent']};
    --dark: {c['dark']};
    --surface: {c['surface']};
    --text: {c['text']};
    --muted: {c['muted']};

    --font-heading: {f['heading']};
    --font-body: {f['body']};
    --font-mono: {f['mono']};

    --radius: 12px;
    --shadow: 0 4px 20px rgba(123, 47, 247, 0.1);
}}

body {{
    background: var(--dark);
    color: var(--text);
    font-family: var(--font-body);
    line-height: 1.6;
}}

h1, h2, h3 {{
    font-family: var(--font-heading);
    background: linear-gradient(90deg, var(--secondary), var(--primary));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}

.card {{
    background: var(--surface);
    border: 1px solid #222;
    border-radius: var(--radius);
    padding: 1.5rem;
    transition: all 0.2s;
}}

.card:hover {{
    border-color: var(--primary);
    box-shadow: var(--shadow);
    transform: translateY(-2px);
}}

.btn-primary {{
    background: linear-gradient(135deg, var(--primary), var(--secondary));
    color: white;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: var(--radius);
    font-weight: 600;
    cursor: pointer;
}}

.badge {{
    display: inline-block;
    background: rgba(123, 47, 247, 0.2);
    color: var(--primary);
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.75rem;
}}

code {{
    font-family: var(--font-mono);
    background: var(--surface);
    padding: 2px 6px;
    border-radius: 4px;
}}"""

        filepath = VISUAL_DIR / "building_theme.css"
        with open(filepath, "w", encoding="utf-8") as f_out:
            f_out.write(css)

        return f"🎨 THÈME CSS GÉNÉRÉ\n\n{css[:1500]}\n\n📄 {filepath.name}"

    def handle_command(self, command: str) -> str:
        """Route les commandes visual."""
        cmd = command.lower().strip()

        if cmd in ("/visual", "/brand"):
            return self.get_brand_guide()
        elif cmd == "/visual guide":
            return self.generate_style_guide()
        elif cmd == "/visual css":
            return self.generate_css_theme()
        else:
            return (
                "🎨 EMPIRE VISUEL\n\n"
                "/visual — Guide de marque\n"
                "/visual guide — Style guide complet\n"
                "/visual css — Thème CSS officiel"
            )
