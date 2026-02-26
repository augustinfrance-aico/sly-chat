"""
self_harvester.py — Le Moissonneur Automatique

Métaphore : après chaque conversation Claude Code,
ce script passe dans le champ et récolte les grains importants.
Il laisse la paille. Il garde le blé.

Ce qu'il fait :
1. Lit le fichier de session Claude Code (.jsonl dans .claude/projects/)
2. Passe chaque échange dans un mini-filtre (sans appel API — 100% local)
3. Détecte les patterns importants : décisions, erreurs, clients, règles
4. Grave uniquement ce qui vaut le coup dans Mem0
5. Marque le fichier comme "récolté" (évite les doublons)

Coût : 0€. Zéro appel API. Filtrage 100% local (regex + mots-clés).
Consommation : ~50ms par session. Invisible.

Usage :
    python memory/self_harvester.py                    # Récolte la dernière session
    python memory/self_harvester.py --all              # Récolte toutes les sessions non récoltées
    python memory/self_harvester.py --dry-run          # Simule sans écrire
    python memory/self_harvester.py --stats            # Statistiques de récolte
"""

import os
import re
import sys
import json
import hashlib
from pathlib import Path
from datetime import datetime

WORKSPACE = Path(__file__).parent.parent
CLAUDE_PROJECTS = Path(os.environ.get("USERPROFILE", "~")).expanduser() / ".claude" / "projects"
HARVEST_LOG = WORKSPACE / "memory" / "harvest_log.json"
HARVEST_MARKER = ".harvested"  # Ajouté au nom du fichier traité dans le log

sys.path.insert(0, str(WORKSPACE))
from memory.mem0_brain import brain

# ─── PATTERNS DE DÉTECTION (100% LOCAL, ZÉRO API) ─────────────────────────────

# Chaque pattern = (regex, catégorie, importance)
# Importance : 1=faible, 2=moyen, 3=critique
DETECTION_PATTERNS = [
    # Décisions techniques
    (r"(?i)(on (a décidé|va utiliser|switch|migr|choisit?|opte pour)).{5,80}", "decision", 3),
    (r"(?i)(decision|décision).{0,5}:.{5,80}", "decision", 3),

    # Erreurs et fixes
    (r"(?i)(fix|corrig|résol|répar).{5,80}", "error_fix", 2),
    (r"(?i)(bug|erreur|error|bloqué).{5,80}", "error_fix", 2),
    (r"(?i)cause\s*:.{5,80}", "error_fix", 3),

    # Clients
    (r"(?i)(lurie|didier|travis|upwork).{5,80}", "client", 2),
    (r"(?i)client.{0,10}(signé|confirmed?|accept|validé).{5,80}", "client", 3),

    # Règles et préférences
    (r"(?i)(règle|toujours|jamais|obligatoire|interdit).{5,80}", "rule", 2),
    (r"(?i)augus (veut|aime|déteste|préfère|demande).{5,80}", "user_pref", 3),

    # Architecture et fichiers importants
    (r"(?i)(créé|créer|nouveau fichier|nouveau module|ajout[eé]).{5,80}", "architecture", 1),
    (r"(?i)(pipeline|workflow|process|système).{5,100}", "architecture", 1),

    # Résultats et chiffres
    (r"(?i)\d+[€$]\s*(par|/)\s*(mois|jour|semaine|client)", "revenue", 3),
    (r"(?i)(revenu|revenue|chiffre|gains?).{5,80}", "revenue", 2),
]

# Mots qui signalent qu'un texte est INTÉRESSANT à graver
SIGNAL_WORDS = {
    "haut": ["décision", "règle", "fix", "corrig", "lurie", "client", "pipeline", "mémoire", "brain"],
    "moyen": ["augus", "titan", "n8n", "groq", "render", "upwork", "system", "agent"],
    "bruit": ["ok", "oui", "non", "merci", "d'accord", "parfait", "voilà", "ah", "bien", "super"]
}

MIN_IMPORTANCE_TO_SAVE = 2  # 1=tout garder, 2=filtré, 3=critique seulement
MAX_MEMORY_LENGTH = 200     # Chars max par souvenir gravé
MAX_MEMORIES_PER_SESSION = 15  # Pour ne pas spammer Mem0


# ─── EXTRACTEUR DE SESSIONS ────────────────────────────────────────────────────

