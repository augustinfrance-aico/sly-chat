# ERRORS — Journal Self-Annealing

> Ce fichier est la mémoire des erreurs du système.
> **Consulter en premier** avant tout run. **Mettre à jour** après tout incident.
> Le but : ne jamais répéter deux fois la même erreur.

---

## Format d'une entrée

```
### [DATE] — [PIPELINE] — [AGENT]
**Erreur** : Description exacte de ce qui a échoué
**Contexte** : Inputs utilisés, environnement, état du système
**Cause racine** : Pourquoi ça a échoué (pas les symptômes)
**Fix appliqué** : Ce qui a résolu le problème
**Directive mise à jour** : Quel fichier a été modifié
**Statut** : ✅ Résolu / ⚠️ Contournement / ❌ Problème ouvert
```

---

## Erreurs résolues

### 2026-02-18 — NEWS — Workflow n8n Moldova
**Erreur** : 7ème news ne s'envoyait pas
**Contexte** : Trigger 9PM New York, destinataire en Moldavie
**Cause racine** : 9PM NY = 4h du matin Moldavie → personne ne lit
**Fix appliqué** : Trigger changé à Noon New York = 19h Moldavie
**Directive mise à jour** : CLAUDE.md (note timezone)
**Statut** : ✅ Résolu

### 2026-02-18 — TITAN — telegram_bot.py
**Erreur** : Messages en doublon envoyés plusieurs fois
**Contexte** : Bot en polling, même message_id traité plusieurs fois
**Cause racine** : Pas de déduplication sur les message_id entrants
**Fix appliqué** : Set `processed_messages` max 500, purge à 200
**Directive mise à jour** : CLAUDE.md (section Anti-doublon)
**Statut** : ✅ Résolu

### 2026-02-19 — N8N — Push workflow
**Erreur** : Push JSON workflow échoue sur n8n
**Contexte** : Import via API, champs `tags` et `staticData` présents
**Cause racine** : Ces champs sont read-only sur l'API n8n
**Fix appliqué** : Retirer `tags` et `staticData` avant tout push JSON
**Directive mise à jour** : CLAUDE.md (section Bugs Résolus)
**Statut** : ✅ Résolu

### 2026-02-19 — PYTHON — Encoding Windows
**Erreur** : `UnicodeDecodeError: 'cp1252' codec can't decode`
**Contexte** : Scripts Python sur Windows avec caractères UTF-8
**Cause racine** : Windows ouvre les fichiers en cp1252 par défaut
**Fix appliqué** : Ajouter `encoding='utf-8'` à tous les `open()`
**Directive mise à jour** : CLAUDE.md (section Bugs Résolus)
**Statut** : ✅ Résolu

### 2026-02-20 — TITAN — Groq rate limit
**Erreur** : `429 Rate Limit` sur Groq après ~100k tokens/jour
**Contexte** : Modèle unique Groq, usage intensif
**Cause racine** : Quota par modèle, pas par compte
**Fix appliqué** : Cascade 6 modèles Groq (quotas séparés) + Gemini fallback
**Directive mise à jour** : CLAUDE.md (Décisions Techniques)
**Statut** : ✅ Résolu

---

## Erreurs ouvertes

### 2026-02-19 — N8N — Accès instance Railway Lurie
**Erreur** : Impossible d'accéder à l'instance n8n Railway de Lurie
**Contexte** : Pas d'invitation, pas d'API key fournie
**Cause racine** : Attente d'autorisation du client
**Fix appliqué** : Aucun — en attente
**Directive mise à jour** : Aucune
**Statut** : ⚠️ Bloqué côté client

---

## Patterns récurrents (meta-analyse)

| Pattern | Occurrences | Règle préventive |
|---------|------------|------------------|
| Timezone NY vs Europe | 1 | Toujours convertir : NY = Moldavie -7h |
| Encoding cp1252 Windows | 1 | `encoding='utf-8'` partout, sans exception |
| API rate limit mono-modèle | 1 | Toujours avoir fallback ou cascade |
| Champs read-only API tiers | 1 | Lire la doc API avant tout push/update |

---

## Règle de mise à jour

Après chaque incident :
1. Ajouter une entrée ici dans les 10 minutes
2. Si récurrent → ajouter au tableau "Patterns récurrents"
3. Si la directive est la cause → la signaler à Augus pour update explicite
4. Ne pas modifier les directives existantes sans approbation Augus
