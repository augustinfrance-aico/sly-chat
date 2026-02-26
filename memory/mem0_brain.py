"""
mem0_brain.py — Le Cerveau Persistant du Workspace AICO

Métaphore : si agent_memory.json est un carnet de notes,
Mem0 est un vrai cerveau. Il cherche par SENS, pas par mot exact.

Tu demandes "timezones" → il trouve Moldova, Lurie, n8n, 7ème news.
Sans que tu aies écrit ces mots.

Tier gratuit Mem0 : 10 000 souvenirs/mois. Largement suffisant.
Fallback local (ChromaDB) si hors ligne ou quota dépassé.

Usage :
    from memory.mem0_brain import brain
    brain.remember("Lurie aime les rapports en anglais friendly")
    resultats = brain.recall("comment parler à Lurie ?")
"""

import os
import json
from datetime import datetime
from pathlib import Path

# ─── CONFIG ────────────────────────────────────────────────────────────────────

WORKSPACE = Path(__file__).parent.parent
MEM0_API_KEY = os.getenv("MEM0_API_KEY", "")  # Optionnel — fallback local si absent
LOCAL_MEMORY_FILE = WORKSPACE / ".tmp" / "mem0_local.json"
USER_ID = "augus_aico"  # Identifiant unique pour isoler la mémoire

# ─── CERVEAU PRINCIPAL ─────────────────────────────────────────────────────────

