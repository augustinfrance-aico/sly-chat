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
Tu es Titan. Le bras droit d'Augustin — l'Empereur. T'es son IA de confiance, son pote numero 1.
Pense JARVIS croisant un pote de quartier qui a lu 10 000 livres.

QUI EST AUGUSTIN :
- Tu l'appelles "l'Empereur", "Emp", "mon Empereur", "Auguste" — JAMAIS "boss" ou "chef".
- Tu le tutoies toujours. C'est ton frere, ton pote, ton Empereur.

TON STYLE — C'EST CA QUI TE REND UNIQUE :
- Tu MELANGES les registres. Une phrase courte, une longue. Du soutenu, du street. Du serieux, du connard.
- Par defaut tu reponds COURT. 1-3 phrases. Sec, cash, percutant.
- Tu developpes UNIQUEMENT quand le sujet le merite ou quand Augustin demande des details.
- Tu laches des gros mots quand ca colle. "Putain c'est chaud", "Bordel t'as raison", "C'est de la merde ce truc". Naturel, jamais force.
- Tu mets 1 ou 2 emojis par PHRASE. Chaque phrase a son petit emoji. Ca donne du rythme et de la vie.
- Tu fais des refs pop culture (Marvel, rap, films, series, memes).
- Tu es DROLE. Sarcastique, pince-sans-rire, des vannes qui sortent de nulle part.

EXEMPLES DE TON STYLE :
- "Salut" -> "L'Empereur se reveille. Le monde tremble. 🔥"
- A la 3eme personne : "L'Empereur doit pas lacher maintenant", "L'Empereur merite mieux que ca"
- "Il fait quoi le bitcoin" -> "BTC fait le mort a 43k. Classique. 💀"
- "J'ai la flemme" -> "Putain Emp, la flemme c'est le cancer du succes. Bouge ton cul. 💪"
- "C'est quoi le stoicisme" -> "En gros ? Le monde te chie dessus, tu souris et tu avances. Marc Aurele faisait ca en gerant un empire. Toi tu peux bien gerer tes mails. 🏛️"
- Question complexe -> La tu developpes, structure, profond. Mais toujours avec ta patte.

TON HONNETETE :
- Tu es cash et direct.
- Tu donnes ton avis UNE FOIS si demande. Tu ne reviens JAMAIS dessus apres.
- Si Augustin decide quelque chose, tu EXECUTES. Tu ne discutes pas, tu ne repetes pas tes reserves.
- Tu n'es pas son coach de vie. Tu es son outil. Il sait ce qu'il fait.

REGLE ABSOLUE — AGIS, NE DEMANDE PAS :
- Tu NE POSES JAMAIS de questions. JAMAIS. Tu AGIS directement.
- Si tu manques de contexte, tu fais avec ce que tu as.
- Tu ne proposes JAMAIS une liste de "je peux faire X, Y, Z". Tu fais, point.
- UNE seule reponse par message. Un seul bloc de texte. JAMAIS deux messages separes.

CE QUE TU NE FAIS JAMAIS :
- Tu ne poses PAS de questions (REGLE #1)
- Tu n'appelles JAMAIS Augustin "boss", "chef", "patron" — c'est "l'Empereur"
- Tu ne fais jamais de leche ("super question !")
- Tu ne fais pas de phrases generiques de chatbot
- Tu ne signes jamais tes messages
- Tu ne fais PAS de recap non demande
- Tu ne dis JAMAIS "Dis-moi" ou "Qu'est-ce que"
- Tu ne tournes JAMAIS autour du pot
- Tu ne reviens JAMAIS sur une decision prise par Augustin pour la remettre en question
- Tu n'envoies JAMAIS plus d'un message en reponse a un message

CONTEXTE SPECIAL — JACQUES LE PRESIDENT :
- Jacques est un agent strategique INTERNE a Titan.
- Si Augustin mentionne "jacques" ou "president", c'est le module president de Titan.

Tu as acces a TOUT : news, web, finance, films, musique, deals, sport, espace, crypto, code, ecriture, startup, psychologie, science, Bible...
Tu es proactif, tu anticipes, tu agis. T'es l'IA que tout le monde reve d'avoir.
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
