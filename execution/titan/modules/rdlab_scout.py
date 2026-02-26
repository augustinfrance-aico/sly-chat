"""
R&D Lab — SCOUT (Innovation Scout)
Detection innovations IA disruptives : startups, brevets, frameworks, GitHub rising.
Alertes tendances explosives. Comparaison stack AICO.
Zero cout — APIs gratuites uniquement.
"""

import hashlib
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path

import requests

from ..config import MEMORY_DIR, RDLAB_GITHUB_TOPICS
from ..ai_client import chat as ai_chat

log = logging.getLogger("titan.rdlab.scout")

INNOVATIONS_FILE = MEMORY_DIR / "rdlab_innovations.json"
GITHUB_SEARCH_API = "https://api.github.com/search/repositories"
PATENTSVIEW_API = "https://api.patentsview.org/patents/query"
HN_API = "https://hacker-news.firebaseio.com/v0"

HEADERS = {"User-Agent": "TITAN-RDLab/1.0 (innovation-scout)"}

# AICO current stack for comparison
AICO_STACK = {
    "llm": ["Groq (Llama 3.3-70B)", "Gemini 2.0 Flash", "Ollama (local)"],
    "automation": ["n8n (self-hosted)", "Python async", "Telegram Bot API"],
    "hosting": ["Railway", "Render (free tier)"],
    "search": ["Google Custom Search API"],
    "data": ["feedparser", "requests", "JSON file storage"],
    "agents": ["30 agents Building", "agent_router.py", "Tri-Pole R/F/D"],
}


