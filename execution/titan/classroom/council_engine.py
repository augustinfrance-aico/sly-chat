"""
GRAND CONSEIL — Table ronde stratégique à 12 agents.

Mode premium de la Classroom AICO.
- 12 agents max autour d'une table circulaire
- Lumière centrale (Titan Core)
- Duels entre agents
- Forcer un agent à argumenter l'opposé
- Vote pondéré par expertise
- Score de conviction (0-100)
- Rapport stratégique synthétisé + plan d'action

Isolation complète — n'importe pas brain.py.
"""

import asyncio
import logging
import random
import time
from typing import Optional

log = logging.getLogger("titan.classroom.council")

try:
    from ..ai_client import chat as ai_chat
except ImportError:
    ai_chat = None

from .classroom_registry import (
    CLASSROOM_AGENTS,
    get_agent,
    select_agents,
    POLE_COLORS,
)
from .council_state import council_state


# === EXPERTISE WEIGHTS (pour votes pondérés) ===
EXPERTISE_WEIGHTS = {
    # Domaine → agents qui ont le plus de poids
    "strategie":    {"OMEGA": 3, "CORTEX": 3, "SIBYL": 2, "SENTINEL": 2, "GLITCH": 1},
    "vente":        {"CLOSER": 3, "KAISER": 3, "PRISM": 2, "ONYX": 2, "LEDGER": 2},
    "tech":         {"ANVIL": 3, "VOLT": 3, "SPECTER": 2, "PULSE": 2, "DATUM": 1},
    "contenu":      {"PHILOMÈNE": 3, "FRESCO": 2, "VIRAL": 2, "FRANKLIN": 2, "PIXEL": 1},
    "croissance":   {"RACOON": 3, "VIRAL": 2, "NICHE": 2, "CLOSER": 2, "GLITCH": 1},
    "finance":      {"LEDGER": 3, "DATUM": 2, "PRISM": 2, "ONYX": 1, "CORTEX": 1},
    "innovation":   {"CIPHER": 3, "RADAR": 2, "PROTO": 2, "GLITCH": 2, "SIBYL": 1},
    "risque":       {"SPECTER": 3, "DREYFUS": 2, "HAVOC": 2, "SHADOW": 3, "DATUM": 1},
    "general":      {},  # poids égal pour tout le monde
}

# Sièges de la table ronde (positions en degrés, 0=nord)
TABLE_POSITIONS = {i: (i * 30) % 360 for i in range(12)}


def _detect_domain(subject: str) -> str:
    """Détecte le domaine à partir du sujet."""
    subject_lower = subject.lower()
    domain_keywords = {
        "strategie": ["strateg", "vision", "direction", "plan", "objectif", "roadmap", "pivot"],
        "vente": ["vente", "client", "deal", "prix", "offre", "prospect", "contrat", "closing"],
        "tech": ["code", "bug", "api", "deploy", "tech", "système", "archi", "module"],
        "contenu": ["contenu", "post", "email", "copy", "branding", "video", "story"],
        "croissance": ["growth", "lead", "acquisition", "scale", "outreach", "linkedin"],
        "finance": ["revenu", "budget", "coût", "marge", "rentab", "invest", "argent"],
        "innovation": ["innov", "ia", "futur", "research", "rdlab", "proto", "experiment"],
        "risque": ["risque", "sécurité", "danger", "menace", "audit", "faille"],
    }
    for domain, keywords in domain_keywords.items():
        if any(kw in subject_lower for kw in keywords):
            return domain
    return "general"


def _get_expertise_weight(agent_name: str, domain: str) -> int:
    """Retourne le poids d'expertise d'un agent pour un domaine (1 par défaut)."""
    weights = EXPERTISE_WEIGHTS.get(domain, {})
    return weights.get(agent_name, 1)


