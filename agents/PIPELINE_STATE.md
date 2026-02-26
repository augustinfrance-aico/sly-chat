# PIPELINE STATE — Traçabilité et Observabilité

> Ce fichier documente l'état connu de chaque pipeline.
> Il est mis à jour manuellement après chaque session de travail.
> Pour l'état en temps réel d'un run : voir `.tmp/run_state.json`

---

## KDP Pipeline — État courant

| Niche | EN | FR | DE | ES | IT | JP | Status global |
|-------|----|----|----|----|----|----|---------------|
| blood_sugar_log | — | — | — | — | — | — | 🔲 Non démarré |
| blood_pressure | — | — | — | — | — | — | 🔲 Non démarré |
| fodmap_journal | — | — | — | — | — | — | 🔲 Non démarré |
| adhd_planner | — | — | — | — | — | — | 🔲 Non démarré |
| sobriety_journal | — | — | — | — | — | — | 🔲 Non démarré |
| pregnancy_journal | — | — | — | — | — | — | 🔲 Non démarré |
| grief_journal | — | — | — | — | — | — | 🔲 Non démarré |
| medication_tracker | — | — | — | — | — | — | 🔲 Non démarré |

**Légende** : ✅ Publié | 🔄 En cours | ❌ Échec | 🔲 Non démarré | ⏸️ En pause

**KPI semaine** : 0 / 10 carnets cible

---

## STOCK Pipeline — État courant

| Niche | Images générées | Approuvées Shutterstock | Autres plateformes | Status |
|-------|----------------|------------------------|-------------------|--------|
| african_business_pro | 0 (50 prompts prêts) | — | — | 🟠 Batch 001 prêt à générer |
| seniors_tech | 0 | — | — | 🔲 Non démarré |
| muslim_families | 0 | — | — | 🔲 Non démarré |
| disability_professional | 0 | — | — | 🔲 Non démarré |
| coworking_africa_asia | 0 | — | — | 🔲 Non démarré |
| modern_agriculture | 0 | — | — | 🔲 Non démarré |
| nonbinary_professional | 0 | — | — | 🔲 Non démarré |
| sea_cuisine | 0 | — | — | 🔲 Non démarré |

**KPI semaine** : 0 / 250 images cible

---

## LEADS Pipeline — État courant

| Campagne | Leads générés | Qualifiés (>60) | Campagne email | Status |
|----------|--------------|-----------------|----------------|--------|
| Didier Carrette (Lyon) | 300 | ~300 | Non démarré | ✅ Leads prêts |

---

## Historique des runs (derniers 10)

| Date | Pipeline | Niche | Langue | Status | Durée | Erreurs |
|------|----------|-------|--------|--------|-------|---------|
| 2026-02-25 | STOCK | african_business_pro | — | 🟠 Batch 001 créé (50 prompts) | — | — |

*Se met à jour après chaque run.*

---

## Métriques globales

```
Sessions totales       : 0
Runs complétés         : 0
Runs échoués           : 0
Taux de succès         : N/A

Carnets KDP publiés    : 0
Images stock uploadées : 0
Revenus estimés/mois   : 0€

Erreurs documentées    : 5 (dans ERRORS.md)
Fixes appliqués        : 5
Taux résolution        : 100%
```

---

## Décisions de priorité

```
Semaine courante → Lancer dans cet ordre :
  1. blood_sugar_log EN (niche #1, volume maximal)
  2. blood_pressure EN (niche #2, demande forte)
  3. PIXEL : african_business_pro batch 50 images

Semaine suivante :
  1. TRANSLATOR × 5 langues sur blood_sugar_log
  2. blood_pressure FR + DE
  3. PIXEL : seniors_tech batch 50 images
```

*Cette section est mise à jour par ORCHESTRATOR.md en début de semaine.*
