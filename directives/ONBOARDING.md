# ONBOARDING — Intégrer un Nouvel Agent dans l'Empire

> Le système est conçu pour grandir. Quand Augus dit "je veux un agent qui fait X",
> ce fichier explique comment l'intégrer proprement en moins de 30 minutes.
> Résultat : l'agent fonctionne, il est raccordé à la mémoire, et l'équipe le connaît.

---

## Les 5 étapes d'intégration

### Étape 1 — Définir la mission (5 min)

Répondre à ces 4 questions avant d'écrire quoi que ce soit :

```
1. Qu'est-ce que cet agent produit de concret ?
   (pas "il aide à X" — qu'est-ce qu'il livre exactement ?)

2. De quoi a-t-il besoin pour démarrer ?
   (quels fichiers, quelles infos, quels outils)

3. À qui passe-t-il son output ?
   (quel agent suivant dans le pipeline, ou directement à Augus ?)

4. Comment sait-on qu'il a bien fait son travail ?
   (KPI mesurable, pas "qualité subjective")
```

Si une de ces questions reste sans réponse → ne pas créer l'agent, clarifier d'abord avec Augus.

---

### Étape 2 — Créer la fiche de poste (10 min)

Créer le fichier `agents/{pôle}/{NOM_AGENT}.md` avec ce template :

```markdown
# AGENT {NOM} — {Titre du rôle}

## Mission
[1-2 phrases max. Ce qu'il fait, pas comment.]

## Stack
- **Outil principal** : [Claude Max / Midjourney / Python / etc.]
- **Coût** : 0€ / [coût si inévitable]

## Inputs requis
| Paramètre | Type | Exemple |
|-----------|------|---------|
| [param1] | string / enum / integer | [exemple] |

## Outputs garantis
| Fichier | Format | Contenu |
|---------|--------|---------|
| .tmp/{nom}_{niche}_{langue}.{ext} | [format] | [description] |

## Workflow d'exécution
1. Recevoir : [liste des inputs]
2. Faire : [actions séquentielles]
3. Vérifier : [critères de validation]
4. Livrer : [liste des outputs]

## Conditions d'échec
- [condition 1]
- [condition 2]

## KPIs
- [métrique 1] : objectif [valeur]
- [métrique 2] : objectif [valeur]
```

---

### Étape 3 — Câbler au système (10 min)

**3a. Ajouter au ROSTER**
Dans `agents/ROSTER.md`, ajouter une fiche sous le bon pôle :
```
### {NOM} — {Titre}
Rôle      : [mission 1 phrase]
Directive : agents/{pôle}/{NOM}.md
Reçoit    : [inputs]
Livre     : [outputs]
Temps cible: X min
```

**3b. Ajouter aux CONTRACTS**
Dans `directives/CONTRACTS.md`, ajouter le contrat complet YAML de l'agent
(inputs_requis, outputs_garantis, prerequis, conditions_echec)

**3c. Mettre à jour l'INDEX**
Dans `agents/INDEX.md`, ajouter l'agent dans le bon flux pipeline

**3d. Mettre à jour PIPELINE_STATE**
Dans `agents/PIPELINE_STATE.md`, ajouter une ligne de tracking si l'agent produit des livrables mesurables

**3e. Mettre à jour ORCHESTRATOR**
Dans `directives/ORCHESTRATOR.md`, ajouter l'agent dans la matrice "pipeline → directive" si c'est un nouveau pipeline

---

### Étape 4 — Premier run test (5 min)

```
1. Préparer les inputs minimaux pour un test
2. Lancer l'agent sur un cas simple (pas le cas le plus complexe)
3. Vérifier que l'output respecte le contrat
4. Si échec → ANNEALING.md avant de continuer
5. Si succès → noter dans DECISION_LOG.md (nouveau membre de l'équipe)
```

---

### Étape 5 — Documenter les apprentissages (immédiat)

Après le premier run :
```
→ agent_memory.json : ajouter dans session_notes[] "Nouvel agent {NOM} intégré le [date]"
→ DECISION_LOG.md : ajouter entrée "Création agent {NOM} — pourquoi, alternatives rejetées"
→ ERRORS.md : si incident lors du test → documenter le fix
```

---

## Checklist d'intégration (à cocher)

```
□ Mission définie (4 questions répondues)
□ Fichier agents/{pôle}/{NOM}.md créé
□ Ajouté dans ROSTER.md
□ Contrat ajouté dans CONTRACTS.md
□ INDEX.md mis à jour
□ PIPELINE_STATE.md mis à jour (si applicable)
□ ORCHESTRATOR.md mis à jour (si nouveau pipeline)
□ Premier run test réussi
□ Apprentissages documentés
```

---

## Agents qu'on NE crée PAS

| Demande | Pourquoi on ne crée pas d'agent | Alternative |
|---------|--------------------------------|-------------|
| "Un agent qui fait tout" | Trop vague, pas de mission précise | Décomposer en agents spécialisés |
| "Un agent qui optimise" | Sans KPI précis, impossible à évaluer | Définir d'abord le KPI |
| "Un agent de backup" | Redondance inutile | Ajouter un fallback dans le contrat de l'agent existant |
| Un agent qui dépense de l'argent | Décision financière = Augus | Créer l'agent, mais action irréversible = escalade obligatoire |

---

## Nommage des agents

```
Convention :
- Nom en majuscules, 1 mot
- Anglais uniquement (universel)
- Verbe d'action ou métier humain (pas de noms abstraits)

✅ SCRIBE, COVER, PUBLISHER, REVIEWER, OUTREACH, SCORER
❌ OPTIMIZER_V2, AGENT_HELPER, MODULE_7, PROCESSING_UNIT
```

Le nom doit dire ce que l'agent fait. Si quelqu'un lit le nom et ne comprend pas la mission → mauvais nom.
