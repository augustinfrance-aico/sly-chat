"""
AGENT ROUTER — Moteur d'auto-sélection des experts
Analyse le message d'Augus et retourne les agents pertinents avec leur voix.

Usage dans Claude Code :
    from agents.agent_router import route, format_council

    agents = route("je veux faire un post LinkedIn et pitcher mon service")
    print(format_council(agents))
"""

import re
from typing import List, Dict
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.agent_profiles import AGENTS


def _normalize(text: str) -> str:
    """Lowercase + suppression accents basique pour matching."""
    text = text.lower()
    replacements = {
        'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
        'à': 'a', 'â': 'a', 'ä': 'a',
        'ù': 'u', 'û': 'u', 'ü': 'u',
        'î': 'i', 'ï': 'i',
        'ô': 'o', 'ö': 'o',
        'ç': 'c',
    }
    for accent, plain in replacements.items():
        text = text.replace(accent, plain)
    return text


def route(message: str) -> List[Dict]:
    """
    Analyse le message et retourne TOUS les agents pertinents.
    Pas de limite — on vise l'excellence, pas la concision.

    Returns: liste de dicts {name, specialty, voice, score}
    """
    msg_normalized = _normalize(message)
    words = set(re.findall(r'\b\w+\b', msg_normalized))

    scored = []

    for agent_name, profile in AGENTS.items():
        score = 0
        matched_triggers = []

        for trigger in profile["triggers"]:
            trigger_norm = _normalize(trigger)
            # Match exact phrase ou mot isolé
            if trigger_norm in msg_normalized:
                score += 2
                matched_triggers.append(trigger)
            else:
                # Match partiel sur les mots du trigger
                trigger_words = set(trigger_norm.split())
                overlap = trigger_words & words
                if overlap and len(overlap) / len(trigger_words) >= 0.6:
                    score += 1
                    matched_triggers.append(trigger)

        if score > 0:
            scored.append({
                "name": agent_name,
                "specialty": profile["specialty"],
                "voice": profile["voice"],
                "score": score,
                "matched": matched_triggers[:3],  # pour debug
            })

    # Trier par score décroissant
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored


def format_council(agents: List[Dict], message: str = "") -> str:
    """
    Formate la réponse du conseil d'agents activés.
    Chaque agent se présente avec sa voix + sa mission sur cette demande.
    """
    if not agents:
        return ""

    lines = []
    lines.append(f"━━━ CONSEIL ACTIVÉ — {len(agents)} AGENT(S) ━━━\n")

    for agent in agents:
        lines.append(f"▸ **{agent['name']}** — {agent['specialty']}")
        lines.append(f"  {agent['voice']}\n")

    lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    return "\n".join(lines)


def format_brief(agents: List[Dict]) -> str:
    """
    Version courte — juste les noms et leurs rôles sur cette mission.
    Pour injection en system prompt.
    """
    if not agents:
        return ""

    lines = ["=== AGENTS ACTIVÉS SUR CETTE DEMANDE ==="]
    for a in agents:
        lines.append(f"[{a['name']}] {a['specialty']}")
        lines.append(f"  Voix : {a['voice'].split(chr(10))[0]}")
    lines.append("")
    lines.append("Tu intègres la perspective de CHACUN de ces agents dans ta réponse.")
    lines.append("Chaque agent apporte son angle spécifique. Tu fondes en un seul output cohérent.")
    lines.append("==========================================")

    return "\n".join(lines)


if __name__ == "__main__":
    # Test rapide
    test_messages = [
        "je veux faire un post LinkedIn pour montrer mes 25 agents",
        "urgent mon script python plante en prod",
        "comment je structure mon pipeline KDP cette semaine",
        "j'hésite sur mon pricing pour un client Upwork",
        "brainstorm idées pour un nouveau ruisseau de revenus passifs",
    ]

    for msg in test_messages:
        print(f"\n>>> MESSAGE : {msg}")
        agents = route(msg)
        if agents:
            print(f"    Agents activés ({len(agents)}) : {', '.join(a['name'] for a in agents)}")
        else:
            print("    Aucun agent spécifique — réponse générale")
