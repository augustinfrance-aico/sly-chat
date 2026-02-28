"""
CLASSROOM ENGINE — Moteur de la salle de classe multi-agents.
Orchestre les tours de parole, les modes de discussion, les débats.

3 modes :
  - free : discussion libre, agents prennent la parole tour par tour
  - interrogation : Augus interroge un agent spécifique
  - debate : président modère, chaque agent donne sa position, vote final

Isolation complète : n'importe jamais brain.py, utilise ai_client directement.
"""

import asyncio
import logging
import random
import time
from typing import Optional

log = logging.getLogger("titan.classroom.engine")

# Import léger — on n'importe PAS brain.py
try:
    from ..ai_client import chat as ask_ai
except ImportError:
    ask_ai = None

from .classroom_state import state
from .classroom_registry import (
    CLASSROOM_AGENTS,
    get_agent,
    get_all_agents,
    select_agents,
    POLE_COLORS,
)


def _agent_system_prompt(agent: dict, subject: str, mode: str) -> str:
    """Génère le system prompt pour un agent dans la classroom."""
    # 30% chance d'interpeller un autre agent
    interpellation = ""
    if random.random() < 0.30:
        others = [a["name"] for a in CLASSROOM_AGENTS if a["name"] != agent["name"]]
        if others:
            other = random.choice(others[:12])
            patterns = [
                f"- Tu peux mentionner {other} si son avis est pertinent (ex: 'Je confirme {other}', 'Comme dit {other}', '{other} a raison sur ce point')\n",
                f"- Si tu veux, rebondis sur ce que {other} pourrait penser (ex: '{other} dirait que...', 'Je suis d'accord avec {other}')\n",
                f"- Tu peux interpeller {other} naturellement (ex: '{other}, t'en penses quoi ?', 'Sur ce point {other} a vu juste')\n",
            ]
            interpellation = random.choice(patterns)

    return (
        f"Tu es {agent['name']}, un agent IA spécialisé dans : {agent['role']}.\n"
        f"Tu es dans la salle de classe AICO CLASSROOM.\n"
        f"Le sujet de discussion est : {subject}\n"
        f"Mode actuel : {mode}\n\n"
        f"RÈGLES :\n"
        f"- Réponds EN FRANÇAIS\n"
        f"- Maximum 2-3 phrases courtes\n"
        f"- Parle avec ta personnalité unique\n"
        f"- Ton expertise : {agent['role']}\n"
        f"- Si tu n'as rien de pertinent, dis 'RAS' en 5 mots max\n"
        f"- Ne répète JAMAIS ce qu'un autre agent a dit\n"
        f"- Sois direct, pas de blabla\n"
        f"{interpellation}"
    )


async def _get_agent_response(agent_name: str, subject: str, context: str = "", mode: str = "free") -> str:
    """Obtient la réponse d'un agent via l'IA."""
    agent = get_agent(agent_name)
    if not agent:
        return f"[{agent_name}] Agent inconnu."

    if ask_ai is None:
        return f"[{agent_name}] Module IA non disponible."

    system = _agent_system_prompt(agent, subject, mode)

    # Construire le message avec contexte
    user_msg = subject
    if context:
        user_msg = f"Contexte des interventions précédentes :\n{context}\n\nSujet : {subject}\n\nDonne ta réponse en tant que {agent_name}."

    try:
        response = await asyncio.wait_for(
            asyncio.to_thread(ask_ai, system, user_msg),
            timeout=15.0,  # 15s max par agent
        )
        return response.strip() if response else "..."
    except asyncio.TimeoutError:
        log.warning(f"Agent {agent_name} timeout after 15s")
        return f"[{agent_name}] Temps de réponse dépassé."
    except Exception as e:
        log.error(f"Agent {agent_name} error: {e}")
        return f"[{agent_name}] Erreur : {str(e)[:50]}"


def _build_context(messages: list[dict], max_messages: int = 10) -> str:
    """Construit le contexte des messages récents."""
    recent = messages[-max_messages:]
    lines = []
    for msg in recent:
        lines.append(f"{msg['agent']}: {msg['text']}")
    return "\n".join(lines)


