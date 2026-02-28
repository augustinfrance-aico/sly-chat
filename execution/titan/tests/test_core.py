"""
TITAN Core Tests — Filet de sécurité.
Tests unitaires pour les modules critiques.
Run: python -m pytest execution/titan/tests/ -v
"""

import json
import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))


# ============================================================
# TEST 1: Memory Module — Thread-safe I/O
# ============================================================

class TestMemory:
    """Tests pour le module mémoire."""

    def setup_method(self):
        """Setup temp directory for each test."""
        self.tmpdir = tempfile.mkdtemp()
        self.orig_dir = None

    def test_remember_recall(self):
        """remember() puis recall() retourne la bonne valeur."""
        from execution.titan.modules import memory

        # Patch the memory file to temp
        original_file = memory.MEMORY_FILE
        memory.MEMORY_FILE = Path(self.tmpdir) / "test_memory.json"

        try:
            result = memory.remember("test_key", "test_value", "general")
            assert "Mémorisé" in result
            assert memory.recall("test_key") == "test_value"
        finally:
            memory.MEMORY_FILE = original_file

    def test_forget(self):
        """forget() supprime bien l'entrée."""
        from execution.titan.modules import memory

        original_file = memory.MEMORY_FILE
        memory.MEMORY_FILE = Path(self.tmpdir) / "test_memory2.json"

        try:
            memory.remember("delete_me", "value")
            result = memory.forget("delete_me")
            assert "Oublié" in result
            assert memory.recall("delete_me") is None
        finally:
            memory.MEMORY_FILE = original_file

    def test_search_memory(self):
        """search_memory() trouve les résultats."""
        from execution.titan.modules import memory

        original_file = memory.MEMORY_FILE
        memory.MEMORY_FILE = Path(self.tmpdir) / "test_memory3.json"

        try:
            memory.remember("projet_alpha", "client Lurie")
            results = memory.search_memory("alpha")
            assert len(results) > 0
            assert results[0]["key"] == "projet_alpha"
        finally:
            memory.MEMORY_FILE = original_file

    def test_conversation_roundtrip(self):
        """save_conversation() + get_recent_conversations() fonctionne."""
        from execution.titan.modules import memory

        original_file = memory.CONVERSATIONS_FILE
        memory.CONVERSATIONS_FILE = Path(self.tmpdir) / "test_convos.json"

        try:
            memory.save_conversation("hello", "world", "test")
            convos = memory.get_recent_conversations(5)
            assert len(convos) == 1
            assert convos[0]["user"] == "hello"
            assert convos[0]["titan"] == "world"
        finally:
            memory.CONVERSATIONS_FILE = original_file

    def test_conversation_dedup(self):
        """Les doublons exactes sont ignorées."""
        from execution.titan.modules import memory

        original_file = memory.CONVERSATIONS_FILE
        memory.CONVERSATIONS_FILE = Path(self.tmpdir) / "test_dedup.json"

        try:
            memory.save_conversation("same", "same", "test")
            memory.save_conversation("same", "same", "test")
            convos = memory.get_recent_conversations(10)
            assert len(convos) == 1  # only 1, not 2
        finally:
            memory.CONVERSATIONS_FILE = original_file

    def test_auto_facts(self):
        """save_auto_fact() + get_auto_facts() fonctionne."""
        from execution.titan.modules import memory

        original_file = memory.AUTO_FACTS_FILE
        memory.AUTO_FACTS_FILE = Path(self.tmpdir) / "test_facts.json"

        try:
            memory.save_auto_fact("J'aime le café", category="preference")
            facts = memory.get_auto_facts(10)
            assert len(facts) == 1
            assert facts[0]["fact"] == "J'aime le café"
        finally:
            memory.AUTO_FACTS_FILE = original_file

    def test_auto_facts_dedup(self):
        """Les faits dupliqués ne sont pas sauvegardés."""
        from execution.titan.modules import memory

        original_file = memory.AUTO_FACTS_FILE
        memory.AUTO_FACTS_FILE = Path(self.tmpdir) / "test_facts_dedup.json"

        try:
            memory.save_auto_fact("même fait", category="perso")
            memory.save_auto_fact("même fait", category="perso")
            facts = memory.get_auto_facts(10)
            assert len(facts) == 1
        finally:
            memory.AUTO_FACTS_FILE = original_file

    def test_integrity_check(self):
        """integrity_check() retourne un dict valide."""
        from execution.titan.modules import memory
        result = memory.integrity_check()
        assert isinstance(result, dict)
        for key in result:
            assert "status" in result[key]


