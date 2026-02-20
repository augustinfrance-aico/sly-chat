"""
AI News Summarizer - Utilise Claude pour creer un resume
des actualites IA pertinent pour un office notarial.
Genere un script de journal TV d'1 minute.
"""

import os
import sys
import json
from datetime import datetime
from typing import List, Dict

# Fix Windows encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env'))
except ImportError:
    pass

import anthropic


SUMMARY_PROMPT = """Tu es un journaliste specialise dans l'intelligence artificielle.
Tu travailles pour un office notarial innovant qui veut rester a la pointe de l'actualite IA.

Voici les {count} articles d'actualite IA les plus pertinents de la semaine:

{articles_text}

---

Genere un RESUME STRUCTURE en francais avec exactement ces sections:

## FLASH ACTU IA - {date}

### Les 3 infos cles de la semaine
(Les 3 actualites les plus importantes, 2-3 phrases chacune max)

### Impact pour les notaires
(2-3 points concrets sur comment ces avancees IA peuvent impacter le metier de notaire, les actes, la relation client, etc.)

### Le chiffre de la semaine
(Un chiffre marquant tire des actualites)

### A surveiller
(1-2 tendances a suivre pour les prochaines semaines)

---

REGLES:
- Sois concis et percutant (pas de blabla)
- Utilise un ton professionnel mais accessible
- Maximum 400 mots au total
- Pas de jargon technique incomprehensible
- Mets en avant ce qui peut concretement impacter un office notarial
"""

SCRIPT_PROMPT = """Tu es un presentateur de journal TV specialise tech/IA, avec un style dynamique et accessible.
Tu presentes un mini-journal d'1 minute pour une equipe de notaires.

Voici le resume des actualites:

{summary}

---

Transforme ce resume en un SCRIPT DE PRESENTATION ORALE d'exactement 1 minute (environ 150 mots).

FORMAT DU SCRIPT:
[INTRO]
(Salutation energique + accroche, 10 secondes)

[ACTU 1]
(Premiere info cle, 15 secondes)

[ACTU 2]
(Deuxieme info cle, 15 secondes)

[IMPACT NOTAIRES]
(Lien concret avec le metier, 10 secondes)

[OUTRO]
(Conclusion + teaser semaine prochaine, 10 secondes)

REGLES:
- Ecris comme on PARLE (pas comme on ecrit)
- Phrases courtes et punchy
- Pas de mots trop techniques
- Le texte doit etre lu a voix haute en 1 minute pile
- Ton dynamique, positif, un peu humoristique
- Commence par "Bonjour a tous! Bienvenue dans votre Flash IA de la semaine!"
- Termine par "A la semaine prochaine pour votre prochain Flash IA!"
- Ne mets PAS les indications [INTRO] etc. dans le texte final, juste le texte a lire
- Ecris UNIQUEMENT le texte a lire, rien d'autre
"""


def create_articles_text(articles: List[Dict]) -> str:
    """Formate les articles pour le prompt."""
    text_parts = []
    for i, art in enumerate(articles, 1):
        text_parts.append(
            f"[{i}] {art['title']}\n"
            f"    Source: {art['source']}\n"
            f"    Resume: {art['summary'][:300]}\n"
            f"    Date: {art.get('date', 'N/A')}\n"
            f"    Lien: {art.get('link', 'N/A')}"
        )
    return "\n\n".join(text_parts)


def generate_summary(articles: List[Dict]) -> str:
    """Genere le resume structure avec Claude."""
    client = anthropic.Anthropic()

    articles_text = create_articles_text(articles)
    today = datetime.now().strftime("%d/%m/%Y")

    prompt = SUMMARY_PROMPT.format(
        count=len(articles),
        articles_text=articles_text,
        date=today
    )

    print("[AI] Generation du resume avec Claude...")

    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}]
    )

    summary = response.content[0].text
    print("[OK] Resume genere")
    return summary


def generate_tv_script(summary: str) -> str:
    """Genere le script TV d'1 minute avec Claude."""
    client = anthropic.Anthropic()

    prompt = SCRIPT_PROMPT.format(summary=summary)

    print("[AI] Generation du script TV avec Claude...")

    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=800,
        messages=[{"role": "user", "content": prompt}]
    )

    script = response.content[0].text
    print("[OK] Script TV genere")
    return script


def save_outputs(summary: str, script: str, output_dir: str = None):
    """Sauvegarde le resume et le script."""
    if output_dir is None:
        output_dir = os.path.dirname(os.path.abspath(__file__))

    date_str = datetime.now().strftime("%Y-%m-%d")

    # Resume
    summary_path = os.path.join(output_dir, f"resume_{date_str}.md")
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(summary)
    print(f"[OK] Resume: {summary_path}")

    # Script TV
    script_path = os.path.join(output_dir, f"script_{date_str}.txt")
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(script)
    print(f"[OK] Script: {script_path}")

    return summary_path, script_path


if __name__ == "__main__":
    from news_scraper import load_news_cache, fetch_news, save_news_cache

    # Charger ou recuperer les news
    articles = load_news_cache()
    if not articles:
        articles = fetch_news()
        save_news_cache(articles)

    if not articles:
        print("[ERROR] Aucun article trouve")
        sys.exit(1)

    # Generer le resume
    summary = generate_summary(articles)
    print("\n" + "=" * 70)
    print(summary)
    print("=" * 70)

    # Generer le script TV
    script = generate_tv_script(summary)
    print("\n" + "=" * 70)
    print(script)
    print("=" * 70)

    # Sauvegarder
    save_outputs(summary, script)