def _council_system_prompt(agent: dict, subject: str, role_override: str = "") -> str:
    """System prompt pour un agent au Grand Conseil."""
    role = role_override or agent["role"]
    return (
        f"Tu es {agent['name']}, expert en : {role}.\n"
        f"Tu sièges au GRAND CONSEIL — table ronde stratégique de 12 agents.\n"
        f"Le sujet : {subject}\n\n"
        f"RÈGLES DU CONSEIL :\n"
        f"- Maximum 2-3 phrases percutantes\n"
        f"- Parle avec autorité et conviction\n"
        f"- Donne ton avis tranché — pas de 'ça dépend'\n"
        f"- Apporte UN angle unique basé sur ton expertise\n"
        f"- Si tu contredis un autre, nomme-le et dis pourquoi\n"
        f"- Français. Direct. Zéro blabla.\n"
    )


def _duel_system_prompt(agent: dict, opponent_name: str, opponent_position: str, subject: str) -> str:
    """System prompt pour un duel entre deux agents."""
    return (
        f"Tu es {agent['name']}, expert en : {agent['role']}.\n"
        f"Tu es en DUEL au Grand Conseil contre {opponent_name}.\n"
        f"Sa position : \"{opponent_position}\"\n"
        f"Sujet : {subject}\n\n"
        f"RÈGLES DU DUEL :\n"
        f"- Réfute son argument avec des faits/logique\n"
        f"- Propose une alternative concrète\n"
        f"- 2-3 phrases max, percutantes\n"
        f"- Nomme ton adversaire quand tu le contredis\n"
        f"- Pas d'accord mou — tranche !\n"
    )


def _reverse_system_prompt(agent: dict, original_position: str, subject: str) -> str:
    """System prompt pour forcer un agent à argumenter l'opposé."""
    return (
        f"Tu es {agent['name']}, mais tu dois ARGUMENTER L'OPPOSÉ de ta position initiale.\n"
        f"Ta position originale : \"{original_position}\"\n"
        f"Sujet : {subject}\n\n"
        f"EXERCICE DE PENSÉE INVERSE :\n"
        f"- Trouve les meilleurs arguments CONTRE ta propre position\n"
        f"- Sois aussi convaincant que possible\n"
        f"- 2-3 phrases, comme si tu y croyais vraiment\n"
        f"- Commence par 'En réalité...' ou 'L'argument inverse...'\n"
    )


async def _ask_agent(system: str, user_msg: str, timeout: float = 15.0) -> str:
    """Appel IA pour un agent du Conseil."""
    if ai_chat is None:
        return "[Module IA non disponible]"
    try:
        response = await asyncio.wait_for(
            asyncio.to_thread(ai_chat, system, user_msg, 512),
            timeout=timeout,
        )
        return response.strip() if response else "..."
    except asyncio.TimeoutError:
        return "[Temps dépassé]"
    except Exception as e:
        log.error(f"Council AI error: {e}")
        return f"[Erreur: {str(e)[:40]}]"


def _conviction_score(text: str) -> int:
    """Score de conviction 0-100 basé sur la réponse.
    Heuristique locale, zero cost."""
    score = 50
    text_lower = text.lower()
    length = len(text)

    # Longueur (trop court = faible conviction)
    if length < 20:
        score -= 20
    elif length > 60:
        score += 10

    # Mots forts → haute conviction
    strong_words = ["absolument", "certain", "évident", "crucial", "impératif",
                    "fondamental", "critique", "essentiel", "sans doute", "clairement",
                    "il faut", "on doit", "priorité", "urgence", "maintenant"]
    score += sum(5 for w in strong_words if w in text_lower)

    # Mots faibles → basse conviction
    weak_words = ["peut-être", "éventuellement", "ça dépend", "pas sûr",
                  "je ne sais pas", "possiblement", "on verra"]
    score -= sum(8 for w in weak_words if w in text_lower)

    # Structure (arguments numérotés = +)
    if any(f"{i}." in text or f"{i})" in text for i in range(1, 5)):
        score += 10

    # Ponctuation forte
    score += text.count("!") * 3
    score -= text.count("?") * 5

    return min(100, max(0, score))


# ============================================================
# PHASE 1 — Convocation du Conseil
# ============================================================