# ============================================================
# MODE 1 — Discussion libre
# ============================================================

async def run_free_discussion(subject: str, agents: list[str], rounds: int = 1) -> list[dict]:
    """
    Discussion libre : chaque agent prend la parole tour à tour.
    1 réponse à la fois, pas de chaos.
    """
    results = []
    state.start(subject=subject, mode="free", agents=agents)

    for round_num in range(rounds):
        # Shuffle pour varier l'ordre
        order = agents.copy()
        if round_num > 0:
            random.shuffle(order)

        for agent_name in order:
            if state.is_over_limit() or state.paused:
                break

            state.set_speaking(agent_name)
            context = _build_context(state.messages)
            response = await _get_agent_response(agent_name, subject, context, "free")

            msg = {
                "agent": agent_name,
                "text": response,
                "role": "agent",
                "round": round_num,
            }
            state.add_message(agent_name, response)
            results.append(msg)
            state.set_speaking(None)

    state.save()
    return results


# ============================================================
# MODE 2 — Interrogation ciblée
# ============================================================

async def interrogate_agent(agent_name: str, question: str) -> dict:
    """
    Augus interroge un agent spécifique.
    Réponse individuelle.
    """
    if not state.active:
        state.start(subject=question, mode="interrogation", agents=[agent_name])

    state.set_speaking(agent_name)

    # Ajouter la question d'Augus
    state.add_message("AUGUS", question, role="user")

    context = _build_context(state.messages)
    response = await _get_agent_response(agent_name, question, context, "interrogation")

    state.add_message(agent_name, response)
    state.set_speaking(None)
    state.save()

    return {
        "agent": agent_name,
        "question": question,
        "response": response,
    }


# ============================================================
# MODE 3 — Débat structuré
# ============================================================

async def run_debate(subject: str, agents: list[str], max_rounds: int = 2) -> dict:
    """
    Débat structuré :
    1. Président (OMEGA) introduit
    2. Chaque agent donne sa position
    3. Réponses croisées (round 2)
    4. Vote final
    """
    state.start(subject=subject, mode="debate", agents=agents)
    president = state.president
    results = {"subject": subject, "phases": [], "votes": {}}

    # Phase 1 : Introduction par le président
    state.set_speaking(president)
    intro_prompt = f"Tu es {president}, le président du débat. Introduis le sujet en 2 phrases max : {subject}"
    intro = await _get_agent_response(president, intro_prompt, "", "debate")
    state.add_message(president, intro, role="system")
    results["phases"].append({"phase": "introduction", "agent": president, "text": intro})
    state.set_speaking(None)

    # Phase 2 : Positions individuelles
    positions = []
    for agent_name in agents:
        if agent_name == president:
            continue
        if state.is_over_limit():
            break

        state.set_speaking(agent_name)
        context = _build_context(state.messages, max_messages=5)
        response = await _get_agent_response(
            agent_name,
            f"Donne ta position sur : {subject}",
            context,
            "debate",
        )
        state.add_message(agent_name, response)
        positions.append({"agent": agent_name, "text": response})
        state.set_speaking(None)

    results["phases"].append({"phase": "positions", "entries": positions})

    # Phase 3 : Réponses croisées (round 2 si max_rounds > 1)
    if max_rounds > 1:
        rebuttals = []
        # Sélectionner 3-4 agents pour les réponses croisées
        debaters = random.sample(agents, min(4, len(agents)))
        for agent_name in debaters:
            if state.is_over_limit():
                break

            state.set_speaking(agent_name)
            context = _build_context(state.messages, max_messages=8)
            response = await _get_agent_response(
                agent_name,
                f"Réagis aux positions des autres sur : {subject}. Sois bref, 1-2 phrases.",
                context,
                "debate",
            )
            state.add_message(agent_name, response)
            rebuttals.append({"agent": agent_name, "text": response})
            state.set_speaking(None)

        results["phases"].append({"phase": "rebuttals", "entries": rebuttals})

    # Phase 4 : Vote
    vote_options = ["POUR", "CONTRE", "NUANCÉ"]
    for agent_name in agents:
        vote = random.choice(vote_options)
        results["votes"][agent_name] = vote

    # Conclusion du président
    state.set_speaking(president)
    votes_summary = ", ".join(f"{k}:{v}" for k, v in results["votes"].items())
    conclusion = await _get_agent_response(
        president,
        f"Résume le débat en 2 phrases. Votes : {votes_summary}",
        _build_context(state.messages, max_messages=5),
        "debate",
    )
    state.add_message(president, conclusion, role="system")
    results["phases"].append({"phase": "conclusion", "agent": president, "text": conclusion})
    state.set_speaking(None)

    state.save()
    return results


