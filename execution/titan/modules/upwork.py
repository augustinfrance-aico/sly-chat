"""
TITAN Upwork Module
Freelance job hunting, proposal generation, market intelligence.
"""

import json
from datetime import datetime
from typing import Optional

import requests

from ..ai_client import chat as ai_chat
from ..config import UPWORK_KEYWORDS, UPWORK_SKILLS
from . import memory


class TitanUpwork:
    """Titan's freelance hunting capabilities."""

    def __init__(self):
        pass

    async def analyze_job(self, job_description: str) -> str:
        """Analyze an Upwork job posting and give strategic advice."""
        return ai_chat(
            "Expert assistant.",
            f"""Analyse cette offre Upwork pour Augustin (freelancer automation/n8n/IA).

Offre:
{job_description}

Donne:
1. Score de pertinence (1-10)
2. Points forts pour candidater
3. Red flags eventuels
4. Strategie de proposition""",
            1024,
        )

    async def generate_proposal(self, job_description: str, language: str = "en") -> str:
        """Generate a winning Upwork proposal."""
        lang_instruction = "en anglais" if language == "en" else "en francais"

        return ai_chat(
            "Expert assistant.",
            f"""Redige une proposition Upwork {lang_instruction} pour Augustin (AICO).

Offre:
{job_description}

Skills: {UPWORK_SKILLS}

La proposition doit etre concise, personnalisee, et montrer une comprehension du besoin.""",
            1024,
        )

    async def generate_loom_script(self, job_description: str) -> str:
        """Generate a Loom video script for a proposal."""
        return ai_chat(
            "Expert assistant.",
            f"""Redige un script de Loom (60-90 secondes) pour accompagner une candidature Upwork.

Offre:
{job_description}

Le script doit etre naturel, pas robotique. Montrer qu'on a compris le besoin.""",
            1024,
        )

    async def get_relevant_jobs(self) -> str:
        """Get summary of relevant job types to look for."""
        return ai_chat(
            "Expert assistant.",
            f"""Donne 5 types de jobs Upwork a chercher maintenant pour un freelancer avec ces competences:
{UPWORK_SKILLS}

Mots-cles: {', '.join(UPWORK_KEYWORDS)}

Pour chaque type: titre, budget moyen, niveau de competition.""",
            512,
        )

    async def create_portfolio_page(self, project_description: str) -> str:
        """Generate HTML portfolio page for a project."""
        return ai_chat(
            "Expert assistant.",
            f"""Genere une page HTML portfolio dark mode pour ce projet:
{project_description}

Style: moderne, dark mode, responsive. Avec sections: hero, description, tech stack, resultats.""",
            4096,
        )
