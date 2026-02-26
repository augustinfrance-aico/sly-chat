"""
R&D Lab — HORIZON (Strategic Predictive Vision)
Vision 3-5 ans ecosysteme IA. Projections, detection obsolescence, scenarios futurs.
Zero cout.
"""

import json
import logging
from datetime import datetime
from pathlib import Path

from ..config import MEMORY_DIR
from ..ai_client import chat as ai_chat

log = logging.getLogger("titan.rdlab.horizon")

HORIZON_FILE = MEMORY_DIR / "rdlab_horizon.json"
PAPERS_FILE = MEMORY_DIR / "rdlab_papers.json"
INNOVATIONS_FILE = MEMORY_DIR / "rdlab_innovations.json"

# AICO stack for obsolescence check
AICO_STACK_COMPONENTS = [
    ("Groq free tier (Llama 3.3-70B)", "LLM inference gratuite"),
    ("Gemini 2.0 Flash", "LLM fallback gratuit"),
    ("Ollama local", "LLM local zero-cost"),
    ("feedparser + requests", "Data fetching"),
    ("n8n self-hosted", "Workflow automation"),
    ("JSON file storage", "Persistence layer"),
    ("Telegram Bot API (polling)", "Interface utilisateur"),
    ("Railway / Render free tier", "Hosting"),
    ("Python 3.14 async", "Runtime"),
    ("Claude Code CLI", "Dev environment"),
]


