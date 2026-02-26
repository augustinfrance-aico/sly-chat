"""
TITAN Journal Module — Le Journal du Suzerain
3 questions le soir, compilation automatique, patterns détectés.

[MURRAY + PHILOMÈNE + ZEN]

Features:
- 3 questions contextuelles à 21h30
- Stockage des réponses en mémoire persistante
- Compilation hebdo/mensuelle
- Détection de patterns (humeur, productivité, thèmes récurrents)
- Export markdown du journal
"""

import json
import logging
import random
from datetime import datetime, timedelta
from pathlib import Path

from ..ai_client import chat

log = logging.getLogger("titan.journal")

MEMORY_DIR = Path(__file__).parent.parent / "memory"
JOURNAL_FILE = MEMORY_DIR / "journal.json"
JOURNAL_EXPORT_DIR = MEMORY_DIR / "journal_exports"


# === QUESTIONS POOL ===
# Variées, jamais chiantes, tournent chaque soir

EVENING_QUESTIONS = [
    # Productivité
    ["Meilleur truc que t'as fait aujourd'hui — en 1 phrase.",
     "Qu'est-ce qui t'a freiné aujourd'hui (si quelque chose) ?",
     "Demain, quelle est LA priorité ?"],
    # Mindset
    ["Sur quoi t'as réfléchi aujourd'hui (même en fond) ?",
     "Un truc qui t'a surpris ou appris quelque chose ?",
     "Comment tu te sens là, honnêtement ? (1 mot suffit)"],
    # Stratégie
    ["Qu'est-ce qui avance bien dans l'empire ?",
     "Qu'est-ce qui stagne ou te frustre ?",
     "Une idée qui t'est venue aujourd'hui ?"],
    # Créatif
    ["Si t'avais 4h de libre demain, tu ferais quoi ?",
     "Un truc que t'as vu/lu/entendu qui t'a marqué ?",
     "Qu'est-ce que tu voudrais que le Building fasse cette nuit ?"],
    # Perso
    ["T'as pris du temps pour toi aujourd'hui ?",
     "Qu'est-ce qui t'a fait sourire ?",
     "Un truc que tu veux te rappeler dans 30 jours ?"],
]


