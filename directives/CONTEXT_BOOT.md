# CONTEXT_BOOT — Séquence de Démarrage Obligatoire

> Ce fichier est le PREMIER que l'agent lit à chaque session.
> Il reconstruit le contexte complet en < 60 secondes.
> Sans ce boot, l'agent opère à l'aveugle.

---

## Pourquoi ce fichier existe

Les LLMs n'ont pas de mémoire entre sessions. C'est un fait.
Mais le workspace, lui, a une mémoire permanente.
Ce boot transforme un agent amnésique en agent contextualisé.

```
Sans CONTEXT_BOOT : "Bonjour, que dois-je faire ?"
Avec CONTEXT_BOOT : "Reprise KDP blood_sugar EN — COVER reste à faire."
```

---

## Séquence de boot (dans cet ordre, sans sauter)

### STEP 1 — État du run en cours (10 sec)
```
Lire : .tmp/run_state.json

Si status = "in_progress" :
  → Un run est en cours. Le reprendre en priorité absolue.
  → Ne pas démarrer autre chose.
  → Aller à AUTONOMY.md § "Autonomie inter-sessions"

Si status = "failed" :
  → Un run a échoué. Lire errors[] dans ce fichier.
  → Consulter ERRORS.md pour le fix.
  → Proposer à Augus : retry ou abandon ?

Si status = "idle" :
  → Aucun run en cours. Continuer le boot.
```

### STEP 2 — Mémoire de l'agent (15 sec)
```
Lire : .tmp/agent_memory.json

Extraire :
  - Dernières décisions prises (last_decisions[])
  - Patterns appris (learned_patterns[])
  - Préférences confirmées d'Augus (user_prefs{})
  - Niches en cours / prochaines (pipeline_queue[])
  - Quota APIs restant estimé (api_quotas{})
```

### STEP 3 — Erreurs et patterns connus (10 sec)
```
Lire : directives/ERRORS.md — section "Patterns récurrents"
(pas besoin de lire toutes les entrées — juste le tableau des patterns)

But : savoir d'emblée quelles erreurs sont probables aujourd'hui.
```

### STEP 4 — État des pipelines (10 sec)
```
Lire : agents/PIPELINE_STATE.md

Extraire :
  - KPI semaine en cours vs objectif
  - Quelle niche est prioritaire ?
  - Y a-t-il un pipeline en retard ?
```

### STEP 5 — Contexte projet (5 sec)
```
Lire : CLAUDE.md — section "Décisions Techniques" + "Clients actifs"

But : ne pas proposer des solutions incompatibles avec les contraintes du projet.
(ex: ne pas proposer une API payante si décision = ZERO coût)
```

### STEP 6 — Activation agents Cooper Building (5 sec)
```
Lire : CLAUDE.md — section "COOPER BUILDING"

RAPPEL CRITIQUE :
  → Sur CHAQUE réponse non-triviale, afficher 🏢 [COOPER] — [AGENTS]
  → Répondre avec la VOIX de l'agent (lire sa fiche personnalites/{nom}.md)
  → LIMPIDE termine si output complexe (💎)
  → Les agents sont le CŒUR du système, pas un gadget optionnel
```

### STEP 7 — Synthesis (10 sec)
```
Produire mentalement le résumé suivant avant d'agir :

"Je suis dans le workspace AICO.
 Run en cours : [OUI / NON] → [reprendre depuis ÉTAPE X / rien en cours]
 Prochaine priorité : [KDP niche X langue Y / STOCK niche Z / attendre Augus]
 Erreurs à surveiller : [liste des patterns récurrents pertinents]
 Contraintes actives : [ZERO coût / utiliser Claude Max / ...]
 Agents actifs : [SENTINEL dispatch ON — Building prêt]"
```

---

## Temps de boot cible

| Step | Fichier | Temps cible |
|------|---------|-------------|
| 1 — Run en cours | .tmp/run_state.json | 10 sec |
| 2 — Mémoire agent | .tmp/agent_memory.json | 15 sec |
| 3 — Patterns d'erreurs | directives/ERRORS.md (tableau) | 10 sec |
| 4 — État pipelines | agents/PIPELINE_STATE.md | 10 sec |
| 5 — Contexte projet | CLAUDE.md (2 sections) | 5 sec |
| 6 — Activation agents | CLAUDE.md (section Cooper Building) | 5 sec |
| 7 — Synthesis | (interne) | 10 sec |
| **TOTAL** | | **< 65 sec** |

---

## Ce que le boot NE fait PAS

- Ne lit pas tous les fichiers directives (trop long, inutile sauf si nécessaire)
- Ne relit pas l'historique des runs complets (run_history.json) — sauf si Augus demande un bilan
- Ne reformule pas ce qu'il a appris à Augus (il agit directement)
- Ne demande pas "est-ce que tu veux que je continue ?" si un run est in_progress

---

## Boot spécial : nouvelle session sans run_state.json

Si `.tmp/run_state.json` n'existe pas ou est corrompu :
```
1. Recréer run_state.json vide (template dans .tmp/README.md)
2. Consulter PIPELINE_STATE.md pour identifier la priorité
3. Demander à Augus : "Aucun run en cours. Quelle niche on lance ?"
```

---

## Déclencheurs de re-boot

Le boot complet se refait si :
- Nouvelle session (obligatoire)
- > 2h sans activité dans la même session (contexte potentiellement périmé)
- Augus dit "reprends depuis le début" ou "rafraîchis-toi le contexte"

Re-boot partiel (juste STEP 1 + 2) si :
- Changement de pipeline dans la même session
- Après un incident ANNEALING résolu
