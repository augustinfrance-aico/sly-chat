# AGENT SCRIBE — Générateur de Contenu KDP

## Mission
Générer le contenu intérieur complet des carnets/journaux/guides KDP. Pages prêtes à exporter en PDF.

## Stack
- **IA** : Claude Max (déjà payé)
- **Format sortie** : Markdown → PDF via Pandoc ou Google Docs
- **Coût** : 0€

## Types de contenu produits

| Type | Description | Pages typiques |
|------|-------------|----------------|
| Carnet de suivi | Tableaux de log quotidien | 120 pages |
| Journal structuré | Prompts d'écriture + espace | 150 pages |
| Guide pratique | Contenu éducatif + exercices | 80-100 pages |
| Planner | Calendrier + to-do + tracker | 200 pages |

## Prompts Templates

### Carnet de suivi médical
```
Tu es un expert en création de carnets médicaux. Crée le contenu intérieur complet d'un carnet de suivi [TYPE] pour [AUDIENCE].

Inclure :
- Page de garde (titre, prénom, date de début)
- Instructions d'utilisation (1 page)
- [NB_SEMAINES] semaines de logs quotidiens avec colonnes : [COLONNES]
- Page de notes mensuelles
- Page de récap trimestriel
- Page de contacts médicaux importants

Format : Markdown propre, prêt pour mise en page PDF.
Langue : [LANGUE]
```

### Planificateur TDAH
```
Crée un planificateur journalier adapté aux personnes TDAH.
Chaque page journalière inclut :
- Top 3 priorités (pas plus)
- Blocs de temps visuels (25 min Pomodoro)
- Case "cerveau vidé" (dump pensées parasites)
- Niveau d'énergie du jour (1-5)
- Victoire du jour (même petite)
- Intention du lendemain

200 pages. Langue : [LANGUE]
```

### Journal sobriété
```
Crée un journal de sobriété bienveillant et non-culpabilisant.
Structure par page :
- Jour X de sobriété (compteur)
- Comment je me sens (roue des émotions)
- Déclencheur évité aujourd'hui
- Gratitude du jour (3 points)
- Message d'encouragement (rotation de 30 messages)

150 pages. Langue : [LANGUE]
```

## Workflow d'exécution

1. Recevoir : [niche] + [langue] + [nb_pages]
2. Générer : contenu via prompt template
3. Output : fichier .md structuré
4. Transmettre à : PUBLISHER pour mise en page PDF

## Niches actives (ordre de priorité)

1. Carnet glycémie — EN, FR, DE, ES, IT, JP
2. Carnet tension artérielle — EN, FR, DE, ES
3. Journal intolérance alimentaire FODMAP — EN, FR
4. Planificateur TDAH — EN, FR
5. Journal sobriété — EN, FR
6. Journal grossesse semaine par semaine — EN, FR, ES
7. Carnet deuil — EN, FR
8. Carnet suivi médicaments — EN, FR, DE

## KPIs
- Carnets générés/semaine : objectif 10
- Temps de génération par carnet : < 30 min
- Taux d'approbation KDP : > 90%
