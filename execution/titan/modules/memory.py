"""
TITAN Memory Module v2.0
Persistent memory across sessions — Titan never forgets.

v2.0 Upgrades:
- Thread-safe file I/O (locks prevent concurrent corruption)
- Auto-backup before writes (recoverable if crash)
- Smarter conversation compression (keep recent + relevant)
- Memory integrity checks
- Access frequency tracking

Features:
- Key-value memory (remember/recall)
- Conversation history (25-msg window, 500 max)
- Context awareness (knows what happened before)
- Auto-tagging and categorization
- Search through memories
- Auto-facts extraction
- Contacts CRM
"""

import json
import os
import shutil
import threading
from datetime import datetime
from pathlib import Path
from typing import Optional


MEMORY_DIR = Path(__file__).parent.parent / "memory"
MEMORY_DIR.mkdir(exist_ok=True)

MEMORY_FILE = MEMORY_DIR / "titan_memory.json"
CONVERSATIONS_FILE = MEMORY_DIR / "conversations.json"
CONTACTS_FILE = MEMORY_DIR / "contacts.json"
AUTO_FACTS_FILE = MEMORY_DIR / "auto_facts.json"

# === THREAD-SAFE I/O ===
_file_locks: dict[str, threading.Lock] = {}


def _get_lock(filepath: Path) -> threading.Lock:
    """Get or create a lock for a specific file."""
    key = str(filepath)
    if key not in _file_locks:
        _file_locks[key] = threading.Lock()
    return _file_locks[key]


def _load_json(filepath: Path) -> dict:
    with _get_lock(filepath):
        if filepath.exists():
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, UnicodeDecodeError):
                # Corrupted file — try backup
                backup = filepath.with_suffix(".json.bak")
                if backup.exists():
                    try:
                        with open(backup, "r", encoding="utf-8") as f:
                            return json.load(f)
                    except Exception:
                        pass
                return {}
    return {}


def _save_json(filepath: Path, data: dict):
    with _get_lock(filepath):
        # Backup before write (safety net)
        if filepath.exists():
            backup = filepath.with_suffix(".json.bak")
            try:
                shutil.copy2(filepath, backup)
            except Exception:
                pass
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


def integrity_check() -> dict:
    """Vérifie l'intégrité de tous les fichiers mémoire."""
    results = {}
    for name, path in [("memory", MEMORY_FILE), ("conversations", CONVERSATIONS_FILE),
                        ("contacts", CONTACTS_FILE), ("auto_facts", AUTO_FACTS_FILE)]:
        try:
            if path.exists():
                data = _load_json(path)
                size = path.stat().st_size
                results[name] = {"status": "ok", "size_kb": round(size / 1024, 1),
                                  "entries": len(data.get("entries", data.get("history", data.get("facts", data.get("contacts", [])))))}
            else:
                results[name] = {"status": "missing"}
        except Exception as e:
            results[name] = {"status": "corrupted", "error": str(e)[:100]}
    return results


# === KEY-VALUE MEMORY ===

def remember(key: str, value: str, category: str = "general") -> str:
    """Save something to memory. Titan never forgets."""
    memory = _load_json(MEMORY_FILE)

    if "entries" not in memory:
        memory["entries"] = {}

    memory["entries"][key.lower()] = {
        "value": value,
        "category": category,
        "saved_at": datetime.now().isoformat(),
        "access_count": 0,
    }

    _save_json(MEMORY_FILE, memory)
    return f"Mémorisé : {key} → {value}"


def recall(key: str) -> Optional[str]:
    """Recall something from memory."""
    memory = _load_json(MEMORY_FILE)
    entries = memory.get("entries", {})

    entry = entries.get(key.lower())
    if entry:
        entry["access_count"] += 1
        entry["last_accessed"] = datetime.now().isoformat()
        _save_json(MEMORY_FILE, memory)
        return entry["value"]

    # Fuzzy search
    for k, v in entries.items():
        if key.lower() in k or k in key.lower():
            v["access_count"] += 1
            v["last_accessed"] = datetime.now().isoformat()
            _save_json(MEMORY_FILE, memory)
            return f"[Match partiel: {k}] {v['value']}"

    return None


def search_memory(query: str) -> list:
    """Search through all memories."""
    memory = _load_json(MEMORY_FILE)
    entries = memory.get("entries", {})
    results = []

    query_lower = query.lower()
    for key, entry in entries.items():
        if (query_lower in key or
            query_lower in entry["value"].lower() or
            query_lower in entry.get("category", "").lower()):
            results.append({
                "key": key,
                "value": entry["value"],
                "category": entry.get("category", "general"),
                "saved_at": entry.get("saved_at", ""),
            })

    return results


