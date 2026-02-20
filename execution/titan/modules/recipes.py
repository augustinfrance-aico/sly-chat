"""
TITAN Recipes Module
Quick recipes, meal ideas, nutrition info.
"""

import random

from ..ai_client import chat as ai_chat


class TitanRecipes:
    """Chef Titan a votre service."""

    def __init__(self):
        pass

    QUICK_MEALS = [
        {"name": "Pates carbonara", "time": "15 min", "cal": "~550 kcal"},
        {"name": "Salade cesar", "time": "10 min", "cal": "~400 kcal"},
        {"name": "Wrap poulet", "time": "10 min", "cal": "~450 kcal"},
        {"name": "Omelette fromage", "time": "5 min", "cal": "~350 kcal"},
        {"name": "Bowl riz saumon", "time": "15 min", "cal": "~500 kcal"},
        {"name": "Croque-monsieur", "time": "10 min", "cal": "~400 kcal"},
        {"name": "Soupe legumes", "time": "20 min", "cal": "~200 kcal"},
        {"name": "Steak frites", "time": "20 min", "cal": "~700 kcal"},
        {"name": "Tartine avocat", "time": "5 min", "cal": "~350 kcal"},
        {"name": "Risotto champignons", "time": "25 min", "cal": "~500 kcal"},
    ]

    def quick_meal(self) -> str:
        """Suggest a quick meal."""
        meal = random.choice(self.QUICK_MEALS)
        return (
            f"🍽 REPAS RAPIDE\n\n"
            f"👉 {meal['name']}\n"
            f"⏱ {meal['time']}\n"
            f"🔥 {meal['cal']}\n\n"
            f"Tape /recipe {meal['name']} pour la recette complete."
        )

    async def recipe(self, dish: str) -> str:
        """Get a full recipe."""
        return ai_chat("Expert assistant.", f"""Donne la recette de: "{dish}"

Format:
🍽 [NOM]
⏱ Temps: X min
👥 Pour: X personnes
🔥 Calories: ~X kcal/portion

INGREDIENTS:
- ...

ETAPES:
1. ...

ASTUCE CHEF:
...

En francais, concis.""", 1500)

    async def meal_plan(self, goal: str = "equilibre") -> str:
        """Generate a daily meal plan."""
        return ai_chat("Expert assistant.", f"""Cree un plan repas pour une journee, objectif: {goal}""", 1500)

    async def with_ingredients(self, ingredients: str) -> str:
        """Suggest a recipe based on available ingredients."""
        return ai_chat("Expert assistant.", f"""J'ai ces ingredients: {ingredients}""", 1000)
