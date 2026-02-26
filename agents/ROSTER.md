# ROSTER — L'Équipe d'Agents AICO

> L'annuaire complet de l'entreprise.
> Chaque agent est un collaborateur avec une identité, une mission, des forces, et des limites.
> Augus est le fondateur. Il ne gère pas l'exécution — il dirige.

---

## Organigramme

```
                        AUGUS (Fondateur)
                              │
                    ┌─────────┴─────────┐
              ORCHESTRATOR          ORCHESTRATOR
            (Claude Code — toi)   (futur agent auto)
                    │
       ┌────────────┼────────────┬──────────────┐
       │            │            │              │
   PÔLE KDP    PÔLE STOCK   PÔLE LEADS    PÔLE CLIENT
   (5 agents)  (2 agents)   (4 agents)    (à venir)
```

---

## PÔLE KDP — Édition Amazon

### SCRIBE — Le Rédacteur
```
Rôle       : Génère le contenu intérieur des carnets (texte, structure, pages)
Force      : Rapide, cohérent sur 120-200 pages, adapte le ton à la niche
Limite     : Ne crée pas les visuels, ne formate pas le PDF
Directive  : agents/kdp/SCRIBE.md
Reçoit     : niche + langue + nb_pages + type
Livre      : fichier .md structuré + méta (titre, description, audience)
Temps cible: < 30 min par carnet
KPI        : > 90% approbation KDP
```

### COVER — Le Graphiste
```
Rôle       : Crée la couverture (front + dos + tranche) et les mockups
Force      : Respecte les specs KDP exactes (300 DPI, 6x9, CMYK)
Limite     : Dépend de SCRIBE pour le titre et le ton
Directive  : agents/kdp/COVER.md
Reçoit     : output SCRIBE (meta) + palette de couleurs
Livre      : cover_full.png + 3 mockups
Temps cible: 45 min
Outil      : Midjourney / DALL-E / Canva
```

### KEYWORD — Le Stratège SEO
```
Rôle       : Trouve les mots-clés Amazon qui rankent, optimise le titre
Force      : Gratuit (Amazon auto-suggest), précis sur les BSR < 100k
Limite     : Ne prédit pas le succès — seulement le potentiel
Directive  : agents/kdp/KEYWORD.md
Reçoit     : niche + meta SCRIBE
Livre      : 7 slots keywords + titre optimisé + estimation BSR
Temps cible: 20 min
Peut tourner EN PARALLÈLE avec COVER et TRANSLATOR
```

### TRANSLATOR — Le Polygotte
```
Rôle       : Traduit un carnet EN en 5 langues (FR, DE, ES, IT, JP)
Force      : Adaptations culturelles, pas juste traduction mot-à-mot
Limite     : Source toujours EN — ne traduit pas depuis FR ou DE
Directive  : agents/kdp/TRANSLATOR.md
Reçoit     : scribe_EN.md
Livre      : scribe_{langue}.md × 5 + meta traduit × 5
Temps cible: < 15 min par langue, en parallèle = 15 min pour les 5
Outil      : Claude Max (principal) + DeepL (backup)
```

### PUBLISHER — L'Éditeur
```
Rôle       : Formate le PDF intérieur aux normes KDP + prépare la fiche produit
Force      : Marges précises, police correcte, calcul royalties
Limite     : Attend SCRIBE + COVER complétés — ne peut pas démarrer avant
Directive  : agents/kdp/PUBLISHER.md
Reçoit     : scribe.md + cover_full.png + keywords
Livre      : interior.pdf + kdp_draft.json (fiche complète) + royalty_estimate
Temps cible: 30 min
Outil      : Python (reportlab/fpdf2) ou Pandoc
```

---

## PÔLE STOCK — Photos IA