def list_memories(category: str = None) -> list:
    """List all memories, optionally filtered by category."""
    memory = _load_json(MEMORY_FILE)
    entries = memory.get("entries", {})

    results = []
    for key, entry in entries.items():
        if category and entry.get("category") != category:
            continue
        results.append({
            "key": key,
            "value": entry["value"],
            "category": entry.get("category", "general"),
        })

    return results


def forget(key: str) -> str:
    """Remove something from memory."""
    memory = _load_json(MEMORY_FILE)
    entries = memory.get("entries", {})

    if key.lower() in entries:
        del entries[key.lower()]
        _save_json(MEMORY_FILE, memory)
        return f"Oublié : {key}"

    return f"Pas trouvé en mémoire : {key}"


# === CONTACTS ===

def save_contact(name: str, info: dict) -> str:
    """Save a contact (client, lead, partner)."""
    contacts = _load_json(CONTACTS_FILE)

    if "contacts" not in contacts:
        contacts["contacts"] = {}

    contacts["contacts"][name.lower()] = {
        **info,
        "name": name,
        "saved_at": datetime.now().isoformat(),
    }

    _save_json(CONTACTS_FILE, contacts)
    return f"Contact sauvegardé : {name}"


def get_contact(name: str) -> Optional[dict]:
    """Get a contact's info."""
    contacts = _load_json(CONTACTS_FILE)
    entries = contacts.get("contacts", {})

    contact = entries.get(name.lower())
    if contact:
        return contact

    # Fuzzy search
    for k, v in entries.items():
        if name.lower() in k or k in name.lower():
            return v

    return None


def list_contacts() -> list:
    """List all contacts."""
    contacts = _load_json(CONTACTS_FILE)
    return list(contacts.get("contacts", {}).values())


# === CONVERSATION HISTORY ===

def save_conversation(user_msg: str, titan_reply: str, context: str = "telegram"):
    """Save a conversation exchange. Skips exact duplicates."""
    convos = _load_json(CONVERSATIONS_FILE)

    if "history" not in convos:
        convos["history"] = []

    # Déduplication — skip si le dernier message est identique
    if convos["history"]:
        last = convos["history"][-1]
        if last.get("user") == user_msg and last.get("titan") == titan_reply:
            return

    convos["history"].append({
        "user": user_msg,
        "titan": titan_reply,
        "context": context,
        "timestamp": datetime.now().isoformat(),
    })

    # Keep last 500 conversations
    if len(convos["history"]) > 500:
        convos["history"] = convos["history"][-500:]

    _save_json(CONVERSATIONS_FILE, convos)


def get_recent_conversations(n: int = 10, context: str = None) -> list:
    """Get recent conversation history."""
    convos = _load_json(CONVERSATIONS_FILE)
    history = convos.get("history", [])

    if context:
        history = [h for h in history if h.get("context") == context]

    return history[-n:]


def get_conversation_context(n: int = 5) -> str:
    """Get formatted recent conversation context for Claude."""
    recent = get_recent_conversations(n)
    if not recent:
        return "Pas de conversation récente."

    lines = []
    for conv in recent:
        lines.append(f"Augustin: {conv['user']}")
        lines.append(f"Titan: {conv['titan']}")

    return "\n".join(lines)


# === AUTO FACTS (mémoire automatique extraite des conversations) ===

def save_auto_fact(fact: str, category: str = "general", source: str = "conversation"):
    """Save an automatically extracted fact."""
    data = _load_json(AUTO_FACTS_FILE)
    if "facts" not in data:
        data["facts"] = []

    # Evite les doublons exacts
    existing = [f["fact"].lower() for f in data["facts"]]
    if fact.lower() in existing:
        return

    data["facts"].append({
        "fact": fact,
        "category": category,
        "source": source,
        "saved_at": datetime.now().isoformat(),
    })

    # Garde les 200 derniers faits max
    if len(data["facts"]) > 200:
        data["facts"] = data["facts"][-200:]

    _save_json(AUTO_FACTS_FILE, data)


def get_auto_facts(n: int = 30) -> list:
    """Get the most recent auto-extracted facts."""
    data = _load_json(AUTO_FACTS_FILE)
    return data.get("facts", [])[-n:]


def get_auto_facts_summary(n: int = 20) -> str:
    """Get auto-facts formatted for the system prompt."""
    facts = get_auto_facts(n)
    if not facts:
        return ""
    lines = [f"- [{f['category']}] {f['fact']}" for f in facts]
    return "\n".join(lines)


def forget_auto_fact(keyword: str) -> str:
    """Remove auto-facts containing a keyword."""
    data = _load_json(AUTO_FACTS_FILE)
    facts = data.get("facts", [])
    before = len(facts)
    data["facts"] = [f for f in facts if keyword.lower() not in f["fact"].lower()]
    after = len(data["facts"])
    _save_json(AUTO_FACTS_FILE, data)
    removed = before - after
    return f"{removed} fait(s) supprimé(s) contenant '{keyword}'"
