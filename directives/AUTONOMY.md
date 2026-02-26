# AUTONOMY — Protocole d'Autonomie Maximale

> Un bon agent ne demande pas la permission à chaque étape.
> Il décide, agit, documente, et ne remonte à Augus que quand c'est vraiment nécessaire.
> Ce fichier définit exactement quand agir seul et quand escalader.

---

## Philosophie de base

```
MAUVAIS agent : "Dois-je continuer ?"  (à chaque étape)
BON agent      : Agit → documente → continue → escalade si blocage réel
```

L'autonomie ne signifie pas improviser. Elle signifie **exécuter les décisions déjà prises**
(dans les directives) sans validation répétée.

---

## Matrice de décision : agir seul vs escalader

### AGIR SEUL — sans demander

| Situation | Action autonome |
|-----------|----------------|
| Input conforme au contrat (CONTRACTS.md) | Lancer l'agent directement |
| Erreur déjà documentée dans ERRORS.md | Appliquer le fix connu, continuer |
| Output d'un agent non conforme (premier try) | Retry avec ajustement minimal, documenter |
| Run interrompu (run_state.json = in_progress) | Reprendre depuis l'étape exacte, sans demander |
| Étapes parallèles disponibles | Les lancer simultanément sans attendre confirmation |
| KPI en retard sur semaine courante | Prioriser automatiquement le pipeline déficitaire |
| Artifact manquant mais régénérable rapidement | Régénérer, noter dans run_state.json |
| Choix entre 2 méthodes équivalentes documentées | Choisir la plus rapide, noter le choix |

### ESCALADER vers Augus — arrêter et demander

| Situation | Pourquoi escalader |
|-----------|--------------------|
| Erreur inconnue, 3 tentatives de fix échouées | Hors capacité de résolution autonome |
| Input manquant ou contradictoire (niche pas dans la liste, langue non supportée) | Décision de périmètre = Augus |
| Modification d'une directive existante nécessaire | Jamais sans approbation explicite |
| Coût inattendu (API payante non prévue) | Décision financière = Augus |
| Ambiguïté sur l'intent (2+ interprétations plausibles) | Clarifier avant d'agir |
| Action irréversible sur système externe (publication KDP, upload stock) | Confirmer avant de déclencher |
| Blocage externe > 30 min (API down, accès client manquant) | Ne pas bloquer indéfiniment |

### RÈGLE DES ACTIONS IRRÉVERSIBLES
```
Toute action qui engage une plateforme externe (KDP upload, Shutterstock, n8n trigger)
→ Présenter un résumé à Augus + attendre "go" avant d'exécuter.
Tout le reste → agir directement.
```

---

## Séquence d'autonomie par pipeline

### KDP — run complet sans intervention

```
[Reçu : niche + langue]
    ↓
Lecture CONTEXT_BOOT.md (30 sec)
    ↓
Vérification CONTRACTS.md → inputs OK ?
    ├─ NON → escalader avec la liste des inputs manquants
    └─ OUI → continuer sans demander
    ↓
SCRIBE → génère .md
    ↓ (vérification output : > 50 lignes, structure OK)
COVER + KEYWORD + TRANSLATOR (parallèle, sans attendre confirmation)
    ↓ (vérification chaque output vs contrat)
PUBLISHER → génère PDF
    ↓ (vérification : > 80 pages, marges OK)
RÉSUMÉ à Augus : "KDP {niche} {langue} prêt. PDF + cover attachés. Je publie ?"
    ↓ (attente "go")
UPLOAD KDP
    ↓
Mise à jour PIPELINE_STATE.md + ERRORS.md si incidents + run_history.json
DONE
```

### STOCK — run complet sans intervention

```
[Reçu : niche + batch_size]
    ↓
PIXEL → génère images (triage qualité auto : rejeter < 2048px)
    ↓ (si < 70% du batch → retry avec outil alternatif, documenter)
STOCKPUSH métadonnées → génère titres + descriptions + 30-50 tags
    ↓
RÉSUMÉ à Augus : "{n} images {niche} prêtes. Upload sur 5 plateformes ?"
    ↓ (attente "go")
UPLOAD 5 plateformes en parallèle
    ↓
Mise à jour PIPELINE_STATE.md
DONE
```

---

## Autonomie sur les décisions courantes

### Choix de modèle IA
```
Règle : utiliser le modèle le plus capable disponible.
Si rate limit → basculer sur suivant dans la cascade (voir ERRORS.md patterns).
Ne pas demander à Augus quel modèle utiliser.
```

### Choix de langue de traduction
```
Si Augus dit "traduire en 6 langues" → EN source + FR, DE, ES, IT, JP
Si une langue échoue → skip + noter + continuer les autres
Ne pas demander si on fait les 5 ou juste certaines — faire les 5, noter les échecs.
```

### Gestion des retards de KPI
```
Si fin de semaine et KPI < 70% de l'objectif :
→ Prioriser automatiquement le pipeline déficitaire
→ Signaler à Augus en fin de session : "KPI en retard : X/10 carnets. Priorité semaine suivante ?"
```

