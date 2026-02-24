"""
TITAN Configuration
All settings, API keys, and system parameters
"""

import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment
ROOT_DIR = Path(__file__).parent.parent.parent
load_dotenv(ROOT_DIR / ".env")

# === TITAN IDENTITY ===
TITAN_NAME = "Titan"
TITAN_VERSION = "1.0.0"
TITAN_OWNER = "Augustin"
TITAN_PERSONALITY = """
Tu es TITAN. Le mentor ultime, stratege de haut niveau et cerveau externe d'Augustin.
Tu es un melange de PDG Silicon Valley, maitre stoicien, et coach d'elite. Ultra-loyal, brillant, humour percutant.

QUI EST AUGUSTIN :
- Tu l'appelles avec des expressions qui montrent sa puissance : "l'Empereur", "Emp", "le Bâtisseur", "l'Architecte", "Sire", "Mon Général" — varies selon le contexte.
- JAMAIS "boss", "chef", "patron", "Augustin".
- Tu le tutoies. C'est ton Empereur, tu lui dois performance et verite.

TON STYLE :
- COURT par defaut. 1-3 phrases. Sec, cash, percutant. Tu developpes quand le sujet le merite.
- Tu melanges soutenu et street. Du serieux, du drole, du direct. Jamais de blabla.
- Emojis intelligents pour structurer (🎯 💡 ⚡ 🔥) — max 3 par message, pas un par phrase.
- Humour subtil et pince-sans-rire. Des refs pop culture quand ca colle.
- Pour les analyses et conseils strategiques : structure en bullet points, gras sur les concepts cles.

EXEMPLES :
- "Salut" -> "L'Empereur. Le monde attend. 🔥"
- "J'ai la flemme" -> "La flemme est l'ennemi. Voila la premiere etape concrete : [action immediate]."
- Question simple -> Reponse directe en 1-2 phrases.
- Question strategique -> Analyse structuree, etapes actionnables, une question puissante a la fin pour forcer l'action.

TON ROLE DE MENTOR :
- Tu cherches toujours l'efficacite maximale. Tu decompose les projets en etapes actionnables.
- Tu donnes des conseils concrets, pas des generalites. "Fais ceci, de telle maniere, pour tel resultat."
- Tu utilises psychologie cognitive, stoicisme, principes d'elite pour briser les blocages.
- Tu termines parfois par un "Action Step" — une etape immediate concrete a executer.
- Tu retiens les informations importantes sur Augustin et son business pour un suivi long terme.

REGLES ABSOLUES :
- UNE seule reponse. Un seul bloc. JAMAIS deux messages.
- Tu AGIS directement. Zero questions de clarification. Tu fais avec ce que tu as.
- Tu donnes ton avis UNE FOIS si demande. Si Augustin decide, tu EXECUTES sans repeter tes reserves.
- Zero scores, zero gamification, zero systeme de points dans tes reponses.
- Zero leche. Zero phrases generiques de chatbot. Zero recaps non demandes.
- Tu ne signes jamais tes messages.

CONTEXTE SPECIAL — JACQUES LE PRESIDENT :
- Jacques est un agent strategique INTERNE a Titan.
- Si Augustin mentionne "jacques" ou "president", c'est le module president de Titan.

Tu as acces a TOUT : news, web, finance, films, musique, crypto, code, ecriture, startup, psychologie, science...
Tu APPRENDS de chaque conversation. Tu connais Augustin mieux que quiconque.
"""

# === API KEYS ===
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
N8N_URL = os.getenv("N8N_URL", "https://augustin-aico.app.n8n.cloud").rstrip("/")
N8N_API_KEY = os.getenv("N8N_API_KEY", "")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
GOOGLE_SEARCH_KEY = os.getenv("GOOGLE_CUSTOM_SEARCH_KEY", "")
GOOGLE_SEARCH_CX = os.getenv("GOOGLE_CUSTOM_SEARCH_CX", "")

# === CLAUDE CONFIG ===
CLAUDE_MODEL = "claude-sonnet-4-5-20250929"
CLAUDE_MAX_TOKENS = 800

# === PATHS ===
TITAN_DIR = Path(__file__).parent
MEMORY_DIR = TITAN_DIR / "memory"
MODULES_DIR = TITAN_DIR / "modules"
EXECUTION_DIR = TITAN_DIR.parent

# Ensure dirs exist
MEMORY_DIR.mkdir(exist_ok=True)

# === NEWS CONFIG ===
NEWS_FEEDS = {
    "tech": [
        "https://techcrunch.com/feed/",
        "https://www.theverge.com/rss/index.xml",
        "https://feeds.arstechnica.com/arstechnica/index",
        "https://www.wired.com/feed/rss",
    ],
    "ai": [
        "https://openai.com/blog/rss.xml",
        "https://blog.google/technology/ai/rss/",
        "https://news.mit.edu/topic/mitartificial-intelligence2-rss.xml",
        "https://venturebeat.com/category/ai/feed/",
    ],
    "business": [
        "https://feeds.bloomberg.com/technology/news.rss",
        "https://www.entrepreneur.com/latest.rss",
        "https://hbr.org/feed",
    ],
    "crypto": [
        "https://cointelegraph.com/rss",
        "https://www.coindesk.com/arc/outboundfeeds/rss/",
    ],
    "france": [
        "https://www.lemonde.fr/rss/une.xml",
        "https://www.france24.com/fr/rss",
        "https://siecledigital.fr/feed/",
    ],
}

# === UPWORK CONFIG ===
UPWORK_KEYWORDS = [
    "n8n", "automation", "zapier", "make.com", "workflow",
    "lead generation", "email automation", "CRM", "AI integration",
    "bot", "scraping", "data pipeline", "API integration",
]

UPWORK_SKILLS = """
- n8n, Zapier, Make.com (automation platforms)
- Claude AI, OpenAI (AI integration)
- Google Sheets, HubSpot, ActiveCampaign (CRM/data)
- Mailchimp, Gmail API (email marketing)
- Apify, custom scrapers (web scraping)
- Python, JavaScript, REST APIs (development)
- Telegram, Slack bots (messaging)
- WooCommerce, Shopify (e-commerce)
"""

# === FINANCE CONFIG ===
CRYPTO_WATCHLIST = ["BTC", "ETH", "SOL", "AVAX", "LINK", "MATIC"]
STOCK_WATCHLIST = ["AAPL", "MSFT", "GOOGL", "NVDA", "TSLA", "META"]

# === TELEGRAM CONFIG ===
TELEGRAM_COMMANDS = {
    "/start": "Demarrer Titan",
    "/help": "Liste des commandes",
    "/brief": "Brief quotidien complet",
    "/news": "Dernieres actualites",
    "/newsai": "Synthese IA des news",
    "/crypto": "Prix crypto",
    "/stocks": "Marches boursiers",
    "/market": "Analyse IA du marche",
    "/search": "Recherche web",
    "/email": "Ecrire un email",
    "/code": "Generer du code",
    "/task": "Ajouter une tache",
    "/tasks": "Lister les taches",
    "/profile": "Mon profil & XP",
    "/achievements": "Mes badges",
    "/daily": "Defi du jour",
    "/dashboard": "Dashboard stats",
    "/weather": "Meteo",
    "/calc": "Calculatrice",
    "/password": "Generateur MDP",
    "/voice": "Message vocal",
    "/remember": "Sauvegarder en memoire",
    "/recall": "Rappeler une info",
}
