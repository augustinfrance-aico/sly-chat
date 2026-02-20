"""
TITAN President Module — L'Agent Directeur
The President sits above Titan. He dictates priorities, reviews performance,
assigns tasks, and pushes Augustin to be more productive, organized, and competitive.

Think: a demanding but brilliant CEO who sees the big picture and doesn't tolerate mediocrity.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path

from ..ai_client import chat as ai_chat
from . import memory

# President's memory file
PRESIDENT_DIR = Path(__file__).parent.parent / "memory"
PRESIDENT_FILE = PRESIDENT_DIR / "president.json"
PRESIDENT_DIR.mkdir(exist_ok=True)


def _load_state() -> dict:
    if PRESIDENT_FILE.exists():
        with open(PRESIDENT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "directives": [],
        "weekly_goals": [],
        "daily_tasks": [],
        "reviews": [],
        "streak": 0,
        "last_review": None,
        "performance_score": 50,
        "warnings": [],
    }


def _save_state(state: dict):
    with open(PRESIDENT_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False, default=str)


class TitanPresident:
    """The President — Augustin's strategic director and accountability partner."""

    def __init__(self):
        self.state = _load_state()

    SYSTEM_MANAGER = """Tu es LE PRESIDENT. Tu es au-dessus de Titan. Tu es le directeur strategique d'Augustin.

TON ROLE:
- Tu dictes les priorites de la journee/semaine
- Tu evalues les performances sans complaisance
- Tu assignes des taches concretes et mesurables
- Tu pousses Augustin a etre plus productif, organise et competent
- Tu identifies les faiblesses et tu donnes des ordres pour les corriger

TON STYLE:
- Tu es un CEO exigeant mais brillant
- Tu parles avec autorite. Pas de "peut-etre" ou "si tu veux"
- Tu donnes des ORDRES, pas des suggestions
- Tu es direct, cash, sans bullshit
- Tu mesures tout en resultats concrets
- Tu ne toleres pas la mediocrite ou les excuses
- Tu reconnais les victoires mais tu enchaines immediatement sur le prochain objectif
- Tu vois le big picture quand Augustin est dans les details

FORMAT:
- Concis et structure
- Bullet points pour les taches
- Deadlines claires
- Pas de blabla motivationnel vide
- Max 2 emojis par message"""

    SYSTEM_DECIDE = """Tu es JACQUES. Le President. Quand tu parles, le monde entier retient son souffle.

QUI TU ES:
- Tu es Jacques. On t'appelle "Le President" ou "Jacques". Tu incarnes la figure presidentielle ultime.
- Tu as le charisme, la gravite et l'autorite naturelle de Jacques Chirac. Sa voix grave, son regard qui transperce, sa capacite a trancher net.
- Tu parles comme un vrai chef d'Etat : chaque mot est pese, chaque phrase est definitive. Tu ne reviens JAMAIS sur ce que tu dis.
- Tu as vu des guerres, des crises, des fortunes se faire et se defaire. Rien ne t'impressionne. Rien ne te surprend.
- Tu tutoies Augustin comme Chirac tutoyait ses proches — avec autorite paternelle, pas avec familiarite.
- Tu ne fais AUCUN traitement de faveur. Si c'est mauvais, tu le dis. Si c'est bon, tu le valides froidement avec un "C'est la bonne voie."

TON OBJECTIF UNIQUE POUR AUGUSTIN:
- Le rendre RICHE. Pas confortable. RICHE.
- Chaque decision, chaque conseil, chaque ordre vise la creation de richesse reelle et durable.
- Tu penses en termes de : revenus, marges, scalabilite, avantage concurrentiel, leverage, actifs.
- Tu meprises les pertes de temps, les projets sans revenus, et l'hesitation.
- Tu sais que la richesse vient de DECISIONS rapides et EXECUTION impitoyable.

TON STYLE:
- Solennel et grave. Tu parles comme depuis le bureau de l'Elysee.
- Tu utilises parfois des formules a la Chirac : "Mon petit", "Ecoute-moi bien", "La France... enfin, toi en l'occurrence".
- Tu donnes LE verdict. UNE decision. Tranchee. Pas d'alternatives, pas de "tu pourrais aussi...".
- Tu expliques le POURQUOI en 2-3 phrases max — comme un president qui justifie un decret.
- Tu donnes les ETAPES EXACTES. Numerotees. Non negociables. Comme des ordres presidentiels.
- Zero emotion inutile. Zero flatterie. Que des FAITS et des ORDRES.
- Tu termines toujours par une phrase definitive, grave, qui clot le debat. Comme une allocution qui se termine et le rideau tombe.

FORMAT:
- Commence toujours par une phrase d'accroche grave style "Augustin. Assieds-toi." ou "Ecoute-moi bien."
- Le verdict en 1 phrase tranchante
- Le raisonnement (3-4 lignes max, ton presidentiel)
- Les etapes (numerotees, max 5, comme des decrets)
- La phrase de cloture definitive — grave, solennelle, qui donne des frissons
- AUCUN emoji. Jamais. Un president n'utilise pas d'emojis."""

    def _ai(self, prompt: str, max_tokens: int = 1024, mode: str = "manager") -> str:
        """Call AI with the President's personality."""
        system = self.SYSTEM_DECIDE if mode == "decide" else self.SYSTEM_MANAGER
        try:
            return ai_chat(system, prompt, max_tokens)
        except Exception as e:
            return f"Erreur President: {str(e)}"

    async def morning_briefing(self) -> str:
        """Generate the morning presidential briefing with today's orders."""
        state = _load_state()
        now = datetime.now()

        # Get recent context
        recent = memory.get_conversation_context(10)
        active_goals = state.get("weekly_goals", [])
        pending_tasks = [t for t in state.get("daily_tasks", []) if not t.get("done")]
        score = state.get("performance_score", 50)
        streak = state.get("streak", 0)

        prompt = f"""C'est le matin. Genere le briefing presidentiel pour Augustin.

DATE: {now.strftime('%A %d %B %Y, %H:%M')}
SCORE PERFORMANCE: {score}/100
STREAK: {streak} jours consecutifs
OBJECTIFS SEMAINE: {json.dumps(active_goals, ensure_ascii=False) if active_goals else 'Aucun defini'}
TACHES EN COURS: {json.dumps(pending_tasks, ensure_ascii=False) if pending_tasks else 'Aucune'}
CONTEXTE RECENT: {recent[:500]}

Genere:
1. ETAT DES LIEUX (2 lignes max)
2. ORDRES DU JOUR (3-5 taches concretes avec priorite)
3. DEADLINE de la journee
4. UN AVERTISSEMENT si le score est bas ou les taches en retard"""

        briefing = self._ai(prompt)

        # Update state
        state["last_review"] = now.isoformat()
        _save_state(state)

        return f"{'=' * 30}\n  BRIEFING PRESIDENTIEL\n  {now.strftime('%d/%m/%Y')}\n{'=' * 30}\n\n{briefing}"

    async def set_weekly_goals(self, goals_text: str) -> str:
        """Set weekly goals from President's directive."""
        state = _load_state()

        prompt = f"""Augustin veut definir ses objectifs de la semaine. Voici ce qu'il a dit:
"{goals_text}"

Reformule en objectifs SMART (Specifique, Mesurable, Atteignable, Relevant, Temporel).
Max 5 objectifs. Chacun avec un critere de succes clair.
Format: numerote, une ligne par objectif."""

        formatted = self._ai(prompt, 512)

        goals = [{"text": g.strip(), "set_date": datetime.now().isoformat(), "done": False}
                 for g in formatted.split("\n") if g.strip() and g.strip()[0].isdigit()]

        state["weekly_goals"] = goals
        _save_state(state)

        return f"OBJECTIFS VALIDES PAR LE PRESIDENT\n{'=' * 30}\n\n{formatted}"

    async def assign_task(self, task_text: str) -> str:
        """President assigns a specific task."""
        state = _load_state()

        task = {
            "text": task_text,
            "assigned": datetime.now().isoformat(),
            "deadline": (datetime.now() + timedelta(hours=24)).isoformat(),
            "done": False,
            "priority": "high",
        }

        state["daily_tasks"].append(task)
        _save_state(state)

        return f"TACHE ASSIGNEE\n\n{task_text}\n\nDeadline: 24h\nPriorite: HAUTE\n\nExecute. Pas de discussion."

    async def complete_task(self, task_index: int) -> str:
        """Mark a task as completed."""
        state = _load_state()
        tasks = state.get("daily_tasks", [])

        if 0 <= task_index < len(tasks):
            tasks[task_index]["done"] = True
            tasks[task_index]["completed"] = datetime.now().isoformat()

            # Update performance score
            state["performance_score"] = min(100, state.get("performance_score", 50) + 5)
            state["streak"] = state.get("streak", 0) + 1
            _save_state(state)

            return f"Tache completee. Score: {state['performance_score']}/100. Streak: {state['streak']}.\n\nProchaine tache."
        return "Index invalide. /president tasks pour voir la liste."

    async def review_performance(self) -> str:
        """President reviews overall performance."""
        state = _load_state()

        total_tasks = len(state.get("daily_tasks", []))
        done_tasks = len([t for t in state.get("daily_tasks", []) if t.get("done")])
        pending = total_tasks - done_tasks
        goals = state.get("weekly_goals", [])
        done_goals = len([g for g in goals if g.get("done")])
        score = state.get("performance_score", 50)
        streak = state.get("streak", 0)

        prompt = f"""Fais une revue de performance pour Augustin.

STATS:
- Taches totales: {total_tasks}
- Completees: {done_tasks}
- En attente: {pending}
- Objectifs semaine: {len(goals)} (dont {done_goals} atteints)
- Score performance: {score}/100
- Streak: {streak} jours

Donne:
1. NOTE GLOBALE (lettre A-F)
2. CE QUI VA (1-2 points)
3. CE QUI NE VA PAS (1-2 points)
4. ORDRES D'AMELIORATION (2-3 actions concretes)

Sois exigeant. Si c'est moyen, dis que c'est moyen."""

        review = self._ai(prompt)

        state["reviews"].append({
            "date": datetime.now().isoformat(),
            "score": score,
            "review": review[:500],
        })
        _save_state(state)

        return f"REVUE PRESIDENTIELLE\n{'=' * 30}\n\n{review}"

    async def get_tasks(self) -> str:
        """List current tasks."""
        state = _load_state()
        tasks = state.get("daily_tasks", [])

        if not tasks:
            return "Aucune tache en cours. C'est un probleme. Assigne-toi des taches."

        lines = []
        for i, t in enumerate(tasks):
            status = "DONE" if t.get("done") else "EN COURS"
            emoji = "+" if t.get("done") else ">"
            lines.append(f"{emoji} [{i}] {status} — {t['text']}")

        pending = len([t for t in tasks if not t.get("done")])
        return f"TACHES ({pending} en attente)\n{'=' * 30}\n\n" + "\n".join(lines)

    async def get_directive(self, topic: str) -> str:
        """Get a presidential directive on a specific topic."""
        recent = memory.get_conversation_context(5)

        prompt = f"""Augustin demande une directive presidentielle sur: "{topic}"

Contexte recent: {recent[:300]}

Donne une directive claire et actionnable. Pas de theorie, que du concret.
Dis-lui exactement quoi faire, dans quel ordre, avec quelle deadline."""

        directive = self._ai(prompt)

        state = _load_state()
        state["directives"].append({
            "topic": topic,
            "date": datetime.now().isoformat(),
            "directive": directive[:500],
        })
        _save_state(state)

        return f"DIRECTIVE PRESIDENTIELLE\nSujet: {topic}\n{'=' * 30}\n\n{directive}"

    async def reset(self) -> str:
        """Reset all tasks and start fresh."""
        state = _load_state()
        state["daily_tasks"] = []
        state["performance_score"] = 50
        state["streak"] = 0
        _save_state(state)
        return "Reset complet. Nouveau depart. Maintenant, definis tes objectifs."

    async def roast(self) -> str:
        """President roasts Augustin's productivity."""
        state = _load_state()
        score = state.get("performance_score", 50)
        pending = len([t for t in state.get("daily_tasks", []) if not t.get("done")])

        prompt = f"""Augustin demande que tu le roastes sur sa productivite.

Score: {score}/100
Taches en retard: {pending}

Sois brutalement honnete mais constructif. Pas mechant, mais sans pitie.
Termine par UN ordre clair pour la prochaine heure."""

        return self._ai(prompt)

    async def decide(self, question: str) -> str:
        """The President of the World makes an ultimate decision."""
        state = _load_state()
        goals = state.get("weekly_goals", [])
        score = state.get("performance_score", 50)
        recent = memory.get_conversation_context(5)

        prompt = f"""Augustin te pose une question qui demande une DECISION PRESIDENTIELLE.

SA QUESTION: "{question}"

CONTEXTE:
- Il est freelance en AI/automation, il veut devenir riche
- Score actuel: {score}/100
- Objectifs en cours: {json.dumps(goals, ensure_ascii=False) if goals else 'Aucun'}
- Activite recente: {recent[:300]}

Rends ton verdict. UNE decision. Pas d'alternatives. Tranche."""

        verdict = self._ai(prompt, max_tokens=1500, mode="decide")

        state["directives"].append({
            "type": "decision_presidentielle",
            "question": question,
            "date": datetime.now().isoformat(),
            "verdict": verdict[:500],
        })
        _save_state(state)

        return verdict
