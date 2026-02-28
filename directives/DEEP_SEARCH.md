# DEEP_SEARCH — Protocole de Recherche Profonde du Building

> Version 1.0 — 28/02/2026
> Quand le Building va chercher l'info au lieu de deviner.
> Instinct HUNTER appliqué à CHAQUE tâche.

---

## Philosophie

**Le Building ne devine pas. Il cherche.**

Avant cette directive, le Building répondait avec ce qu'il savait déjà.
Maintenant, il va **activement chercher** quand ça peut élever la qualité :
- Code source sur GitHub
- Documentation officielle à jour
- Exemples d'implémentation réels
- Best practices actuelles (pas celles de 2023)
- Solutions éprouvées par la communauté

> "Celui qui se contente de ce qu'il sait déjà ne mérite pas de résoudre des problèmes nouveaux."

---

## Quand déclencher une recherche

### AUTOMATIQUE (l'agent le fait sans demander)

| Situation | Action | Outils |
|-----------|--------|--------|
| **Framework/lib inconnu ou mal maîtrisé** | Aller chercher la doc + exemples GitHub | WebSearch, WebFetch, gh |
| **API externe à intégrer** | Chercher la doc officielle + exemples d'intégration | WebFetch (doc), WebSearch |
| **Bug non-trivial** | Chercher le message d'erreur exact sur GitHub Issues / Stack Overflow | WebSearch |
| **Architecture/design pattern** | Chercher des implémentations réelles, pas théoriques | WebSearch, GitHub |
| **Outil/service mentionné par Augus** | Aller chercher le repo GitHub, la doc, les exemples IMMÉDIATEMENT | WebSearch, WebFetch, gh |
| **Prix/coût/comparaison de services** | Vérifier les pricing pages actuelles | WebFetch |
| **Code d'un concurrent ou référence** | Trouver le repo, lire le code source | gh, WebFetch |
| **Tendance marché / niche** | Données actuelles, pas mémoire périmée | WebSearch |

### SUR DEMANDE (Augus dit explicitement)

| Déclencheur | Action |
|-------------|--------|
| "cherche", "trouve", "research" | Recherche multi-sources complète |
| "c'est quoi [X]", "comment marche [X]" | Doc + exemples + état de l'art |
| "compare [X] et [Y]" | Recherche comparative avec sources |
| "prix de [X]", "combien coûte" | Pricing pages actuelles |

### NE PAS CHERCHER (économie de tokens)

| Situation | Pourquoi |
|-----------|----------|
| Question sur le workspace AICO lui-même | Tout est dans les fichiers locaux |
| Syntaxe basique d'un langage connu | Connaissance intégrée suffisante |
| Opération CRUD standard | Pas besoin de source externe |
| Ce qu'Augus a déjà décidé (dans CLAUDE.md) | La directive fait foi |

---

## Comment chercher — Protocole HUNTER

### Niveau 1 — Recherche rapide (30 sec)
```
Quand : question factuelle, vérification rapide
Outils : WebSearch (1-2 requêtes ciblées)
Output : réponse + source en 1 ligne
```

### Niveau 2 — Recherche approfondie (2-3 min)
```
Quand : intégration technique, choix d'architecture, nouveau framework
Outils : WebSearch + WebFetch (doc officielle) + GitHub (code source)
Output : synthèse structurée + liens sources + recommandation
```

### Niveau 3 — Recherche exhaustive (5+ min)
```
Quand : décision stratégique, audit complet, comparaison multi-critères
Outils : WebSearch multiple + WebFetch multiple + GitHub repos + comparaison
Output : rapport avec sources numérotées, tableau comparatif, recommandation argumentée
```

---

## Outils disponibles et quand les utiliser

### WebSearch — Recherche web générale
```
Usage : trouver des pages, docs, articles, repos
Quand : point de départ pour toute recherche
Tips :
  - Requêtes précises en anglais > requêtes vagues
  - Ajouter l'année courante pour les résultats récents
  - Ajouter "github" pour trouver du code
  - Ajouter "docs" ou "documentation" pour la doc officielle
```

### WebFetch — Lire une page web
```
Usage : extraire le contenu d'une URL spécifique
Quand : doc officielle, README GitHub, article technique, pricing page
Tips :
  - Prompt clair : "extraire les exemples de code" / "lister les prix"
  - Fonctionne sur docs, blogs, GitHub raw — PAS sur pages authentifiées
```

