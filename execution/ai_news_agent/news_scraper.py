"""
AI News Scraper - Collecte les dernieres actualites IA depuis plusieurs sources.
Filtre et priorise les news pertinentes pour un office notarial.
"""

import requests
import feedparser
import json
import os
import re
from datetime import datetime, timedelta
from typing import List, Dict, Any


# Sources RSS et web pour l'actualite IA
RSS_FEEDS = [
    {
        "name": "TechCrunch AI",
        "url": "https://techcrunch.com/category/artificial-intelligence/feed/",
        "lang": "en",
        "priority": 1
    },
    {
        "name": "The Verge AI",
        "url": "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
        "lang": "en",
        "priority": 1
    },
    {
        "name": "MIT Technology Review",
        "url": "https://www.technologyreview.com/feed/",
        "lang": "en",
        "priority": 2
    },
    {
        "name": "VentureBeat AI",
        "url": "https://venturebeat.com/category/ai/feed/",
        "lang": "en",
        "priority": 1
    },
    {
        "name": "Google AI Blog",
        "url": "https://blog.google/technology/ai/rss/",
        "lang": "en",
        "priority": 2
    },
    {
        "name": "OpenAI Blog",
        "url": "https://openai.com/blog/rss.xml",
        "lang": "en",
        "priority": 1
    },
    {
        "name": "Siecledigital IA",
        "url": "https://siecledigital.fr/tag/intelligence-artificielle/feed/",
        "lang": "fr",
        "priority": 1
    },
    {
        "name": "Usine Digitale IA",
        "url": "https://www.usine-digitale.fr/intelligence-artificielle/rss",
        "lang": "fr",
        "priority": 2
    },
]

# Mots-cles pour filtrer les articles pertinents pour un notaire
NOTAIRE_KEYWORDS = [
    # Juridique / Legal
    "legal", "law", "juridique", "justice", "regulation", "reglement",
    "compliance", "conformite", "RGPD", "GDPR", "privacy", "vie privee",
    "contract", "contrat", "signature", "authentification", "identite",
    "notaire", "notary", "immobilier", "real estate", "property",
    "document", "acte", "blockchain", "smart contract",
    # Business / Productivite
    "automation", "automatisation", "productivity", "productivite",
    "workflow", "enterprise", "business", "office", "bureau",
    "copilot", "assistant", "agent", "chatbot",
    # Technologie cle
    "GPT", "Claude", "Gemini", "LLM", "ChatGPT", "OpenAI", "Anthropic",
    "Google", "Microsoft", "Apple", "Meta",
    # Impact societal
    "emploi", "job", "travail", "ethique", "ethic", "security", "securite",
    "deepfake", "fraud", "fraude", "biometric", "biometrique",
]

# Mots-cles qui augmentent la pertinence notariale
NOTAIRE_BOOST_KEYWORDS = [
    "notaire", "notary", "legal", "juridique", "immobilier", "real estate",
    "contrat", "contract", "signature", "document", "acte",
    "regulation", "RGPD", "GDPR", "authentification", "blockchain",
    "fraud", "fraude", "identity", "identite",
]


def fetch_rss_articles(max_age_days: int = 7) -> List[Dict[str, Any]]:
    """Recupere les articles des flux RSS."""
    articles = []
    cutoff_date = datetime.now() - timedelta(days=max_age_days)

    for feed_info in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_info["url"])

            for entry in feed.entries[:15]:
                # Date de publication
                pub_date = None
                if hasattr(entry, "published_parsed") and entry.published_parsed:
                    pub_date = datetime(*entry.published_parsed[:6])
                elif hasattr(entry, "updated_parsed") and entry.updated_parsed:
                    pub_date = datetime(*entry.updated_parsed[:6])

                if pub_date and pub_date < cutoff_date:
                    continue

                title = entry.get("title", "Sans titre")
                summary = entry.get("summary", entry.get("description", ""))
                # Nettoyer le HTML du summary
                summary = re.sub(r"<[^>]+>", "", summary).strip()[:500]
                link = entry.get("link", "")

                articles.append({
                    "title": title,
                    "summary": summary,
                    "link": link,
                    "source": feed_info["name"],
                    "lang": feed_info["lang"],
                    "priority": feed_info["priority"],
                    "date": pub_date.isoformat() if pub_date else datetime.now().isoformat(),
                })

        except Exception as e:
            print(f"[WARN] Erreur flux {feed_info['name']}: {e}")

    return articles


