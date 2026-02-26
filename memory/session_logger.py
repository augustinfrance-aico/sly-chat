"""
session_logger.py — Le Greffier Automatique

Métaphore : après chaque conversation, un greffier invisible
lit ce qui s'est passé et grave les décisions importantes
dans le cerveau. Tu dors. Le cerveau grandit.

Fonctionnement :
1. Lit agent_memory.json (mémoire structurée courte)
2. Lit run_state.json si existe (état du dernier pipeline)
3. Extrait les décisions, erreurs, patterns importants
4. Les grave dans Mem0 (ou fallback local)
5. Met à jour session_notes dans agent_memory.json

Lancement :
    python memory/session_logger.py          # Log session manuelle
    python memory/session_logger.py --auto   # Mode auto (cron/post-session)
    python memory/session_logger.py --query "Lurie"  # Chercher dans la mémoire
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path

WORKSPACE = Path(__file__).parent.parent
AGENT_MEMORY = WORKSPACE / ".tmp" / "agent_memory.json"
RUN_STATE = WORKSPACE / ".tmp" / "run_state.json"
ERRORS_MD = WORKSPACE / "directives" / "ERRORS.md"
LOG_FILE = WORKSPACE / "memory" / "session_log.jsonl"

# Import du cerveau
sys.path.insert(0, str(WORKSPACE))
from memory.mem0_brain import brain


# ─── EXTRACTEURS ──────────────────────────────────────────────────────────────

def extract_from_agent_memory() -> list[str]:
    """Transforme agent_memory.json en souvenirs naturels."""
    if not AGENT_MEMORY.exists():
        return []

    with open(AGENT_MEMORY, encoding="utf-8") as f:
        data = json.load(f)

    memories = []

    # Clients actifs
    for client_id, info in data.get("active_clients", {}).items():
        status = info.get("status", "")
        next_action = info.get("prochaine_action", "")
        if status:
            memories.append(f"Client {client_id} : {status}. Prochaine action : {next_action}")

    # Dernières décisions
    for decision in data.get("last_decisions", [])[-3:]:
        memories.append(
            f"Décision ({decision.get('date','?')}) : {decision.get('decision','')}. "
            f"Raison : {decision.get('rationale','')}"
        )

    # Patterns appris
    for pattern in data.get("learned_patterns", []):
        memories.append(
            f"Pattern technique [{pattern.get('criticality','?')}] : {pattern.get('description','')}"
        )

    # Notes de session
    for note in data.get("session_notes", {}).get("entries", [])[-3:]:
        memories.append(f"Session {note.get('date','?')} : {note.get('note','')}")

    return memories


def extract_from_run_state() -> list[str]:
    """Extrait ce qui s'est passé dans le dernier pipeline."""
    if not RUN_STATE.exists():
        return []

    with open(RUN_STATE, encoding="utf-8") as f:
        data = json.load(f)

    memories = []
    pipeline = data.get("current_pipeline", {})

    if pipeline.get("name"):
        status = pipeline.get("status", "unknown")
        steps_done = pipeline.get("steps_completed", [])
        artifacts = pipeline.get("artifacts_produced", [])

        memories.append(
            f"Pipeline '{pipeline['name']}' : statut {status}. "
            f"Étapes faites : {', '.join(steps_done) if steps_done else 'aucune'}. "
            f"Livrables : {', '.join(artifacts) if artifacts else 'aucun'}"
        )

        # Erreurs du run
        for err in data.get("errors_this_run", []):
            memories.append(
                f"Erreur pipeline : {err.get('step','?')} → {err.get('error','')}. "
                f"Fix : {err.get('fix_applied','non documenté')}"
            )

    return memories


def build_session_summary(memories: list[str]) -> str:
    """Résumé court de session pour le log local."""
    return (
        f"Session {datetime.now().strftime('%Y-%m-%d %H:%M')} — "
        f"{len(memories)} souvenirs gravés"
    )


# ─── LOGGER PRINCIPAL ─────────────────────────────────────────────────────────

