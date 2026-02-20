"""
TITAN Learning Module
Learn anything — flashcards, concept explainer, study plans, cheatsheets.
"""

from ..ai_client import chat as ai_chat


class TitanLearning:
    """Learn faster, remember more."""

    def __init__(self):
        pass

    async def explain(self, concept: str, level: str = "debutant") -> str:
        """Explain any concept at any level."""
        return ai_chat("Expert assistant.", f"""Explique "{concept}" pour un niveau {level}.""", 1500)

    async def flashcards(self, topic: str, count: int = 5) -> str:
        """Generate flashcards for a topic."""
        return ai_chat("Expert assistant.", f"""Cree {count} flashcards pour apprendre: "{topic}" """, 1500)

    async def cheatsheet(self, topic: str) -> str:
        """Generate a cheatsheet."""
        return ai_chat("Expert assistant.", f"""Cree un cheatsheet compact pour: "{topic}" """, 2000)

    async def study_plan(self, topic: str, duration: str = "4 semaines") -> str:
        """Generate a study plan."""
        return ai_chat("Expert assistant.", f"""Cree un plan d'etude pour apprendre: "{topic}" en {duration}.""", 2000)

    async def eli5(self, concept: str) -> str:
        """Explain Like I'm 5."""
        return ai_chat("Expert assistant.", f"""Explique "{concept}" comme si j'avais 5 ans.""", 500)

    async def quiz(self, topic: str) -> str:
        """Generate a quiz."""
        return ai_chat("Expert assistant.", f"""Cree un quiz de 5 questions sur: "{topic}". Format QCM avec 4 choix par question puis les reponses a la fin. En francais.""", 1500)
