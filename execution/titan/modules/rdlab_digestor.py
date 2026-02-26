"""
R&D Lab — ARXIV (Research Digestor 2.0)
Veille recherche IA automatisee : arXiv, Semantic Scholar, GitHub trending, HuggingFace.
Scoring impact, digest quotidien/hebdo, extraction methodes.
Zero cout — APIs gratuites uniquement.
"""

import hashlib
import json
import logging
import re
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
from xml.etree import ElementTree

import feedparser
import requests

from ..config import (
    MEMORY_DIR,
    RDLAB_ARXIV_CATEGORIES,
    RDLAB_GITHUB_TOPICS,
    RDLAB_RELEVANCE_KEYWORDS,
    RDLAB_RSS_FEEDS,
)
from ..ai_client import chat as ai_chat

log = logging.getLogger("titan.rdlab.digestor")

PAPERS_FILE = MEMORY_DIR / "rdlab_papers.json"
ARXIV_API = "https://export.arxiv.org/api/query"
SEMANTIC_SCHOLAR_API = "https://api.semanticscholar.org/graph/v1/paper/search"
GITHUB_SEARCH_API = "https://api.github.com/search/repositories"
HUGGINGFACE_PAPERS_API = "https://huggingface.co/api/daily_papers"

HEADERS = {"User-Agent": "TITAN-RDLab/1.0 (research-bot)"}