def select_council(subject: str, requested_agents: list[str] | None = None) -> list[dict]:
    """Sélectionne les 12 agents pour le Conseil.
    Si pas de requête spécifique, sélection intelligente basée sur le domaine."""
    if requested_agents:
        selected = [a for a in CLASSROOM_AGENTS if a["name"] in requested_agents]
        return selected[:12]

    domain = _detect_domain(subject)

    # Toujours inclure OMEGA (président) et FRANKLIN (synthèse)
    mandatory = ["OMEGA", "FRANKLIN"]

    # Top agents pour le domaine
    domain_weights = EXPERTISE_WEIGHTS.get(domain, {})
    weighted_agents = sorted(domain_weights.items(), key=lambda x: x[1], reverse=True)
    domain_picks = [name for name, _ in weighted_agents if name not in mandatory][:6]

    # Compléter avec des profils diversifiés
    all_names = [a["name"] for a in CLASSROOM_AGENTS]
    remaining = [n for n in all_names if n not in mandatory and n not in domain_picks]
    random.shuffle(remaining)
    fillers = remaining[:12 - len(mandatory) - len(domain_picks)]

    council_names = mandatory + domain_picks + fillers
    return [a for a in CLASSROOM_AGENTS if a["name"] in council_names][:12]


# ============================================================
# PHASE 2 — Tour de table
# ============================================================

async def run_tour_de_table(subject: str, agents: list[dict]) -> list[dict]:
    """Chaque agent donne sa position initiale. Séquentiel pour cohérence."""
    council_state.start(subject=subject, agents=[a["name"] for a in agents])
    results = []
    context_lines = []

    for agent in agents:
        system = _council_system_prompt(agent, subject)
        context = "\n".join(context_lines[-6:]) if context_lines else ""
        user_msg = f"Sujet : {subject}"
        if context:
            user_msg = f"Positions précédentes :\n{context}\n\nSujet : {subject}\nTa position :"

        council_state.set_speaking(agent["name"])
        response = await _ask_agent(system, user_msg)
        conviction = _conviction_score(response)

        entry = {
            "agent": agent["name"],
            "emoji": agent["emoji"],
            "pole": agent["pole"],
            "text": response,
            "conviction": conviction,
            "weight": _get_expertise_weight(agent["name"], _detect_domain(subject)),
            "seat": agents.index(agent),
        }
        results.append(entry)
        council_state.add_position(agent["name"], response, conviction)
        context_lines.append(f"{agent['name']}: {response}")
        council_state.set_speaking(None)

    return results


# ============================================================
# PHASE 3 — Duel
# ============================================================

async def run_duel(agent1_name: str, agent2_name: str, subject: str) -> dict:
    """Duel entre deux agents — chacun réfute l'autre."""
    a1 = get_agent(agent1_name)
    a2 = get_agent(agent2_name)
    if not a1 or not a2:
        return {"error": "Agent(s) inconnu(s)"}

    # Récupérer positions existantes
    a1_pos = council_state.get_position(agent1_name)
    a2_pos = council_state.get_position(agent2_name)

    # Agent 1 attaque Agent 2
    system1 = _duel_system_prompt(a1, agent2_name, a2_pos or "position inconnue", subject)
    council_state.set_speaking(agent1_name)
    attack1 = await _ask_agent(system1, f"Réfute la position de {agent2_name} sur : {subject}")
    conv1 = _conviction_score(attack1)

    # Agent 2 riposte
    system2 = _duel_system_prompt(a2, agent1_name, attack1, subject)
    council_state.set_speaking(agent2_name)
    attack2 = await _ask_agent(system2, f"Riposte à {agent1_name} : \"{attack1}\"")
    conv2 = _conviction_score(attack2)

    council_state.set_speaking(None)
    council_state.add_duel(agent1_name, agent2_name, attack1, attack2, conv1, conv2)

    winner = agent1_name if conv1 >= conv2 else agent2_name

    return {
        "agent1": {"name": agent1_name, "emoji": a1["emoji"], "attack": attack1, "conviction": conv1},
        "agent2": {"name": agent2_name, "emoji": a2["emoji"], "attack": attack2, "conviction": conv2},
        "winner": winner,
        "margin": abs(conv1 - conv2),
    }


# ============================================================
# PHASE 4 — Argument opposé forcé
# ============================================================