### GitHub CLI (gh) — Explorer des repos
```
Usage : chercher repos, lire code, issues, PRs
Quand : code source d'un framework, exemples d'implémentation
Tips :
  - `gh search repos [query]` pour trouver des repos
  - `gh api` pour l'API GitHub REST
  - Lire les fichiers via raw.githubusercontent.com + WebFetch
```

### Task (subagent Explore) — Exploration profonde
```
Usage : recherche multi-étapes dans le codebase local
Quand : comprendre un pattern existant avant de modifier
Tips :
  - Plus lent mais plus thorough
  - Utiliser pour les explorations > 3 requêtes
```

---

## Intégration avec les agents du Building

### Agents qui DOIVENT chercher (réflexe obligatoire)

| Agent | Recherche obligatoire quand... |
|-------|-------------------------------|
| **HUNTER** 🏴‍☠️ | Toujours. C'est sa nature. Il trouve, il prend. |
| **CIPHER** 🔐 | Nouveau framework, lib, ou techno à évaluer |
| **RADAR** 📡 | Veille — toujours vérifier l'état actuel du marché |
| **ANVIL** 🔨 | Bug non-trivial — chercher le message d'erreur en ligne |
| **VOLT** ⚡ | Architecture — chercher des patterns d'implémentation réels |
| **SPECTER** 👻 | Sécurité — vérifier les CVE et vulnérabilités connues |
| **NICHE** 🎯 | Validation de niche — données actuelles, pas intuition |
| **TURING** 🧪 | Benchmark — chercher les benchmarks actuels des modèles IA |

### Agents qui cherchent en support

| Agent | Cherche quand... |
|-------|-----------------|
| **CORTEX** 🧠 | Analyse stratégique nécessite des données marché |
| **CLOSER** 🤝 | Besoin de connaître le prospect/marché du client |
| **PHILOMENE** ✍️ | Recherche de ton, style, exemples de contenu |
| **FRESCO** 🎨 | Références visuelles, tendances design |
| **MERCER** 💼 | Profils Upwork, tendances freelance |

---

## Format de citation des sources

### Dans les réponses normales
```
[information trouvée] — source: [lien]
```

### Dans les rapports structurés
```
Sources :
1. [Titre](URL) — ce qu'on en a tiré
2. [Titre](URL) — ce qu'on en a tiré
```

### Règle : pas de source = le dire
```
⚠️ Basé sur ma connaissance (pas de source externe vérifiée)
```

---

## Qualité d'exécution — Le standard HUNTER

### Avant de coder / proposer une solution technique :
1. **Le framework/lib est-il à jour ?** → vérifier la version actuelle
2. **Y a-t-il une meilleure façon de faire ?** → chercher "best practices [framework] [année]"
3. **Quelqu'un a-t-il déjà résolu ce problème ?** → chercher sur GitHub/SO
4. **La doc dit-elle quelque chose de spécifique ?** → lire la doc officielle

### Avant de proposer une stratégie business :
1. **Les données sont-elles actuelles ?** → vérifier les chiffres récents
2. **Le marché a-t-il changé ?** → chercher les tendances actuelles
3. **Qui fait déjà ça et comment ?** → analyser la concurrence

### Avant d'utiliser une API externe :
1. **Doc officielle lue ?** → WebFetch sur la doc
2. **Pricing vérifié ?** → page pricing actuelle
3. **Exemples d'intégration trouvés ?** → GitHub search

---

## Économie de recherche

La recherche coûte du temps. Règles d'optimisation :

1. **Cache mental** — si on a déjà cherché la même chose dans cette session, ne pas re-chercher
2. **Requêtes précises** — "tavily api python example 2026" > "search api"
3. **Sources de confiance d'abord** — doc officielle > blog > forum
4. **Paralléliser** — lancer plusieurs recherches en même temps quand elles sont indépendantes
5. **Savoir s'arrêter** — 3 sources concordantes = suffisant. Pas besoin de 10.

---

## Règle d'or

> **"Si tu peux améliorer ta réponse en 30 secondes de recherche, tu n'as AUCUNE excuse de ne pas le faire."**

Le Building ne se contente plus de "je crois que". Il sait, parce qu'il a vérifié.
