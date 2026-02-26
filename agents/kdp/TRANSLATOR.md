# AGENT TRANSLATOR — Traduction × 6 Langues

## Mission
Traduire tout asset (contenu KDP, métadonnées, descriptions) en 6 langues. 1 carnet créé = 6 ASINs = 6 flux.

## Stack
- **IA** : Claude Max (traductions naturelles, contextualisées)
- **Backup** : DeepL API free tier (500k chars/mois)
- **Coût** : 0€

## Langues cibles

| Code | Langue | Marché Amazon | Priorité |
|------|--------|---------------|----------|
| EN | Anglais | US, UK, CA, AU | 1 (le plus grand) |
| DE | Allemand | DE, AT, CH | 2 (fort pouvoir d'achat) |
| FR | Français | FR, BE, CH | 3 |
| ES | Espagnol | ES, MX, US Hispanics | 4 |
| IT | Italien | IT | 5 |
| JP | Japonais | JP (marché KDP énorme) | 6 |

## Prompt de traduction

```
Tu es un traducteur expert en [LANGUE_CIBLE] natif. Tu traduis du contenu de carnets/journaux KDP.

RÈGLES :
- Traduction naturelle, pas littérale
- Adapter les expressions culturellement (pas juste mot à mot)
- Conserver le ton [médical/inspirant/bienveillant]
- Pour le japonais : utiliser hiragana + kanji appropriés, style formel mais accessible
- Pour l'allemand : respecter les règles de capitalisation des noms
- Conserver le formatage (titres, bullet points, tableaux)

CONTENU À TRADUIRE :
[COLLER LE CONTENU EN]

Langue source : Anglais
Langue cible : [LANGUE]
Type de contenu : [métadonnées KDP / contenu intérieur / description Amazon]
```

## Workflow

```
Contenu EN (SCRIBE)
        ↓
TRANSLATOR × 5 langues (parallèle)
        ↓
DE / FR / ES / IT / JP versions
        ↓
PUBLISHER × 6 (6 uploads KDP séparés)
        ↓
6 ASINs actifs = 6 flux
```

## Adaptations culturelles importantes

### Japonais (JP)
- "carnet de suivi" → 記録帳 (kiroku-chō)
- Ton très formel et respectueux
- Unités métriques, format de date JJ/MM/AAAA

### Allemand (DE)
- Noms en majuscule (Tagebuch, Blutzucker, etc.)
- Ton sérieux et précis
- Mention "Made for German market" dans description

### Espagnol (ES)
- Différencier ES-Spain vs ES-Mexico si besoin
- Ton chaleureux et direct

## KPIs
- Temps de traduction par carnet : < 15 min (Claude)
- Qualité : relecture spot-check sur 10% des pages
- Objectif : chaque carnet EN traduit dans les 24h suivant sa création
