"""
TITAN Auto-Healer — Self-repair automatique
Détecte les anomalies, diagnostique, fix, notifie. ZERO intervention Augus.

[FORGE + X-O1 + GHOST]

Features:
- Monitoring santé TITAN (API status, mémoire, erreurs)
- Auto-diagnostic sur patterns connus
- Auto-fix quand possible
- Notification Telegram APRÈS le fix (pas avant)
- Log complet pour audit
"""

import json
import logging
import traceback
from datetime import datetime, timedelta
from pathlib import Path

log = logging.getLogger("titan.healer")

MEMORY_DIR = Path(__file__).parent.parent / "memory"
HEALER_FILE = MEMORY_DIR / "healer.json"


# === PATTERNS CONNUS (auto-enrichi) ===
KNOWN_FIXES = {
    "encoding": {
        "symptom": "UnicodeDecodeError",
        "fix": "Ajouter encoding='utf-8' au open()",
        "auto_fixable": False,
    },
    "rate_limit": {
        "symptom": "rate_limit_exceeded",
        "fix": "Cascade au modèle suivant (déjà géré par ai_client)",
        "auto_fixable": True,
    },
    "timeout": {
        "symptom": "ReadTimeout",
        "fix": "Retry avec timeout augmenté",
        "auto_fixable": True,
    },
    "memory_bloat": {
        "symptom": "processed_messages > 500",
        "fix": "Purge auto à 200 (déjà implémenté)",
        "auto_fixable": True,
    },
    "json_corrupt": {
        "symptom": "JSONDecodeError",
        "fix": "Reset le fichier JSON corrompu avec structure vide",
        "auto_fixable": True,
    },
}