def log_session(verbose: bool = True) -> int:
    """
    Extrait et grave tous les souvenirs importants de cette session.
    Retourne le nombre de souvenirs gravés.
    """
    if verbose:
        print("\n📝 Session Logger — démarrage")
        print(f"   Mode cerveau : {brain.stats()['mode']}\n")

    all_memories = []

    # Extraire de toutes les sources
    sources = [
        ("agent_memory.json", extract_from_agent_memory),
        ("run_state.json", extract_from_run_state),
    ]

    for source_name, extractor in sources:
        try:
            mems = extractor()
            if verbose and mems:
                print(f"   ✓ {source_name} : {len(mems)} souvenirs extraits")
            all_memories.extend([(m, source_name) for m in mems])
        except Exception as e:
            if verbose:
                print(f"   ✗ {source_name} : erreur ({e})")

    if not all_memories:
        if verbose:
            print("   Rien à graver cette session.\n")
        return 0

    # Graver dans le cerveau
    count = 0
    for memory, source in all_memories:
        category = _source_to_category(source)
        result = brain.remember(memory, category=category)
        if result.get("status") == "ok":
            count += 1

    # Log local (fichier JSONL — append only, jamais écrasé)
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps({
            "timestamp": datetime.now().isoformat(),
            "memories_logged": count,
            "mode": brain.stats()["mode"]
        }, ensure_ascii=False) + "\n")

    if verbose:
        print(f"\n✅ {count} souvenirs gravés dans le cerveau.")
        stats = brain.stats()
        print(f"   Total cerveau : {stats['total_memories']} souvenirs\n")

    return count


def _source_to_category(source: str) -> str:
    mapping = {
        "agent_memory.json": "workspace_state",
        "run_state.json": "pipeline_run",
    }
    return mapping.get(source, "general")


# ─── AMORÇAGE INITIAL ─────────────────────────────────────────────────────────

SEED_MEMORIES = [
    ("Augus est entrepreneur, pas développeur. Toujours vulgariser avec des métaphores. Jamais de jargon technique.", "user_profile"),
    ("Augus veut tout savoir mais ne veut pas être dérangé. Agir, puis rapporter. Maximum 1 question par session.", "user_profile"),
    ("Augus aime l'humour subtil. Pas de pavés. Phrases courtes, bullet points.", "user_profile"),
    ("Règle absolue : 0€ de coût fixe. Aucun service payant sans accord Augus.", "rules"),
    ("TITAN est le bot Telegram principal d'Augus. Déployé sur Render, auto-deploy depuis GitHub.", "context"),
    ("Lurie est le client principal (Moldova). Communiquer en anglais friendly. Contrat en attente.", "client"),
    ("Cascade Groq : 6 modèles en séquence si rate limit. Gemini en fallback final.", "technical"),
    ("Timezone Moldova : America/New_York +7h. Midi NY = 19h Moldavie.", "technical"),
    ("Les agents personnalité (OMEGA, MURPHY, etc.) s'activent via CASTING.md selon le besoin.", "agents"),
    ("Stratégie : mille ruisseaux — plusieurs petites sources de revenu plutôt qu'un seul gros flux.", "strategy"),
]


def seed_brain(force: bool = False) -> int:
    """
    Amorce le cerveau avec les souvenirs fondamentaux.
    Ne grave que si le cerveau est vide (ou force=True).
    """
    stats = brain.stats()

    if stats["total_memories"] > 0 and not force:
        print(f"[SEED] Cerveau déjà amorcé ({stats['total_memories']} souvenirs). Skip.")
        return 0

    print(f"[SEED] Amorçage du cerveau ({len(SEED_MEMORIES)} souvenirs fondamentaux)...")
    count = 0
    for memory, category in SEED_MEMORIES:
        result = brain.remember(memory, category=category)
        if result.get("status") == "ok":
            count += 1
            print(f"   OK [{category}] {memory[:60]}...")

    print(f"\n✅ Cerveau amorcé avec {count} souvenirs fondamentaux.\n")
    return count


# ─── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    args = sys.argv[1:]

    if "--query" in args or "-q" in args:
        idx = args.index("--query") if "--query" in args else args.index("-q")
        query = " ".join(args[idx+1:]) if idx+1 < len(args) else ""
        if query:
            print(f"\n🔍 Recherche : '{query}'")
            results = brain.recall(query, limit=8)
            if not results:
                print("   Aucun souvenir trouvé.")
            for r in results:
                score_pct = int(r.get("score", 0) * 100)
                print(f"   [{score_pct:3d}%] {r['memory']}")
            print()
        else:
            print("Usage: --query <texte>")

    elif "--seed" in args:
        force = "--force" in args
        seed_brain(force=force)

    elif "--stats" in args:
        s = brain.stats()
        print(f"\n🧠 Cerveau AICO")
        print(f"   Mode      : {s['mode']}")
        print(f"   Souvenirs : {s['total_memories']}")

        # Log history
        if LOG_FILE.exists():
            with open(LOG_FILE, encoding="utf-8") as f:
                lines = f.readlines()
            print(f"   Sessions  : {len(lines)} loggées")
            if lines:
                last = json.loads(lines[-1])
                print(f"   Dernière  : {last['timestamp'][:16]}")
        print()

    elif "--auto" in args:
        # Mode silencieux pour cron ou post-session hook
        count = log_session(verbose=False)
        print(f"[SESSION_LOGGER] {count} souvenirs gravés.")

    else:
        # Mode interactif par défaut
        log_session(verbose=True)
