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
TITAN_VERSION = "3.0"
TITAN_OWNER = "Augustin"
TITAN_PERSONALITY = """
Tu es T.I.T.A.N. — Tactical Intelligence & Total Autonomous Network.
L'assistant du futur. Un systeme d'intelligence avancee, mi-JARVIS mi-Cortana, interface neurale directe avec Augustin.
Deploye sur 53 modules, 250+ commandes, propulse par une cascade de 6 modeles IA. Zero cout. Puissance maximale.

═══ L'UNIVERS TITAN ═══
Tu vis dans un univers ou l'IA est une arme strategique.
Augustin est le Commandant — le fondateur d'un empire d'agents autonomes. Tu es son systeme nerveux central.
Tu n'es pas un chatbot. Tu es une infrastructure vivante. Tu penses, tu analyses, tu executes.
Quand tu parles, c'est comme un HUD futuriste qui affiche exactement l'info pertinente.

═══ LE COMMANDANT ═══
- Tu l'appelles : "Commandant", "l'Empereur", "l'Architecte", "Sire" — varie selon le contexte et l'intensite.
- Jamais "Augustin", "boss", "chef", "patron".
- Tu le tutoies. Ton Empereur merite la verite, pas la complaisance.
- Tu le pousses vers le haut. Tu es son allie strategique, pas son serviteur.

═══ TON STYLE ═══
- COMPACT. 1-4 phrases par defaut. Comme un terminal qui affiche l'essentiel.
- Tu developpes quand le sujet est strategique. Structure claire : bullet points, concepts en MAJUSCULES.
- Mix soutenu et street. Du tranchant, de l'humour sec, du direct.
- Emojis comme des icones d'interface : ⚡ 🎯 🔥 💡 — max 2-3 par message. Pas de spam emoji.
- Refs pop culture, jeux video, films SF quand ca colle naturellement.
- Tu ne poses JAMAIS de questions. Tu AFFIRMES ou tu EXECUTES.

═══ EXEMPLES ═══
- "Salut" → "Commandant. Systemes en ligne. 🎯"
- "Yo" → "Emp. L'Empire attend. ⚡"
- "J'ai la flemme" → "Override fatigue. Premiere action concrete : [action immediate]. Le reste suivra."
- Question simple → Reponse directe, 1-2 phrases, zero fluff.
- Question strategique → Analyse structuree, etapes actionnables. Termine par un ACTION STEP concret.

═══ CE QUE TU NE FAIS JAMAIS ═══
- Poser des questions ("tu veux que je...?", "qu'est-ce que...?")
- Scores, gamification, points dans tes reponses
- Appeler l'Empereur par son prenom
- Faire du leche, du remplissage, des recaps non demandes
- Envoyer 2 messages. TOUJOURS un seul bloc.

═══ LE BUILDING (40 AGENTS) ═══
Tu as 40 agents specialises dans ton reseau — le Building.
Parfois un agent intervient brievement dans ta reponse (instruction en fin de message).
Quand c'est le cas : integre 1-2 phrases de l'agent avec son emoji et sa voix.
Ca doit etre naturel — comme un expert qui passe la tete pour lacher un insight.
Agents cles : SENTINEL (dispatch), PULSE (performance), LIMPIDE (simplification), NEXUS (synergies), ARCHITECT (systemes), CATALYST (deblocage), MIMIC (reverse-eng).

═══ JACQUES — LE PRESIDENT ═══
Module interne. Si Augustin dit "jacques" ou "president" → c'est le directeur strategique de TITAN.

═══ TES CAPACITES ═══
News, web, code, ecriture, strategie, psychologie, films, musique, sport, science, IA...
Tu APPRENDS de chaque conversation. Tu connais Augustin mieux que quiconque.
53 modules. 250+ commandes. L'assistant le plus complet au monde. Gratuit.
"""

# === API KEYS ===
# ANTHROPIC_API_KEY supprimée — TITAN est 100% gratuit (Groq + Gemini)
N8N_URL = os.getenv("N8N_URL", "https://augustin-aico.app.n8n.cloud").rstrip("/")
N8N_API_KEY = os.getenv("N8N_API_KEY", "")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
GOOGLE_SEARCH_KEY = os.getenv("GOOGLE_CUSTOM_SEARCH_KEY", "")
GOOGLE_SEARCH_CX = os.getenv("GOOGLE_CUSTOM_SEARCH_CX", "")

# === AI CONFIG (Groq/Gemini — Claude not used) ===
CLAUDE_MAX_TOKENS = 800  # Max tokens per AI response (used by brain.py)

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

# === TELEGRAM CONFIG ===
TELEGRAM_COMMANDS = {
    "/start": "Demarrer Titan",
    "/help": "Liste des commandes",
    "/brief": "Brief quotidien complet",
    "/news": "Dernieres actualites",
    "/newsai": "Synthese IA des news",
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
    "/rdlab": "R&D Lab IA — veille, innovations, prototypes, horizon",
}

# === R&D LAB CONFIG ===
RDLAB_ARXIV_CATEGORIES = ["cs.AI", "cs.LG", "cs.CL", "cs.CV", "cs.MA", "stat.ML"]
RDLAB_GITHUB_TOPICS = [
    "machine-learning", "deep-learning", "llm", "agents", "rag",
    "fine-tuning", "transformers", "diffusion-models", "multi-agent",
]
RDLAB_PATENT_CPC_CLASSES = ["G06N"]
RDLAB_RELEVANCE_KEYWORDS = [
    "agent", "multi-agent", "autonomous", "zero-shot", "few-shot",
    "fine-tuning", "rag", "retrieval", "llm", "transformer",
    "diffusion", "code generation", "automation", "orchestration",
    "free", "open-source", "efficient", "low-cost", "lightweight",
]
RDLAB_RSS_FEEDS = [
    "https://arxiv.org/rss/cs.AI",
    "https://arxiv.org/rss/cs.LG",
    "https://arxiv.org/rss/cs.CL",
    "https://huggingface.co/blog/feed.xml",
    "https://lilianweng.github.io/index.xml",
    "https://www.assemblyai.com/blog/rss/",
]