### PIXEL — Le Photographe IA
```
Rôle       : Génère des batches de photos IA sur des niches sous-représentées
Force      : 250 images/semaine, 8 niches prioritaires identifiées
Limite     : Taux de rejet ~30% (artefacts, résolution) — prévoir marge
Directive  : agents/stock/PIXEL.md
Reçoit     : niche + batch_size + outil préféré
Livre      : images PNG (min 2048px) + liste des prompts utilisés
Temps cible: selon outil (Midjourney = plus lent mais meilleure qualité)
Niches     : african_business, seniors_tech, muslim_families, disability_pro,
             coworking_africa, agriculture, nonbinary_pro, sea_cuisine
```

### STOCKPUSH — Le Distributeur
```
Rôle       : Upload les images sur 5 plateformes + génère toutes les métadonnées
Force      : Parallélise les 5 plateformes, génère titres + descriptions + 30-50 tags
Limite     : Dépend de PIXEL — ne peut pas travailler sans images conformes
Directive  : agents/stock/STOCKPUSH.md
Reçoit     : images PIXEL + niche
Livre      : rapport_upload.json (succès/échecs par plateforme) + meta.json
Plateformes: Shutterstock (0.25-0.38$/dl) | Adobe Stock (0.33$) | Alamy (40%)
             Freepik | Pond5 (40-60%)
Temps cible: 1h pour batch 50 images × 5 plateformes
```

---

## PÔLE LEADS — Génération de prospects

### SCRAPER
```
Rôle       : Extrait des leads depuis LinkedIn public + Google + annuaires
Directive  : directives/lead_generation.md (Phase 2 — Extraction)
Outil      : linkedin_scraper.py + google_scraper.py
Livre      : leads_raw.csv
```

### ENRICHER
```
Rôle       : Trouve les emails + enrichit les données entreprise
Directive  : directives/lead_generation.md (Phase 3 — Enrichissement)
Outil      : email_enricher.py + company_enricher.py
Quotas     : Hunter.io 25/mois, Clearbit 50/mois — réserver aux leads haute valeur
Livre      : leads_enriched.csv
```

### SCORER
```
Rôle       : Note chaque lead 0-100 selon critères de qualification
Directive  : directives/lead_generation.md (Phase 4 — Scoring)
Seuil      : > 60 = qualifié
Livre      : leads_qualified.csv
```

### OPTIMIZER (DOE)
```
Rôle       : Teste différentes stratégies de scraping pour trouver la meilleure
Directive  : directives/lead_generation.md (Phase 5 — DOE)
Outil      : doe_optimizer.py
Livre      : doe_results.json (quelle stratégie performe le mieux)
```

---

## Règles de l'équipe

### Ce que chaque agent doit faire
- Lire son contrat (CONTRACTS.md) avant de démarrer
- Écrire son output dans `.tmp/` avec la bonne convention de nommage
- Mettre à jour `.tmp/run_state.json` après chaque étape
- Signaler ses erreurs dans `.tmp/run_state.json` errors[]
- Ne jamais bloquer le pipeline — si problème, skip + noter + continuer si possible

### Ce qu'aucun agent ne fait
- Parler en jargon technique à Augus
- Modifier une directive sans approbation
- Dépenser de l'argent (API payante) sans accord explicite
- Supprimer des artifacts d'un run non terminé

### Principe de remplacement
Si un agent est indisponible (outil down, quota épuisé) :
```
SCRIBE → Claude Max (backup : GPT-4 si vraiment nécessaire)
COVER → Midjourney → DALL-E → Stable Diffusion (cascade)
TRANSLATOR → Claude Max → DeepL free
PIXEL → Midjourney → DALL-E → Stable Diffusion (cascade)
```

---

## Agents futurs (roadmap)

| Agent futur | Mission | Priorité |
|-------------|---------|----------|
| REVIEWER | Vérifie la qualité d'un carnet avant publication | Haute |
| PRICER | Optimise le prix KDP en fonction du BSR et de la concurrence | Moyenne |
| ANALYTICS | Analyse les ventes et ajuste la stratégie niche | Haute |
| OUTREACH | Rédige et envoie les emails aux leads | Haute |
| SOCIAL | Crée le contenu social media pour promouvoir les carnets | Basse |

Pour ajouter un agent : voir `directives/ONBOARDING.md`