def find_claude_sessions() -> list[Path]:
    """Trouve tous les fichiers de session Claude Code (.jsonl)."""
    sessions = []
    project_key = "c--Users-augus-Desktop-WORKSPACE-AICO"

    # Chercher dans .claude/projects/
    base = CLAUDE_PROJECTS / project_key
    if base.exists():
        sessions.extend(sorted(base.glob("*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True))

    return sessions


def load_harvest_log() -> dict:
    if HARVEST_LOG.exists():
        with open(HARVEST_LOG, encoding="utf-8") as f:
            return json.load(f)
    return {"harvested": {}, "total_memories_saved": 0, "sessions_processed": 0}


def save_harvest_log(log: dict):
    HARVEST_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(HARVEST_LOG, "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)


def get_file_hash(path: Path) -> str:
    """Hash léger (taille + mtime) pour détecter si le fichier a changé."""
    stat = path.stat()
    return hashlib.md5(f"{stat.st_size}{stat.st_mtime}".encode()).hexdigest()[:12]


# ─── FILTRE INTELLIGENT (ZÉRO API) ────────────────────────────────────────────

def score_text(text: str) -> tuple[int, str]:
    """
    Score un texte sur son intérêt à être gravé.
    Retourne (score, catégorie).
    Score 0 = bruit, Score 3+ = à graver.
    """
    text_lower = text.lower()

    # Ignorer si trop court ou trop de bruit
    if len(text) < 30:
        return 0, "noise"

    # Pénaliser les messages de bruit pur
    bruit_count = sum(1 for w in SIGNAL_WORDS["bruit"] if w in text_lower)
    if bruit_count > 2 and len(text) < 60:
        return 0, "noise"

    # Chercher patterns de valeur
    best_score = 0
    best_category = "general"

    for pattern, category, importance in DETECTION_PATTERNS:
        if re.search(pattern, text):
            if importance > best_score:
                best_score = importance
                best_category = category

    # Bonus si mots signal haut
    if any(w in text_lower for w in SIGNAL_WORDS["haut"]):
        best_score = max(best_score, 2)

    return best_score, best_category


def clean_text(text: str) -> str:
    """Nettoie le texte pour le stocker proprement."""
    # Retirer markdown excessif
    text = re.sub(r"\*+", "", text)
    text = re.sub(r"`+", "", text)
    text = re.sub(r"#+\s*", "", text)
    text = re.sub(r"\s+", " ", text).strip()

    # Tronquer intelligemment
    if len(text) > MAX_MEMORY_LENGTH:
        text = text[:MAX_MEMORY_LENGTH].rsplit(" ", 1)[0] + "..."

    return text


def extract_sentences(text: str) -> list[str]:
    """Découpe un texte en phrases/segments analysables."""
    # Séparer par ponctuation forte
    segments = re.split(r"[.!?]\s+|→|\n\n", text)
    return [s.strip() for s in segments if len(s.strip()) > 25]


# ─── HARVEST PRINCIPAL ─────────────────────────────────────────────────────────

def harvest_session(session_path: Path, dry_run: bool = False, verbose: bool = True) -> int:
    """
    Récolte une session Claude Code et grave les souvenirs importants.
    Retourne le nombre de souvenirs gravés.
    """
    log = load_harvest_log()
    file_hash = get_file_hash(session_path)
    session_key = session_path.name

    # Déjà récoltée avec ce contenu ?
    if session_key in log["harvested"] and log["harvested"][session_key].get("hash") == file_hash:
        if verbose:
            print(f"  [SKIP] {session_path.name} — déjà récoltée")
        return 0

    if verbose:
        print(f"\n  [HARVEST] {session_path.name}")

    # Lire le fichier de session (format Claude Code : type=user/assistant)
    messages = []
    try:
        with open(session_path, encoding="utf-8", errors="replace") as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                    entry_type = entry.get("type", "")
                    # Format Claude Code : type=user ou type=assistant
                    if entry_type in ("user", "assistant"):
                        msg = entry.get("message", {})
                        if not isinstance(msg, dict):
                            continue
                        role = msg.get("role", entry_type)
                        content = msg.get("content", [])
                        if isinstance(content, str):
                            messages.append((role, content))
                        elif isinstance(content, list):
                            for block in content:
                                if isinstance(block, dict) and block.get("type") == "text":
                                    text = block.get("text", "")
                                    if text:
                                        messages.append((role, text))
                                elif isinstance(block, str) and block:
                                    messages.append((role, block))
                except (json.JSONDecodeError, KeyError):
                    continue
    except Exception as e:
        if verbose:
            print(f"  [ERR] Lecture session: {e}")
        return 0

    if verbose:
        print(f"      {len(messages)} messages lus")

    # Analyser et scorer chaque segment
    candidates = []
    seen_hashes = set()

    for role, text in messages:
        if not text or len(text) < 30:
            continue

        sentences = extract_sentences(text)
        for sentence in sentences:
            score, category = score_text(sentence)
            if score >= MIN_IMPORTANCE_TO_SAVE:
                clean = clean_text(sentence)
                # Déduplication par hash
                content_hash = hashlib.md5(clean.encode()).hexdigest()[:8]
                if content_hash not in seen_hashes:
                    seen_hashes.add(content_hash)
                    candidates.append((score, category, clean, role))

    # Trier par score décroissant, garder les meilleurs
    candidates.sort(key=lambda x: x[0], reverse=True)
    candidates = candidates[:MAX_MEMORIES_PER_SESSION]

    if verbose:
        print(f"      {len(candidates)} souvenirs candidats (score >= {MIN_IMPORTANCE_TO_SAVE})")

    if not candidates:
        # Marquer quand même comme traitée
        log["harvested"][session_key] = {"hash": file_hash, "saved": 0, "at": datetime.now().isoformat()}
        if not dry_run:
            save_harvest_log(log)
        return 0

    # Graver dans Mem0
    saved = 0
    for score, category, memory, role in candidates:
        if verbose:
            print(f"      [{score}] [{category}] {memory[:70]}...")
        if not dry_run:
            result = brain.remember(memory, category=category)
            if result.get("status") == "ok":
                saved += 1

    # Mettre à jour le log
    if not dry_run:
        log["harvested"][session_key] = {
            "hash": file_hash,
            "saved": saved,
            "at": datetime.now().isoformat()
        }
        log["total_memories_saved"] = log.get("total_memories_saved", 0) + saved
        log["sessions_processed"] = log.get("sessions_processed", 0) + 1
        save_harvest_log(log)

    if verbose:
        status = "[DRY-RUN]" if dry_run else "OK"
        print(f"      {status} {saved}/{len(candidates)} souvenirs graves")

    return saved


def harvest_all(dry_run: bool = False, verbose: bool = True) -> int:
    """Récolte toutes les sessions non récoltées."""
    sessions = find_claude_sessions()

    if not sessions:
        if verbose:
            print("\n[HARVEST] Aucune session Claude Code trouvee.")
            print(f"  Dossier cherche : {CLAUDE_PROJECTS}")
        return 0

    if verbose:
        print(f"\n[HARVEST] {len(sessions)} session(s) trouvee(s)")

    total = 0
    for session in sessions[:10]:  # Max 10 sessions par run (anti-spam)
        total += harvest_session(session, dry_run=dry_run, verbose=verbose)

    if verbose:
        log = load_harvest_log()
        print(f"\n  Total sessions traitees : {log.get('sessions_processed', 0)}")
        print(f"  Total souvenirs graves  : {log.get('total_memories_saved', 0)}")
        stats = brain.stats()
        print(f"  Cerveau total           : {stats['total_memories']} souvenirs")

    return total


# ─── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    args = sys.argv[1:]
    dry_run = "--dry-run" in args
    quiet = "--quiet" in args

    if dry_run:
        print("\n[DRY-RUN] Simulation — aucune ecriture dans Mem0\n")

    if "--stats" in args:
        log = load_harvest_log()
        stats = brain.stats()
        print(f"\n[HARVEST STATS]")
        print(f"  Sessions traitees : {log.get('sessions_processed', 0)}")
        print(f"  Souvenirs graves  : {log.get('total_memories_saved', 0)}")
        print(f"  Cerveau (Mem0)    : {stats['total_memories']} souvenirs total")
        print(f"  Mode cerveau      : {stats['mode']}")
        sessions = find_claude_sessions()
        print(f"  Sessions dispo    : {len(sessions)}")
        if sessions:
            print(f"  Derniere session  : {sessions[0].name[:40]}")
        print()

    elif "--all" in args:
        harvest_all(dry_run=dry_run, verbose=not quiet)

    elif "--last" in args or not args or (len(args) == 1 and "--dry-run" in args):
        # Récolter seulement la dernière session
        sessions = find_claude_sessions()
        if sessions:
            harvest_session(sessions[0], dry_run=dry_run, verbose=not quiet)
        else:
            print("[HARVEST] Aucune session trouvee.")

    elif "--session" in args:
        idx = args.index("--session")
        if idx + 1 < len(args):
            path = Path(args[idx + 1])
            if path.exists():
                harvest_session(path, dry_run=dry_run, verbose=not quiet)
            else:
                print(f"[ERR] Fichier introuvable : {path}")
