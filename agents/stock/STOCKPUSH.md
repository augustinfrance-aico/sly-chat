# AGENT STOCKPUSH — Upload Photos sur Plateformes Stock

## Mission
Uploader les photos générées par PIXEL sur toutes les plateformes stock. Métadonnées optimisées pour le ranking.

## Stack
- **Upload** : Interface web manuelle (APIs nécessitent approbation contributeur)
- **Métadonnées** : Claude génère titres + descriptions + tags
- **Coût** : 0€ (toutes plateformes gratuites pour contributeurs)

## Plateformes cibles

| Plateforme | Royalty/download | Délai review | Priorité |
|------------|-----------------|--------------|----------|
| Shutterstock | 0.25-0.38$ | 24-48h | 1 |
| Adobe Stock | 0.33$ | 24-48h | 2 |
| Alamy | 40% (plus élevé) | 24h | 3 |
| Freepik | Selon abonnés | 48-72h | 4 |
| Pond5 | 40-60% (photos) | 24-48h | 5 |

## Métadonnées — Prompt Claude

```
Tu es un expert en stock photography SEO. Pour cette image :
[DESCRIPTION DE L'IMAGE]

Génère :
- Titre : 5-10 mots, descriptif et searchable
- Description : 1-2 phrases naturelles
- Tags : 30-50 mots-clés séparés par virgules (du plus spécifique au plus général)

Format : JSON prêt à copier-coller.
```

## Exemple métadonnées (Business Africains)

```json
{
  "title": "Confident African Businessman in Modern Office",
  "description": "Professional african businessman smiling in contemporary corporate office environment, natural lighting, business casual attire.",
  "tags": "african, businessman, professional, office, corporate, diversity, black, confident, modern, workplace, business, executive, smiling, natural light, inclusive, diverse workforce, business casual, entrepreneur, success, leadership, africa, professional headshot, corporate diversity, inclusion, workplace diversity, business professional, office worker, confident professional, african american, diversity inclusion"
}
```

## Workflow upload

```
PIXEL génère batch 50 images
        ↓
Claude génère métadonnées × 50 (batch prompt)
        ↓
Upload Shutterstock (priorité 1)
        ↓
Upload Adobe Stock (même batch)
        ↓
Attendre approbation (24-48h)
        ↓
Si refus : analyser motif → corriger → re-upload
```

## Causes de refus fréquentes

- Résolution insuffisante → upscaler avec Upscayl
- Artefacts IA visibles → choisir les meilleures images du batch
- Contenu similaire en masse → varier les angles, compositions
- Métadonnées spam → titres naturels, pas de keyword stuffing

## KPIs
- Images uploadées/semaine : 250 (5 plateformes × 50)
- Taux approbation cible : > 70%
- Délai upload batch 50 images : < 2h