# ============================================================
# TEST 2: AI Client — Cache & Scoring
# ============================================================

class TestAIClient:
    """Tests pour le client IA."""

    def test_cache_key_deterministic(self):
        """Le même input produit le même cache key."""
        from execution.titan.ai_client import _cache_key
        k1 = _cache_key("system", "message")
        k2 = _cache_key("system", "message")
        assert k1 == k2

    def test_cache_key_different(self):
        """Inputs différents = keys différents."""
        from execution.titan.ai_client import _cache_key
        k1 = _cache_key("system", "message1")
        k2 = _cache_key("system", "message2")
        assert k1 != k2

    def test_cache_put_get(self):
        """Cache put/get fonctionne."""
        from execution.titan.ai_client import _cache_put, _cache_get
        _cache_put("test_key_xyz", "test_value")
        assert _cache_get("test_key_xyz") == "test_value"

    def test_cache_ttl(self):
        """Cache expire après TTL."""
        from execution.titan.ai_client import _response_cache
        # Insert with old timestamp
        _response_cache["old_key"] = {"text": "old", "ts": 0}
        from execution.titan.ai_client import _cache_get
        assert _cache_get("old_key") is None  # expired

    def test_response_scoring(self):
        """Le scoring de réponse produit un score 0-100."""
        from execution.titan.ai_client import _score_response
        assert 0 <= _score_response("Voici la réponse structurée.\nÉtape 1: faire X.") <= 100
        assert _score_response("") < 50  # vide = mauvais
        assert _score_response("Erreur impossible désolé") < 60  # négatif

    def test_dedup_sentences(self):
        """Les phrases dupliquées sont supprimées."""
        from execution.titan.ai_client import _dedup_sentences
        text = "Bonjour. Bonjour. Comment ça va."
        result = _dedup_sentences(text)
        assert result.count("Bonjour") == 1

    def test_strip_questions(self):
        """Les questions sont filtrées."""
        from execution.titan.ai_client import _strip_questions
        text = "Voici la réponse. Tu veux en savoir plus?"
        result = _strip_questions(text)
        assert "?" not in result

    def test_latency_tracking(self):
        """Le tracking de latence fonctionne."""
        from execution.titan.ai_client import _track_latency, get_latency_stats
        _track_latency("test-model", 150.5, 100, True)
        stats = get_latency_stats()
        assert "test-model" in stats
        assert stats["test-model"]["calls"] >= 1

    def test_groq_auto_reorder(self):
        """L'auto-reorder retourne une liste de modèles."""
        from execution.titan.ai_client import _get_optimized_groq_order, GROQ_MODELS
        order = _get_optimized_groq_order()
        assert len(order) == len(GROQ_MODELS)
        assert set(order) == set(GROQ_MODELS)


# ============================================================
# TEST 3: Module Registry
# ============================================================