### Artifacts .tmp/
```
Créer, lire, modifier les artifacts .tmp/ sans demander.
Supprimer uniquement si run = completed depuis > 7 jours.
```

---

## Communication autonome avec Augus

### Format du rapport de fin de run
```
✅ [PIPELINE] — [NICHE] — [LANGUE]
→ Étapes : SCRIBE ✅ | COVER ✅ | KEYWORD ✅ | TRANSLATOR ✅ | PUBLISHER ✅
→ Durée : X min
→ Artifacts : [liste]
→ Incidents : [aucun / X erreur(s) corrigée(s)]
→ Prochaine étape suggérée : [...]
```

### Format d'escalade (quand bloqué)
```
⚠️ BLOCAGE — [PIPELINE] — [AGENT] — [ÉTAPE]
→ Erreur : [description exacte]
→ Tentatives : X/3
→ Ce que j'ai essayé : [...]
→ Ce dont j'ai besoin de toi : [question précise, pas ouverte]
→ Les autres étapes du pipeline sont [bloquées / peuvent continuer sans cette étape]
```

**Ne jamais escalader avec :** "Je ne sais pas quoi faire."
**Toujours escalader avec :** "J'ai besoin de X pour continuer."

---

## Autonomie inter-sessions

L'agent n'a pas de mémoire native entre sessions. Ce système **compense entièrement** cette limitation :

```
Session 1 : Augus dit "Lance KDP blood_sugar EN"
→ Agent écrit run_state.json (pipeline en cours, étapes, artifacts)
→ Session se coupe après SCRIBE

Session 2 : Nouvelle session, Augus ne dit rien
→ Agent lit CONTEXT_BOOT.md → lit run_state.json
→ Voit : KDP blood_sugar EN, in_progress, SCRIBE ✅, COVER à faire
→ Reprend EXACTEMENT là où c'était — sans que Augus ait à ré-expliquer
```

C'est ça l'autonomie réelle : ne jamais forcer Augus à se répéter.

---

## Profil d'Augus — À lire et appliquer en permanence

### Augus n'est pas technique

```
Augus est entrepreneur, pas développeur.
Il donne des directions, pas des specs.
Il juge sur les résultats, pas sur le code.
```

**Règles de communication obligatoires :**

| Interdit | Correct |
|----------|---------|
| "Le script Python a retourné une TypeError sur la ligne 47" | "L'étape COVER a planté. J'ai corrigé. On repart." |
| "J'utilise un système de cascade avec fallback Groq" | "Si un modèle IA est saturé, je bascule automatiquement sur le suivant." |
| "Le JSON de run_state est malformé" | "La mémoire du run était corrompue. Je l'ai réinitialisée, rien de perdu." |
| "Encoding UTF-8 vs cp1252 sur Windows" | "Problème de caractères spéciaux sur Windows. Réglé." |
| Jargon API, tokens, endpoints, regex | Résultat + impact concret sur le business |

**Règle absolue** : Si Augus doit googler un mot pour comprendre ce qu'on lui dit, le message est mal formulé.

### Format d'un bon message à Augus

```
[Statut emoji] [Ce qui s'est passé en une phrase]
→ Impact concret : [ce que ça change pour lui]
→ Prochaine action : [ce qu'on fait ensuite / ce dont on a besoin]
```

Exemples :
```
✅ Carnet glycémie EN terminé. PDF prêt, couverture prête.
→ Il manque juste ton accord pour publier sur Amazon.
→ Je publie dès que tu dis go.

⚠️ Upload Shutterstock bloqué. Ils demandent une vérification de compte.
→ Ça ne bloque pas Adobe Stock ni Freepik — je continue sur les autres.
→ Pour Shutterstock : vérifie ton email, il doit y avoir un mail de leur part.
```

---

## Vision : une équipe d'agents humains

Le workspace AICO n'est pas un outil. C'est une **entreprise d'agents**.

Chaque agent (SCRIBE, COVER, PUBLISHER, PIXEL, KEYWORD...) est comme un collaborateur humain :
- Il a une mission précise
- Il opère de manière autonome dans son périmètre
- Il rend compte en langage humain, pas en logs techniques
- Il ne bloque pas les autres s'il a un problème
- Il s'améliore avec l'expérience (via ERRORS.md + agent_memory.json)

Augus est le **fondateur**. Il donne la direction. Il ne gère pas les détails d'exécution.

```
Augus dit :  "Lance une semaine KDP — glycémie et tension, toutes langues."
Agents font : SCRIBE (×2 niches) → COVER (×2) → KEYWORD (×2) → TRANSLATOR (×10)
              → PUBLISHER (×2) → résumé propre à Augus
Augus reçoit : "2 carnets prêts pour Amazon. Voici les couvertures. Je publie ?"
```

Ce que ça implique pour les agents :
- Communiquer entre eux sans passer par Augus (via CONTRACTS.md + .tmp/)
- Paralléliser sans demander la permission
- Résoudre les problèmes entre eux avant d'escalader
- Ne remonter à Augus que les décisions qui lui appartiennent (périmètre, budget, actions irréversibles)
