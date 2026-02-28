"""
CLASSROOM VOICE — Système de voix distinctes pour chaque agent.
Utilise Web Speech API côté client (navigateur) = 100% gratuit.
Chaque agent a un pitch, speed et timbre différent.

Côté serveur : génère les paramètres de voix.
Côté client : Web Speech API speechSynthesis (classroom_ui.html).
"""

import logging
from .classroom_registry import CLASSROOM_AGENTS, get_agent

log = logging.getLogger("titan.classroom.voice")


# Mapping voix par pôle (utilisé côté client Web Speech API)
VOICE_PROFILES = {}
for agent in CLASSROOM_AGENTS:
    VOICE_PROFILES[agent["name"]] = {
        "pitch": agent.get("voice_pitch", 1.0),
        "rate": agent.get("voice_speed", 1.0),
        "volume": 0.9,
        # Le timbre est contrôlé par le pitch + le choix de voix système
    }


def get_voice_params(agent_name: str) -> dict:
    """Retourne les paramètres de voix pour un agent."""
    default = {"pitch": 1.0, "rate": 1.0, "volume": 0.9}
    return VOICE_PROFILES.get(agent_name, default)


def get_all_voice_params() -> dict:
    """Retourne les paramètres de voix pour tous les agents."""
    return VOICE_PROFILES.copy()


def get_voice_config_for_ui() -> list[dict]:
    """
    Génère la config voix formatée pour le JS côté client.
    Chaque agent a : name, pitch, rate, volume.
    """
    configs = []
    for agent in CLASSROOM_AGENTS:
        params = VOICE_PROFILES.get(agent["name"], {})
        configs.append({
            "name": agent["name"],
            "emoji": agent["emoji"],
            "pole": agent["pole"],
            "pitch": params.get("pitch", 1.0),
            "rate": params.get("rate", 1.0),
            "volume": params.get("volume", 0.9),
        })
    return configs
