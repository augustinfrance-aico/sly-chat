# INDEX AGENTS — Empire AICO

> Point d'entrée de l'empire. Tout commence ici.
> Avant tout run : lire ce fichier + CONTEXT_BOOT.md

---

## Équipe complète

→ **[ROSTER.md](ROSTER.md)** — Fiches de poste de chaque agent (forces, limites, KPI)
→ **[PIPELINE_STATE.md](PIPELINE_STATE.md)** — État en temps réel de tous les pipelines

---

## FLUX 1 — KDP (Carnets Amazon)

| Agent | Fichier | Mission |
|-------|---------|---------|
| SCRIBE | [kdp/SCRIBE.md](kdp/SCRIBE.md) | Génère le contenu intérieur des carnets |
| COVER | [kdp/COVER.md](kdp/COVER.md) | Crée les couvertures + mockups |
| PUBLISHER | [kdp/PUBLISHER.md](kdp/PUBLISHER.md) | Formate PDF + publie sur KDP |
| TRANSLATOR | [kdp/TRANSLATOR.md](kdp/TRANSLATOR.md) | Traduit en 6 langues = 6 ASINs |
| KEYWORD | [kdp/KEYWORD.md](kdp/KEYWORD.md) | SEO Amazon, mots-clés qui rankent |

## FLUX 2 — STOCK MEDIA (Photos IA)

| Agent | Fichier | Mission |
|-------|---------|---------|
| PIXEL | [stock/PIXEL.md](stock/PIXEL.md) | Génère photos IA par batch thématique |
| STOCKPUSH | [stock/STOCKPUSH.md](stock/STOCKPUSH.md) | Upload + métadonnées sur Shutterstock, Adobe, etc. |

---

## Pipelines complets

```
KDP :
SCRIBE (EN)
  ↓
COVER + KEYWORD + TRANSLATOR×5  ← EN PARALLÈLE
  ↓
PUBLISHER → KDP Upload
→ 6 ASINs Amazon (EN + 5 langues)

STOCK :
PIXEL (250 images/semaine, 8 niches)
  ↓
STOCKPUSH (5 plateformes en parallèle)
→ Revenus passifs
```

---

## Système de gouvernance

| Fichier | Rôle |
|---------|------|
| [../directives/ORCHESTRATOR.md](../directives/ORCHESTRATOR.md) | Cerveau — qui décide quoi lancer |
| [../directives/CONTRACTS.md](../directives/CONTRACTS.md) | Interfaces entre agents |
| [../directives/AUTONOMY.md](../directives/AUTONOMY.md) | Quand agir seul vs escalader à Augus |
| [../directives/ANNEALING.md](../directives/ANNEALING.md) | Protocole réparation si un agent plante |
| [../directives/ERRORS.md](../directives/ERRORS.md) | Mémoire des erreurs + fixes |
| [../directives/MEMORY_PROTOCOL.md](../directives/MEMORY_PROTOCOL.md) | Comment la mémoire fonctionne |
| [../directives/CONTEXT_BOOT.md](../directives/CONTEXT_BOOT.md) | Séquence démarrage obligatoire |
| [../directives/WEEKLY_BRIEF.md](../directives/WEEKLY_BRIEF.md) | Bilan hebdomadaire automatique |
| [../directives/DECISION_LOG.md](../directives/DECISION_LOG.md) | Journal des décisions stratégiques |
| [../directives/ONBOARDING.md](../directives/ONBOARDING.md) | Comment intégrer un nouvel agent |

## Mémoire partagée

| Fichier | Rôle |
|---------|------|
| [../.tmp/run_state.json](../.tmp/run_state.json) | État du run en cours (lire EN PREMIER) |
| [../.tmp/agent_memory.json](../.tmp/agent_memory.json) | Mémoire persistante (patterns, prefs, quotas) |
| [../.tmp/README.md](../.tmp/README.md) | Convention nommage artifacts |
| [../.tmp/CLEANUP.md](../.tmp/CLEANUP.md) | Règles de nettoyage |

---

## Règle OMEGA
> Coût 0€. Zéro intervention après lancement. Duplicable en < 2h sur nouvelle niche.
> Augus dirige. Les agents exécutent. Le système apprend.