async def force_reverse(agent_name: str, subject: str) -> dict:
    """Force un agent à argumenter l'opposé de sa position."""
    agent = get_agent(agent_name)
    if not agent:
        return {"error": "Agent inconnu"}

    original = council_state.get_position(agent_name)
    if not original:
        return {"error": f"{agent_name} n'a pas encore donné sa position"}

    system = _reverse_system_prompt(agent, original, subject)
    council_state.set_speaking(agent_name)
    response = await _ask_agent(system, f"Argumente l'opposé de ta position sur : {subject}")
    conviction = _conviction_score(response)
    council_state.set_speaking(None)

    council_state.add_reverse(agent_name, original, response, conviction)

    return {
        "agent": agent_name,
        "emoji": agent["emoji"],
        "original_position": original,
        "reverse_position": response,
        "reverse_conviction": conviction,
    }


# ============================================================
# PHASE 5 — Vote pondéré
# ============================================================

async def run_weighted_vote(subject: str, options: list[str] | None = None) -> dict:
    """Vote pondéré par expertise. Chaque agent vote, poids selon domaine."""
    if not council_state.active:
        return {"error": "Conseil pas actif"}

    agents = council_state.seated_agents
    domain = _detect_domain(subject)
    options = options or ["POUR", "CONTRE", "NUANCÉ"]

    votes = {}
    total_weight = 0
    weighted_results = {opt: 0 for opt in options}

    for agent_name in agents:
        agent = get_agent(agent_name)
        if not agent:
            continue

        weight = _get_expertise_weight(agent_name, domain)
        position = council_state.get_position(agent_name)
        conviction = council_state.get_conviction(agent_name)

        # L'agent vote via IA
        system = (
            f"Tu es {agent_name}. Tu votes sur : {subject}\n"
            f"Ta position était : \"{position or 'non exprimée'}\"\n"
            f"Options : {', '.join(options)}\n"
            f"Réponds UNIQUEMENT par une des options. Un seul mot."
        )
        council_state.set_speaking(agent_name)
        raw_vote = await _ask_agent(system, f"Ton vote ? ({'/'.join(options)})")
        council_state.set_speaking(None)

        # Parser le vote
        chosen = options[0]  # default
        raw_upper = raw_vote.upper().strip()
        for opt in options:
            if opt.upper() in raw_upper:
                chosen = opt
                break

        # Conviction booste le poids (+0-50%)
        conviction_bonus = (conviction or 50) / 200  # 0 → 0, 100 → 0.5
        effective_weight = weight * (1 + conviction_bonus)

        votes[agent_name] = {
            "vote": chosen,
            "weight": weight,
            "conviction": conviction or 50,
            "effective_weight": round(effective_weight, 2),
        }
        weighted_results[chosen] += effective_weight
        total_weight += effective_weight

    # Normaliser les résultats
    percentages = {}
    for opt in options:
        percentages[opt] = round((weighted_results[opt] / total_weight * 100) if total_weight else 0, 1)

    winner = max(percentages, key=percentages.get)

    council_state.set_vote_results(votes, percentages, winner)

    return {
        "subject": subject,
        "domain": domain,
        "votes": votes,
        "percentages": percentages,
        "winner": winner,
        "total_weight": round(total_weight, 2),
        "agents_count": len(votes),
    }


# ============================================================
# PHASE 6 — Rapport stratégique
# ============================================================

