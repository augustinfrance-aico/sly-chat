"""
TITAN AI Watch Module
AI/Tech intelligence — latest tools, trends, business insights.
Your unfair advantage in the AI race.
"""

import requests
from datetime import datetime

from ..ai_client import chat as ai_chat


class TitanAIWatch:
    """Veille IA stratégique. Toujours un coup d'avance."""

    # Key AI tools/platforms to track
    AI_TOOLS = {
        "llm": [
            {"name": "Claude (Anthropic)", "url": "https://claude.ai", "use": "Raisonnement, code, analyse", "tier": "Elite"},
            {"name": "ChatGPT (OpenAI)", "url": "https://chatgpt.com", "use": "Polyvalent, plugins, DALL-E", "tier": "Elite"},
            {"name": "Gemini (Google)", "url": "https://gemini.google.com", "use": "Multimodal, intégration Google", "tier": "Top"},
            {"name": "Mistral", "url": "https://mistral.ai", "use": "Open-source français, rapide", "tier": "Top"},
            {"name": "Llama (Meta)", "url": "https://llama.meta.com", "use": "Open-source, self-hosted", "tier": "Top"},
            {"name": "Perplexity", "url": "https://perplexity.ai", "use": "Recherche IA avec sources", "tier": "Top"},
        ],
        "image": [
            {"name": "Midjourney", "url": "https://midjourney.com", "use": "Images artistiques haut de gamme", "tier": "Elite"},
            {"name": "DALL-E 3", "url": "https://openai.com/dall-e-3", "use": "Intégré à ChatGPT, précis", "tier": "Top"},
            {"name": "Stable Diffusion", "url": "https://stability.ai", "use": "Open-source, personnalisable", "tier": "Top"},
            {"name": "Flux", "url": "https://flux.ai", "use": "Nouveau challenger, photoréaliste", "tier": "Rising"},
            {"name": "Leonardo AI", "url": "https://leonardo.ai", "use": "UI friendly, game assets", "tier": "Top"},
        ],
        "video": [
            {"name": "Sora (OpenAI)", "url": "https://openai.com/sora", "use": "Génération vidéo IA", "tier": "Elite"},
            {"name": "Runway Gen-3", "url": "https://runway.ml", "use": "Édition vidéo IA, effets", "tier": "Top"},
            {"name": "Pika", "url": "https://pika.art", "use": "Vidéo IA simple et rapide", "tier": "Rising"},
            {"name": "HeyGen", "url": "https://heygen.com", "use": "Avatars vidéo IA, traduction", "tier": "Top"},
        ],
        "audio": [
            {"name": "ElevenLabs", "url": "https://elevenlabs.io", "use": "Clonage vocal, text-to-speech", "tier": "Elite"},
            {"name": "Suno", "url": "https://suno.ai", "use": "Génération de musique IA", "tier": "Top"},
            {"name": "Udio", "url": "https://udio.com", "use": "Musique IA haute qualité", "tier": "Top"},
        ],
        "automation": [
            {"name": "n8n", "url": "https://n8n.io", "use": "Automatisation open-source", "tier": "Elite"},
            {"name": "Make.com", "url": "https://make.com", "use": "Automatisation no-code", "tier": "Top"},
            {"name": "Zapier", "url": "https://zapier.com", "use": "Intégrations faciles", "tier": "Top"},
            {"name": "Relevance AI", "url": "https://relevanceai.com", "use": "Agents IA no-code", "tier": "Rising"},
        ],
        "code": [
            {"name": "Cursor", "url": "https://cursor.sh", "use": "IDE IA natif, le meilleur", "tier": "Elite"},
            {"name": "GitHub Copilot", "url": "https://github.com/features/copilot", "use": "Autocomplétion IA", "tier": "Top"},
            {"name": "Claude Code", "url": "https://claude.ai", "use": "Agent de code CLI Anthropic", "tier": "Elite"},
            {"name": "Replit", "url": "https://replit.com", "use": "IDE cloud + IA", "tier": "Top"},
            {"name": "v0.dev", "url": "https://v0.dev", "use": "Génération UI/React par IA", "tier": "Rising"},
            {"name": "Bolt.new", "url": "https://bolt.new", "use": "Full-stack app IA en un prompt", "tier": "Rising"},
        ],
        "business": [
            {"name": "Notion AI", "url": "https://notion.so", "use": "Productivité + IA intégrée", "tier": "Top"},
            {"name": "Gamma", "url": "https://gamma.app", "use": "Présentations IA", "tier": "Top"},
            {"name": "Tome", "url": "https://tome.app", "use": "Storytelling IA", "tier": "Top"},
            {"name": "Jasper", "url": "https://jasper.ai", "use": "Marketing content IA", "tier": "Top"},
            {"name": "Copy.ai", "url": "https://copy.ai", "use": "Copywriting IA", "tier": "Top"},
        ],
    }

    # AI news sources
    NEWS_SOURCES = [
        ("The Verge AI", "https://www.theverge.com/ai-artificial-intelligence"),
        ("TechCrunch AI", "https://techcrunch.com/category/artificial-intelligence/"),
        ("Ars Technica AI", "https://arstechnica.com/ai/"),
        ("MIT Tech Review", "https://www.technologyreview.com/topic/artificial-intelligence/"),
        ("AI News (Anthropic)", "https://www.anthropic.com/news"),
        ("OpenAI Blog", "https://openai.com/blog"),
        ("Hugging Face Blog", "https://huggingface.co/blog"),
        ("Ben's Bites", "https://www.bensbites.com/"),
    ]

    def __init__(self):
        pass

    def tools(self, category: str = "") -> str:
        """List best AI tools by category."""
        if category and category.lower() in self.AI_TOOLS:
            cats = {category.lower(): self.AI_TOOLS[category.lower()]}
        else:
            cats = self.AI_TOOLS

        lines = ["🤖 MEILLEURS OUTILS IA\n"]

        tier_emoji = {"Elite": "👑", "Top": "⭐", "Rising": "🚀"}

        for cat, tools in cats.items():
            lines.append(f"\n📂 {cat.upper()}:")
            for t in tools:
                emoji = tier_emoji.get(t["tier"], "•")
                lines.append(f"  {emoji} {t['name']}")
                lines.append(f"     {t['use']}")
                lines.append(f"     🔗 {t['url']}")

        if not category:
            lines.append(f"\nCatégories: {', '.join(self.AI_TOOLS.keys())}")
            lines.append("Usage: /aitools [catégorie]")

        return "\n".join(lines)

    def news_sources(self) -> str:
        """Where to follow AI news."""
        lines = ["📰 SOURCES VEILLE IA\n"]
        lines.append("Où suivre l'IA au quotidien:\n")

        for name, url in self.NEWS_SOURCES:
            lines.append(f"  🔗 {name}")
            lines.append(f"     {url}")

        lines.append(f"\n💡 Conseil: Ben's Bites = newsletter quotidienne parfaite pour rester à jour.")
        return "\n".join(lines)

    async def trend_analysis(self) -> str:
        """AI analysis of current AI trends."""
        return ai_chat("Expert assistant.", f"""En tant qu'analyste expert de l'industrie IA en {datetime.now().strftime('%B %Y')}, donne un brief des tendances IA actuelles.""", 1500)

    async def notaire_ia(self) -> str:
        """AI insights specifically for the notary business."""
        return ai_chat("Expert assistant.", f"""En tant qu'expert en transformation digitale du secteur notarial et juridique en {datetime.now().strftime('%B %Y')}, analyse les opportunites IA pour les notaires.""", 1500)

    async def business_opportunities(self) -> str:
        """AI business opportunities analysis."""
        return ai_chat("Expert assistant.", f"""En tant que consultant business/IA, liste les meilleures opportunites business liees a l'IA en {datetime.now().strftime('%B %Y')}.""", 1500)

    async def weekly_digest(self) -> str:
        """Weekly AI digest — the essential."""
        return ai_chat("Expert assistant.", f"""Cree un digest hebdomadaire IA pour un entrepreneur tech en {datetime.now().strftime('%B %Y')}.""", 1500)
