# ANNEALING — Protocole Self-Repair Opérationnel

> "Self-annealing" = le système se répare et se renforce automatiquement après chaque échec.
> Ce n'est pas de la magie. C'est un protocole précis à suivre, étape par étape.

---

## Analogie physique

En métallurgie, l'annealng = chauffer un métal puis le refroidir lentement pour éliminer les failles internes.
Ici : chaque erreur = une faille. Le protocole = le refroidissement contrôlé qui rend le système plus fort.

---

## Quand déclencher ce protocole

```
Déclencher ANNEALING si :
  ✗ Un agent retourne une erreur ou un output vide
  ✗ Un output ne respecte pas le contrat (directives/CONTRACTS.md)
  ✗ Un run reste en status "in_progress" depuis > 2h (dans .tmp/run_state.json)
  ✗ Un même problème apparaît 2+ fois dans directives/ERRORS.md
```

Ne pas déclencher si :
- C'est un timeout réseau ponctuel → retry 1 fois, c'est tout
- C'est une erreur d'input Augus → demander clarification

---

## Les 5 étapes (dans l'ordre, pas de saut)

### Étape 1 — DIAGNOSE (< 5 min)

```
1.1 Capturer l'erreur exacte :
    - Message d'erreur complet
    - Agent qui a échoué
    - Inputs reçus
    - État de .tmp/run_state.json au moment de l'échec

1.2 Consulter directives/ERRORS.md
    - Ce problème existe déjà ? → Appliquer le fix documenté → aller à Étape 3
    - Problème nouveau ? → Continuer vers Étape 2

1.3 Identifier la cause racine (pas le symptôme)
    MAUVAIS: "L'API a retourné 429"
    BON: "Le modèle X a atteint son quota journalier parce qu'on l'utilise en modèle unique sans fallback"
```

### Étape 2 — FIX (la solution minimale qui fonctionne)

```
2.1 Trouver le fix le plus simple possible
    Règle : le fix doit fonctionner MAINTENANT, pas être parfait pour toujours

2.2 Appliquer le fix sur l'outil/script concerné
    - Script Python → modifier le fichier dans execution/
    - Workflow n8n → modifier le nœud concerné
    - Prompt agent → adapter l'appel (sans modifier la directive source)

2.3 Tester sur un cas minimal
    Ne pas retester sur le run complet — tester l'unité qui a échoué isolément
```

### Étape 3 — VALIDATE

```
3.1 Relancer l'agent qui a échoué avec les mêmes inputs
3.2 Vérifier que l'output respecte le contrat (directives/CONTRACTS.md)
3.3 Si succès → Étape 4
3.4 Si échec → retour Étape 2 (max 3 itérations)
    Après 3 tentatives sans succès : stopper + alerter Augus avec diagnostic complet
```

### Étape 4 — DOCUMENT (obligatoire, même si rapide)

```
4.1 Ajouter une entrée dans directives/ERRORS.md :
    - Date, pipeline, agent
    - Erreur exacte
    - Cause racine
    - Fix appliqué
    - Statut : ✅ Résolu

4.2 Si le fix modifie un script execution/ → noter le fichier modifié
4.3 Si le problème révèle une lacune dans une directive → noter en WARNING
    (ne pas modifier la directive sans approbation Augus)
```

### Étape 5 — STRENGTHEN (le système est maintenant plus fort)

```
5.1 Mettre à jour .tmp/run_state.json :
    - Ajouter l'erreur dans le tableau "errors" de ce run
    - Marquer l'étape comme retry_success ou failed

5.2 Si le même pattern apparaît 2+ fois dans ERRORS.md :
    Ajouter au tableau "Patterns récurrents" dans ERRORS.md
    Proposer à Augus une modification préventive de la directive

5.3 Reprendre le pipeline depuis l'étape échouée (pas depuis le début)
    Utiliser les artifacts déjà produits dans .tmp/ — ne pas régénérer ce qui fonctionne
```

---

## Décision arbre complet

```
Erreur détectée
    │
    ├─ Vu dans ERRORS.md ?
    │   ├─ OUI → appliquer fix connu → valider → reprendre pipeline
    │   └─ NON → diagnostiquer cause racine
    │               │
    │               ├─ Fix < 5 min ? → appliquer → valider → documenter → reprendre
    │               │
    │               ├─ Fix > 5 min ou incertain ?
    │               │   → tenter fix minimal → si succès : documenter → reprendre
    │               │                        → si échec ×3 : STOPPER + alerter Augus
    │               │
    │               └─ Blocage externe (API down, accès client manquant) ?
    │                   → Marquer ⚠️ dans ERRORS.md → skip ce step si possible
    │                   → Alerter Augus avec contexte complet
    │
    └─ Pipeline reprend depuis l'étape suivante (pas depuis le début)
```

---

## Règle d'or de l'annealing

> Ne jamais perdre le travail déjà fait.
> Les artifacts dans `.tmp/` sont sacrés tant que le run n'est pas `completed`.
> Un pipeline qui reprend repart de là où il s'est arrêté — jamais de zéro.

---

## Anti-patterns à éviter absolument

| Anti-pattern | Pourquoi c'est mauvais | Ce qu'il faut faire |
|-------------|------------------------|---------------------|
| Retry en boucle sans diagnostic | Masque le vrai problème | Diagnostiquer d'abord |
| Modifier une directive "au vol" sans approbation | Perd la traçabilité | Logger dans ERRORS.md + proposer à Augus |
| Relancer le pipeline depuis le début | Gaspille du temps | Reprendre depuis l'étape échouée |
| Ignorer une erreur "mineure" | Elle revient toujours | Documenter même les warnings |
| Fix complexe sous pression | Introduit de nouveaux bugs | Fix minimal d'abord, amélioration après |