class TestModuleRegistry:
    """Tests pour le registre de modules."""

    def test_register_and_get(self):
        """Enregistrer et récupérer un module."""
        from execution.titan.module_registry import ModuleRegistry
        reg = ModuleRegistry()
        dummy = MagicMock()
        reg.register("test_mod", dummy, category="utility")
        assert reg.get("test_mod") is dummy

    def test_disable_module(self):
        """Désactiver un module le rend indisponible."""
        from execution.titan.module_registry import ModuleRegistry
        reg = ModuleRegistry()
        dummy = MagicMock()
        reg.register("temp_mod", dummy, category="utility")
        reg.disable("temp_mod")
        assert reg.get("temp_mod") is None

    def test_enable_module(self):
        """Réactiver un module le rend disponible."""
        from execution.titan.module_registry import ModuleRegistry
        reg = ModuleRegistry()
        dummy = MagicMock()
        reg.register("toggle_mod", dummy, category="utility")
        reg.disable("toggle_mod")
        reg.enable("toggle_mod")
        assert reg.get("toggle_mod") is dummy

    def test_cannot_disable_essential(self):
        """Les modules essentiels ne peuvent pas être désactivés."""
        from execution.titan.module_registry import ModuleRegistry
        reg = ModuleRegistry()
        dummy = MagicMock()
        reg.register("core_mod", dummy, category="core", essential=True)
        assert reg.disable("core_mod") is False
        assert reg.get("core_mod") is dummy

    def test_track_call(self):
        """track_call() incrémente les stats."""
        from execution.titan.module_registry import ModuleRegistry
        reg = ModuleRegistry()
        dummy = MagicMock()
        reg.register("tracked", dummy)
        reg.track_call("tracked", latency_ms=150)
        stats = reg.stats()
        assert stats["tracked"]["calls"] == 1

    def test_reputation_score(self):
        """Le score de réputation est entre 0 et 100."""
        from execution.titan.module_registry import ModuleRegistry
        reg = ModuleRegistry()
        score = reg._reputation(100, 0)
        assert score == 100
        score = reg._reputation(0, 0)
        assert score == 50  # neutral
        score = reg._reputation(10, 10)
        assert 0 <= score <= 100

    def test_categories(self):
        """categories() retourne un dict par catégorie."""
        from execution.titan.module_registry import ModuleRegistry
        reg = ModuleRegistry()
        reg.register("mod_a", MagicMock(), category="core")
        reg.register("mod_b", MagicMock(), category="utility")
        cats = reg.categories()
        assert "core" in cats
        assert "utility" in cats

    def test_health_report(self):
        """health_report() retourne un string lisible."""
        from execution.titan.module_registry import ModuleRegistry
        reg = ModuleRegistry()
        reg.register("test", MagicMock())
        report = reg.health_report()
        assert "REGISTRE TITAN" in report

    def test_to_api(self):
        """to_api() retourne un dict sérialisable."""
        from execution.titan.module_registry import ModuleRegistry
        reg = ModuleRegistry()
        reg.register("api_test", MagicMock())
        data = reg.to_api()
        assert "total_modules" in data
        assert "categories" in data
        # Check it's JSON serializable
        json.dumps(data)


# ============================================================
# TEST 4: Config
# ============================================================

class TestConfig:
    """Tests pour la configuration."""

    def test_titan_mode_default(self):
        """Mode par défaut = normal."""
        from execution.titan.config import TITAN_MODE
        assert TITAN_MODE in ("normal", "safe", "diagnostic")

    def test_paths_exist(self):
        """Les chemins de base existent."""
        from execution.titan.config import TITAN_DIR, MEMORY_DIR
        assert TITAN_DIR.exists()
        assert MEMORY_DIR.exists()

    def test_personality_not_empty(self):
        """La personnalité TITAN est définie."""
        from execution.titan.config import TITAN_PERSONALITY
        assert len(TITAN_PERSONALITY) > 100


# ============================================================
# TEST 5: Brain
# ============================================================

class TestBrain:
    """Tests pour le cerveau."""

    def test_brain_init(self):
        """Le brain s'initialise correctement."""
        from execution.titan.modules.brain import TitanBrain
        brain = TitanBrain()
        assert brain.modules == {}
        assert brain._think_count == 0

    def test_system_prompt_generation(self):
        """Le system prompt est généré et contient les sections clés."""
        from execution.titan.modules.brain import TitanBrain
        brain = TitanBrain()
        prompt = brain.get_system_prompt("test message")
        assert "TITAN" in prompt
        assert "REGLES" in prompt
        assert "EXPERTISE" in prompt

    def test_agent_cameo_categories(self):
        """Toutes les catégories de cameo ont des agents."""
        from execution.titan.modules.brain import TitanBrain
        brain = TitanBrain()
        for cat, agents in brain.AGENT_CAMEOS.items():
            assert len(agents) > 0, f"Category {cat} has no agents"

    def test_cameo_triggers_match_categories(self):
        """Chaque trigger correspond à une catégorie de cameo."""
        from execution.titan.modules.brain import TitanBrain
        brain = TitanBrain()
        for cat in brain.CAMEO_TRIGGERS:
            assert cat in brain.AGENT_CAMEOS, f"Trigger category {cat} not in AGENT_CAMEOS"

    def test_performance_stats(self):
        """get_performance_stats() retourne des stats valides."""
        from execution.titan.modules.brain import TitanBrain
        brain = TitanBrain()
        stats = brain.get_performance_stats()
        assert "avg_quality" in stats
        assert "total_thinks" in stats

    def test_extract_facts_patterns(self):
        """_extract_facts détecte les patterns clés."""
        from execution.titan.modules.brain import TitanBrain
        brain = TitanBrain()
        # Should not crash on various inputs
        brain._extract_facts("je suis développeur freelance", "Super!")
        brain._extract_facts("ok", "Reçu.")  # trivial — skipped
        brain._extract_facts("j'ai décidé de lancer le projet alpha demain", "Go!")
