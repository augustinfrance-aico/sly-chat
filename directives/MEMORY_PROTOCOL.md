# MEMORY PROTOCOL — Mémoire Persistante des Agents

> Un agent sans mémoire répète les mêmes erreurs et ne capitalise jamais sur ses succès.
> Ce protocole définit QUI stocke QUOI, OÙ, et COMMENT.

---

## Les 3 niveaux de mémoire

```
NIVEAU 1 — Court terme (session)
    Fichier : .tmp/run_state.json
    Durée : pendant un run actif
    Contenu : état du pipeline, artifacts, erreurs du run

NIVEAU 2 — Moyen terme (projet)
    Fichier : .tmp/run_history.json
    Durée : jusqu'à archivage manuel
    Contenu : historique des runs, métriques cumulées, patterns détectés

NIVEAU 3 — Long terme (système)
    Fichiers : directives/ERRORS.md + agents/PIPELINE_STATE.md
    Durée : permanente
    Contenu : fixes validés, état des pipelines, décisions architecturales
```

---

## Flux d'écriture par événement

### Quand un run commence
```
→ Écrire dans .tmp/run_state.json :
  - pipeline, niche, langue, started_at
  - status: "in_progress"
  - steps_remaining: [liste complète des agents]
```

### Quand une étape se complète
```
→ Mettre à jour .tmp/run_state.json :
  - Déplacer l'étape de steps_remaining → steps_completed
  - Ajouter l'artifact produit dans artifacts{}
  - Mettre à jour last_updated
```

### Quand une erreur survient
```
→ Immédiatement : ajouter à run_state.json errors[]
→ Après fix : ajouter à directives/ERRORS.md
→ Si pattern récurrent : mettre à jour tableau Patterns dans ERRORS.md
```

### Quand un run se complète
```
→ run_state.json : status = "completed", ajouter completed_at
→ Copier le résumé du run dans .tmp/run_history.json
→ Mettre à jour agents/PIPELINE_STATE.md (niche + langue = ✅)
→ Remettre run_state.json à idle
```

### Quand un run échoue (non récupérable)
```
→ run_state.json : status = "failed"
→ Documenter dans directives/ERRORS.md
→ Ne pas supprimer les artifacts — ils peuvent servir à un retry
→ Alerter Augus avec le contexte complet
```

---

## run_history.json — Format

```json
{
  "runs": [
    {
      "id": "run_001",
      "pipeline": "KDP",
      "niche": "blood_sugar_log",
      "langue": "EN",
      "started_at": "2026-02-25T10:00:00Z",
      "completed_at": "2026-02-25T11:15:00Z",
      "duration_min": 75,
      "status": "completed",
      "steps": ["SCRIBE", "COVER", "KEYWORD", "TRANSLATOR", "PUBLISHER"],
      "errors": [],
      "artifacts_finals": [
        ".tmp/interior_blood_sugar_EN.pdf",
        ".tmp/cover_blood_sugar_EN_full.png"
      ],
      "notes": "Premier run de la niche. COVER a nécessité un retry (DPI)."
    }
  ],

  "kpi_cumul": {
    "carnets_publies": 0,
    "images_uploadees": 0,
    "leads_generes": 300,
    "taux_succes_runs": null,
    "derniere_mise_a_jour": null
  }
}
```

---

## Règles de lecture (ordre obligatoire au début de chaque session)

```
1. Lire directives/ERRORS.md
   → Patterns connus, fixes disponibles

2. Lire .tmp/run_state.json
   → Y a-t-il un run en_cours ou failed non traité ?
   → Si oui : le reprendre avant tout

3. Lire agents/PIPELINE_STATE.md
   → Où en est-on sur les KPIs ?
   → Quelle est la prochaine priorité ?

4. Lire directives/ORCHESTRATOR.md (si besoin de décision de pipeline)

5. Lire directives/CONTRACTS.md avant de lancer un agent
   → Vérifier que les inputs sont disponibles
```

---

## Ce que les agents NE stockent PAS ici

- Contenu généré (carnets, images, leads) → dans `.tmp/` selon convention nommage
- Secrets / API keys → dans `.env` uniquement
- Code → dans `execution/` uniquement
- Conversations avec Augus → dans CLAUDE.md (mémoire humaine)

---

## Maintenance

| Action | Fréquence | Responsable |
|--------|-----------|-------------|
| Archiver runs complétés dans run_history.json | Après chaque run | Agent (auto) |
| Mettre à jour PIPELINE_STATE.md | Après chaque run | Agent (auto) |
| Mettre à jour agent_memory.json | Après chaque session | Agent (auto) |
| Nettoyer .tmp/ artifacts > 7 jours | Hebdomadaire | Augus ou agent |
| Réviser ERRORS.md patterns | Mensuel | Augus + agent |
| Réviser KPI targets dans PIPELINE_STATE | Mensuel | Augus |

---

## Couche apprentissage — Comment le système s'améliore seul

### Principe
Chaque run produit des données. Ces données alimentent la mémoire.
La mémoire influence les prochains runs. Le système devient plus précis à chaque itération.

```
Run N    → résultats, erreurs, durée, patterns
    ↓
agent_memory.json (learned_patterns, session_notes)
    ↓
Run N+1  → décisions meilleures, erreurs évitées, temps réduit
```

### Ce que l'agent apprend et stocke automatiquement

| Donnée observée | Où stocker | Format |
|-----------------|-----------|--------|
| Erreur nouvelle + fix | ERRORS.md + agent_memory.learned_patterns | Entrée structurée |
| Décision importante prise | agent_memory.last_decisions[] | {date, decision, rationale} |
| Quota API atteint | agent_memory.api_quotas | Mise à jour du modèle concerné |
| Préférence Augus confirmée | agent_memory.user_prefs | Clé-valeur |
| Durée réelle d'un run vs estimée | run_history.json + PIPELINE_STATE.md | Métriques |
| Taux rejet plateforme (Shutterstock, etc.) | ERRORS.md patterns + PIPELINE_STATE | Float |
| Niche qui performe mal (BSR élevé) | agent_memory.session_notes | Note avec date |

### Règles d'apprentissage

```
1. N'apprendre que ce qui est confirmé (pas les hypothèses)
   → "Groq rate limit quand modèle unique" = confirmé 1 fois → stocker
   → "peut-être que Shutterstock préfère X" = hypothèse → ne pas stocker encore

2. Mettre à jour, ne pas dupliquer
   → Avant d'écrire un nouveau pattern : vérifier s'il existe déjà dans learned_patterns[]
   → Mettre à jour l'entrée existante plutôt qu'en créer une nouvelle

3. Purger ce qui est obsolète
   → Si un fix est intégré dans la directive source → retirer de learned_patterns (devenu redondant)
   → last_decisions[] : garder max 10 entrées, purger les plus anciennes

4. Calibrer les estimations de durée
   → Après chaque run : comparer durée réelle vs durée estimée
   → Ajuster les estimations futures dans ORCHESTRATOR.md si écart > 30%
```

### Signal que le système apprend vraiment

```
Session 1 : "L'agent Groq plante" → Fix documenté → 45 min perdues
Session 2 : Boot lit learned_patterns → évite automatiquement le modèle unique
            → 0 min perdues sur ce problème

Session 1 : COVER prend 45 min (estimation : 20 min)
Session 3 : agent_memory sait que COVER = 45 min → planning ajusté
            → Augus reçoit des ETA fiables

Session 1 : Niche blood_sugar EN publiée → BSR initial 180k
Session 5 : agent_memory sait que cette niche est viable (BSR < 200k)
            → priorisée automatiquement pour les prochaines langues
```
