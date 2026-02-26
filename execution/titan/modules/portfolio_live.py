"""
TITAN Portfolio Live — Le Portfolio Vivant
Se met à jour tout seul. Chaque projet terminé = auto-ajout.

[BASQUIAT + FORGE + GHOST]

Features:
- Détection auto de nouveaux projets
- Génération HTML dark mode
- Screenshot/description auto
- Grandit tout seul
"""

import json
import logging
from datetime import datetime
from pathlib import Path

from ..ai_client import chat

log = logging.getLogger("titan.portfolio_live")

ROOT_DIR = Path(__file__).parent.parent.parent.parent
MEMORY_DIR = Path(__file__).parent.parent / "memory"
PORTFOLIO_FILE = MEMORY_DIR / "portfolio_live.json"
PORTFOLIO_HTML = ROOT_DIR / "portfolios" / "building_live.html"


class TitanPortfolioLive:
    """Portfolio vivant — grandit pendant que tu dors."""

    def __init__(self):
        pass

    def _load(self) -> dict:
        if PORTFOLIO_FILE.exists():
            with open(PORTFOLIO_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"projects": [], "last_generated": ""}

    def _save(self, data: dict):
        with open(PORTFOLIO_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add_project(self, name: str, description: str = "", category: str = "automation") -> str:
        """Ajoute un projet au portfolio."""
        data = self._load()

        # Vérifier doublon
        existing = [p["name"].lower() for p in data["projects"]]
        if name.lower() in existing:
            return f"Projet '{name}' déjà dans le portfolio."

        # Générer description IA si pas fournie
        if not description:
            try:
                description = chat(
                    "Tu es BASQUIAT — copywriter portfolio. "
                    "Écris une description de projet en 2-3 phrases. "
                    "Style : professionnel mais avec du caractère. "
                    "Mentionne les technos et le résultat.",
                    f"Projet : {name}, catégorie : {category}",
                    max_tokens=150,
                )
            except Exception:
                description = f"Projet {category} — {name}"

        project = {
            "name": name,
            "description": description,
            "category": category,
            "date_added": datetime.now().strftime("%Y-%m-%d"),
            "tags": [category],
        }

        data["projects"].append(project)
        self._save(data)

        # Re-générer le HTML
        self._generate_html(data)

        return f"✅ Projet ajouté au portfolio : {name}\n📄 HTML mis à jour."

    def _generate_html(self, data: dict):
        """Génère le portfolio HTML dark mode."""
        projects = data.get("projects", [])

        cards_html = ""
        for p in projects:
            cards_html += f"""
            <div class="card">
                <div class="card-category">{p['category'].upper()}</div>
                <h3>{p['name']}</h3>
                <p>{p['description']}</p>
                <div class="card-date">{p['date_added']}</div>
            </div>
            """

        html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Building IA — Portfolio Live</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            background: #0a0a0f;
            color: #e0e0e0;
            font-family: 'Segoe UI', system-ui, sans-serif;
            padding: 2rem;
        }}
        .header {{
            text-align: center;
            margin-bottom: 3rem;
            padding: 2rem;
            background: linear-gradient(135deg, #1a1a2e, #16213e);
            border-radius: 16px;
            border: 1px solid #333;
        }}
        .header h1 {{
            font-size: 2.5rem;
            background: linear-gradient(90deg, #00d4ff, #7b2ff7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .header p {{ color: #888; margin-top: 0.5rem; }}
        .stats {{
            display: flex;
            justify-content: center;
            gap: 2rem;
            margin-top: 1.5rem;
        }}
        .stat {{
            background: #1a1a2e;
            padding: 1rem 2rem;
            border-radius: 12px;
            text-align: center;
        }}
        .stat-number {{ font-size: 2rem; color: #00d4ff; font-weight: bold; }}
        .stat-label {{ font-size: 0.8rem; color: #666; }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 1.5rem;
            max-width: 1200px;
            margin: 0 auto;
        }}
        .card {{
            background: #12121a;
            border: 1px solid #222;
            border-radius: 12px;
            padding: 1.5rem;
            transition: transform 0.2s, border-color 0.2s;
        }}
        .card:hover {{
            transform: translateY(-4px);
            border-color: #7b2ff7;
        }}
        .card h3 {{ color: #fff; margin-bottom: 0.5rem; }}
        .card p {{ color: #999; font-size: 0.9rem; line-height: 1.5; }}
        .card-category {{
            display: inline-block;
            background: #7b2ff730;
            color: #7b2ff7;
            padding: 2px 10px;
            border-radius: 20px;
            font-size: 0.75rem;
            margin-bottom: 0.8rem;
        }}
        .card-date {{ color: #555; font-size: 0.8rem; margin-top: 1rem; }}
        .footer {{
            text-align: center;
            margin-top: 3rem;
            color: #444;
            font-size: 0.8rem;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>BUILDING IA</h1>
        <p>Empire d'agents autonomes — Portfolio Live</p>
        <div class="stats">
            <div class="stat">
                <div class="stat-number">{len(projects)}</div>
                <div class="stat-label">PROJETS</div>
            </div>
            <div class="stat">
                <div class="stat-number">25</div>
                <div class="stat-label">AGENTS</div>
            </div>
            <div class="stat">
                <div class="stat-number">0€</div>
                <div class="stat-label">COÛT</div>
            </div>
        </div>
    </div>
    <div class="grid">
        {cards_html}
    </div>
    <div class="footer">
        Auto-généré par TITAN — Dernière MàJ : {datetime.now().strftime('%Y-%m-%d %H:%M')}
    </div>
</body>
</html>"""

        PORTFOLIO_HTML.parent.mkdir(parents=True, exist_ok=True)
        with open(PORTFOLIO_HTML, "w", encoding="utf-8") as f:
            f.write(html)

        data["last_generated"] = datetime.now().isoformat()
        self._save(data)

    def list_projects(self) -> str:
        """Liste les projets du portfolio."""
        data = self._load()
        projects = data.get("projects", [])
        if not projects:
            return "Portfolio vide. /portfolio add [nom] pour commencer."

        lines = [f"📁 PORTFOLIO LIVE ({len(projects)} projets)\n"]
        for p in projects:
            lines.append(f"• [{p['category']}] {p['name']} — {p['date_added']}")
        return "\n".join(lines)

    def handle_command(self, command: str) -> str:
        """Route les commandes portfolio."""
        cmd = command.strip()

        if cmd.lower() in ("/portfolio", "/folio"):
            return self.list_projects()
        elif cmd.lower().startswith("/portfolio add "):
            parts = cmd[15:].strip().split("|")
            name = parts[0].strip()
            desc = parts[1].strip() if len(parts) > 1 else ""
            cat = parts[2].strip() if len(parts) > 2 else "automation"
            return self.add_project(name, desc, cat)
        else:
            return (
                "📁 PORTFOLIO VIVANT\n\n"
                "/portfolio — Liste des projets\n"
                "/portfolio add [nom] — Ajouter un projet\n"
                "/portfolio add [nom]|[description]|[catégorie]\n\n"
                "Le HTML se met à jour automatiquement."
            )