async def generate_report(subject: str) -> dict:
    """Génère le rapport stratégique final — OMEGA synthétise tout."""
    if not council_state.active:
        return {"error": "Conseil pas actif"}

    data = council_state.to_dict()
    positions = data.get("positions", {})
    duels = data.get("duels", [])
    reverses = data.get("reverses", [])
    vote = data.get("vote_results", {})

    # Résumé des positions
    pos_summary = "\n".join(
        f"- {name}: {p['text'][:100]} (conviction: {p['conviction']})"
        for name, p in positions.items()
    )

    # Résumé des duels
    duel_summary = "\n".join(
        f"- {d['agent1']} vs {d['agent2']}: gagnant conviction {d['winner']}"
        for d in duels
    ) if duels else "Aucun duel"

    # Résumé des reverses
    rev_summary = "\n".join(
        f"- {r['agent']}: position inversée — {r['reverse'][:80]}"
        for r in reverses
    ) if reverses else "Aucun reverse"

    # Résumé du vote
    vote_text = ""
    if vote:
        vote_text = f"Vote: {vote.get('winner', '?')} ({vote.get('percentages', {})})"

    # OMEGA rédige le rapport
    system = (
        "Tu es OMEGA, le directeur stratégique de l'empire AICO.\n"
        "Tu rédiges le RAPPORT STRATÉGIQUE du Grand Conseil.\n\n"
        "FORMAT OBLIGATOIRE :\n"
        "📋 SYNTHÈSE (2-3 phrases — l'essentiel)\n"
        "⚡ DÉCISION (la conclusion du Conseil)\n"
        "📌 PLAN D'ACTION (3-5 actions concrètes numérotées)\n"
        "⚠️ RISQUES (1-2 risques identifiés)\n"
        "🎯 PROCHAINE ÉTAPE (1 action immédiate)\n\n"
        "Sois concis, stratégique, actionnable. Français."
    )

    user_msg = (
        f"SUJET : {subject}\n\n"
        f"POSITIONS DES AGENTS :\n{pos_summary}\n\n"
        f"DUELS :\n{duel_summary}\n\n"
        f"ARGUMENTS INVERSÉS :\n{rev_summary}\n\n"
        f"VOTE PONDÉRÉ :\n{vote_text}\n\n"
        f"Rédige le rapport stratégique final."
    )

    report_text = await _ask_agent(system, user_msg, timeout=25.0)

    # FRANKLIN résume
    franklin_system = (
        "Tu es FRANKLIN. Résume ce rapport en 2 phrases ultra-claires pour Augus. "
        "Pas de jargon. L'essentiel uniquement."
    )
    franklin_summary = await _ask_agent(franklin_system, report_text, timeout=10.0)

    report = {
        "subject": subject,
        "report": report_text,
        "franklin_summary": franklin_summary,
        "stats": {
            "agents_count": len(positions),
            "duels_count": len(duels),
            "reverses_count": len(reverses),
            "vote_winner": vote.get("winner", "N/A"),
            "avg_conviction": round(
                sum(p["conviction"] for p in positions.values()) / max(len(positions), 1)
            ),
        },
        "generated_at": time.time(),
    }

    council_state.set_report(report)
    return report


# ============================================================
# FULL COUNCIL SESSION — Tout en un
# ============================================================

async def run_full_council(subject: str, requested_agents: list[str] | None = None) -> dict:
    """Session complète du Grand Conseil :
    1. Convocation (12 agents)
    2. Tour de table
    3. Vote pondéré
    4. Rapport stratégique
    """
    # 1. Convocation
    agents = select_council(subject, requested_agents)

    # 2. Tour de table
    positions = await run_tour_de_table(subject, agents)

    # 3. Vote pondéré
    vote = await run_weighted_vote(subject)

    # 4. Rapport
    report = await generate_report(subject)

    return {
        "subject": subject,
        "agents": [{"name": a["name"], "emoji": a["emoji"], "pole": a["pole"]} for a in agents],
        "positions": positions,
        "vote": vote,
        "report": report,
        "session_id": council_state.session_id,
    }


# ============================================================
# COMMANDES TELEGRAM
# ============================================================

