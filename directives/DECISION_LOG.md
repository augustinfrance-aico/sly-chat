# DECISION_LOG — Journal des Décisions Stratégiques

> Chaque décision importante prise dans le projet y est enregistrée.
> But : ne jamais se demander "pourquoi on a fait ça" — la réponse est ici.
> L'agent consulte ce fichier avant de proposer quelque chose qui contredit une décision passée.

---

## Format d'une entrée

```
### [DATE] — [DOMAINE] — [TITRE COURT]
**Décision** : Ce qui a été décidé (1-2 phrases)
**Pourquoi** : La raison (business, pas technique)
**Alternatives rejetées** : Ce qu'on n'a pas fait et pourquoi
**Impact** : Ce que ça change concrètement
**Révisable si** : Conditions dans lesquelles cette décision pourrait changer
```

---

## Décisions actives

### 2026-02-20 — INFRASTRUCTURE — Coût zéro absolu pour TITAN
**Décision** : TITAN n'utilise que des services gratuits (Groq free, Gemini free, Render free).
**Pourquoi** : Les crédits Anthropic sont épuisés. TITAN est un outil perso — pas question de payer un abonnement pour l'usage quotidien.
**Alternatives rejetées** : Garder Anthropic (payant), passer à OpenAI (payant)
**Impact** : Cascade 6 modèles Groq + Gemini fallback. Qualité légèrement inférieure à Claude, suffisante pour usage quotidien.
**Révisable si** : Revenus KDP/STOCK atteignent 500€/mois → réactiver Claude pour TITAN

### 2026-02-20 — INFRASTRUCTURE — TITAN sur Render (pas Railway)
**Décision** : TITAN est déployé sur Render, auto-deploy depuis GitHub.
**Pourquoi** : Railway était plus complexe à gérer. Render = push code → deploy automatique.
**Alternatives rejetées** : Railway (gardé pour l'instance n8n de Lurie uniquement)
**Impact** : Tout push sur le repo GitHub `augustinfrance-aico/titan-bot` redéploie TITAN automatiquement.
**Révisable si** : Render devient payant ou instable

### 2026-02-19 — ARCHITECTURE — Polling Telegram (pas webhook)
**Décision** : TITAN fonctionne en polling (il demande les messages toutes les X secondes) plutôt qu'en webhook (les messages arrivent en push).
**Pourquoi** : Le webhook nécessite un serveur avec URL publique stable + SSL. Le polling marche partout sans configuration.
**Alternatives rejetées** : Webhook Modal (plus complexe, plus fragile)
**Impact** : Légère latence (1-3 sec) sur les réponses. Acceptable pour usage perso.
**Révisable si** : TITAN devient un produit pour clients → passer en webhook obligatoire

### 2026-02-25 — WORKSPACE — Enrichissement système agents (pas modification)
**Décision** : Tous les nouveaux fichiers système sont créés dans `directives/` et `agents/`. Les fichiers existants ne sont jamais modifiés sans approbation Augus.
**Pourquoi** : Préserver ce qui fonctionne. Éviter les régressions.
**Alternatives rejetées** : Réécrire AGENTS.md, modifier les agents kdp/* existants
**Impact** : Le système grandit par addition, pas par remplacement.
**Révisable si** : Un fichier existant contient une erreur grave ou est obsolète

### 2026-02-25 — ÉQUIPE — Vision entreprise d'agents
**Décision** : Chaque agent (SCRIBE, COVER, etc.) est traité comme un collaborateur humain avec une mission, une fiche de poste, et des standards de communication.
**Pourquoi** : Augus n'est pas technique. L'équipe doit fonctionner comme une vraie entreprise où le fondateur donne la direction et l'équipe exécute.
**Alternatives rejetées** : Traiter les agents comme des scripts à lancer manuellement
**Impact** : Langage humain dans tous les rapports, autonomie maximale, escalade seulement sur décisions stratégiques.
**Révisable si** : Jamais — c'est la philosophie fondatrice du workspace

### 2026-02-18 — CLIENT LURIE — Workflow n8n sur Railway
**Décision** : L'instance n8n de Lurie reste sur Railway (pas migrée ailleurs).
**Pourquoi** : C'est l'infrastructure du client — on ne touche pas sans son accord.
**Impact** : On doit attendre une invitation ou une API key pour y accéder.
**Révisable si** : Lurie donne accès ou demande une migration

---

## Décisions annulées / révisées

### 2026-02-19 → 2026-02-20 — TITAN IA — Switch Anthropic → Groq
**Décision initiale** : TITAN utilisait l'API Anthropic (Claude)
**Révisée le** : 2026-02-20
**Nouvelle décision** : Cascade Groq + Gemini fallback
**Raison du changement** : Crédits Anthropic épuisés. Groq free tier suffisant.

---

## Règles du Decision Log

1. **Toute décision ayant un impact > 1 semaine mérite une entrée**
2. **Ne jamais effacer une décision** — seulement la déplacer en "annulées/révisées"
3. **Avant de proposer quelque chose à Augus** : vérifier que ça ne contredit pas une décision active
4. **Augus peut invalider n'importe quelle décision** — noter la révision ici
