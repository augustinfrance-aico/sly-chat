"""
R&D Lab — DOCTORANT (Interface Unifiee)
Agregation des 4 agents R&D Lab. Test d'hypotheses. Smart search. Dashboard data.
Zero cout.
"""

import json
import logging
from datetime import datetime
from pathlib import Path

from ..config import MEMORY_DIR
from ..ai_client import chat as ai_chat

log = logging.getLogger("titan.rdlab.doctorant")

DASHBOARD_FILE = MEMORY_DIR / "rdlab_dashboard.json"
PAPERS_FILE = MEMORY_DIR / "rdlab_papers.json"
INNOVATIONS_FILE = MEMORY_DIR / "rdlab_innovations.json"
EXPERIMENTS_FILE = MEMORY_DIR / "rdlab_experiments.json"
HORIZON_FILE = MEMORY_DIR / "rdlab_horizon.json"


class TitanRDLabDoctorant:
    """DOCTORANT — L'Interface Unifiee. Synthese R&D, hypotheses, dashboard."""

    def __init__(self):
        self.data = self._load()

    # === PERSISTENCE ===

    def _load(self) -> dict:
        if DASHBOARD_FILE.exists():
            try:
                with open(DASHBOARD_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                pass
        return {"last_update": None, "searches": [], "hypotheses": []}

    def _save(self):
        with open(DASHBOARD_FILE, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def _read_json(self, filepath: Path) -> dict:
        if filepath.exists():
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                pass
        return {}

    # === AGGREGATION ===

    def get_full_dashboard_data(self) -> dict:
        """Aggregate data from all 4 R&D agents for dashboard API."""
        papers_data = self._read_json(PAPERS_FILE)
        innovations_data = self._read_json(INNOVATIONS_FILE)
        experiments_data = self._read_json(EXPERIMENTS_FILE)
        horizon_data = self._read_json(HORIZON_FILE)

        return {
            "papers": papers_data.get("papers", [])[:20],
            "github_repos": papers_data.get("github_repos", [])[:10],
            "innovations": innovations_data.get("innovations", [])[:15],
            "patents": innovations_data.get("patents", [])[:10],
            "alerts": innovations_data.get("alerts", [])[:10],
            "experiments": experiments_data.get("experiments", [])[:20],
            "experiment_stats": experiments_data.get("stats", {}),
            "forecasts": horizon_data.get("forecasts", [])[-3:],
            "obsolescence": horizon_data.get("obsolescence_checks", [])[-1:],
            "stats": {
                "papers_count": len(papers_data.get("papers", [])),
                "innovations_count": len(innovations_data.get("innovations", [])),
                "experiments_count": len(experiments_data.get("experiments", [])),
                "forecasts_count": len(horizon_data.get("forecasts", [])),
                "alerts_active": len([
                    a for a in innovations_data.get("alerts", [])
                    if a.get("level") in ("HOT", "EXPLOSIVE")
                ]),
                "last_papers_fetch": papers_data.get("last_fetch"),
                "last_innovations_fetch": innovations_data.get("last_fetch"),
                "last_forecast": horizon_data.get("last_forecast"),
            },
        }

    # === HYPOTHESIS TESTING ===

    async def hypothesis_test(self, question: str) -> str:
        """User poses a question, agent proposes a test/simulation."""
        # Gather recent context
        papers_data = self._read_json(PAPERS_FILE)
        recent_papers = "\n".join(
            f"- {p['title'][:60]} (score: {p.get('score', '?')})"
            for p in papers_data.get("papers", [])[:5]
        ) or "Aucun paper en cache."

        prompt = f"""Question de l'utilisateur: {question}

Papers recents disponibles:
{recent_papers}

Propose:
1. HYPOTHESE TESTABLE (1 phrase precise)
2. EXPERIENCE CONCRETE (script Python outline, 3-5 etapes)
3. RESULTAT ATTENDU (qu'est-ce que ca prouverait)
4. EFFORT ESTIME (minutes/heures)
5. PAPER LIE (lequel de la liste, si pertinent)

Format structure, actionnable, en francais."""

        result = ai_chat(
            "Tu es DOCTORANT, expert en design experimental IA. Structure, concis.",
            prompt,
            max_tokens=500,
        )

        # Log hypothesis
        self.data["hypotheses"].append({
            "question": question,
            "result": result[:500],
            "date": datetime.now().isoformat(),
        })
        if len(self.data["hypotheses"]) > 20:
            self.data["hypotheses"] = self.data["hypotheses"][-20:]
        self._save()

        return f"🎓 TEST D'HYPOTHESE\n❓ {question}\n\n{result}"

    # === SMART SEARCH ===

    def smart_search(self, query: str) -> str:
        """Search across all R&D Lab data sources."""
        query_lower = query.lower()
        results = {"papers": [], "innovations": [], "experiments": []}

        # Search papers
        papers_data = self._read_json(PAPERS_FILE)
        for p in papers_data.get("papers", []):
            if query_lower in p.get("title", "").lower() or query_lower in p.get("abstract", "").lower():
                results["papers"].append(p)

        # Search innovations
        innovations_data = self._read_json(INNOVATIONS_FILE)
        for i in innovations_data.get("innovations", []):
            text = f"{i.get('name', '')} {i.get('description', '')} {i.get('title', '')}".lower()
            if query_lower in text:
                results["innovations"].append(i)

        # Search experiments
        experiments_data = self._read_json(EXPERIMENTS_FILE)
        for e in experiments_data.get("experiments", []):
            if query_lower in e.get("title", "").lower() or query_lower in e.get("spec", "").lower():
                results["experiments"].append(e)

        total = sum(len(v) for v in results.values())
        if total == 0:
            return f"🔍 Aucun resultat pour '{query}' dans le R&D Lab."

        output = f"🔍 RECHERCHE R&D LAB — '{query}' ({total} resultats)\n\n"

        if results["papers"]:
            output += f"📚 PAPERS ({len(results['papers'])})\n"
            for p in results["papers"][:3]:
                output += f"  [{p.get('score', '?')}/10] {p['title'][:60]}\n"
            output += "\n"

        if results["innovations"]:
            output += f"🔭 INNOVATIONS ({len(results['innovations'])})\n"
            for i in results["innovations"][:3]:
                output += f"  {i.get('name', i.get('title', ''))} (⭐{i.get('stars', i.get('score', 0))})\n"
            output += "\n"

        if results["experiments"]:
            output += f"🧪 EXPERIMENTS ({len(results['experiments'])})\n"
            for e in results["experiments"][:3]:
                output += f"  [{e.get('status', '?')}] {e['title'][:60]}\n"

        return output

    # === WEEKLY SUMMARY ===

    def get_weekly_summary(self) -> str:
        """Cross-agent weekly summary for the brief."""
        data = self.get_full_dashboard_data()
        stats = data["stats"]

        summary = (
            f"🎓 R&D LAB — RESUME HEBDO\n\n"
            f"📚 Papers scannés : {stats['papers_count']}\n"
            f"🔭 Innovations detectées : {stats['innovations_count']}\n"
            f"🧪 Experiences : {stats['experiments_count']}\n"
            f"🔮 Forecasts : {stats['forecasts_count']}\n"
            f"🚨 Alertes actives : {stats['alerts_active']}\n"
        )

        # Add latest alerts
        if data["alerts"]:
            summary += "\n🚨 ALERTES:\n"
            for a in data["alerts"][:3]:
                summary += f"  [{a['level']}] {a['name']}\n"

        # Add latest forecast snippet
        if data["forecasts"]:
            latest = data["forecasts"][-1]
            summary += f"\n🔮 DERNIER FORECAST ({latest['date'][:10]}):\n"
            summary += f"  {latest['forecast'][:200]}...\n"

        return summary

    # === DASHBOARD SUMMARY (for /rdlab command) ===

    def get_dashboard_summary(self) -> str:
        """Quick dashboard summary for Telegram."""
        data = self.get_full_dashboard_data()
        stats = data["stats"]

        output = (
            f"🎓 R&D LAB — DASHBOARD\n"
            f"{'=' * 30}\n\n"
            f"📚 Papers : {stats['papers_count']} (last: {(stats.get('last_papers_fetch') or 'jamais')[:10]})\n"
            f"🔭 Innovations : {stats['innovations_count']} (last: {(stats.get('last_innovations_fetch') or 'jamais')[:10]})\n"
            f"🧪 Experiments : {stats['experiments_count']}\n"
            f"🔮 Forecasts : {stats['forecasts_count']} (last: {(stats.get('last_forecast') or 'jamais')[:10]})\n"
            f"🚨 Alertes : {stats['alerts_active']}\n"
        )

        # Top 3 papers
        if data["papers"]:
            output += "\n📚 TOP PAPERS:\n"
            for p in data["papers"][:3]:
                output += f"  [{p.get('score', '?')}/10] {p['title'][:50]}\n"

        # Active alerts
        if data["alerts"]:
            output += "\n🚨 ALERTES:\n"
            for a in data["alerts"][:3]:
                output += f"  [{a['level']}] {a['name']}\n"

        output += "\n📌 Commandes: /rdlab papers | scout | experiment | horizon | hypothesis"
        return output

    # === COMMAND HANDLER ===

    def handle_command(self, text: str) -> str:
        """Handle all /rdlab commands — routes to sub-modules."""
        parts = text.strip().split(maxsplit=3)

        # Sub-routing to other R&D modules
        if len(parts) >= 2:
            sub = parts[1] if len(parts) > 1 else ""

            if sub == "papers":
                from .rdlab_digestor import TitanRDLabDigestor
                digestor = TitanRDLabDigestor()
                return digestor.handle_command(text)

            if sub == "scout":
                from .rdlab_scout import TitanRDLabScout
                scout = TitanRDLabScout()
                return scout.handle_command(text)

            if sub == "experiment":
                from .rdlab_experiment import TitanRDLabExperiment
                experiment = TitanRDLabExperiment()
                return experiment.handle_command(text)

            if sub == "horizon":
                from .rdlab_horizon import TitanRDLabHorizon
                horizon = TitanRDLabHorizon()
                return horizon.handle_command(text)

            if sub == "hypothesis" and len(parts) >= 3:
                question = " ".join(parts[2:])
                import asyncio
                return asyncio.get_event_loop().run_until_complete(self.hypothesis_test(question))

            if sub == "search" and len(parts) >= 3:
                query = " ".join(parts[2:])
                return self.smart_search(query)

            if sub == "weekly":
                return self.get_weekly_summary()

            if sub == "dashboard":
                return self.get_dashboard_summary()

        # Default: dashboard summary
        return self.get_dashboard_summary()
