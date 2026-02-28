"""
TITAN Brain v2.0 — The Core Intelligence
Routes requests to the right module, maintains context, thinks.

v2.0 Upgrades:
- Smart Context Window (relevant + recent, not just chronological)
- Response quality scoring (local heuristic, zero cost)
- Adaptive system prompt (shorter for trivial, full for strategic)
- Performance tracking integration
"""

import json
import logging
import random
import re
import time
from datetime import datetime
from typing import Optional

from ..ai_client import chat as ai_chat, _score_response
from ..config import (
    CLAUDE_MAX_TOKENS,
    TITAN_PERSONALITY, TITAN_NAME, TITAN_OWNER,
    TELEGRAM_COMMANDS,
)
from . import memory
from .personal import TitanPersonal

log = logging.getLogger("titan.brain")


class TitanBrain:
    """The central intelligence of Titan."""

    # Agents du Building — pour les cameos (~30% des messages)
    # 50 agents — Opération Expansion
    # 18 agents absorbés, compétences transférées aux survivants
    AGENT_CAMEOS = {
        "strategie": [
            ("🦅 OMEGA", "vision empire, big picture"),
            ("🧠 CORTEX", "structure, plan d'action"),
            ("🔮 SIBYL", "timing, tendances, vision 3-5 ans"),
            ("🎯 SENTINEL", "dispatch, orchestration, coordination"),
            ("🐺 SLY", "tactique terrain, coordination opérationnelle"),
        ],
        "vente": [
            ("👑 KAISER", "deals, négociation, diplomatie"),
            ("🎯 CLOSER", "closing, conversion, rétention"),
            ("💠 PRISM", "pricing, psychologie des offres"),
            ("🪞 MIRAGE", "psychologie cognitive, influence éthique"),
        ],
        "creation": [
            ("✍️ PHILOMÈNE", "copywriting, long-form, traduction"),
            ("🎨 FRESCO", "branding, visuel, scripts vidéo"),
            ("📱 VIRAL", "réseaux sociaux, LinkedIn, viral"),
            ("🌅 AURORA", "imagination pure, concepts radicaux"),
            ("📜 ORPHEUS", "narration longue, storytelling profond"),
        ],
        "tech": [
            ("⚡ VOLT", "code, automatisation, architecture"),
            ("🔨 ANVIL", "debug, exécution, déblocage"),
            ("👻 SPECTER", "veille, sécurité, reverse-eng"),
            ("💓 PULSE", "performance, latence, audit setup"),
            ("🐢 BENTLEY", "architecture technique, hacking éthique"),
            ("🔄 FLUX", "automation, n8n/Make, workflows"),
        ],
        "croissance": [
            ("🦝 RACOON", "growth, outreach, cold prospection"),
            ("📱 VIRAL", "réseaux sociaux, audience"),
        ],
        "mindset": [
            ("🐢 FRANKLIN", "recul, sagesse, clarté"),
            ("⚔️ DREYFUS", "discipline, cadence, qualité"),
        ],
        "creatif": [
            ("⚡ GLITCH", "idées folles, brainstorm — AUDITE l'idée et propose un twist créatif"),
            ("🎯 NICHE", "détecte les niches — AUDITE l'idée sous l'angle marché"),
            ("🎨 FRESCO", "vision artistique — AUDITE le visuel/branding"),
            ("🕹️ PIXEL", "game design, gamification, UX interactive"),
            ("🌅 AURORA", "imagination — AUDITE l'idée sous l'angle visionnaire"),
        ],
        "business": [
            ("📒 LEDGER", "rentabilité, marges, projections"),
            ("🖤 ONYX", "premium, image, crédibilité"),
        ],
        "recherche": [
            ("🎯 NICHE", "niches, opportunités"),
            ("📊 DATUM", "data, KPIs, monitoring"),
        ],
        "setup": [
            ("💓 PULSE", "audit setup, extensions, benchmarks"),
            ("⚡ VOLT", "infra, architecture système"),
            ("👻 SPECTER", "sécurité, audit permissions"),
        ],
        "simplification": [
            ("🐢 FRANKLIN", "vulgarise, simplifie, sagesse"),
            ("⚡ GLITCH", "explique avec des angles inattendus"),
        ],
        "prospection": [
            ("🦝 RACOON", "cold outreach, séquences, prospection"),
            ("🎯 CLOSER", "suivi client, rétention, onboarding"),
        ],
        "qualite": [
            ("⚔️ DREYFUS", "contrôle qualité, standards, discipline"),
            ("👻 SPECTER", "reverse-engineering, benchmark concurrence"),
            ("📐 VIRGILE", "correction, clean code, cohérence"),
        ],
        "architecture": [
            ("⚡ VOLT", "design systèmes, architecture, pipelines"),
            ("🧠 CORTEX", "structure, fondations"),
        ],
        "synergie": [
            ("🕸️ NEXUS", "synergies inter-projets, cascades"),
            ("🦅 OMEGA", "vision empire, arbitrage"),
        ],
        "negociation": [
            ("👑 KAISER", "négociation, diplomatie, deals"),
            ("🎯 CLOSER", "objections, closing"),
        ],
        "traduction": [
            ("✍️ PHILOMÈNE", "traduction, localisation, qualité"),
        ],
        "deblocage": [
            ("🔨 ANVIL", "exécution brute, déblocage"),
            ("⚔️ DREYFUS", "discipline, cadence"),
            ("🦛 MURRAY", "force brute, déploiement massif"),
        ],
        "analytics": [
            ("📊 DATUM", "monitoring, KPIs, data, trends"),
        ],
        "rdlab": [
            ("🔐 CIPHER", "veille recherche IA, papers, synthèse R&D"),
            ("📡 RADAR", "innovations IA, startups, frameworks"),
            ("🧪 PROTO", "prototypage expérimental, paper-to-code"),
        ],
        "imagination": [
            ("🌅 AURORA", "concepts radicaux, visions créatives"),
            ("⚡ GLITCH", "idées folles, connexions inattendues"),
        ],
        "upwork": [
            ("🎪 MERCER", "proposals, JSS, profil Upwork"),
            ("🎯 CLOSER", "closing, conversion"),
            ("🪞 MIRAGE", "psychologie du prospect"),
        ],
        "benchmark_ia": [
            ("🤖 TURING", "évaluation modèles, scoring LLM"),
            ("🔐 CIPHER", "veille recherche IA"),
            ("📡 RADAR", "innovations, frameworks"),
        ],
        "automation": [
            ("🔄 FLUX", "n8n, Make, Zapier, workflows"),
            ("⚡ VOLT", "architecture, pipelines"),
            ("👻 SPECTER", "intégrations API, sécurité"),
        ],
        "contournement": [
            ("🏴‍☠️ HUNTER", "contournement, alternatives, bypass, scraping"),
            ("👻 SPECTER", "reverse-engineering, failles"),
            ("🐺 SLY", "tactique furtive, infiltration"),
        ],
        "legal": [
            ("⚖️ JUSTICE", "contrats, RGPD, IP, conformité"),
            ("📒 LEDGER", "audit financier"),
        ],
        "audio": [
            ("🎙️ ECHO", "sound design, podcast, audio branding"),
            ("🎨 FRESCO", "storytelling visuel + audio"),
        ],
        "leadership": [
            ("🐺 SLY", "tactique, coordination terrain"),
            ("🐢 BENTLEY", "planification tech, architecture"),
            ("🦛 MURRAY", "déploiement, force d'exécution"),
            ("🦅 OMEGA", "vision empire, arbitrage"),
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
        "imagination": ["imagin", "concept", "rêve", "vision", "inventer", "futuriste", "utopi"],
        "upwork": ["upwork", "proposal", "freelance", "gig", "mission", "connect", "jss", "top rated"],
        "benchmark_ia": ["benchmark", "evaluer", "comparer", "llm", "modele ia", "fine-tun", "scoring ia"],
        "automation": ["automat", "workflow", "n8n", "make", "zapier", "webhook", "trigger", "no-code"],
        "contournement": ["bloqu", "impossible", "payant", "interdit", "limit", "contourner", "bypass", "alternative", "gratuit", "scrap", "hack", "faille", "workaround", "plan b"],
        "legal": ["contrat", "juridique", "legal", "rgpd", "propriete intellectuelle", "licence", "cgv", "droits"],
        "audio": ["audio", "podcast", "son", "sound", "voix", "musique", "jingle", "mastering"],
        "leadership": ["leader", "chef", "diriger", "commander", "equipe", "management", "cooper gang"],
    }

    def __init__(self):
        self.modules = {}
        self.boot_time = datetime.now()
        self.personal = TitanPersonal()
        self._response_scores: list[dict] = []  # last 50 response quality scores
        self._think_count = 0

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

    def _smart_context(self, user_message: str) -> str:
        """Smart Context Window — pondéré par pertinence + récence.
        15 plus récents (toujours) + 10 les plus pertinents parmi les plus anciens.
        Résultat : contexte plus intelligent, même budget tokens."""
        all_convos = memory.get_recent_conversations(50)
        if not all_convos:
            return "Pas de conversation récente."

        # 15 plus récents — toujours présents
        recent = all_convos[-15:]

        # 10 les plus pertinents parmi les messages plus anciens
        older = all_convos[:-15]
        if older and user_message:
            keywords = set(user_message.lower().split())
            scored = []
            for conv in older:
                user_text = conv.get("user", "").lower()
                overlap = len(keywords & set(user_text.split()))
                if overlap > 0:
                    scored.append((overlap, conv))
            scored.sort(key=lambda x: x[0], reverse=True)
            relevant = [c for _, c in scored[:10]]
        else:
            relevant = []

        # Combiner : pertinents d'abord, puis récents
        combined = relevant + recent
        lines = []
        for conv in combined:
            lines.append(f"Augustin: {conv.get('user', '')}")
            lines.append(f"Titan: {conv.get('titan', '')}")
        return "\n".join(lines)

    def get_system_prompt(self, user_message: str = "") -> str:
        """Build the full system prompt with smart context.
        Memory injection: smart conversation history + personal profile + manual memories
        + auto-facts + contacts. Adaptive: lighter for trivial messages."""

        # Smart context window (relevant + recent)
        recent_context = self._smart_context(user_message)

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

        # Uptime
        uptime_min = int((datetime.now() - self.boot_time).total_seconds() // 60)

        return f"""{TITAN_PERSONALITY}

═══ PROFIL COMMANDANT ═══
{personal_profile}

═══ SYSTÈME ═══
Date: {datetime.now().strftime('%A %d %B %Y, %H:%M')}
Uptime: {uptime_min} min | Modules: {modules_list} | Messages: {self._think_count}

═══ MÉMOIRE ═══
{memory_summary if memory_summary else "(vide)"}

═══ FAITS APPRIS ═══
{auto_facts if auto_facts else "(aucun fait auto-extrait)"}

═══ CONTACTS ═══
{contacts_summary if contacts_summary else "(aucun)"}

═══ HISTORIQUE (smart context — recent + relevant) ═══
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
        """Process a message and generate a response.
        v2.0: Smart context, response scoring, performance tracking."""
        self._think_count += 1
        t0 = time.time()

        # Check for special commands first
        command_response = await self._handle_command(user_message)
        if command_response:
            memory.save_conversation(user_message, command_response, context)
            return command_response

        # Build messages with smart context (passes user message for relevance scoring)
        system = self.get_system_prompt(user_message)

        # Check if we need to use a specific module
        module_context = await self._get_module_context(user_message)

        # Agent cameo (~30% du temps, un agent du Building intervient)
        cameo = self._get_agent_cameo(user_message)

        content = user_message
        if module_context:
            content = f"{content}\n\n[DONNÉES MODULE]\n{module_context}"
        if cameo:
            content = f"{content}\n\n{cameo}"

        # Call AI (cascade: Ollama → Groq → Gemini)
        try:
            reply = ai_chat(system, content, CLAUDE_MAX_TOKENS)

            # Response quality scoring (local, zero cost)
            quality = _score_response(reply)
            elapsed_ms = (time.time() - t0) * 1000
            self._response_scores.append({
                "quality": quality,
                "latency_ms": round(elapsed_ms, 1),
                "msg_len": len(user_message),
                "reply_len": len(reply),
                "ts": datetime.now().isoformat(),
            })
            # Keep last 100 scores
            if len(self._response_scores) > 100:
                self._response_scores = self._response_scores[-100:]

            log.debug(f"Brain: Q={quality}, {elapsed_ms:.0f}ms, {len(reply)} chars")

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

    def get_performance_stats(self) -> dict:
        """Stats de performance du brain — pour le dashboard."""
        if not self._response_scores:
            return {"avg_quality": 0, "avg_latency_ms": 0, "total_thinks": self._think_count}
        scores = self._response_scores
        return {
            "avg_quality": round(sum(s["quality"] for s in scores) / len(scores), 1),
            "avg_latency_ms": round(sum(s["latency_ms"] for s in scores) / len(scores), 1),
            "total_thinks": self._think_count,
            "recent_scores": scores[-10:],
        }

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