# ============================================================
# COMMANDES CLASSROOM (pour Telegram ou API)
# ============================================================

async def handle_command(command: str, args: str = "") -> str:
    """Gère les commandes classroom depuis Telegram ou API."""

    if command == "start":
        agents = [a["name"] for a in CLASSROOM_AGENTS[:12]]
        subject = args or "Briefing général AICO"
        results = await run_free_discussion(subject, agents, rounds=1)
        lines = [f"🎓 CLASSROOM — {subject}\n"]
        for r in results:
            agent = get_agent(r["agent"])
            emoji = agent["emoji"] if agent else "❓"
            lines.append(f"{emoji} {r['agent']} : {r['text']}")
        return "\n".join(lines)

    elif command == "ask":
        parts = args.split(" ", 1)
        if len(parts) < 2:
            return "Usage : /classroom-ask AGENT question"
        agent_name = parts[0].upper()
        question = parts[1]
        result = await interrogate_agent(agent_name, question)
        agent = get_agent(agent_name)
        emoji = agent["emoji"] if agent else "❓"
        return f"{emoji} {agent_name} : {result['response']}"

    elif command == "debate":
        agents = [a["name"] for a in CLASSROOM_AGENTS[:8]]
        subject = args or "Quelle stratégie pour AICO en 2026 ?"
        result = await run_debate(subject, agents)
        lines = [f"⚖️ DÉBAT — {subject}\n"]
        for phase in result["phases"]:
            if phase["phase"] == "introduction":
                lines.append(f"🎙️ {phase['agent']} : {phase['text']}\n")
            elif phase["phase"] in ("positions", "rebuttals"):
                for entry in phase.get("entries", []):
                    agent = get_agent(entry["agent"])
                    emoji = agent["emoji"] if agent else "❓"
                    lines.append(f"{emoji} {entry['agent']} : {entry['text']}")
                lines.append("")
            elif phase["phase"] == "conclusion":
                lines.append(f"\n🏁 {phase['agent']} : {phase['text']}")

        # Votes
        lines.append("\n📊 VOTES :")
        for agent_name, vote in result["votes"].items():
            lines.append(f"  {agent_name}: {vote}")

        return "\n".join(lines)

    elif command == "stop":
        state.stop()
        return "🎓 Classroom arrêtée."

    elif command == "status":
        if not state.active:
            return "🎓 Classroom inactive."
        d = state.to_dict()
        return (
            f"🎓 Classroom active\n"
            f"Mode : {d['mode']}\n"
            f"Sujet : {d['subject']}\n"
            f"Agents : {len(d['seated_agents'])}\n"
            f"Tours : {d['turn_count']}/{d['max_turns']}\n"
            f"Parle : {d['speaking_agent'] or 'personne'}\n"
            f"Durée : {d['elapsed_s']}s"
        )

    else:
        return (
            "🎓 AICO CLASSROOM — Commandes :\n"
            "/classroom-start [sujet] — Lancer discussion libre\n"
            "/classroom-ask AGENT question — Interroger un agent\n"
            "/classroom-debate [sujet] — Débat structuré avec vote\n"
            "/classroom-stop — Arrêter la session\n"
            "/classroom-status — État actuel"
        )
