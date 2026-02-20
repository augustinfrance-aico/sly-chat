"""
TITAN Personal Module
Learns about Augustin from every conversation.
Builds a deep personal profile over time.
Remembers preferences, goals, habits, relationships, history.
"""

import json
from datetime import datetime
from pathlib import Path

from ..config import MEMORY_DIR
from ..ai_client import chat as ai_chat


PROFILE_FILE = MEMORY_DIR / "personal_profile.json"


def _load_profile() -> dict:
    if PROFILE_FILE.exists():
        return json.loads(PROFILE_FILE.read_text(encoding="utf-8"))
    return _default_profile()


def _save_profile(data: dict):
    PROFILE_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def _default_profile() -> dict:
    return {
        "identity": {
            "name": "Augustin",
            "alias": "boss",
            "company": "AICO",
        },
        "preferences": {},
        "goals": [],
        "interests": [],
        "dislikes": [],
        "relationships": {},
        "habits": [],
        "personality_notes": [],
        "life_events": [],
        "skills": [],
        "learning_log": [],
        "last_updated": "",
    }


class TitanPersonal:
    """Te connaître mieux que tu te connais toi-même."""

    def __init__(self):
        profile = _load_profile()
        if not profile.get("last_updated"):
            _save_profile(profile)

    def get_profile_summary(self) -> str:
        """Get a formatted summary of what Titan knows about you."""
        p = _load_profile()

        lines = ["👤 CE QUE JE SAIS SUR TOI\n"]

        # Identity
        identity = p.get("identity", {})
        if identity:
            lines.append(f"📛 {identity.get('name', '?')} ({identity.get('company', '?')})")

        # Interests
        interests = p.get("interests", [])
        if interests:
            lines.append(f"\n🎯 INTÉRÊTS:")
            for i in interests[-10:]:
                lines.append(f"  • {i}")

        # Goals
        goals = p.get("goals", [])
        if goals:
            lines.append(f"\n🏆 OBJECTIFS:")
            for g in goals[-5:]:
                lines.append(f"  • {g}")

        # Preferences
        prefs = p.get("preferences", {})
        if prefs:
            lines.append(f"\n⭐ PRÉFÉRENCES:")
            for k, v in list(prefs.items())[-10:]:
                lines.append(f"  • {k}: {v}")

        # Skills
        skills = p.get("skills", [])
        if skills:
            lines.append(f"\n💪 COMPÉTENCES:")
            for s in skills[-8:]:
                lines.append(f"  • {s}")

        # Relationships
        rels = p.get("relationships", {})
        if rels:
            lines.append(f"\n👥 PERSONNES:")
            for name, info in list(rels.items())[-5:]:
                lines.append(f"  • {name}: {info}")

        # Personality notes
        notes = p.get("personality_notes", [])
        if notes:
            lines.append(f"\n🧠 NOTES:")
            for n in notes[-5:]:
                lines.append(f"  • {n}")

        # Life events
        events = p.get("life_events", [])
        if events:
            lines.append(f"\n📅 ÉVÉNEMENTS:")
            for e in events[-5:]:
                lines.append(f"  • {e}")

        if len(lines) <= 2:
            lines.append("\nJe te connais pas encore très bien. Parle-moi, je retiens tout.")

        lines.append(f"\n📊 Dernière mise à jour: {p.get('last_updated', 'jamais')}")
        return "\n".join(lines)

    def get_profile_for_brain(self) -> str:
        """Get a compact profile string for the brain's system prompt."""
        p = _load_profile()

        parts = []

        identity = p.get("identity", {})
        if identity.get("name"):
            parts.append(f"Nom: {identity['name']}")
        if identity.get("company"):
            parts.append(f"Entreprise: {identity['company']}")

        interests = p.get("interests", [])
        if interests:
            parts.append(f"Intérêts: {', '.join(interests[-8:])}")

        goals = p.get("goals", [])
        if goals:
            parts.append(f"Objectifs: {', '.join(goals[-5:])}")

        prefs = p.get("preferences", {})
        if prefs:
            pref_str = "; ".join([f"{k}={v}" for k, v in list(prefs.items())[-8:]])
            parts.append(f"Préférences: {pref_str}")

        skills = p.get("skills", [])
        if skills:
            parts.append(f"Compétences: {', '.join(skills[-6:])}")

        rels = p.get("relationships", {})
        if rels:
            rel_str = "; ".join([f"{n}: {info}" for n, info in list(rels.items())[-5:]])
            parts.append(f"Personnes: {rel_str}")

        notes = p.get("personality_notes", [])
        if notes:
            parts.append(f"Notes perso: {'; '.join(notes[-5:])}")

        dislikes = p.get("dislikes", [])
        if dislikes:
            parts.append(f"N'aime pas: {', '.join(dislikes[-5:])}")

        return "\n".join(parts) if parts else "Profil en cours de construction."

    async def auto_learn(self, user_message: str, titan_reply: str):
        """Automatically extract personal info from conversations."""
        msg = user_message.lower()

        # Skip short messages — nothing personal in "ok" or "salut"
        if len(user_message) < 30:
            return

        # Only trigger on clearly personal statements
        triggers = [
            "j'aime", "je déteste", "je préfère", "j'adore",
            "mon objectif", "mon but", "mon projet",
            "il s'appelle", "elle s'appelle", "c'est mon", "c'est ma",
            "je travaille", "je bosse", "mon job", "mon taf",
            "ma passion", "mon hobby",
            "ma copine", "mon pote", "mon frère", "ma soeur", "ma famille",
            "mon anniversaire", "né le",
            "j'habite", "je vis à",
        ]

        if not any(t in msg for t in triggers):
            return  # Nothing personal to learn

        try:
            prompt = f"""Analyse ce message d'Augustin et extrais les informations personnelles:
Message: "{user_message}"
Reponse Titan: "{titan_reply[:200]}"

Retourne un JSON avec les champs pertinents:
{{"interests": [], "goals": [], "skills": [], "preferences": {{}}, "relationships": {{}}, "life_events": []}}
Retourne UNIQUEMENT le JSON, rien d'autre. Si rien a extraire, retourne {{}}"""
            text = ai_chat("Expert en extraction de donnees personnelles.", prompt, 500)
            # Extract JSON from response
            if "{" in text:
                json_start = text.index("{")
                json_end = text.rindex("}") + 1
                extracted = json.loads(text[json_start:json_end])
            else:
                return

            if not extracted or extracted == {}:
                return

            # Merge into profile
            profile = _load_profile()

            for field in ["interests", "goals", "skills", "dislikes", "personality_notes", "life_events"]:
                new_items = extracted.get(field, [])
                if new_items:
                    existing = profile.get(field, [])
                    for item in new_items:
                        if item and item not in existing:
                            existing.append(item)
                    profile[field] = existing[-30:]  # Keep last 30

            # Preferences (dict merge)
            new_prefs = extracted.get("preferences", {})
            if new_prefs:
                profile.setdefault("preferences", {}).update(new_prefs)

            # Relationships (dict merge)
            new_rels = extracted.get("relationships", {})
            if new_rels:
                profile.setdefault("relationships", {}).update(new_rels)

            profile["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            _save_profile(profile)

        except Exception:
            pass  # Silent fail, don't disrupt conversation

    def update_profile(self, field: str, value: str) -> str:
        """Manually update profile."""
        profile = _load_profile()

        list_fields = ["interests", "goals", "skills", "dislikes", "personality_notes", "life_events", "habits"]
        dict_fields = ["preferences", "relationships", "identity"]

        if field in list_fields:
            profile.setdefault(field, []).append(value)
            profile[field] = profile[field][-30:]
        elif field in dict_fields:
            parts = value.split(":", 1)
            if len(parts) == 2:
                profile.setdefault(field, {})[parts[0].strip()] = parts[1].strip()
            else:
                return f"Format pour {field}: /profileset {field} clé: valeur"
        else:
            return f"Champ inconnu: {field}. Dispo: {', '.join(list_fields + dict_fields)}"

        profile["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        _save_profile(profile)
        return f"✅ Profil mis à jour: {field} → {value}"

    def clear_field(self, field: str) -> str:
        """Clear a profile field."""
        profile = _load_profile()
        if field in profile:
            if isinstance(profile[field], list):
                profile[field] = []
            elif isinstance(profile[field], dict):
                profile[field] = {}
            _save_profile(profile)
            return f"🗑️ Champ '{field}' vidé."
        return f"Champ '{field}' non trouvé."