async def handle_command(command: str, args: str = "") -> str:
    """Gère les commandes Grand Conseil depuis Telegram ou API."""

    if command == "start":
        subject = args or "Stratégie AICO — prochaine étape"
        result = await run_full_council(subject)

        lines = [f"⚜️ GRAND CONSEIL — {subject}\n"]

        # Positions
        lines.append("━━━ TOUR DE TABLE ━━━")
        for p in result["positions"]:
            bar = "█" * (p["conviction"] // 10) + "░" * (10 - p["conviction"] // 10)
            lines.append(f"{p['emoji']} {p['agent']} [{bar}] {p['conviction']}%")
            lines.append(f"   {p['text'][:120]}\n")

        # Vote
        v = result["vote"]
        lines.append("━━━ VOTE PONDÉRÉ ━━━")
        for opt, pct in v.get("percentages", {}).items():
            lines.append(f"  {opt}: {pct}%")
        lines.append(f"  → Décision : {v.get('winner', '?')}\n")

        # Rapport
        lines.append("━━━ RAPPORT STRATÉGIQUE ━━━")
        lines.append(result["report"].get("report", "Pas de rapport."))
        lines.append(f"\n💎 FRANKLIN : {result['report'].get('franklin_summary', '')}")

        return "\n".join(lines)

    elif command == "duel":
        parts = args.split(" ", 2)
        if len(parts) < 2:
            return "Usage : /conseil-duel AGENT1 AGENT2 [sujet]"
        a1, a2 = parts[0].upper(), parts[1].upper()
        subject = parts[2] if len(parts) > 2 else council_state.subject or "Débat libre"
        result = await run_duel(a1, a2, subject)
        if "error" in result:
            return f"❌ {result['error']}"
        d = result
        return (
            f"⚔️ DUEL — {d['agent1']['name']} vs {d['agent2']['name']}\n\n"
            f"{d['agent1']['emoji']} {d['agent1']['name']} ({d['agent1']['conviction']}%) :\n"
            f"  {d['agent1']['attack']}\n\n"
            f"{d['agent2']['emoji']} {d['agent2']['name']} ({d['agent2']['conviction']}%) :\n"
            f"  {d['agent2']['attack']}\n\n"
            f"🏆 Gagnant : {d['winner']} (+{d['margin']}pts)"
        )

    elif command == "reverse":
        agent_name = args.strip().upper() if args else ""
        if not agent_name:
            return "Usage : /conseil-reverse AGENT"
        subject = council_state.subject or "Sujet du Conseil"
        result = await force_reverse(agent_name, subject)
        if "error" in result:
            return f"❌ {result['error']}"
        return (
            f"🔄 ARGUMENT INVERSÉ — {result['emoji']} {result['agent']}\n\n"
            f"Position originale :\n  {result['original_position']}\n\n"
            f"Position inversée ({result['reverse_conviction']}%) :\n  {result['reverse_position']}"
        )

    elif command == "vote":
        subject = council_state.subject or args or "Vote libre"
        result = await run_weighted_vote(subject)
        if "error" in result:
            return f"❌ {result['error']}"
        lines = [f"📊 VOTE PONDÉRÉ — {subject}\n"]
        for name, v in result["votes"].items():
            agent = get_agent(name)
            emoji = agent["emoji"] if agent else "❓"
            lines.append(f"{emoji} {name}: {v['vote']} (poids: {v['effective_weight']})")
        lines.append(f"\n→ {result['winner']} l'emporte ({result['percentages']})")
        return "\n".join(lines)

    elif command == "report":
        subject = council_state.subject or "Stratégie AICO"
        result = await generate_report(subject)
        if "error" in result:
            return f"❌ {result['error']}"
        return (
            f"📋 RAPPORT STRATÉGIQUE\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n"
            f"{result['report']}\n\n"
            f"💎 FRANKLIN : {result['franklin_summary']}\n\n"
            f"📊 Stats : {result['stats']['agents_count']} agents, "
            f"{result['stats']['duels_count']} duels, "
            f"conviction moy. {result['stats']['avg_conviction']}%"
        )

    elif command == "stop":
        council_state.stop()
        return "⚜️ Grand Conseil terminé."

    elif command == "status":
        if not council_state.active:
            return "⚜️ Grand Conseil inactif."
        d = council_state.to_dict()
        return (
            f"⚜️ Grand Conseil actif\n"
            f"Sujet : {d['subject']}\n"
            f"Agents : {len(d['seated_agents'])}\n"
            f"Positions : {len(d['positions'])}\n"
            f"Duels : {len(d['duels'])}\n"
            f"Vote : {'oui' if d.get('vote_results') else 'non'}\n"
            f"Durée : {d.get('elapsed_s', 0)}s"
        )

    else:
        return (
            "⚜️ GRAND CONSEIL — Commandes :\n"
            "/conseil [sujet] — Lancer un Grand Conseil complet\n"
            "/conseil-duel AGENT1 AGENT2 — Duel entre deux agents\n"
            "/conseil-reverse AGENT — Forcer argument opposé\n"
            "/conseil-vote — Vote pondéré\n"
            "/conseil-report — Rapport stratégique\n"
            "/conseil-stop — Terminer le Conseil\n"
            "/conseil-status — État actuel"
        )
