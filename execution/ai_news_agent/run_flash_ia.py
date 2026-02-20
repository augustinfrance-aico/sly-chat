"""
Flash IA - Commande principale
Lance tout le pipeline: collecte news -> resume -> script -> video

Usage:
    python run_flash_ia.py                  # Pipeline complet (texte + video)
    python run_flash_ia.py --text-only      # Resume texte uniquement (rapide)
    python run_flash_ia.py --refresh        # Force le rafraichissement des news
    python run_flash_ia.py --days 3         # News des 3 derniers jours
"""

import os
import sys
import argparse
from datetime import datetime

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# Ajouter le dossier parent au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from news_scraper import fetch_news, save_news_cache, load_news_cache
from news_summarizer import generate_summary, generate_tv_script, save_outputs


BANNER = """
============================================================
   FLASH IA - Journal des Actualites IA pour Notaires
============================================================
"""


def run_pipeline(text_only: bool = False, refresh: bool = False, days: int = 7):
    """Execute le pipeline complet."""
    print(BANNER)
    print(f"[START] {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print(f"        Mode: {'Texte seul' if text_only else 'Texte + Video'}")
    print(f"        Periode: {days} derniers jours")
    print()

    output_dir = os.path.dirname(os.path.abspath(__file__))

    # Etape 1: Collecte des news
    print("=" * 60)
    print("ETAPE 1 - Collecte des actualites IA")
    print("=" * 60)

    articles = []
    if not refresh:
        articles = load_news_cache(output_dir)
        if articles:
            print(f"[CACHE] {len(articles)} articles charges depuis le cache")

    if not articles or refresh:
        articles = fetch_news(max_age_days=days, top_n=10)
        save_news_cache(articles, output_dir)

    if not articles:
        print("[ERROR] Impossible de recuperer des articles. Verifiez votre connexion.")
        return None

    print(f"\n[OK] {len(articles)} articles prets pour l'analyse\n")

    # Afficher les titres
    for i, art in enumerate(articles[:5], 1):
        print(f"  {i}. {art['title'][:80]}")
        print(f"     ({art['source']})")

    # Etape 2: Resume IA
    print("\n" + "=" * 60)
    print("ETAPE 2 - Generation du resume IA (Claude)")
    print("=" * 60)

    summary = generate_summary(articles)

    print("\n--- RESUME ---")
    print(summary)
    print("-" * 60)

    # Etape 3: Script TV
    print("\n" + "=" * 60)
    print("ETAPE 3 - Generation du script TV")
    print("=" * 60)

    script = generate_tv_script(summary)

    print("\n--- SCRIPT (1 min) ---")
    print(script)
    print("-" * 60)

    # Sauvegarder textes
    save_outputs(summary, script, output_dir)

    # Etape 4: Video (optionnel)
    if not text_only:
        print("\n" + "=" * 60)
        print("ETAPE 4 - Generation de la video")
        print("=" * 60)

        try:
            from video_generator import generate_video
            video_path = generate_video(script, output_dir)

            print(f"\n[VIDEO] {video_path}")

            # Essayer de jouer le son Harry Potter a la fin
            try:
                sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                from harry_potter_sound import play_harry_potter_sound
                play_harry_potter_sound()
            except Exception:
                pass

        except Exception as e:
            print(f"[WARN] Erreur generation video: {e}")
            print("       Le resume texte a ete genere avec succes.")
            video_path = None
    else:
        video_path = None

    # Resume final
    print("\n" + "=" * 60)
    print("[TERMINE] Flash IA genere avec succes!")
    print("=" * 60)

    date_str = datetime.now().strftime("%Y-%m-%d")
    print(f"\n  Fichiers generes:")
    print(f"  - Resume:  resume_{date_str}.md")
    print(f"  - Script:  script_{date_str}.txt")
    if video_path:
        print(f"  - Video:   flash_ia_{date_str}.mp4")
    print()

    return {
        "summary": summary,
        "script": script,
        "video_path": video_path,
        "articles_count": len(articles)
    }


def main():
    parser = argparse.ArgumentParser(description="Flash IA - Journal IA pour Notaires")
    parser.add_argument("--text-only", action="store_true", help="Resume texte uniquement (pas de video)")
    parser.add_argument("--refresh", action="store_true", help="Force le rafraichissement des news")
    parser.add_argument("--days", type=int, default=7, help="Nombre de jours d'actualites (defaut: 7)")

    args = parser.parse_args()
    run_pipeline(text_only=args.text_only, refresh=args.refresh, days=args.days)


if __name__ == "__main__":
    main()
