"""
CLASSROOM REGISTRY — Charge les 32 agents actifs (26 opé + 6 méta).
Aligné sur agent_profiles.py (post-nettoyage Opération Ascension 27/02/2026).
Chaque agent a : nom, emoji, pôle, couleur, spécialité, voix, position de bureau.
"""

import logging

log = logging.getLogger("titan.classroom.registry")

# Positions des bureaux dans la grille (6 rangées x 6 colonnes max)
_DESK_POSITIONS = [
    (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5),
    (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
    (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5),
    (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5),
    (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5),
    (5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5),
]

# Couleurs par pôle
POLE_COLORS = {
    "CORE": "#1F6FFF",
    "STRAT": "#3A8DFF",
    "VENTE": "#FF9A3C",
    "CONTENU": "#B18CFF",
    "OPS": "#FF3B5C",
    "MARCHE": "#00B8CC",
    "RDLAB": "#5B2DBF",
    "META": "#7A3CFF",
}

# 32 agents actifs — alignés sur agent_profiles.py + personnalites/
CLASSROOM_AGENTS = [
    # CORE (4)
    {"name": "OMEGA",     "emoji": "🌀", "pole": "CORE",    "role": "Vision 360, arbitrage final",           "voice_pitch": 0.8, "voice_speed": 0.9},
    {"name": "SENTINEL",  "emoji": "🎯", "pole": "CORE",    "role": "Dispatch, routing, orchestration",      "voice_pitch": 1.0, "voice_speed": 1.1},
    {"name": "PULSE",     "emoji": "💓", "pole": "CORE",    "role": "Performance, latence, profiling",       "voice_pitch": 1.2, "voice_speed": 1.2},
    {"name": "FRANKLIN",   "emoji": "💎", "pole": "CORE",    "role": "Simplification, clarté absolue",        "voice_pitch": 1.1, "voice_speed": 0.95},

    # STRAT (4)
    {"name": "CORTEX",    "emoji": "🧠", "pole": "STRAT",   "role": "Structure, priorisation, plans",        "voice_pitch": 0.85, "voice_speed": 0.9},
    {"name": "GLITCH",    "emoji": "⚡", "pole": "STRAT",   "role": "Hacks, idées non-conventionnelles",     "voice_pitch": 1.3, "voice_speed": 1.3},
    {"name": "SIBYL",     "emoji": "🔮", "pole": "STRAT",   "role": "Prédiction, tendances, timing",         "voice_pitch": 0.7, "voice_speed": 0.85},
    {"name": "NEXUS",     "emoji": "🕸️", "pole": "STRAT",   "role": "Synergies inter-projets",               "voice_pitch": 0.9, "voice_speed": 1.0},

    # VENTE (5)
    {"name": "CLOSER",    "emoji": "🤝", "pole": "VENTE",   "role": "Closing, vente, conversion",            "voice_pitch": 1.05, "voice_speed": 1.15},
    {"name": "KAISER",    "emoji": "👑", "pole": "VENTE",   "role": "Deals long terme, négociation",         "voice_pitch": 0.75, "voice_speed": 0.85},
    {"name": "PRISM",     "emoji": "💠", "pole": "VENTE",   "role": "Pricing, psychologie des offres",       "voice_pitch": 1.1, "voice_speed": 1.0},
    {"name": "ONYX",      "emoji": "🖤", "pole": "VENTE",   "role": "Premium, haut de gamme",                "voice_pitch": 0.8, "voice_speed": 0.8},
    {"name": "LEDGER",    "emoji": "📒", "pole": "VENTE",   "role": "Business model, chiffres",              "voice_pitch": 1.0, "voice_speed": 1.05},

    # CONTENU (3)
    {"name": "PHILOMÈNE", "emoji": "✒️", "pole": "CONTENU", "role": "Copywriting, prompts chirurgicaux",     "voice_pitch": 0.9, "voice_speed": 0.85},
    {"name": "FRESCO",    "emoji": "🎨", "pole": "CONTENU", "role": "Storytelling visuel, branding",         "voice_pitch": 1.1, "voice_speed": 1.0},
    {"name": "VIRAL",     "emoji": "📱", "pole": "CONTENU", "role": "Réseaux sociaux, LinkedIn",             "voice_pitch": 1.25, "voice_speed": 1.25},

    # OPS (5)
    {"name": "ANVIL",     "emoji": "🔨", "pole": "OPS",     "role": "Debug, exécution brute, commando",      "voice_pitch": 0.7, "voice_speed": 1.2},
    {"name": "DREYFUS",   "emoji": "🛡️", "pole": "OPS",     "role": "Discipline, cadence, qualité",          "voice_pitch": 0.85, "voice_speed": 0.95},
    {"name": "SPECTER",   "emoji": "👻", "pole": "OPS",     "role": "Veille, cybersécurité, APIs",           "voice_pitch": 0.75, "voice_speed": 0.9},
    {"name": "DATUM",     "emoji": "📊", "pole": "OPS",     "role": "Data, métriques, KPIs",                 "voice_pitch": 1.0, "voice_speed": 1.05},
    {"name": "VOLT",      "emoji": "⚡", "pole": "OPS",     "role": "Architecture technique, pipelines",     "voice_pitch": 1.05, "voice_speed": 1.1},

    # MARCHE (2)
    {"name": "NICHE",     "emoji": "🔍", "pole": "MARCHE",  "role": "Niches, opportunités de marché",        "voice_pitch": 1.05, "voice_speed": 1.0},
    {"name": "RACOON",    "emoji": "🦝", "pole": "MARCHE",  "role": "Growth hacking, acquisition",           "voice_pitch": 1.2, "voice_speed": 1.15},

    # RDLAB (3)
    {"name": "CIPHER",    "emoji": "🔐", "pole": "RDLAB",   "role": "Veille IA, digest arXiv/NeurIPS",       "voice_pitch": 0.9, "voice_speed": 0.95},
    {"name": "RADAR",     "emoji": "📡", "pole": "RDLAB",   "role": "Détection startups, brevets",           "voice_pitch": 1.05, "voice_speed": 1.05},
    {"name": "PROTO",     "emoji": "🧪", "pole": "RDLAB",   "role": "Prototypage, mini-POC, benchmark",      "voice_pitch": 1.1, "voice_speed": 1.1},

    # CRÉATIF (1)
    {"name": "PIXEL",     "emoji": "🕹️", "pole": "CORE",    "role": "Game design, gamification, UX",         "voice_pitch": 1.1, "voice_speed": 1.15},

    # MÉTA-COUCHE (6)
    {"name": "DARWIN",    "emoji": "🧬", "pole": "META",    "role": "Évolution agents, mutations",           "voice_pitch": 0.7, "voice_speed": 0.8},
    {"name": "SHADOW",    "emoji": "🕳️", "pole": "META",    "role": "Observation silencieuse, garde-fou",    "voice_pitch": 0.6, "voice_speed": 0.7},
    {"name": "AGORA",     "emoji": "🏛️", "pole": "META",    "role": "Gouvernance, vote pondéré",             "voice_pitch": 0.85, "voice_speed": 0.9},
    {"name": "CHRONOS",   "emoji": "⏳", "pole": "META",    "role": "Simulation 3 futurs, projection",       "voice_pitch": 0.65, "voice_speed": 0.75},
    {"name": "HAVOC",     "emoji": "💥", "pole": "META",    "role": "Stress-test, adversaire interne",       "voice_pitch": 1.3, "voice_speed": 1.4},
    {"name": "ATLAS",     "emoji": "🌌", "pole": "META",    "role": "Vision civilisationnelle 10 ans",       "voice_pitch": 0.6, "voice_speed": 0.7},
]


def get_agent(name: str) -> dict | None:
    """Retourne un agent par nom."""
    for agent in CLASSROOM_AGENTS:
        if agent["name"] == name:
            return agent
    return None


def get_agents_by_pole(pole: str) -> list[dict]:
    """Retourne tous les agents d'un pôle."""
    return [a for a in CLASSROOM_AGENTS if a["pole"] == pole]


def get_all_agents() -> list[dict]:
    """Retourne tous les 32 agents avec position de bureau."""
    result = []
    for i, agent in enumerate(CLASSROOM_AGENTS):
        row, col = _DESK_POSITIONS[i] if i < len(_DESK_POSITIONS) else (i // 6, i % 6)
        result.append({
            **agent,
            "desk_row": row,
            "desk_col": col,
            "color": POLE_COLORS.get(agent["pole"], "#1F6FFF"),
        })
    return result


def get_agent_names() -> list[str]:
    """Liste des noms d'agents."""
    return [a["name"] for a in CLASSROOM_AGENTS]


def select_agents(names: list[str] | None = None, poles: list[str] | None = None, max_count: int = 12) -> list[dict]:
    """Sélectionne des agents par nom ou pôle, avec limite."""
    if names:
        selected = [a for a in CLASSROOM_AGENTS if a["name"] in names]
    elif poles:
        selected = [a for a in CLASSROOM_AGENTS if a["pole"] in poles]
    else:
        selected = CLASSROOM_AGENTS.copy()
    return selected[:max_count]