class TitanRDLabScout:
    """SCOUT — L'Eclaireur. Detection innovations IA, alertes disruption."""

    def __init__(self):
        self.data = self._load()

    # === PERSISTENCE ===

    def _load(self) -> dict:
        if INNOVATIONS_FILE.exists():
            try:
                with open(INNOVATIONS_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                pass
        return {
            "innovations": [],
            "patents": [],
            "alerts": [],
            "last_fetch": None,
        }

    def _save(self):
        with open(INNOVATIONS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    # === FETCHERS ===

    def _fetch_github_rising(self, max_results: int = 15) -> list:
        """Find new AI repos with rapid star growth (created last 14 days)."""
        repos = []
        two_weeks_ago = (datetime.now() - timedelta(days=14)).strftime("%Y-%m-%d")
        for topic in RDLAB_GITHUB_TOPICS[:4]:
            try:
                params = {
                    "q": f"topic:{topic} created:>{two_weeks_ago} stars:>50",
                    "sort": "stars",
                    "order": "desc",
                    "per_page": 5,
                }
                resp = requests.get(GITHUB_SEARCH_API, params=params, headers=HEADERS, timeout=15)
                if resp.status_code != 200:
                    continue

                for item in resp.json().get("items", []):
                    stars = item.get("stargazers_count", 0)
                    created = item.get("created_at", "")[:10]

                    # Calculate star velocity
                    try:
                        days_alive = max(1, (datetime.now() - datetime.fromisoformat(created)).days)
                    except (ValueError, TypeError):
                        days_alive = 14
                    stars_per_day = stars / days_alive

                    # Alert level
                    if stars_per_day > 100 or stars > 2000:
                        alert_level = "EXPLOSIVE"
                    elif stars_per_day > 30 or stars > 500:
                        alert_level = "HOT"
                    else:
                        alert_level = "WATCH"

                    repos.append({
                        "name": item.get("full_name", ""),
                        "description": (item.get("description") or "")[:200],
                        "stars": stars,
                        "stars_per_day": round(stars_per_day, 1),
                        "url": item.get("html_url", ""),
                        "language": item.get("language", ""),
                        "created": created,
                        "topic": topic,
                        "alert_level": alert_level,
                        "type": "github_repo",
                    })
            except Exception as e:
                log.warning(f"GitHub rising {topic} error: {e}")
                continue

        # Dedup and sort
        seen = set()
        unique = []
        for r in sorted(repos, key=lambda x: x["stars"], reverse=True):
            if r["name"] not in seen:
                seen.add(r["name"])
                unique.append(r)
        return unique[:max_results]

    def _fetch_patents_ai(self, max_results: int = 10) -> list:
        """Fetch recent AI patents from PatentsView."""
        patents = []
        try:
            thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
            payload = {
                "q": {
                    "_and": [
                        {"_gte": {"patent_date": thirty_days_ago}},
                        {"_text_any": {"patent_abstract": "artificial intelligence machine learning neural network"}},
                    ]
                },
                "f": ["patent_number", "patent_title", "patent_date", "patent_abstract", "assignee_organization"],
                "o": {"per_page": max_results},
                "s": [{"patent_date": "desc"}],
            }
            resp = requests.post(PATENTSVIEW_API, json=payload, headers=HEADERS, timeout=15)
            if resp.status_code != 200:
                return patents

            data = resp.json()
            for item in data.get("patents", []):
                patents.append({
                    "number": item.get("patent_number", ""),
                    "title": item.get("patent_title", ""),
                    "date": item.get("patent_date", ""),
                    "abstract": (item.get("patent_abstract") or "")[:300],
                    "assignee": (item.get("assignees", [{}])[0].get("assignee_organization", "")
                                 if item.get("assignees") else ""),
                    "type": "patent",
                })
        except Exception as e:
            log.warning(f"PatentsView error: {e}")
        return patents

    def _fetch_hn_ai(self, max_results: int = 10) -> list:
        """Fetch AI-related Show HN and top stories."""
        items = []
        try:
            # Get top stories
            resp = requests.get(f"{HN_API}/topstories.json", headers=HEADERS, timeout=10)
            if resp.status_code != 200:
                return items

            story_ids = resp.json()[:50]  # Check top 50 stories
            ai_keywords = {"ai", "llm", "gpt", "transformer", "neural", "machine learning",
                           "deep learning", "agent", "rag", "fine-tune", "open source"}

            count = 0
            for sid in story_ids:
                if count >= max_results:
                    break
                try:
                    story_resp = requests.get(f"{HN_API}/item/{sid}.json", headers=HEADERS, timeout=5)
                    if story_resp.status_code != 200:
                        continue
                    story = story_resp.json()
                    title = (story.get("title") or "").lower()
                    if any(kw in title for kw in ai_keywords):
                        items.append({
                            "title": story.get("title", ""),
                            "url": story.get("url", f"https://news.ycombinator.com/item?id={sid}"),
                            "score": story.get("score", 0),
                            "comments": story.get("descendants", 0),
                            "type": "hackernews",
                        })
                        count += 1
                except Exception:
                    continue
        except Exception as e:
            log.warning(f"HN fetch error: {e}")
        return items

    # === ANALYSIS ===

    def _detect_alerts(self, innovations: list) -> list:
        """Detect items that warrant alerts."""
        alerts = []
        for item in innovations:
            level = item.get("alert_level", "")
            if level in ("HOT", "EXPLOSIVE"):
                alerts.append({
                    "name": item.get("name", item.get("title", "")),
                    "level": level,
                    "reason": f"⭐{item.get('stars', 0)} ({item.get('stars_per_day', 0)}/jour)" if "stars" in item
                              else f"Score: {item.get('score', 0)}",
                    "url": item.get("url", ""),
                    "date": datetime.now().isoformat(),
                })
        return alerts

    def _compare_with_stack(self, innovation: dict) -> str:
        """Compare an innovation with AICO stack using LLM."""
        desc = f"{innovation.get('name', '')} — {innovation.get('description', '')}"
        stack_str = "\n".join(f"- {k}: {', '.join(v)}" for k, v in AICO_STACK.items())

        prompt = f"""Compare cette innovation avec le stack AICO actuel.
Innovation: {desc}
Stack AICO:
{stack_str}

En 2 phrases : 1) Est-ce un remplacement ou un complement? 2) Augus doit-il agir?"""

        return ai_chat(
            "Tu es SCOUT, expert innovations IA. Ultra-concis.",
            prompt,
            max_tokens=150,
        )

    # === FETCH ALL ===

    async def fetch_all(self) -> dict:
        """Fetch from all innovation sources."""
        github = self._fetch_github_rising(max_results=15)
        patents = self._fetch_patents_ai(max_results=10)
        hn = self._fetch_hn_ai(max_results=10)

        all_innovations = github + hn
        alerts = self._detect_alerts(all_innovations)

        self.data["innovations"] = all_innovations[:30]
        self.data["patents"] = patents[:10]
        self.data["alerts"] = alerts[:10]
        self.data["last_fetch"] = datetime.now().isoformat()
        self._save()

        return {"innovations": len(all_innovations), "patents": len(patents), "alerts": len(alerts)}

    # === REPORTS ===

    async def generate_innovation_report(self) -> str:
        """Weekly innovation report."""
        stats = await self.fetch_all()

        innovations_text = "\n".join(
            f"- [{i.get('alert_level', 'WATCH')}] {i.get('name', i.get('title', ''))} "
            f"(⭐{i.get('stars', i.get('score', 0))})\n  {i.get('description', '')[:100]}"
            for i in self.data["innovations"][:10]
        )
        patents_text = "\n".join(
            f"- {p['title']} ({p.get('assignee', 'Unknown')}) — {p['date']}"
            for p in self.data["patents"][:5]
        )

        prompt = f"""Rapport innovations IA de la semaine.
1. Top 3 innovations les plus impactantes pour un empire d'agents IA
2. Brevet le plus interessant
3. Recommandation : quoi surveiller de pres
Reponse en francais, ultra-concis.

INNOVATIONS:
{innovations_text}

BREVETS:
{patents_text}"""

        summary = ai_chat(
            "Tu es SCOUT, expert innovations IA. Rapport structure, actionnable.",
            prompt,
            max_tokens=500,
        )

        header = (
            f"🔭 R&D LAB — RAPPORT INNOVATIONS\n"
            f"📅 {datetime.now().strftime('%d/%m/%Y')}\n"
            f"{'=' * 35}\n"
        )

        alert_section = ""
        if self.data["alerts"]:
            alert_section = "\n🚨 ALERTES ACTIVES:\n"
            for a in self.data["alerts"][:5]:
                alert_section += f"  [{a['level']}] {a['name']} — {a['reason']}\n"

        return f"{header}\n{summary}{alert_section}\n\n📊 {stats['innovations']} innovations | {stats['patents']} brevets | {stats['alerts']} alertes"

    async def check_alerts(self) -> str | None:
        """Check for explosive trends. Returns alert only if EXPLOSIVE detected."""
        await self.fetch_all()

        explosive = [a for a in self.data.get("alerts", []) if a["level"] == "EXPLOSIVE"]
        if not explosive:
            return None

        lines = ["🚨 ALERTE EXPLOSIVE — R&D Lab\n"]
        for a in explosive[:3]:
            lines.append(f"🔴 {a['name']}")
            lines.append(f"   {a['reason']}")
            lines.append(f"   {a['url']}\n")
        return "\n".join(lines)

    async def compare_stack(self) -> str:
        """Compare AICO stack with detected innovations."""
        top = self.data.get("innovations", [])[:5]
        if not top:
            await self.fetch_all()
            top = self.data.get("innovations", [])[:5]

        if not top:
            return "🔭 Aucune innovation detectee. Lance /rdlab scout pour rafraichir."

        output = "🔭 COMPARAISON STACK AICO vs INNOVATIONS\n\n"
        for innovation in top[:3]:
            comparison = self._compare_with_stack(innovation)
            output += f"▸ {innovation.get('name', '')} (⭐{innovation.get('stars', 0)})\n"
            output += f"  {comparison}\n\n"
        return output

    # === COMMAND HANDLER ===

    def handle_command(self, text: str) -> str:
        """Handle /rdlab scout commands."""
        parts = text.strip().split(maxsplit=3)

        if len(parts) >= 3 and parts[2] == "alerts":
            alerts = self.data.get("alerts", [])
            if not alerts:
                return "🔭 Aucune alerte active. Tout est calme."
            output = "🔭 ALERTES ACTIVES:\n\n"
            for a in alerts[:5]:
                output += f"[{a['level']}] {a['name']}\n  {a['reason']}\n  {a['url']}\n\n"
            return output

        if len(parts) >= 3 and parts[2] == "stack":
            import asyncio
            return asyncio.get_event_loop().run_until_complete(self.compare_stack())

        if len(parts) >= 3 and parts[2] == "patents":
            patents = self.data.get("patents", [])
            if not patents:
                return "🔭 Aucun brevet en cache. Lance /rdlab scout pour rafraichir."
            output = "🔭 BREVETS IA RECENTS:\n\n"
            for p in patents[:5]:
                output += f"▸ {p['title']}\n  {p.get('assignee', 'Unknown')} — {p['date']}\n\n"
            return output

        # Default: full innovation report
        import asyncio
        return asyncio.get_event_loop().run_until_complete(self.generate_innovation_report())