class TitanRDLabHorizon:
    """HORIZON — Le Stratege Temporel. Vision 3-5 ans, obsolescence, scenarios."""

    def __init__(self):
        self.data = self._load()

    # === PERSISTENCE ===

    def _load(self) -> dict:
        if HORIZON_FILE.exists():
            try:
                with open(HORIZON_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                pass
        return {"forecasts": [], "obsolescence_checks": [], "last_forecast": None}

    def _save(self):
        with open(HORIZON_FILE, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    # === SIGNAL AGGREGATION ===

    def _aggregate_signals(self) -> dict:
        """Collect signals from ARXIV and SCOUT data."""
        signals = {
            "research_trends": [],
            "innovation_signals": [],
            "patent_signals": [],
        }

        # Papers signals
        if PAPERS_FILE.exists():
            try:
                with open(PAPERS_FILE, "r", encoding="utf-8") as f:
                    papers_data = json.load(f)
                top_papers = papers_data.get("papers", [])[:10]
                # Extract categories and keywords
                categories = {}
                for p in top_papers:
                    cat = p.get("category", "unknown")
                    categories[cat] = categories.get(cat, 0) + 1
                signals["research_trends"] = [
                    {"category": k, "count": v, "top_paper": next(
                        (p["title"] for p in top_papers if p.get("category") == k), ""
                    )}
                    for k, v in sorted(categories.items(), key=lambda x: -x[1])
                ]
            except (json.JSONDecodeError, OSError):
                pass

        # Innovation signals
        if INNOVATIONS_FILE.exists():
            try:
                with open(INNOVATIONS_FILE, "r", encoding="utf-8") as f:
                    innov_data = json.load(f)
                innovations = innov_data.get("innovations", [])[:10]
                signals["innovation_signals"] = [
                    {
                        "name": i.get("name", i.get("title", "")),
                        "alert_level": i.get("alert_level", "WATCH"),
                        "stars": i.get("stars", i.get("score", 0)),
                    }
                    for i in innovations
                ]
                signals["patent_signals"] = [
                    {"title": p.get("title", ""), "assignee": p.get("assignee", "")}
                    for p in innov_data.get("patents", [])[:5]
                ]
            except (json.JSONDecodeError, OSError):
                pass

        return signals

    # === FORECASTING ===

    async def generate_forecast(self) -> str:
        """Generate a 3-5 year horizon forecast."""
        signals = self._aggregate_signals()

        research_text = "\n".join(
            f"- {s['category']}: {s['count']} papers, top: {s['top_paper'][:60]}"
            for s in signals["research_trends"]
        ) or "Aucun signal recherche disponible."

        innovation_text = "\n".join(
            f"- [{s['alert_level']}] {s['name']} (⭐{s['stars']})"
            for s in signals["innovation_signals"]
        ) or "Aucun signal innovation disponible."

        patent_text = "\n".join(
            f"- {s['title'][:60]} ({s['assignee']})"
            for s in signals["patent_signals"]
        ) or "Aucun brevet recent."

        stack_text = "\n".join(f"- {name}: {desc}" for name, desc in AICO_STACK_COMPONENTS)

        prompt = f"""Signaux actuels de l'ecosysteme IA :

RECHERCHE (papers recents):
{research_text}

INNOVATIONS (startups/repos):
{innovation_text}

BREVETS:
{patent_text}

STACK AICO ACTUEL:
{stack_text}

Genere un FORECAST 3-5 ANS structure :
1. 3 SCENARIOS (optimiste / central / pessimiste) — 2 phrases chacun
2. TECHNOLOGIES QUI VONT DOMINER — top 3
3. TECHNOLOGIES MENACEES D'OBSOLESCENCE — top 3
4. POSITIONNEMENT RECOMMANDE pour AICO (empire d'agents autonomes, zero-cost)
5. ACTIONS CONCRETES (90 prochains jours) — 3 actions max

Reponse en francais, structure, 400 mots max."""

        forecast_text = ai_chat(
            "Tu es HORIZON, futurologue IA. Projections structures, actionnables.",
            prompt,
            max_tokens=800,
        )

        # Save forecast
        forecast_entry = {
            "date": datetime.now().isoformat(),
            "month": datetime.now().strftime("%Y-%m"),
            "signals_count": {
                "research": len(signals["research_trends"]),
                "innovations": len(signals["innovation_signals"]),
                "patents": len(signals["patent_signals"]),
            },
            "forecast": forecast_text,
        }
        self.data["forecasts"].append(forecast_entry)
        if len(self.data["forecasts"]) > 12:
            self.data["forecasts"] = self.data["forecasts"][-12:]
        self.data["last_forecast"] = datetime.now().isoformat()
        self._save()

        header = (
            f"🔮 R&D LAB — FORECAST HORIZON 3-5 ANS\n"
            f"📅 {datetime.now().strftime('%d/%m/%Y')}\n"
            f"{'=' * 40}\n"
        )

        return f"{header}\n{forecast_text}"

    # === OBSOLESCENCE CHECK ===

    async def obsolescence_check(self) -> str:
        """Check AICO stack against innovation signals for obsolescence risks."""
        signals = self._aggregate_signals()

        innovation_text = "\n".join(
            f"- {s['name']} ({s['alert_level']}, ⭐{s['stars']})"
            for s in signals["innovation_signals"]
        ) or "Aucune innovation recente."

        stack_text = "\n".join(f"- {name}: {desc}" for name, desc in AICO_STACK_COMPONENTS)

        prompt = f"""CHECK OBSOLESCENCE — Stack AICO vs innovations detectees.

STACK AICO:
{stack_text}

INNOVATIONS DETECTEES:
{innovation_text}

Pour chaque composant du stack AICO, evalue :
- 🟢 SAFE : aucun risque a 2 ans
- 🟡 WATCH : alternative emergente, surveiller
- 🔴 RISQUE : alternative superieure existe, migration a planifier

Format : une ligne par composant. Ultra-concis."""

        check = ai_chat(
            "Tu es HORIZON, expert detection obsolescence. Direct, factuel.",
            prompt,
            max_tokens=400,
        )

        # Save check
        self.data["obsolescence_checks"].append({
            "date": datetime.now().isoformat(),
            "result": check,
        })
        if len(self.data["obsolescence_checks"]) > 12:
            self.data["obsolescence_checks"] = self.data["obsolescence_checks"][-12:]
        self._save()

        header = "🔮 CHECK OBSOLESCENCE — Stack AICO\n\n"
        return f"{header}{check}"

    # === HISTORY ===

    def get_forecast_history(self, n: int = 4) -> str:
        """Show last N forecasts."""
        forecasts = self.data.get("forecasts", [])[-n:]
        if not forecasts:
            return "🔮 Aucun forecast en historique. Lance /rdlab horizon pour generer."

        output = f"🔮 HISTORIQUE FORECASTS ({len(forecasts)} derniers)\n\n"
        for f in forecasts:
            output += f"📅 {f['date'][:10]} — Signaux: {f['signals_count']}\n"
            output += f"{f['forecast'][:200]}...\n\n"
        return output

    # === COMMAND HANDLER ===

    def handle_command(self, text: str) -> str:
        """Handle /rdlab horizon commands."""
        parts = text.strip().split(maxsplit=3)

        if len(parts) >= 3 and parts[2] == "obsolete":
            import asyncio
            return asyncio.get_event_loop().run_until_complete(self.obsolescence_check())

        if len(parts) >= 3 and parts[2] == "history":
            return self.get_forecast_history()

        # Default: generate forecast
        import asyncio
        return asyncio.get_event_loop().run_until_complete(self.generate_forecast())