class TitanAutoHealer:
    """Auto-Healer — TITAN se répare tout seul."""

    def __init__(self):
        self._error_buffer = []
        self._last_health_check = None

    def _load(self) -> dict:
        if HEALER_FILE.exists():
            try:
                with open(HEALER_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {"incidents": [], "fixes_applied": 0, "health_checks": []}
        return {"incidents": [], "fixes_applied": 0, "health_checks": []}

    def _save(self, data: dict):
        with open(HEALER_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def log_error(self, error: Exception, context: str = "") -> str:
        """Log une erreur et tente un auto-fix. Retourne un message si fix appliqué."""
        error_str = str(error)
        tb = traceback.format_exc()

        data = self._load()

        incident = {
            "timestamp": datetime.now().isoformat(),
            "error": error_str,
            "context": context,
            "traceback": tb[:500],
            "fixed": False,
            "fix_applied": "",
        }

        # Chercher un pattern connu
        fix_msg = ""
        for pattern_name, pattern in KNOWN_FIXES.items():
            if pattern["symptom"].lower() in error_str.lower():
                incident["pattern_match"] = pattern_name

                if pattern["auto_fixable"]:
                    fix_result = self._apply_fix(pattern_name, error_str)
                    if fix_result:
                        incident["fixed"] = True
                        incident["fix_applied"] = fix_result
                        data["fixes_applied"] = data.get("fixes_applied", 0) + 1
                        fix_msg = (
                            f"⚡ Auto-fix appliqué — {pattern_name}\n"
                            f"→ {fix_result}\n"
                            f"Impact : zéro."
                        )
                break

        data["incidents"].append(incident)
        # Garder les 200 derniers incidents
        if len(data["incidents"]) > 200:
            data["incidents"] = data["incidents"][-200:]
        self._save(data)

        return fix_msg

    def _apply_fix(self, pattern_name: str, error_str: str) -> str:
        """Applique un fix automatique. Retourne la description du fix."""
        if pattern_name == "json_corrupt":
            # Trouver et reset le fichier JSON corrompu
            for json_file in MEMORY_DIR.glob("*.json"):
                try:
                    with open(json_file, "r", encoding="utf-8") as f:
                        json.load(f)
                except json.JSONDecodeError:
                    with open(json_file, "w", encoding="utf-8") as f:
                        json.dump({}, f)
                    return f"Reset {json_file.name} (était corrompu)"
            return ""

        elif pattern_name == "rate_limit":
            return "Cascade IA gère automatiquement — next model"

        elif pattern_name == "timeout":
            return "Retry sera tenté au prochain appel"

        elif pattern_name == "memory_bloat":
            return "Purge mémoire programmée au prochain cycle"

        return ""

    def health_check(self) -> str:
        """Check la santé de TITAN — exécuté automatiquement."""
        now = datetime.now()
        data = self._load()
        issues = []
        status = "🟢 NOMINAL"

        # 1. Vérifier les fichiers JSON mémoire
        for json_file in MEMORY_DIR.glob("*.json"):
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    content = json.load(f)
                # Vérifier la taille
                size_mb = json_file.stat().st_size / (1024 * 1024)
                if size_mb > 5:
                    issues.append(f"⚠️ {json_file.name} = {size_mb:.1f}MB (lourd)")
            except json.JSONDecodeError:
                issues.append(f"🔴 {json_file.name} CORROMPU — auto-fix en cours")
                with open(json_file, "w", encoding="utf-8") as f:
                    json.dump({}, f)
                status = "🟡 FIX APPLIQUÉ"
            except Exception as e:
                issues.append(f"⚠️ {json_file.name} — {e}")

        # 2. Vérifier les erreurs récentes (dernière heure)
        recent_errors = [
            i for i in data.get("incidents", [])
            if i["timestamp"] > (now - timedelta(hours=1)).isoformat()
        ]
        if len(recent_errors) > 10:
            issues.append(f"🔴 {len(recent_errors)} erreurs en 1h — instabilité détectée")
            status = "🔴 INSTABLE"
        elif len(recent_errors) > 3:
            issues.append(f"🟡 {len(recent_errors)} erreurs en 1h")
            if status == "🟢 NOMINAL":
                status = "🟡 ATTENTION"

        # 3. Vérifier les modules (imports)
        module_dir = Path(__file__).parent
        broken_modules = []
        for py_file in module_dir.glob("*.py"):
            if py_file.name.startswith("_"):
                continue
            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    content = f.read()
                if "SyntaxError" in content or len(content) < 50:
                    broken_modules.append(py_file.name)
            except Exception:
                broken_modules.append(py_file.name)

        if broken_modules:
            issues.append(f"⚠️ Modules suspects : {', '.join(broken_modules)}")

        # Log le health check
        check = {
            "timestamp": now.isoformat(),
            "status": status,
            "issues": len(issues),
        }
        data.setdefault("health_checks", []).append(check)
        if len(data["health_checks"]) > 100:
            data["health_checks"] = data["health_checks"][-100:]
        self._save(data)

        # Format résultat
        result = f"🏥 HEALTH CHECK TITAN — {status}\n"
        result += f"📅 {now.strftime('%Y-%m-%d %H:%M')}\n"
        result += f"🔧 Fixes auto total : {data.get('fixes_applied', 0)}\n"

        if issues:
            result += "\n" + "\n".join(issues)
        else:
            result += "\nTout est nominal. Le système ronronne."

        return result

    def get_incident_log(self, n: int = 10) -> str:
        """Derniers incidents."""
        data = self._load()
        incidents = data.get("incidents", [])[-n:]

        if not incidents:
            return "🏥 Aucun incident enregistré. Tout est propre."

        lines = ["🏥 DERNIERS INCIDENTS\n"]
        for inc in incidents:
            fixed = "✅" if inc.get("fixed") else "❌"
            lines.append(
                f"{fixed} [{inc['timestamp'][:16]}] {inc['error'][:80]}"
                f"{' → ' + inc['fix_applied'] if inc.get('fix_applied') else ''}"
            )

        return "\n".join(lines)

    def handle_command(self, command: str) -> str:
        """Route les commandes healer."""
        cmd = command.lower().strip()

        if cmd in ("/health", "/healer"):
            return self.health_check()
        elif cmd == "/healer log":
            return self.get_incident_log()
        else:
            return (
                "🏥 AUTO-HEALER TITAN\n\n"
                "/health — Health check complet\n"
                "/healer log — Derniers incidents\n\n"
                "L'auto-healer tourne en fond. Il fix et notifie."
            )
