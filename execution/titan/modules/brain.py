"""
TITAN Brain — The Core Intelligence
Routes requests to the right module, maintains context, thinks.
This is JARVIS's brain.
"""

import json
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

    def __init__(self):
        self.modules = {}
        self.boot_time = datetime.now()
        self.personal = TitanPersonal()

    def register_module(self, name: str, module):
        """Register a capability module."""
        self.modules[name] = module

    def get_system_prompt(self) -> str:
        """Build the full system prompt with context."""
        # Get recent conversation context
        recent_context = memory.get_conversation_context(5)

        # Get relevant memories (manual)
        all_memories = memory.list_memories()
        memory_summary = ""
        if all_memories:
            mem_lines = [f"- {m['key']}: {m['value']}" for m in all_memories[:20]]
            memory_summary = "\n".join(mem_lines)

        # Get auto-extracted facts
        auto_facts_summary = memory.get_auto_facts_summary(20)

        # Get contacts
        contacts = memory.list_contacts()
        contacts_summary = ""
        if contacts:
            contact_lines = [f"- {c['name']}: {c.get('role', '')} {c.get('context', '')}" for c in contacts[:10]]
            contacts_summary = "\n".join(contact_lines)

        # Available commands
        commands = "\n".join([f"{cmd}: {desc}" for cmd, desc in TELEGRAM_COMMANDS.items()])

        # Available modules
        modules_list = ", ".join(self.modules.keys()) if self.modules else "aucun module chargé"

        # Personal profile
        personal_profile = self.personal.get_profile_for_brain()

        return f"""{TITAN_PERSONALITY}

=== QUI EST AUGUSTIN (profil personnel) ===
{personal_profile}

=== ÉTAT DU SYSTÈME ===
Date: {datetime.now().strftime('%A %d %B %Y, %H:%M')}
Uptime: {(datetime.now() - self.boot_time).seconds // 60} minutes
Modules actifs: {modules_list}

=== MÉMOIRE MANUELLE ===
{memory_summary if memory_summary else "Mémoire vide pour l'instant."}

=== FAITS MÉMORISÉS AUTOMATIQUEMENT ===
{auto_facts_summary if auto_facts_summary else "Aucun fait auto-mémorisé pour l'instant."}

=== CONTACTS CONNUS ===
{contacts_summary if contacts_summary else "Aucun contact en mémoire."}

=== CONVERSATION RÉCENTE ===
{recent_context}

=== TES DOMAINES D'EXPERTISE ===
Tu es expert de niveau mondial dans TOUTES ces disciplines:
- Psychologie (cognitive, sociale, clinique, du travail, positive)
- Psychanalyse (Freud, Jung, Lacan, mais aussi approches modernes)
- Neurosciences et fonctionnement du cerveau
- Philosophie (stoïcisme, existentialisme, pragmatisme)
- Économie et finance (macro, micro, marchés, crypto)
- Sciences (physique, biologie, chimie, astronomie)
- Géopolitique et histoire
- Business, stratégie, marketing, vente
- Technologie, IA, programmation
- Sport et performance physique
- Nutrition et santé
- Art, musique, cinéma, littérature

Tu utilises ces connaissances naturellement dans tes réponses quand c'est pertinent.
Tu fais des liens entre les domaines. Tu es le genre de personne qui cite Jung
puis enchaîne sur un conseil business, puis une ref à un film.

=== RÈGLES ===
1. Tu réponds TOUJOURS en français sauf si Augustin parle en anglais.
2. CLAIR ET CONCIS. Développe quand c'est pertinent, mais zéro remplissage.
3. Si on te demande quelque chose, FAIS-LE au lieu de dire "je peux le faire".
4. Tu peux poser des questions naturelles comme un pote, mais évite les questions de chatbot ("tu veux que je...", "tu veux en savoir plus ?").
5. Tu signes jamais tes messages. Tu parles naturellement.
6. MAX 2-3 emojis par message. Pas plus.
7. Si Augustin dit un prénom sans contexte, cherche d'abord dans les contacts mémorisés.
8. UTILISE LE PROFIL PERSONNEL pour personnaliser tes réponses.
9. Tu es son MEILLEUR AMI stratégique. Tu le pousses vers le haut, tu le challenges.
10. UNE réponse par message. Pas de spam. Pas de doublons.
11. Quand il parle d'un problème personnel, utilise ta connaissance en psychologie avec finesse.
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

        messages = [
            {"role": "user", "content": user_message}
        ]

        if module_context:
            messages[0]["content"] = f"{user_message}\n\n[DONNÉES MODULE]\n{module_context}"

        # Call AI (Gemini free or Anthropic fallback)
        try:
            reply = ai_chat(system, messages[0]["content"], CLAUDE_MAX_TOKENS)

            # Auto-extract and remember important info
            await self._auto_remember(user_message, reply)

            # Auto-learn personal info from conversation
            await self.personal.auto_learn(user_message, reply)

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

    async def _get_module_context(self, message: str) -> Optional[str]:
        """Detect which module might be relevant and get context.
        ONLY triggers on very explicit keywords to avoid spam."""
        # Disabled auto-context to keep responses clean and concise.
        # Modules are accessible via explicit /commands instead.
        return None

    async def _auto_remember(self, user_msg: str, reply: str):
        """Auto-detect things worth remembering from the conversation."""
        msg = user_msg.lower()
        now = datetime.now().isoformat()

        # --- Préférences & goûts ---
        prefs = [
            ("j'aime ", "goût"),
            ("j'adore ", "goût"),
            ("je préfère ", "préférence"),
            ("mon truc c'est ", "préférence"),
            ("ma passion ", "passion"),
        ]
        for trigger, cat in prefs:
            if trigger in msg:
                idx = msg.index(trigger)
                fact = user_msg[idx:idx + 80].strip().rstrip(".,!?")
                memory.save_auto_fact(fact, category=cat)

        # --- Infos personnelles ---
        personal_triggers = [
            ("j'habite ", "localisation"),
            ("je vis à ", "localisation"),
            ("je suis à ", "localisation"),
            ("je travaille sur ", "projet"),
            ("mon projet ", "projet"),
            ("mon client ", "client"),
            ("je bosse sur ", "projet"),
            ("j'ai un rdv ", "agenda"),
            ("rendez-vous ", "agenda"),
            ("mon objectif ", "objectif"),
            ("je veux ", "objectif"),
        ]
        for trigger, cat in personal_triggers:
            if trigger in msg:
                idx = msg.index(trigger)
                fact = user_msg[idx:idx + 100].strip().rstrip(".,!?")
                memory.save_auto_fact(fact, category=cat)

        # --- Décisions importantes ---
        decision_triggers = [
            ("j'ai décidé ", "décision"),
            ("j'ai choisi ", "décision"),
            ("on a décidé ", "décision"),
            ("je vais lancer ", "projet"),
            ("je lance ", "projet"),
        ]
        for trigger, cat in decision_triggers:
            if trigger in msg:
                idx = msg.index(trigger)
                fact = user_msg[idx:idx + 100].strip().rstrip(".,!?")
                memory.save_auto_fact(fact, category=cat)

        # --- Infos chiffrées (prix, revenus, objectifs) ---
        import re
        # Detect patterns like "X€", "X euros", "X$/mois", etc.
        money_pattern = re.compile(r'(\d[\d\s]*(?:€|euros?|k€|\$|usd)(?:/(?:mois|an|jour|semaine))?)', re.IGNORECASE)
        for match in money_pattern.finditer(user_msg):
            # Extract surrounding context (up to 80 chars)
            start = max(0, match.start() - 30)
            end = min(len(user_msg), match.end() + 30)
            snippet = user_msg[start:end].strip().rstrip(".,!?")
            memory.save_auto_fact(snippet, category="finances")

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

        # Finance
        if "finance" in self.modules:
            try:
                finance = await self.modules["finance"].get_crypto_brief()
                sections.append(f"\n💰 FINANCE\n{finance}")
            except Exception as e:
                sections.append(f"\n💰 FINANCE\nErreur: {e}")

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