def score_article(article: Dict[str, Any]) -> float:
    """Donne un score de pertinence a un article pour un notaire."""
    text = f"{article['title']} {article['summary']}".lower()
    score = 0.0

    # Score de base selon la priorite de la source
    score += (3 - article.get("priority", 2)) * 2

    # Keywords generaux IA
    for kw in NOTAIRE_KEYWORDS:
        if kw.lower() in text:
            score += 1.0

    # Keywords boost notariale (valent plus)
    for kw in NOTAIRE_BOOST_KEYWORDS:
        if kw.lower() in text:
            score += 3.0

    # Bonus pour les articles en francais (plus accessibles)
    if article.get("lang") == "fr":
        score += 2.0

    # Bonus pour articles recents
    try:
        pub = datetime.fromisoformat(article["date"])
        age_hours = (datetime.now() - pub).total_seconds() / 3600
        if age_hours < 24:
            score += 5.0
        elif age_hours < 48:
            score += 3.0
        elif age_hours < 72:
            score += 1.0
    except (ValueError, TypeError):
        pass

    return score


def filter_and_rank_articles(articles: List[Dict], top_n: int = 10) -> List[Dict]:
    """Filtre et classe les articles par pertinence."""
    for article in articles:
        article["score"] = score_article(article)

    # Trier par score descendant
    ranked = sorted(articles, key=lambda x: x["score"], reverse=True)

    # Garder les top articles avec un score minimum
    filtered = [a for a in ranked if a["score"] >= 3.0]

    # Deduplicate par titre similaire
    seen_titles = set()
    unique = []
    for article in filtered:
        title_key = re.sub(r"[^a-z0-9]", "", article["title"].lower())[:50]
        if title_key not in seen_titles:
            seen_titles.add(title_key)
            unique.append(article)

    return unique[:top_n]


def fetch_news(max_age_days: int = 7, top_n: int = 10) -> List[Dict]:
    """Pipeline complet: recupere, filtre, et classe les news IA."""
    print("[1/3] Collecte des articles depuis les flux RSS...")
    articles = fetch_rss_articles(max_age_days)
    print(f"       {len(articles)} articles trouves")

    print("[2/3] Scoring et filtrage pour pertinence notariale...")
    ranked = filter_and_rank_articles(articles, top_n)
    print(f"       {len(ranked)} articles pertinents selectionnes")

    print("[3/3] Preparation des donnees...")
    return ranked


def save_news_cache(articles: List[Dict], cache_dir: str = None):
    """Sauvegarde les articles dans un cache JSON."""
    if cache_dir is None:
        cache_dir = os.path.dirname(os.path.abspath(__file__))

    cache_path = os.path.join(cache_dir, "news_cache.json")
    data = {
        "fetched_at": datetime.now().isoformat(),
        "count": len(articles),
        "articles": articles
    }

    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"[OK] Cache sauvegarde: {cache_path}")
    return cache_path


def load_news_cache(cache_dir: str = None) -> List[Dict]:
    """Charge les articles depuis le cache."""
    if cache_dir is None:
        cache_dir = os.path.dirname(os.path.abspath(__file__))

    cache_path = os.path.join(cache_dir, "news_cache.json")

    if not os.path.exists(cache_path):
        return []

    with open(cache_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data.get("articles", [])


if __name__ == "__main__":
    articles = fetch_news(max_age_days=7, top_n=10)

    for i, art in enumerate(articles, 1):
        print(f"\n--- [{i}] {art['source']} (score: {art['score']:.1f}) ---")
        print(f"  {art['title']}")
        print(f"  {art['summary'][:150]}...")
        print(f"  {art['link']}")

    save_news_cache(articles)
