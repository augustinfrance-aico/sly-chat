# CONTRACTS — Interfaces Inter-Agents

> Chaque agent est une boîte noire avec des inputs requis et des outputs garantis.
> Avant d'appeler un agent : vérifier que ses inputs sont disponibles.
> Après l'appel : vérifier que ses outputs correspondent au contrat.

---

## Principe

```
Agent A (output) ──→ [CONTRAT] ──→ Agent B (input)

Si A n'a pas produit son output → B ne se lance pas.
Si B reçoit un input non conforme → B rejette et signale.
```

---

## FLUX KDP

### SCRIBE

```yaml
agent: SCRIBE
directive: agents/kdp/SCRIBE.md

inputs_requis:
  - niche: string          # ex: "blood_sugar_log"
  - langue: enum           # EN | FR | DE | ES | IT | JP
  - nb_pages: integer      # ex: 120
  - type: enum             # "suivi" | "journal" | "guide" | "planner"

outputs_garantis:
  - fichier: .tmp/scribe_{niche}_{langue}.md
  - contenu: markdown structuré, complet, pages numérotées
  - meta:
      titre: string
      sous_titre: string
      description_kdp: string (max 4000 chars)
      audience: string

conditions_echec:
  - Output .md vide ou < 50 lignes
  - Niche non trouvée dans la liste active
  - Langue non supportée

action_sur_echec: "Consulter ERRORS.md. Si nouveau cas → ajouter entrée + alerter."
```

### COVER

```yaml
agent: COVER
directive: agents/kdp/COVER.md

inputs_requis:
  - fichier_scribe: .tmp/scribe_{niche}_{langue}.md  # output SCRIBE
  - titre: string           # depuis meta SCRIBE
  - audience: string        # depuis meta SCRIBE
  - palette: enum           # medical | personal_dev | hobby | auto

outputs_garantis:
  - couverture_front: .tmp/cover_{niche}_{langue}_front.png  (300 DPI, 6x9)
  - couverture_full: .tmp/cover_{niche}_{langue}_full.png    (front+spine+back)
  - mockups: [.tmp/mockup_{niche}_{langue}_1.png, ...]       (3 mockups minimum)

conditions_echec:
  - Input SCRIBE absent ou incomplet
  - Image générée < 300 DPI
  - Dimensions non conformes (6"×9")

prerequis: SCRIBE doit être ✅ complété
action_sur_echec: "Stopper pipeline. Logger dans ERRORS.md."
```

### PUBLISHER

```yaml
agent: PUBLISHER
directive: agents/kdp/PUBLISHER.md

inputs_requis:
  - fichier_scribe: .tmp/scribe_{niche}_{langue}.md      # output SCRIBE
  - couverture_full: .tmp/cover_{niche}_{langue}_full.png # output COVER
  - meta_scribe: {titre, sous_titre, description_kdp, audience}

outputs_garantis:
  - pdf_interieur: .tmp/interior_{niche}_{langue}.pdf    (6x9, margins corrects)
  - asin_draft: .tmp/kdp_draft_{niche}_{langue}.json     (métadonnées KDP)
  - royalty_estimate: float                              ($/vente calculé)

conditions_echec:
  - PDF < 80 pages ou > 800 pages (hors specs KDP)
  - Marges incorrectes (gutter < 0.75")
  - SCRIBE ou COVER non complétés

prerequis: SCRIBE ✅ + COVER ✅
action_sur_echec: "Stopper pipeline. Logger dans ERRORS.md."
```

### KEYWORD

```yaml
agent: KEYWORD
directive: agents/kdp/KEYWORD.md

inputs_requis:
  - niche: string
  - langue: enum
  - meta_scribe: {titre, sous_titre, audience}

outputs_garantis:
  - keywords_primary: [string]    (7 slots, 50 chars max chacun)
  - keywords_backend: [string]    (backend KDP, sans répétition titre)
  - title_final: string           (titre optimisé SEO Amazon)
  - bsr_estimate: string          (estimation BSR attendu)

prerequis: SCRIBE ✅ (meta disponible)
action_sur_echec: "Continuer avec keywords génériques — logger en WARNING."
note: "KEYWORD peut tourner en parallèle avec COVER et PUBLISHER"
```

### TRANSLATOR

```yaml
agent: TRANSLATOR
directive: agents/kdp/TRANSLATOR.md

inputs_requis:
  - fichier_source: .tmp/scribe_{niche}_EN.md    # toujours depuis EN
  - langues_cibles: [FR, DE, ES, IT, JP]         # 5 langues (EN = source)
  - meta_source: {titre, description_kdp}

outputs_garantis:
  - par_langue:
      fichier: .tmp/scribe_{niche}_{langue}.md
      meta_traduit: {titre_{langue}, description_{langue}}
  - durée_par_langue: < 15 min

prerequis: SCRIBE EN ✅
note: "Lancer les 5 traductions en PARALLÈLE — pas séquentiellement"
action_sur_echec: "Langue échouée = skip + logger. Ne pas bloquer les autres langues."
```

---

## FLUX STOCK

### PIXEL

```yaml
agent: PIXEL
directive: agents/stock/PIXEL.md

inputs_requis:
  - niche: enum   # african_business | seniors_tech | muslim_families | disability_pro | coworking_africa | agriculture | nonbinary_pro | sea_cuisine
  - batch_size: integer    # ex: 50 images
  - outil: enum            # midjourney | dalle | stable_diffusion

outputs_garantis:
  - images: [.tmp/pixel_{niche}_{n}.png]    (min 2048x2048, < 50MB chacune)
  - prompts_utilisés: .tmp/pixel_{niche}_prompts.json
  - taux_rejet_estimé: float               (basé sur historique ERRORS.md)

conditions_echec:
  - Images < 2048px
  - Artefacts IA visibles (vérification manuelle requise)
  - Batch < 70% du batch_size demandé

action_sur_echec: "Logger niche + outil + taux. Essayer outil alternatif."
```

### STOCKPUSH

```yaml
agent: STOCKPUSH
directive: agents/stock/STOCKPUSH.md

inputs_requis:
  - images: [.tmp/pixel_{niche}_{n}.png]    # output PIXEL
  - niche: string
  - plateformes: [shutterstock, adobe_stock, alamy, freepik, pond5]

outputs_garantis:
  - rapport_upload: .tmp/stockpush_{niche}_{date}.json
      uploads_réussis: integer
      uploads_échoués: integer
      raisons_rejet: [string]
  - métadonnées_générées: .tmp/stockpush_{niche}_meta.json
      par_image: {titre, description, keywords_30_50}

prerequis: PIXEL ✅ (min 50 images conformes)
action_sur_echec: "Plateforme échouée = skip + logger. Ne pas bloquer les autres plateformes."
```

---

## Règles de composition

### Ordre d'exécution KDP
```
SCRIBE (EN)
    ↓
COVER + KEYWORD + TRANSLATOR×5  ← EN PARALLÈLE
    ↓
PUBLISHER (attend SCRIBE + COVER)
    ↓
KDP Upload (attend PUBLISHER + KEYWORD)
```

### Ordre d'exécution STOCK
```
PIXEL (batch par niche)
    ↓
STOCKPUSH (5 plateformes en parallèle)
```

### Règle des outputs
Chaque output produit dans `.tmp/` suit la convention :
```
.tmp/{agent}_{niche}_{langue}_{optionnel}.{extension}
```
Jamais de fichier sans niche dans le nom — pour éviter les collisions entre runs parallèles.

---

## Versioning des contrats

| Version | Date | Changement |
|---------|------|------------|
| 1.0 | 2026-02-25 | Création initiale |
