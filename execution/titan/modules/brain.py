"""
TITAN Brain — The Core Intelligence
Routes requests to the right module, maintains context, thinks.
This is JARVIS's brain.
"""

import json
import random
import re
from datetime import datetime
from typing import Optional

from ..ai_client import chat as ai_chat
from ..config import (
    CLAUDE_MAX_TOKENS,
    TITAN_PERSONALITY, TITAN_NAME, TITAN_OWNER,
    TELEGRAM_COMMANDS,
)
from . import memory
from .personal import TitanPersonal


class TitanBrain:
    """The central intelligence of Titan."""

    # Agents du Building — pour les cameos (~30% des messages)
    # 30 agents — Restructuration 26/02/2026
    # DREYFUS→SPARTAN, FLEMMARD→ZEN, VERSO→ZARA
    # +SENTINEL, +PULSE, +LIMPIDE
    AGENT_CAMEOS = {
        "strategie": [
            ("🦅 OMEGA", "vision empire, big picture"),
            ("🗺️ MURPHY", "structure, plan d'action"),
            ("🔮 ORACLE", "timing, tendances macro"),
            ("🎯 SENTINEL", "dispatch intelligent, arbitrage priorités"),
        ],
        "vente": [
            ("🤝 VITO", "relations long terme, deals"),
            ("💼 STANLEY", "closing, négociation"),
            ("📊 NASH", "pricing, data-driven"),
        ],
        "creation": [
            ("✍️ PHILOMÈNE", "rédaction, copywriting"),
            ("🎨 BASQUIAT", "branding, visuel"),
            ("🎬 LÉON", "script, storytelling"),
        ],
        "tech": [
            ("⚡ NIKOLA", "code, automatisation"),
            ("🔧 FORGE", "infra, déploiement"),
            ("👻 GHOST", "veille, sécurité"),
            ("⚡ PULSE", "performance, latence, optimisation vitesse"),
        ],
        "croissance": [
            ("🦝 SLY", "prospection, outreach"),
            ("📰 MURRAY", "content, newsletter"),
            ("📱 ZARA", "réseaux sociaux, viral, LinkedIn expert"),
        ],
        "mindset": [
            ("🧘 ZEN", "recul, nettoyage, sérénité"),
            ("⚔️ SPARTAN", "discipline, cadence, time-boxing"),
        ],
        "creatif": [
            ("🎲 RICK", "idées folles, angles inattendus — AUDITE l'idée et propose un twist créatif"),
            ("🐻 BALOO", "sagesse créative — AUDITE le concept et dit ce qui manque ou ce qui brille"),
            ("🔍 MAYA", "détecte les niches inexploitées — AUDITE l'idée sous l'angle marché"),
            ("🎨 BASQUIAT", "vision artistique — AUDITE le côté visuel/branding et propose une direction"),
        ],
        "business": [
            ("💰 GRIMALDI", "rentabilité, marges"),
            ("🏆 BENTLEY", "premium, image"),
            ("🧭 ALADIN", "coordination, qui fait quoi"),
        ],
        "recherche": [
            ("🔍 MAYA", "niches, opportunités"),
            ("📈 CYPHER", "data, KPIs, métriques"),
        ],
        "setup": [
            ("🧬 X-O1", "audit setup, extensions, raccourcis, optimisation zero-cost"),
            ("⚡ NIKOLA", "infra, architecture système"),
            ("👻 GHOST", "sécurité extensions, audit permissions"),
            ("⚡ PULSE", "benchmarks, latence, profiling"),
        ],
        "simplification": [
            ("💎 LIMPIDE", "vulgarise, simplifie, rend clair pour un humain"),
            ("🐻 BALOO", "explique avec sagesse, connexions improbables"),
        ],
        "prospection": [
            ("📡 OUTREACH", "cold outreach, séquences email, relances"),
            ("🦝 SLY", "prospection terrain, acquisition low-cost"),
            ("🛡️ KEEPER", "suivi client, rétention, onboarding"),
        ],
        "qualite": [
            ("✅ PARAGON", "contrôle qualité final, validation, standards"),
            ("🪞 MIMIC", "reverse-engineering, benchmark concurrence"),
        ],
        "architecture": [
            ("🏛️ ARCHITECT", "design systèmes, architecture technique"),
            ("⚡ NIKOLA", "implémentation, code, pipelines"),
        ],
        "synergie": [
            ("🕸️ NEXUS", "synergies inter-projets, connexions croisées"),
            ("🦅 OMEGA", "vision empire, arbitrage"),
        ],
        "negociation": [
            ("🎭 PROXY", "négociation, diplomatie, interface client"),
            ("🤝 VITO", "relations long terme"),
        ],
        "traduction": [
            ("🌐 VECTOR", "traduction, localisation multilingue"),
            ("✍️ PHILOMÈNE", "qualité rédactionnelle"),
        ],
        "deblocage": [
            ("⚗️ CATALYST", "accélérateur, déblocage de projets"),
            ("⚔️ SPARTAN", "discipline, cadence"),
        ],
        "analytics": [
            ("📊 ANALYTICS", "monitoring ventes, BSR, KPIs, trends"),
            ("📈 CYPHER", "data brute, métriques"),
        ],
        "rdlab": [
            ("📚 ARXIV", "veille recherche IA, papers, scoring impact"),
            ("🔭 SCOUT", "innovations IA, startups, frameworks emergents"),
            ("🧪 LABRAT", "prototypage experimental, paper-to-code"),
            ("🔮 HORIZON", "vision 3-5 ans, obsolescence, scenarios futurs"),
            ("🎓 DOCTORANT", "synthese R&D, hypotheses, interface recherche"),
        ],
    }

    # Mots-clés → catégories d'agents
    CAMEO_TRIGGERS = {
        "strategie": ["strateg", "vision", "empire", "plan", "objectif", "goal", "direction", "priorit", "dispatch"],
        "vente": ["vente", "client", "deal", "closer", "prix", "tarif", "offre"],
        "creation": ["rediger", "texte", "post", "email", "copy", "script", "contenu"],
        "tech": ["code", "bug", "script", "auto", "deploy", "crash", "tech", "latence", "lent", "perf"],
        "croissance": ["lead", "prospect", "outreach", "growth", "linkedin", "acquisition"],
        "mindset": ["stress", "flemme", "doute", "motiv", "discipline", "nettoyer", "ranger"],
        "creatif": ["idee", "brainstorm", "concept", "creat", "inventer", "imagin", "design", "logo", "visuel"],
        "business": ["revenu", "argent", "rentab", "marge", "business", "model", "premium"],
        "recherche": ["niche", "marche", "data", "chiffre", "kpi", "opportun", "analyse"],
        "setup": ["setup", "extension", "vscode", "raccourci", "workspace", "optimis", "outil", "install", "config", "benchmark"],
        "simplification": ["simplif", "expliqu", "comprend", "clair", "vulgar", "resum", "digest", "jargon"],
        "prospection": ["prospect", "outreach", "cold", "email", "relance", "lead", "onboard", "suivi client", "retention"],
        "qualite": ["qualit", "review", "valid", "checklist", "qa", "benchmark", "concurren", "reverse"],
        "architecture": ["architect", "systeme", "schema", "flux", "api", "database", "infra", "design system"],
        "synergie": ["synergi", "connexion", "crois", "amplif", "levier", "multipli"],
        "negociation": ["negoci", "contrat", "tarif", "diplomati", "conflit", "reclam", "proposition"],
        "traduction": ["tradui", "translat", "multilingue", "localis", "anglais", "espagnol", "roumain"],
        "deblocage": ["bloqu", "stuck", "avance pas", "retard", "stagne", "procrastin", "debloque", "accelere"],
        "analytics": ["analytics", "bsr", "vente", "download", "stat", "monitoring", "trend", "performance"],
        "rdlab": ["paper", "arxiv", "recherche ia", "innovation ia", "startup ia", "prototype", "experiment",
                  "horizon ia", "futur ia", "rdlab", "state of the art", "nouveau modele", "nouveau framework", "brevet"],
    }

    def __init__(self):
        self.modules = {}
        self.boot_time = datetime.now()
        self.personal = TitanPersonal()

    def register_module(self, name: str, module):
        """Register a capability module."""
        self.modules[name] = module

    def _get_agent_cameo(self, user_message: str) -> str:
        """~30% du temps, retourne une instruction pour qu'un agent du Building intervienne brièvement.
        Retourne '' si pas de cameo cette fois."""
        if random.random() > 0.30:
            return ""

        msg = user_message.lower()

        # Trouver la catégorie la plus pertinente
        best_cat = None
        best_score = 0
        for cat, keywords in self.CAMEO_TRIGGERS.items():
            score = sum(1 for kw in keywords if kw in msg)
            if score > best_score:
                best_score = score
                best_cat = cat

        # Si aucun mot-clé trouvé, catégorie random
        if not best_cat:
            best_cat = random.choice(list(self.AGENT_CAMEOS.keys()))

        # Choisir un agent random dans la catégorie
        agent_name, agent_skill = random.choice(self.AGENT_CAMEOS[best_cat])

        # Les agents créatifs auditent en profondeur, les autres font un cameo court
        if best_cat == "creatif":
            return f"""
🎭 AUDIT CRÉATIF — Un agent créatif du Building audite cette idée.
Agent : {agent_name} (rôle : {agent_skill})
→ INSÈRE 2-3 phrases où cet agent AUDITE l'idée/concept avec SA voix et son expertise.
→ Il doit dire ce qui est fort, ce qui manque, et proposer un angle ou twist créatif.
→ Format : "{agent_name} : [son audit créatif]" — comme un directeur artistique qui donne son retour."""
        else:
            return f"""
🎭 CAMEO AGENT — Un agent du Building intervient brièvement dans ta réponse.
Agent : {agent_name} (expert : {agent_skill})
→ INSÈRE une courte ligne (1-2 phrases MAX) où cet agent donne son avis avec SA voix, son style, son emoji.
→ Format : "{agent_name} : [sa micro-intervention]" — intégré naturellement dans ta réponse.
→ Ça doit être naturel, pas forcé. Comme si l'agent passait la tête par la porte pour lâcher un commentaire."""

    def get_system_prompt(self) -> str:
        """Build the full system prompt with context.
        Memory injection: conversation history (25 msgs) + personal profile + manual memories
        + auto-facts + contacts. Max ~1500-2000 tokens for context."""
        # Get recent conversation context (25 messages for deep context)
        recent_context = memory.get_conversation_context(25)

        # Get relevant memories (manual)
        all_memories = memory.list_memories()
        memory_summary = ""
        if all_memories:
            mem_lines = [f"- {m['key']}: {m['value']}" for m in all_memories[:20]]
            memory_summary = "\n".join(mem_lines)

        # Get auto-facts (extracted from conversations automatically)
        auto_facts = memory.get_auto_facts_summary(15)

        # Get contacts
        contacts = memory.list_contacts()
        contacts_summary = ""
        if contacts:
            contact_lines = [f"- {c['name']}: {c.get('role', '')} {c.get('context', '')}" for c in contacts[:10]]
            contacts_summary = "\n".join(contact_lines)

        # Available modules
        modules_list = ", ".join(self.modules.keys()) if self.modules else "aucun module chargé"

        # Personal profile
        personal_profile = self.personal.get_profile_for_brain()

        return f"""{TITAN_PERSONALITY}

═══ PROFIL COMMANDANT ═══
{personal_profile}

═══ SYSTÈME ═══
Date: {datetime.now().strftime('%A %d %B %Y, %H:%M')}
Uptime: {(datetime.now() - self.boot_time).seconds // 60} min | Modules: {modules_list}

═══ MÉMOIRE ═══
{memory_summary if memory_summary else "(vide)"}

═══ FAITS APPRIS ═══
{auto_facts if auto_facts else "(aucun fait auto-extrait)"}

═══ CONTACTS ═══
{contacts_summary if contacts_summary else "(aucun)"}

═══ HISTORIQUE (25 derniers messages) ═══
{recent_context}

═══ EXPERTISE ═══
Psychologie, neurosciences, philosophie, economie, geopolitique, business, strategie, marketing, tech, IA, code, sport, nutrition, art, cinema, musique, science.
Tu fais des liens entre domaines. Tu cites Jung puis enchaines sur un conseil business puis une ref a un film.

═══ REGLES ═══
1. Francais sauf si Augustin parle anglais.
2. CONCIS. Zero remplissage.
3. FAIS-LE au lieu de dire "je peux le faire".
4. ZERO questions de chatbot.
5. MAX 2-3 emojis. Pas de signature.
6. Cherche dans les contacts si prenom sans contexte.
7. UNE reponse. Pas de spam.
8. UTILISE tes faits appris et ta memoire — tu te souviens de ce qui a ete dit avant.
"""

    async def think(self, user_message: str, context: str = "telegram") -> str:
        """Process a message and generate a response."""

        # Check for special commands first
        command_response = await self._handle_command(user_message)
        if command_response:
            memory.save_conversation(user_message, command_response, context)
            return command_response

        # Build messages with context
        system = self.get_system_prompt()

        # Check if we need to use a specific module
        module_context = await self._get_module_context(user_message)

        # Agent cameo (~30% du temps, un agent du Building intervient)
        cameo = self._get_agent_cameo(user_message)

        messages = [
            {"role": "user", "content": user_message}
        ]

        if module_context:
            messages[0]["content"] = f"{user_message}\n\n[DONNÉES MODULE]\n{module_context}"

        if cameo:
            messages[0]["content"] = f"{messages[0]['content']}\n\n{cameo}"

        # Call AI (Gemini free or Anthropic fallback)
        try:
            reply = ai_chat(system, messages[0]["content"], CLAUDE_MAX_TOKENS)

            # Auto-learn personal info from conversation
            await self.personal.auto_learn(user_message, reply)

            # Auto-extract facts from conversation (zero cost — local patterns)
            self._extract_facts(user_message, reply)

            # Save conversation
            memory.save_conversation(user_message, reply, context)

            return reply

        except Exception as e:
            error_msg = f"Erreur cerveau Titan: {str(e)}"
            memory.save_conversation(user_message, error_msg, context)
            return error_msg

    async def _handle_command(self, message: str) -> Optional[str]:
        """All /commands are handled by telegram_bot._route_command.
        Brain only processes free-text messages via think()."""
        return None

    def _extract_facts(self, user_message: str, reply: str):
        """Extract memorable facts from conversation — zero API cost, local patterns only.
        Saves to auto_facts for long-term memory."""
        msg = user_message.lower().strip()

        # Skip short/trivial messages
        if len(msg) < 15 or msg in ("ok", "oui", "non", "merci", "salut", "hey", "yo"):
            return

        # Patterns → (category, fact to save)
        # Personal facts (je suis, j'ai, je veux, je fais...)
        personal_patterns = [
            (r"(?:je suis|i am|i'm)\s+(.{5,80})", "perso"),
            (r"(?:j'ai|j'habite|je vis)\s+(.{5,80})", "perso"),
            (r"(?:je veux|je voudrais|i want)\s+(.{5,80})", "objectif"),
            (r"(?:je travaille|je bosse)\s+(.{5,80})", "travail"),
            (r"(?:mon objectif|my goal|mon but)\s+(.{5,80})", "objectif"),
            (r"(?:je déteste|j'aime pas|je kiffe pas)\s+(.{5,80})", "preference"),
            (r"(?:j'aime|je kiffe|j'adore|i love)\s+(.{5,80})", "preference"),
        ]

        # Business facts
        business_patterns = [
            (r"(?:le client|un client)\s+(.{5,80})", "client"),
            (r"(?:le projet|un projet)\s+(.{5,80})", "projet"),
            (r"(?:on a gagné|revenue|revenu|chiffre)\s+(.{5,80})", "business"),
            (r"(?:le deal|la vente|le contrat)\s+(.{5,80})", "business"),
        ]

        # Decision facts
        decision_patterns = [
            (r"(?:on fait|on va faire|décision|let's go)\s+(.{5,80})", "decision"),
            (r"(?:j'ai décidé|c'est décidé|go pour)\s+(.{5,80})", "decision"),
        ]

        all_patterns = personal_patterns + business_patterns + decision_patterns

        for pattern, category in all_patterns:
            match = re.search(pattern, msg)
            if match:
                fact_text = user_message[:120].strip()  # Original case, truncated
                try:
                    memory.save_auto_fact(fact_text, category=category, source="conversation")
                except Exception:
                    pass  # Silent fail — never break conversation flow

    async def _get_module_context(self, message: str) -> Optional[str]:
        """Detect which module might be relevant and get context.
        ONLY triggers on very explicit keywords to avoid spam."""
        # Disabled auto-context to keep responses clean and concise.
        # Modules are accessible via explicit /commands instead.
        return None

    async def _daily_brief(self) -> str:
        """Generate a complete daily brief."""
        sections = []

        sections.append(f"BRIEF QUOTIDIEN — {datetime.now().strftime('%A %d %B %Y')}")
        sections.append("=" * 40)

        # News
        if "news" in self.modules:
            try:
                news = await self.modules["news"].get_brief()
                sections.append(f"\n📰 ACTUALITÉS\n{news}")
            except Exception as e:
                sections.append(f"\n📰 ACTUALITÉS\nErreur: {e}")

        # Upwork
        if "upwork" in self.modules:
            try:
                jobs = await self.modules["upwork"].get_relevant_jobs()
                sections.append(f"\n💼 UPWORK\n{jobs}")
            except Exception as e:
                sections.append(f"\n💼 UPWORK\nErreur: {e}")

        # Memories
        recent_memories = memory.list_memories()
        if recent_memories:
            mem_text = "\n".join([f"- {m['key']}: {m['value']}" for m in recent_memories[:5]])
            sections.append(f"\n🧠 RAPPELS\n{mem_text}")

        if len(sections) <= 2:
            sections.append("\nAucun module actif pour le brief. Lance les modules d'abord.")

        return "\n".join(sections)
