"""
TITAN Module Registry — Le système nerveux central des modules.
Registre unique, auto-discovery, catégorisation, stats d'usage, activation/désactivation.

Usage:
    from .module_registry import registry
    registry.register("news", TitanNews(), category="intel")
    module = registry.get("news")
    stats = registry.stats()
"""

import importlib
import logging
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, Any

log = logging.getLogger("titan.registry")

MEMORY_DIR = Path(__file__).parent / "memory"
REGISTRY_FILE = MEMORY_DIR / "module_registry.json"


class ModuleRegistry:
    """Registre central de tous les modules TITAN.

    Features:
    - Auto-discovery des modules dans modules/
    - Catégorisation (core, intel, business, content, utility, fun, experiment, rdlab)
    - Stats d'usage (call count, last used, avg latency)
    - Activation/désactivation sans suppression
    - Dépendances déclaratives
    - Scoring de réputation (usage vs erreurs)
    - Persistance stats entre redémarrages
    """

    # Catégories et modules attendus
    MODULE_CATALOG = {
        # === CORE (toujours chargés) ===
        "brain":            {"category": "core",       "module": ".modules.brain",           "class": "TitanBrain",           "essential": True},
        "voice":            {"category": "core",       "module": ".modules.voice",           "class": "TitanVoice",           "essential": True},
        "gamification":     {"category": "core",       "module": ".modules.gamification",    "class": "TitanGamification",    "essential": True},
        "dashboard":        {"category": "core",       "module": ".modules.dashboard",       "class": "TitanDashboard",       "essential": True},
        "president":        {"category": "core",       "module": ".modules.president",       "class": "TitanPresident",       "essential": True},
        "memory":           {"category": "core",       "module": ".modules.memory",          "class": None,                   "essential": True},
        # === INTEL (renseignement & veille) ===
        "news":             {"category": "intel",      "module": ".modules.news",            "class": "TitanNews"},
        "ai_watch":         {"category": "intel",      "module": ".modules.ai_watch",        "class": "TitanAIWatch"},
        "morning_digest":   {"category": "intel",      "module": ".modules.morning_digest",  "class": "TitanMorningDigest"},
        "aggregator":       {"category": "intel",      "module": ".modules.aggregator",      "class": "TitanAggregator"},
        "strategic":        {"category": "intel",      "module": ".modules.strategic",       "class": "TitanStrategic"},
        # === BUSINESS (vente, clients, facturation) ===
        "upwork":           {"category": "business",   "module": ".modules.upwork",          "class": "TitanUpwork"},
        "email":            {"category": "business",   "module": ".modules.email_gen",       "class": "TitanEmailGen"},
        "invoice":          {"category": "business",   "module": ".modules.invoice",         "class": "TitanInvoice"},
        "startup":          {"category": "business",   "module": ".modules.startup",         "class": "TitanStartup"},
        "social":           {"category": "business",   "module": ".modules.social_media",    "class": "TitanSocial"},
        # === CONTENT (création & écriture) ===
        "writing":          {"category": "content",    "module": ".modules.writing",         "class": "TitanWriting"},
        "portfolio":        {"category": "content",    "module": ".modules.portfolio_gen",   "class": "TitanPortfolio"},
        "portfolio_live":   {"category": "content",    "module": ".modules.portfolio_live",  "class": "TitanPortfolioLive"},
        "ai_prompt":        {"category": "content",    "module": ".modules.ai_prompt",       "class": "TitanAIPrompt"},
        "empire_visual":    {"category": "content",    "module": ".modules.empire_visual",   "class": "TitanEmpireVisual"},
        "film":             {"category": "content",    "module": ".modules.film_building",   "class": "TitanFilm"},
        "mega_prompt":      {"category": "content",    "module": ".modules.mega_prompt",     "class": "TitanMegaPrompt"},
        "clones":           {"category": "content",    "module": ".modules.clones",          "class": "TitanClones"},
        # === UTILITY (outils pratiques) ===
        "web":              {"category": "utility",    "module": ".modules.web",             "class": "TitanWeb"},
        "perplexity":       {"category": "utility",    "module": ".modules.perplexity",      "class": "TitanPerplexity"},
        "code":             {"category": "utility",    "module": ".modules.code_assistant",  "class": "TitanCode"},
        "calendar":         {"category": "utility",    "module": ".modules.calendar",        "class": "TitanCalendar"},
        "task_master":      {"category": "utility",    "module": ".modules.task_master",     "class": "TitanTaskMaster"},
        "toolbox":          {"category": "utility",    "module": ".modules.toolbox",         "class": "TitanToolbox"},
        "productivity":     {"category": "utility",    "module": ".modules.productivity",    "class": "TitanProductivity"},
        "seo":              {"category": "utility",    "module": ".modules.seo",             "class": "TitanSEO"},
        "domains":          {"category": "utility",    "module": ".modules.domains",         "class": "TitanDomains"},
        "n8n":              {"category": "utility",    "module": ".modules.n8n",             "class": "TitanN8N"},
        # === WELLNESS (santé, sport, motivation) ===
        "sport_pro":        {"category": "wellness",   "module": ".modules.sport_pro",       "class": "TitanSportPro"},
        "motivation":       {"category": "wellness",   "module": ".modules.motivation",      "class": "TitanMotivation"},
        "coach":            {"category": "wellness",   "module": ".modules.coach",           "class": "TitanCoach"},
        "journal":          {"category": "wellness",   "module": ".modules.journal",         "class": "TitanJournal"},
        "auto_healer":      {"category": "wellness",   "module": ".modules.auto_healer",     "class": "TitanAutoHealer"},
        # === KNOWLEDGE (culture, apprentissage) ===
        "bible":            {"category": "knowledge",  "module": ".modules.bible",           "class": "TitanBible"},
        "culture":          {"category": "knowledge",  "module": ".modules.culture",         "class": "TitanCulture"},
        "library":          {"category": "knowledge",  "module": ".modules.library",         "class": "TitanLibrary"},
        "personal":         {"category": "knowledge",  "module": ".modules.personal",        "class": "TitanPersonal"},
        # === R&D LAB (recherche avancée) ===
        "rdlab_doctorant":  {"category": "rdlab",      "module": ".modules.rdlab_doctorant", "class": "TitanRDLabDoctorant"},
        "rdlab_digestor":   {"category": "rdlab",      "module": ".modules.rdlab_digestor",  "class": "TitanRDLabDigestor"},
        "rdlab_scout":      {"category": "rdlab",      "module": ".modules.rdlab_scout",     "class": "TitanRDLabScout"},
        "rdlab_experiment": {"category": "rdlab",      "module": ".modules.rdlab_experiment","class": "TitanRDLabExperiment"},
        "rdlab_horizon":    {"category": "rdlab",      "module": ".modules.rdlab_horizon",   "class": "TitanRDLabHorizon"},
        # === FINANCE ===
        "finance":          {"category": "finance",    "module": ".modules.finance",         "class": "TitanFinance"},
        "crypto_defi":      {"category": "finance",    "module": ".modules.crypto_defi",     "class": "TitanCryptoDefi"},
    }

    def __init__(self):
        self._modules: dict[str, dict] = {}
        self._instances: dict[str, Any] = {}
        self._boot_time = time.time()
        self._stats = self._load_stats()

    # === REGISTRATION ===

    def register(self, name: str, instance: Any, category: str = "utility",
                 enabled: bool = True, essential: bool = False):
        """Enregistre un module avec son instance."""
        self._modules[name] = {
            "category": category,
            "enabled": enabled,
            "essential": essential,
            "registered_at": datetime.now().isoformat(),
        }
        self._instances[name] = instance

        # Init stats si absent
        if name not in self._stats:
            self._stats[name] = {
                "call_count": 0,
                "error_count": 0,
                "total_latency_ms": 0,
                "last_used": None,
                "last_error": None,
            }
        log.debug(f"Registry: {name} registered ({category})")

    def register_lazy(self, name: str, module_path: str, class_name: str,
                      category: str = "utility", enabled: bool = True):
        """Enregistre un module sans l'importer — chargé au premier appel."""
        self._modules[name] = {
            "category": category,
            "enabled": enabled,
            "essential": False,
            "lazy": True,
            "module_path": module_path,
            "class_name": class_name,
            "registered_at": datetime.now().isoformat(),
        }
        if name not in self._stats:
            self._stats[name] = {
                "call_count": 0,
                "error_count": 0,
                "total_latency_ms": 0,
                "last_used": None,
                "last_error": None,
            }

    # === ACCESS ===

    def get(self, name: str) -> Optional[Any]:
        """Récupère un module. Lazy-load si nécessaire. Retourne None si désactivé."""
        meta = self._modules.get(name)
        if not meta:
            return None
        if not meta.get("enabled", True):
            return None

        # Lazy loading
        if name not in self._instances and meta.get("lazy"):
            try:
                mod = importlib.import_module(meta["module_path"], package="execution.titan")
                cls = getattr(mod, meta["class_name"])
                self._instances[name] = cls()
                log.info(f"Registry: lazy-loaded {name}")
            except Exception as e:
                log.error(f"Registry: failed to load {name}: {e}")
                self._record_error(name, str(e))
                return None

        return self._instances.get(name)

    def track_call(self, name: str, latency_ms: float = 0):
        """Enregistre un appel réussi avec sa latence."""
        if name in self._stats:
            self._stats[name]["call_count"] += 1
            self._stats[name]["total_latency_ms"] += latency_ms
            self._stats[name]["last_used"] = datetime.now().isoformat()

    def _record_error(self, name: str, error: str):
        """Enregistre une erreur pour un module."""
        if name not in self._stats:
            self._stats[name] = {"call_count": 0, "error_count": 0,
                                  "total_latency_ms": 0, "last_used": None, "last_error": None}
        self._stats[name]["error_count"] += 1
        self._stats[name]["last_error"] = f"{datetime.now().isoformat()} — {error[:200]}"

    # === CONTROL ===

    def enable(self, name: str) -> bool:
        """Active un module."""
        if name in self._modules:
            self._modules[name]["enabled"] = True
            log.info(f"Registry: {name} ENABLED")
            return True
        return False

    def disable(self, name: str) -> bool:
        """Désactive un module (sans le supprimer)."""
        meta = self._modules.get(name)
        if not meta:
            return False
        if meta.get("essential"):
            log.warning(f"Registry: cannot disable essential module {name}")
            return False
        meta["enabled"] = False
        log.info(f"Registry: {name} DISABLED")
        return True

    # === STATS & MONITORING ===

    def stats(self) -> dict:
        """Stats complètes de tous les modules."""
        result = {}
        for name, meta in self._modules.items():
            s = self._stats.get(name, {})
            calls = s.get("call_count", 0)
            errors = s.get("error_count", 0)
            total_latency = s.get("total_latency_ms", 0)

            result[name] = {
                "category": meta.get("category", "unknown"),
                "enabled": meta.get("enabled", True),
                "essential": meta.get("essential", False),
                "loaded": name in self._instances,
                "calls": calls,
                "errors": errors,
                "avg_latency_ms": round(total_latency / calls, 1) if calls > 0 else 0,
                "reputation": self._reputation(calls, errors),
                "last_used": s.get("last_used"),
            }
        return result

    def _reputation(self, calls: int, errors: int) -> int:
        """Score réputation 0-100 basé sur usage vs erreurs."""
        if calls == 0:
            return 50  # neutral
        ratio = calls / max(1, calls + errors * 5)  # errors pèsent 5x
        return min(100, max(0, int(ratio * 100)))

    def categories(self) -> dict:
        """Modules groupés par catégorie."""
        cats = {}
        for name, meta in self._modules.items():
            cat = meta.get("category", "unknown")
            if cat not in cats:
                cats[cat] = []
            cats[cat].append({
                "name": name,
                "enabled": meta.get("enabled", True),
                "calls": self._stats.get(name, {}).get("call_count", 0),
            })
        return cats

    def health_report(self) -> str:
        """Rapport santé du registre — texte formaté."""
        total = len(self._modules)
        enabled = sum(1 for m in self._modules.values() if m.get("enabled", True))
        loaded = len(self._instances)
        total_calls = sum(s.get("call_count", 0) for s in self._stats.values())
        total_errors = sum(s.get("error_count", 0) for s in self._stats.values())

        # Top 5 modules les plus utilisés
        top = sorted(self._stats.items(), key=lambda x: x[1].get("call_count", 0), reverse=True)[:5]
        top_str = "\n".join(f"  {n}: {s.get('call_count', 0)} calls" for n, s in top)

        # Modules en erreur
        errored = [(n, s) for n, s in self._stats.items() if s.get("error_count", 0) > 0]
        err_str = "\n".join(f"  ⚠️ {n}: {s['error_count']} erreurs" for n, s in errored) or "  Aucune"

        # Modules inactifs (0 calls, enabled)
        inactive = [n for n, s in self._stats.items()
                     if s.get("call_count", 0) == 0 and self._modules.get(n, {}).get("enabled", True)]

        uptime_min = int((time.time() - self._boot_time) / 60)

        return (
            f"🔧 REGISTRE TITAN — SANTÉ MODULES\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Modules : {enabled}/{total} actifs | {loaded} chargés en RAM\n"
            f"Appels totaux : {total_calls} | Erreurs : {total_errors}\n"
            f"Uptime : {uptime_min} min\n\n"
            f"📊 TOP 5 MODULES\n{top_str}\n\n"
            f"🔴 ERREURS\n{err_str}\n\n"
            f"💤 INACTIFS ({len(inactive)}): {', '.join(inactive[:10])}"
        )

    # === PERSISTENCE ===

    def _load_stats(self) -> dict:
        """Charge les stats persistées."""
        try:
            if REGISTRY_FILE.exists():
                with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception:
            pass
        return {}

    def save_stats(self):
        """Sauvegarde les stats sur disque."""
        try:
            MEMORY_DIR.mkdir(exist_ok=True)
            with open(REGISTRY_FILE, "w", encoding="utf-8") as f:
                json.dump(self._stats, f, ensure_ascii=False, indent=2)
        except Exception as e:
            log.error(f"Registry: save stats failed: {e}")

    # === AUTO-DISCOVERY ===

    def auto_register_from_catalog(self):
        """Enregistre tous les modules du catalogue en mode lazy."""
        for name, info in self.MODULE_CATALOG.items():
            if name not in self._modules:
                self.register_lazy(
                    name=name,
                    module_path=info["module"],
                    class_name=info.get("class", ""),
                    category=info["category"],
                    enabled=True,
                )
        log.info(f"Registry: {len(self.MODULE_CATALOG)} modules catalogués")

    # === API EXPORT (pour command_server) ===

    def to_api(self) -> dict:
        """Export complet pour l'API REST."""
        return {
            "total_modules": len(self._modules),
            "enabled": sum(1 for m in self._modules.values() if m.get("enabled", True)),
            "loaded": len(self._instances),
            "categories": self.categories(),
            "stats": self.stats(),
            "uptime_seconds": int(time.time() - self._boot_time),
        }


# === SINGLETON ===
registry = ModuleRegistry()
