# Memory — Le Cerveau du Workspace

> Avant ce dossier : le workspace avait des notes (agent_memory.json).
> Après : il a un cerveau.

---

## La métaphore simple

**Avant (agent_memory.json) :**
Un carnet papier. Tu retrouves quelque chose seulement si tu sais exactement où chercher.

**Après (Mem0 Brain) :**
Un vrai cerveau. Tu demandes "comment on parle à Lurie ?" → il retrouve tout ce qui concerne Lurie, même si le souvenir dit "client Moldova", "anglais friendly", "contrat en attente".
Il comprend le sens, pas juste les mots.

---

## Les fichiers

| Fichier | Rôle | Métaphore |
|---------|------|-----------|
| `mem0_brain.py` | Le cerveau | Hippocampe — stocke et retrouve |
| `session_logger.py` | Le greffier | Scribe — grave après chaque session |
| `session_log.jsonl` | Le journal | Agenda — trace toutes les sessions |

---

## Comment ça marche

```
Session Claude Code
       ↓
  Décisions prises
  Erreurs corrigées
  Clients avancés
       ↓
session_logger.py (après session)
       ↓
  Extrait le juice
  de agent_memory.json + run_state.json
       ↓
mem0_brain.py → grave dans Mem0
       ↓
Cerveau plus riche pour la prochaine session
```

**Tu fais rien.** Le greffier fait tout.

---

## Modes

### Mode Cloud (Mem0 API — GRATUIT)
- Nécessite : `MEM0_API_KEY` dans `.env`
- Capacité : 10 000 souvenirs/mois gratuit
- Cherche par sens (vectoriel) — le plus intelligent
- Inscription : https://mem0.ai (free tier, pas de CB)

### Mode Local (fallback automatique)
- Aucune clé nécessaire
- Stocké dans `.tmp/mem0_local.json`
- Cherche par mots-clés — moins intelligent mais fonctionnel
- Activé automatiquement si pas de clé Mem0

---

## Commandes rapides

```bash
# Stats du cerveau
python memory/session_logger.py --stats

# Logger la session manuellement
python memory/session_logger.py

# Chercher dans la mémoire
python memory/session_logger.py --query "Lurie"
python memory/session_logger.py --query "erreur timezone"

# Amorcer le cerveau (première fois)
python memory/session_logger.py --seed

# Chercher directement via le cerveau
python memory/mem0_brain.py recall "comment parler à Lurie"
python memory/mem0_brain.py dump
python memory/mem0_brain.py stats
```

---

## Activer le mode Cloud (3 minutes)

1. Aller sur https://mem0.ai → créer compte gratuit
2. Copier la clé API
3. Ajouter dans `.env` :
   ```
   MEM0_API_KEY=m0-xxxxxxxxxxxxxxxx
   ```
4. Lancer : `python memory/session_logger.py --seed`

Le cerveau est amorcé avec 10 souvenirs fondamentaux sur Augus, AICO, les clients, les règles.

---

## Ce qui est gravé automatiquement

- Profil Augus (style, préférences, règles)
- État des clients (Lurie, Didier, Upwork)
- Décisions stratégiques prises
- Patterns techniques appris (erreurs résolues)
- Notes de session importantes

---

## Règle d'or

> Le cerveau s'enrichit. Il ne s'efface jamais.
> Chaque session = +N souvenirs permanents.
> Dans 6 mois, ce workspace sera l'un des plus intelligents possibles.