class TitanJournal:
    """Le Journal du Suzerain — miroir intelligent."""

    def __init__(self):
        JOURNAL_EXPORT_DIR.mkdir(parents=True, exist_ok=True)
        self._waiting_for_answers = False
        self._current_questions = []
        self._current_answers = []
        self._question_index = 0

    def _load(self) -> dict:
        if JOURNAL_FILE.exists():
            with open(JOURNAL_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"entries": [], "patterns": [], "stats": {}}

    def _save(self, data: dict):
        with open(JOURNAL_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def start_evening_session(self) -> str:
        """Démarre la session du soir — envoie la première question."""
        questions = random.choice(EVENING_QUESTIONS)
        self._current_questions = questions
        self._current_answers = []
        self._question_index = 0
        self._waiting_for_answers = True

        return f"🌙 JOURNAL DU SOIR\n\n1/3 — {questions[0]}"

    def is_waiting(self) -> bool:
        return self._waiting_for_answers

    def receive_answer(self, answer: str) -> str:
        """Reçoit une réponse et envoie la question suivante ou termine."""
        if not self._waiting_for_answers:
            return ""

        self._current_answers.append(answer)
        self._question_index += 1

        if self._question_index < len(self._current_questions):
            q = self._current_questions[self._question_index]
            return f"{self._question_index + 1}/3 — {q}"

        # Toutes les réponses reçues — sauvegarder
        self._waiting_for_answers = False
        return self._save_entry()

    def _save_entry(self) -> str:
        """Sauvegarde l'entrée du jour."""
        data = self._load()
        today = datetime.now().strftime("%Y-%m-%d")

        entry = {
            "date": today,
            "timestamp": datetime.now().isoformat(),
            "questions": self._current_questions,
            "answers": self._current_answers,
        }

        # Analyse IA rapide
        try:
            analysis = chat(
                "Tu es ZEN — analyse de journal intime. Réponds en 2-3 phrases max. "
                "Identifie : humeur générale (1 mot), thème dominant, et 1 insight subtil.",
                f"Questions et réponses du jour :\n"
                + "\n".join(f"Q: {q}\nR: {a}" for q, a in
                           zip(self._current_questions, self._current_answers)),
                max_tokens=200,
            )
            entry["analysis"] = analysis
        except Exception:
            entry["analysis"] = ""

        data["entries"].append(entry)

        # Garder les 365 derniers jours
        if len(data["entries"]) > 365:
            data["entries"] = data["entries"][-365:]

        self._save(data)

        response = "📝 Noté.\n"
        if entry.get("analysis"):
            response += f"\n🧘 {entry['analysis']}"

        streak = self._get_streak(data)
        if streak > 1:
            response += f"\n\n🔥 Streak journal : {streak} jours"

        return response

    def _get_streak(self, data: dict) -> int:
        """Calcule la streak journal."""
        entries = data.get("entries", [])
        if not entries:
            return 0

        dates = sorted(set(e["date"] for e in entries), reverse=True)
        streak = 1
        for i in range(len(dates) - 1):
            d1 = datetime.strptime(dates[i], "%Y-%m-%d")
            d2 = datetime.strptime(dates[i + 1], "%Y-%m-%d")
            if (d1 - d2).days == 1:
                streak += 1
            else:
                break
        return streak

    def get_weekly_summary(self) -> str:
        """Résumé de la semaine — patterns et insights."""
        data = self._load()
        entries = data.get("entries", [])

        week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        week_entries = [e for e in entries if e["date"] >= week_ago]

        if not week_entries:
            return "Pas d'entrées journal cette semaine."

        all_answers = []
        for e in week_entries:
            for q, a in zip(e.get("questions", []), e.get("answers", [])):
                all_answers.append(f"[{e['date']}] Q: {q} → R: {a}")

        try:
            summary = chat(
                "Tu es MURRAY — compilateur de journal hebdo. "
                "Analyse les entrées de la semaine. Donne : "
                "1) Humeur dominante, 2) Thèmes récurrents, 3) Ce qui va bien, "
                "4) Ce qui coince, 5) 1 insight que le Suzerain n'a peut-être pas vu. "
                "Format compact, pas de blabla.",
                "\n".join(all_answers),
                max_tokens=500,
            )
            return f"📊 JOURNAL HEBDO ({len(week_entries)} entrées)\n\n{summary}"
        except Exception:
            return f"📊 {len(week_entries)} entrées cette semaine. Analyse indisponible."

    def get_monthly_summary(self) -> str:
        """Résumé mensuel — le portrait du mois."""
        data = self._load()
        entries = data.get("entries", [])

        month_ago = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        month_entries = [e for e in entries if e["date"] >= month_ago]

        if len(month_entries) < 5:
            return "Pas assez d'entrées pour un bilan mensuel (minimum 5)."

        analyses = [e.get("analysis", "") for e in month_entries if e.get("analysis")]

        try:
            portrait = chat(
                "Tu es PHILOMÈNE — portraitiste. "
                "À partir des analyses quotidiennes d'un mois de journal, "
                "dresse un portrait en 5-8 phrases : qui est cette personne ce mois-ci, "
                "qu'est-ce qui la drive, ses forces, ses angles morts, "
                "et 1 recommandation subtile.",
                "\n".join(analyses),
                max_tokens=600,
            )
            return f"🖼️ PORTRAIT DU MOIS ({len(month_entries)} jours)\n\n{portrait}"
        except Exception:
            return f"🖼️ {len(month_entries)} jours de journal ce mois."

    def export_markdown(self, days: int = 30) -> str:
        """Exporte le journal en markdown."""
        data = self._load()
        entries = data.get("entries", [])

        cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        filtered = [e for e in entries if e["date"] >= cutoff]

        if not filtered:
            return "Aucune entrée à exporter."

        lines = [f"# Journal du Suzerain\n", f"Export : derniers {days} jours\n\n---\n"]

        for entry in filtered:
            lines.append(f"\n## {entry['date']}\n")
            for q, a in zip(entry.get("questions", []), entry.get("answers", [])):
                lines.append(f"**{q}**\n> {a}\n")
            if entry.get("analysis"):
                lines.append(f"\n*🧘 {entry['analysis']}*\n")
            lines.append("---\n")

        filepath = JOURNAL_EXPORT_DIR / f"journal_{datetime.now().strftime('%Y%m%d')}.md"
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        return f"📄 Journal exporté → {filepath.name} ({len(filtered)} entrées)"

    def handle_command(self, command: str) -> str:
        """Route les commandes journal."""
        cmd = command.lower().strip()

        if cmd in ("/journal", "/j"):
            return self.start_evening_session()
        elif cmd == "/journal semaine":
            return self.get_weekly_summary()
        elif cmd == "/journal mois":
            return self.get_monthly_summary()
        elif cmd == "/journal export":
            return self.export_markdown()
        else:
            return (
                "📓 JOURNAL DU SUZERAIN\n\n"
                "/journal — Session du soir (3 questions)\n"
                "/journal semaine — Résumé hebdo\n"
                "/journal mois — Portrait mensuel\n"
                "/journal export — Export markdown"
            )