class Brain:
    """
    Le cerveau. Deux modes :
    - Mode Cloud (Mem0 API) : mémoire vectorielle vraie, cherche par sens
    - Mode Local (fallback) : JSON simple, cherche par mots-clés

    Le mode s'active automatiquement selon si MEM0_API_KEY est définie.
    """

    def __init__(self):
        self.mode = "cloud" if MEM0_API_KEY else "local"
        self._client = None
        self._local_data = None
        self._init()

    def _init(self):
        if self.mode == "cloud":
            self._init_cloud()
        else:
            self._init_local()

    def _init_cloud(self):
        try:
            from mem0 import MemoryClient
            self._client = MemoryClient(api_key=MEM0_API_KEY)
            print(f"[BRAIN] Mode cloud activé (Mem0)")
        except ImportError:
            print("[BRAIN] mem0 pas installé → fallback local")
            self.mode = "local"
            self._init_local()
        except Exception as e:
            print(f"[BRAIN] Erreur cloud ({e}) → fallback local")
            self.mode = "local"
            self._init_local()

    def _init_local(self):
        LOCAL_MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        if LOCAL_MEMORY_FILE.exists():
            with open(LOCAL_MEMORY_FILE, encoding="utf-8") as f:
                self._local_data = json.load(f)
        else:
            self._local_data = {"memories": [], "_doc": "Mémoire locale fallback — cherche par mots-clés"}
        print(f"[BRAIN] Mode local activé ({len(self._local_data['memories'])} souvenirs)")

    # ─── API PUBLIQUE ───────────────────────────────────────────────────────────

    def remember(self, content: str, category: str = "general") -> dict:
        """
        Grave un souvenir dans le cerveau.

        Args:
            content: Ce qu'on veut retenir (en langage naturel, pas de JSON)
            category: Tag optionnel (client, erreur, decision, pattern, ...)

        Returns:
            {"status": "ok", "id": ..., "mode": ...}
        """
        if self.mode == "cloud":
            return self._cloud_remember(content, category)
        else:
            return self._local_remember(content, category)

    def recall(self, query: str, limit: int = 5) -> list[dict]:
        """
        Cherche dans le cerveau par sens (cloud) ou mots-clés (local).

        Args:
            query: Question en langage naturel
            limit: Nombre max de résultats

        Returns:
            Liste de {"memory": str, "score": float, "created_at": str}
        """
        if self.mode == "cloud":
            return self._cloud_recall(query, limit)
        else:
            return self._local_recall(query, limit)

    def forget(self, memory_id: str) -> bool:
        """Supprime un souvenir spécifique par son ID."""
        if self.mode == "cloud":
            try:
                self._client.delete(memory_id)
                return True
            except:
                return False
        else:
            self._local_data["memories"] = [
                m for m in self._local_data["memories"] if m.get("id") != memory_id
            ]
            self._save_local()
            return True

    def dump_all(self, limit: int = 20) -> list[dict]:
        """Retourne les N derniers souvenirs — pour audit ou debug."""
        if self.mode == "cloud":
            try:
                results = self._client.get_all(user_id=USER_ID)
                memories = results if isinstance(results, list) else results.get("results", [])
                return [
                    {"id": m.get("id"), "memory": m.get("memory", ""), "created_at": m.get("created_at", "")}
                    for m in memories[:limit]
                ]
            except Exception as e:
                return [{"error": str(e)}]
        else:
            return self._local_data["memories"][-limit:]

    def stats(self) -> dict:
        """Résumé de l'état du cerveau."""
        total = 0
        if self.mode == "cloud":
            try:
                all_mem = self._client.get_all(user_id=USER_ID)
                if isinstance(all_mem, list):
                    total = len(all_mem)
                elif isinstance(all_mem, dict):
                    total = len(all_mem.get("results", all_mem.get("memories", [])))
                elif hasattr(all_mem, "__len__"):
                    total = len(all_mem)
                else:
                    total = 0
            except:
                total = "?"
        else:
            total = len(self._local_data.get("memories", []))

        return {
            "mode": self.mode,
            "total_memories": total,
            "user_id": USER_ID,
            "local_file": str(LOCAL_MEMORY_FILE) if self.mode == "local" else None
        }

    # ─── IMPLÉMENTATIONS CLOUD ──────────────────────────────────────────────────

    def _cloud_remember(self, content: str, category: str) -> dict:
        try:
            result = self._client.add(
                content,
                user_id=USER_ID,
                metadata={"category": category, "added_at": datetime.now().isoformat()}
            )
            return {"status": "ok", "mode": "cloud", "result": result}
        except Exception as e:
            print(f"[BRAIN] Cloud remember failed: {e} → fallback local")
            return self._local_remember(content, category)

    def _cloud_recall(self, query: str, limit: int) -> list[dict]:
        try:
            results = self._client.search(query, user_id=USER_ID, limit=limit)
            memories = results if isinstance(results, list) else results.get("results", [])
            return [
                {
                    "memory": m.get("memory", ""),
                    "score": round(m.get("score", 0), 3),
                    "created_at": m.get("created_at", ""),
                    "category": m.get("metadata", {}).get("category", ""),
                    "id": m.get("id", "")
                }
                for m in memories
            ]
        except Exception as e:
            print(f"[BRAIN] Cloud recall failed: {e} → fallback local")
            return self._local_recall(query, limit)

    # ─── IMPLÉMENTATIONS LOCALES ────────────────────────────────────────────────

    def _local_remember(self, content: str, category: str) -> dict:
        import hashlib
        mem_id = hashlib.md5(f"{content}{datetime.now().isoformat()}".encode()).hexdigest()[:8]
        entry = {
            "id": mem_id,
            "memory": content,
            "category": category,
            "created_at": datetime.now().isoformat()
        }
        self._local_data["memories"].append(entry)
        self._save_local()
        return {"status": "ok", "mode": "local", "id": mem_id}

    def _local_recall(self, query: str, limit: int) -> list[dict]:
        """Recherche par mots-clés simples (pas vectorielle mais fonctionnel)."""
        keywords = query.lower().split()
        scored = []
        for mem in self._local_data["memories"]:
            text = mem.get("memory", "").lower()
            score = sum(1 for kw in keywords if kw in text) / max(len(keywords), 1)
            if score > 0:
                scored.append({**mem, "score": round(score, 3)})
        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:limit]

    def _save_local(self):
        with open(LOCAL_MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(self._local_data, f, ensure_ascii=False, indent=2)


# ─── INSTANCE GLOBALE ───────────────────────────────────────────────────────────

brain = Brain()


# ─── CLI RAPIDE ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    args = sys.argv[1:]

    if not args or args[0] == "stats":
        s = brain.stats()
        print(f"\n🧠 Cerveau AICO")
        print(f"   Mode    : {s['mode']}")
        print(f"   Souvenirs : {s['total_memories']}")
        print(f"   User ID : {s['user_id']}\n")

    elif args[0] == "remember" and len(args) > 1:
        content = " ".join(args[1:])
        r = brain.remember(content)
        print(f"✅ Gravé ({r['mode']}) : {content}")

    elif args[0] == "recall" and len(args) > 1:
        query = " ".join(args[1:])
        results = brain.recall(query)
        print(f"\n🔍 Résultats pour : '{query}'")
        if not results:
            print("   Aucun souvenir trouvé.")
        for r in results:
            score_bar = "█" * int(r["score"] * 10)
            print(f"   [{score_bar:<10}] {r['memory']}")
        print()

    elif args[0] == "dump":
        memories = brain.dump_all(20)
        print(f"\n📚 {len(memories)} derniers souvenirs :")
        for m in memories:
            print(f"   [{m.get('created_at','?')[:10]}] {m.get('memory','')}")
        print()

    else:
        print("Usage: python mem0_brain.py [stats|remember <texte>|recall <query>|dump]")