class TitanRDLabDigestor:
    """ARXIV — Le Bibliothecaire. Veille recherche IA, scoring, digests."""

    def __init__(self):
        self.data = self._load()

    # === PERSISTENCE ===

    def _load(self) -> dict:
        if PAPERS_FILE.exists():
            try:
                with open(PAPERS_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                pass
        return {
            "papers": [],
            "github_repos": [],
            "last_fetch": None,
            "weekly_history": [],
        }

    def _save(self):
        with open(PAPERS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def _paper_id(self, title: str) -> str:
        return hashlib.md5(title.strip().lower().encode()).hexdigest()[:12]

    # === FETCHERS ===

    def _fetch_arxiv(self, max_results: int = 20) -> list:
        """Fetch latest papers from arXiv API."""
        papers = []
        seen = set()
        for cat in RDLAB_ARXIV_CATEGORIES:
            try:
                params = {
                    "search_query": f"cat:{cat}",
                    "sortBy": "submittedDate",
                    "sortOrder": "descending",
                    "max_results": max_results // len(RDLAB_ARXIV_CATEGORIES) + 1,
                }
                resp = requests.get(ARXIV_API, params=params, headers=HEADERS, timeout=15)
                if resp.status_code != 200:
                    continue

                root = ElementTree.fromstring(resp.content)
                ns = {"atom": "http://www.w3.org/2005/Atom"}

                for entry in root.findall("atom:entry", ns):
                    title = entry.find("atom:title", ns)
                    if title is None:
                        continue
                    title_text = re.sub(r"\s+", " ", title.text.strip())
                    pid = self._paper_id(title_text)
                    if pid in seen:
                        continue
                    seen.add(pid)

                    abstract_el = entry.find("atom:summary", ns)
                    abstract = abstract_el.text.strip()[:500] if abstract_el is not None else ""
                    link_el = entry.find("atom:id", ns)
                    link = link_el.text.strip() if link_el is not None else ""
                    published_el = entry.find("atom:published", ns)
                    published = published_el.text[:10] if published_el is not None else ""

                    authors = []
                    for author in entry.findall("atom:author", ns):
                        name_el = author.find("atom:name", ns)
                        if name_el is not None:
                            authors.append(name_el.text.strip())

                    papers.append({
                        "id": pid,
                        "title": title_text,
                        "abstract": abstract,
                        "authors": authors[:5],
                        "url": link,
                        "published": published,
                        "category": cat,
                        "source": "arxiv",
                    })

                time.sleep(3)  # arXiv rate limit: 1 req / 3 sec
            except Exception as e:
                log.warning(f"arXiv fetch {cat} error: {e}")
                continue
        return papers

    def _fetch_semantic_scholar(self, query: str = "large language model", limit: int = 10) -> list:
        """Fetch high-impact papers from Semantic Scholar."""
        papers = []
        try:
            params = {
                "query": query,
                "limit": limit,
                "fields": "title,abstract,citationCount,year,url,publicationDate",
                "year": f"{datetime.now().year}",
            }
            resp = requests.get(SEMANTIC_SCHOLAR_API, params=params, headers=HEADERS, timeout=15)
            if resp.status_code != 200:
                return papers

            data = resp.json()
            for item in data.get("data", []):
                title = item.get("title", "")
                if not title:
                    continue
                pid = self._paper_id(title)
                papers.append({
                    "id": pid,
                    "title": title,
                    "abstract": (item.get("abstract") or "")[:500],
                    "authors": [],
                    "url": item.get("url", ""),
                    "published": item.get("publicationDate", ""),
                    "category": "semantic_scholar",
                    "source": "semantic_scholar",
                    "citations": item.get("citationCount", 0),
                })
        except Exception as e:
            log.warning(f"Semantic Scholar error: {e}")
        return papers

    def _fetch_github_trending(self, max_results: int = 10) -> list:
        """Fetch trending AI/ML repos from GitHub."""
        repos = []
        week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        for topic in RDLAB_GITHUB_TOPICS[:3]:  # Limit to 3 topics to save API calls
            try:
                params = {
                    "q": f"topic:{topic} created:>{week_ago}",
                    "sort": "stars",
                    "order": "desc",
                    "per_page": max_results // 3 + 1,
                }
                resp = requests.get(GITHUB_SEARCH_API, params=params, headers=HEADERS, timeout=15)
                if resp.status_code != 200:
                    continue

                data = resp.json()
                for item in data.get("items", []):
                    repos.append({
                        "name": item.get("full_name", ""),
                        "description": (item.get("description") or "")[:200],
                        "stars": item.get("stargazers_count", 0),
                        "url": item.get("html_url", ""),
                        "language": item.get("language", ""),
                        "created": item.get("created_at", "")[:10],
                        "topic": topic,
                    })
            except Exception as e:
                log.warning(f"GitHub trending error: {e}")
                continue
        # Dedup by name + sort by stars
        seen = set()
        unique = []
        for r in sorted(repos, key=lambda x: x["stars"], reverse=True):
            if r["name"] not in seen:
                seen.add(r["name"])
                unique.append(r)
        return unique[:max_results]

    def _fetch_huggingface_papers(self, limit: int = 10) -> list:
        """Fetch daily papers from HuggingFace."""
        papers = []
        try:
            resp = requests.get(HUGGINGFACE_PAPERS_API, headers=HEADERS, timeout=15)
            if resp.status_code != 200:
                return papers

            data = resp.json()
            for item in data[:limit]:
                paper = item.get("paper", {})
                title = paper.get("title", "")
                if not title:
                    continue
                pid = self._paper_id(title)
                papers.append({
                    "id": pid,
                    "title": title,
                    "abstract": (paper.get("summary") or "")[:500],
                    "authors": [a.get("name", "") for a in paper.get("authors", [])[:5]],
                    "url": f"https://huggingface.co/papers/{paper.get('id', '')}",
                    "published": paper.get("publishedAt", "")[:10],
                    "category": "huggingface",
                    "source": "huggingface",
                    "upvotes": item.get("numUpvotes", 0),
                })
        except Exception as e:
            log.warning(f"HuggingFace papers error: {e}")
        return papers

    def _fetch_rss_feeds(self, max_per_feed: int = 5) -> list:
        """Fetch from AI blog RSS feeds."""
        papers = []
        seen = set()
        for feed_url in RDLAB_RSS_FEEDS:
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries[:max_per_feed]:
                    title = entry.get("title", "")
                    pid = self._paper_id(title)
                    if pid in seen:
                        continue
                    seen.add(pid)
                    summary = entry.get("summary", entry.get("description", ""))
                    summary = re.sub(r"<[^>]+>", " ", summary)[:300]
                    papers.append({
                        "id": pid,
                        "title": title,
                        "abstract": summary,
                        "authors": [],
                        "url": entry.get("link", ""),
                        "published": entry.get("published", ""),
                        "category": "rss",
                        "source": feed.feed.get("title", feed_url),
                    })
            except Exception:
                continue
        return papers

    # === SCORING ===

    def _impact_score(self, paper: dict) -> float:
        """Score a paper 1-10 based on relevance to AICO stack."""
        score = 5.0
        text = f"{paper.get('title', '')} {paper.get('abstract', '')}".lower()

        # Keyword relevance
        keyword_hits = sum(1 for kw in RDLAB_RELEVANCE_KEYWORDS if kw in text)
        score += min(keyword_hits * 0.5, 2.5)

        # Citation boost (Semantic Scholar)
        citations = paper.get("citations", 0)
        if citations > 100:
            score += 1.5
        elif citations > 50:
            score += 1.0
        elif citations > 10:
            score += 0.5

        # HuggingFace upvotes boost
        upvotes = paper.get("upvotes", 0)
        if upvotes > 50:
            score += 1.0
        elif upvotes > 20:
            score += 0.5

        # Recency boost
        pub_date = paper.get("published", "")
        if pub_date:
            try:
                pub = datetime.fromisoformat(pub_date.replace("Z", "+00:00"))
                days_old = (datetime.now(pub.tzinfo) - pub).days if pub.tzinfo else 0
                if days_old < 3:
                    score += 0.5
            except (ValueError, TypeError):
                pass

        return min(round(score, 1), 10.0)

    # === FETCH ALL ===

    async def fetch_all(self) -> dict:
        """Fetch from all sources and update cache."""
        papers = []
        papers.extend(self._fetch_arxiv(max_results=15))
        papers.extend(self._fetch_semantic_scholar(limit=10))
        papers.extend(self._fetch_huggingface_papers(limit=10))
        papers.extend(self._fetch_rss_feeds(max_per_feed=3))

        # Dedup by ID
        seen = set()
        unique_papers = []
        for p in papers:
            if p["id"] not in seen:
                seen.add(p["id"])
                p["score"] = self._impact_score(p)
                unique_papers.append(p)

        # Sort by score
        unique_papers.sort(key=lambda x: x["score"], reverse=True)

        # GitHub trending
        github_repos = self._fetch_github_trending(max_results=10)

        # Update data
        self.data["papers"] = unique_papers[:50]  # Keep top 50
        self.data["github_repos"] = github_repos[:10]
        self.data["last_fetch"] = datetime.now().isoformat()
        self._save()

        return {"papers": len(unique_papers), "repos": len(github_repos)}

    # === DIGESTS ===

    async def generate_daily_digest(self) -> str:
        """Generate daily R&D digest — top 5 papers + 3 trending repos."""
        stats = await self.fetch_all()

        top_papers = self.data["papers"][:5]
        top_repos = self.data["github_repos"][:3]

        if not top_papers and not top_repos:
            return "📚 R&D DIGEST — Aucune donnee disponible aujourd'hui."

        # Build context for LLM summary
        papers_text = "\n".join(
            f"- [{p['score']}/10] {p['title']} ({p['source']})\n  {p['abstract'][:150]}"
            for p in top_papers
        )
        repos_text = "\n".join(
            f"- ⭐{r['stars']} {r['name']} — {r['description'][:100]}"
            for r in top_repos
        )

        prompt = f"""Voici les top papers et repos IA du jour.
Pour chaque paper : 1 phrase ce que ca fait, 1 phrase comment Augus peut l'utiliser MAINTENANT.
Pour les repos : 1 phrase par repo.
Reponse en francais, ultra-concis.

PAPERS:
{papers_text}

GITHUB TRENDING:
{repos_text}"""

        summary = ai_chat(
            "Tu es ARXIV, agent de veille recherche IA. Ultra-concis, actionnable.",
            prompt,
            max_tokens=500,
        )

        header = (
            f"📚 R&D LAB — DIGEST QUOTIDIEN\n"
            f"📅 {datetime.now().strftime('%d/%m/%Y')}\n"
            f"{'=' * 30}\n"
        )

        return f"{header}\n{summary}\n\n📊 {stats['papers']} papers scannés | {stats['repos']} repos trending"

    async def generate_weekly_report(self) -> str:
        """Generate weekly R&D report — deeper analysis."""
        if not self.data["papers"]:
            await self.fetch_all()

        top_papers = self.data["papers"][:10]
        top_repos = self.data["github_repos"][:5]

        papers_text = "\n".join(
            f"- [{p['score']}/10] {p['title']} ({p['category']})\n  {p['abstract'][:200]}"
            for p in top_papers
        )
        repos_text = "\n".join(
            f"- ⭐{r['stars']} {r['name']} — {r['description'][:150]}"
            for r in top_repos
        )

        prompt = f"""Rapport hebdomadaire R&D IA.
1. Top 3 tendances de la semaine (1 phrase chacune)
2. Paper le plus impactant pour AICO (agents autonomes, zero-cost)
3. Repo le plus utile a integrer
4. Methode/architecture a surveiller
Reponse en francais, structuree, 300 mots max.

PAPERS:
{papers_text}

GITHUB:
{repos_text}"""

        summary = ai_chat(
            "Tu es ARXIV, expert veille recherche IA. Rapport structure, actionnable.",
            prompt,
            max_tokens=800,
        )

        # Save to weekly history
        self.data["weekly_history"] = self.data.get("weekly_history", [])
        self.data["weekly_history"].append({
            "date": datetime.now().isoformat(),
            "papers_count": len(top_papers),
            "repos_count": len(top_repos),
        })
        if len(self.data["weekly_history"]) > 12:
            self.data["weekly_history"] = self.data["weekly_history"][-12:]
        self._save()

        header = (
            f"📚 R&D LAB — RAPPORT HEBDOMADAIRE\n"
            f"📅 Semaine du {datetime.now().strftime('%d/%m/%Y')}\n"
            f"{'=' * 35}\n"
        )

        return f"{header}\n{summary}"

    def search_papers(self, query: str) -> str:
        """Search cached papers by keyword."""
        query_lower = query.lower()
        results = [
            p for p in self.data.get("papers", [])
            if query_lower in p.get("title", "").lower()
            or query_lower in p.get("abstract", "").lower()
        ]
        if not results:
            return f"🔍 Aucun paper trouve pour '{query}'. Lance /rdlab papers pour rafraichir."

        output = f"🔍 {len(results)} paper(s) pour '{query}':\n\n"
        for p in results[:5]:
            output += f"[{p['score']}/10] {p['title']}\n{p['url']}\n\n"
        return output

    # === COMMAND HANDLER ===

    def handle_command(self, text: str) -> str:
        """Handle /rdlab papers commands."""
        parts = text.strip().split(maxsplit=3)

        if len(parts) >= 3 and parts[2] == "weekly":
            import asyncio
            return asyncio.get_event_loop().run_until_complete(self.generate_weekly_report())

        if len(parts) >= 4 and parts[2] == "search":
            query = parts[3]
            return self.search_papers(query)

        # Default: daily digest (sync wrapper)
        import asyncio
        return asyncio.get_event_loop().run_until_complete(self.generate_daily_digest())
