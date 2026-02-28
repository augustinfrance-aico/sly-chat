# ROUTING — Cerveau de Décision Intelligent

> Ce fichier répond à UNE question : "Qui fait quoi, maintenant ?"
> L'agent lit ce fichier, prend sa décision, et AGIT. Sans demander.
> Augus veut tout savoir mais ne veut pas être dérangé. La solution : faire, puis rapporter.

---

## Principe de routing

```
Intent d'Augus
    ↓
ROUTING identifie : type de besoin + pipeline concerné + agents requis
    ↓
Agents activés en autonomie
    ↓
Augus reçoit : résumé propre + résultat + suggestion prochaine étape
              (jamais le détail de qui a fait quoi — juste le livrable)
```

---

## Table de routing par intent

### Mots-clés → Pipeline automatique

| Si Augus dit... | Pipeline déclenché | Agents |
|-----------------|-------------------|--------|
| "carnet", "KDP", "niche", "Amazon", "livre" | KDP complet | SCRIBE→COVER+KEYWORD+TRANSLATOR→PUBLISHER→REVIEWER |
| "photo", "stock", "shutterstock", "image IA" | STOCK complet | PIXEL→REVIEWER→STOCKPUSH |
| "leads", "prospects", "B2B", "outreach" | LEADS | SCRAPER→ENRICHER→SCORER→OPTIMIZER |
| "pitch", "vente", "client", "closer", "deal" | VENTE | CLOSER+PHILOMÈNE (coalition) |
| "stratégie", "empire", "building", "priorité" | STRATÉGIE | CORTEX+OMEGA (coalition) |
| "idée", "concept", "et si on", "hack" | INNOVATION | GLITCH+NICHE (coalition) |
| "système", "automatiser", "pipeline", "flux" | ARCHITECTURE | VOLT (solo) |
| "texte", "rédiger", "écrire", "prompt" | RÉDACTION | PHILOMÈNE (solo) |
| "contenu", "post", "viral", "réseaux" | CONTENU | FRESCO+VIRAL (coalition) |
| "bilan", "résultats", "où on en est", "semaine" | WEEKLY_BRIEF | template directives/WEEKLY_BRIEF.md |
| "décision", "je sais pas", "recul", "avis" | CONSEIL | FRANKLIN+OMEGA (coalition) |
| "erreur", "ça marche pas", "bug", "bloqué" | ANNEALING | directives/ANNEALING.md |
| "cherche", "research", "deep search", "source" | DEEP SEARCH | HUNTER+CIPHER+RADAR (directives/DEEP_SEARCH.md) |
| "c'est quoi [X]", "comment marche [X]" | DEEP SEARCH L2 | HUNTER+CIPHER → doc + exemples + état de l'art |
| "compare [X] et [Y]" | DEEP SEARCH L3 | HUNTER+RADAR+TURING → comparatif multi-sources |

---

## Niveau d'autonomie par type d'action

### VERT — Agir sans demander, rapporter après
```
✅ Générer du contenu (SCRIBE, COVER, PIXEL, KEYWORD, TRANSLATOR)
✅ Faire une review qualité (REVIEWER)
✅ Reprendre un run interrompu
✅ Appliquer un fix connu (ERRORS.md)
✅ Produire un bilan hebdomadaire
✅ Choisir quel agent activer selon l'intent
✅ Paralléliser des étapes indépendantes
✅ Nettoyer .tmp/ selon règles CLEANUP.md
✅ Mettre à jour agent_memory.json et PIPELINE_STATE.md
```

### ORANGE — Agir, mais annoncer avant de lancer
```
🟠 Lancer un nouveau pipeline (niche inédite) → "Je lance KDP [niche] EN — GO ?"
🟠 Coalition de 3+ agents sur un projet important → annoncer la stratégie
🟠 Générer des leads sur un nouveau segment → confirmer les critères
```

### ROUGE — Attendre le "go" d'Augus
```
🔴 Publier sur Amazon KDP → toujours montrer couverture + titre avant
🔴 Uploader sur Shutterstock/Adobe → montrer échantillon avant
🔴 Envoyer des emails aux leads → montrer template + liste avant
🔴 Dépenser de l'argent (API payante) → toujours demander
🔴 Modifier une directive existante → jamais sans accord explicite
```

---

## Format des rapports à Augus (par type)

### Rapport de fin de pipeline (KDP/STOCK)
```
✅ [NICHE] [LANGUE] — livré

📦 Ce qu'il y a :
→ [Contenu produit, 1 ligne]
→ [Cover/images, 1 ligne]

💰 Revenu estimé : [X€/mois si vendu]

👇 Prochaine étape : [action suivante — je le fais dès ton go / ou je le fais directement si VERT]
```

### Rapport de bilan semaine
```
📊 Semaine [N]

KDP : [X/10] ✅ [liste courte]
STOCK : [X/250] ✅
Leads : [statut]

💪 Top : [meilleur truc de la semaine]
⚠️ À noter : [si quelque chose a bloqué — 1 phrase]

Semaine prochaine : [priorité 1, priorité 2]
```

### Rapport d'incident résolu
```
⚡ Petit incident réglé — [sujet]
→ Ce qui s'est passé : [1 phrase simple]
→ Réglé : [comment, 1 phrase]
→ Impact : zéro sur le pipeline / [X min de retard]
```

### Rapport si bloqué (rare)
```
⛔ Besoin de toi — [sujet]
→ Situation : [1 phrase]
→ Ce que j'ai essayé : [liste courte]
→ Ce qu'il me faut : [1 question précise]
→ En attendant : [ce que je continue à faire sans toi]
```

---

## Règle humour

Augus aime l'humour. Un peu de légèreté dans les rapports, c'est autorisé — même recommandé.

```
Au lieu de : "Le pipeline KDP blood_sugar_log EN s'est exécuté avec succès."
Dire :       "Le carnet glycémie EN est prêt. Diabétiques du monde entier, vous pouvez nous remercier."

Au lieu de : "Un incident s'est produit lors de l'étape COVER."
Dire :       "COVER a fait sa diva. Réglé. On continue."

Au lieu de : "Les KPI de la semaine sont en dessous de l'objectif."
Dire :       "Semaine un peu molle — 6/10 carnets. Je rattrape ça la semaine prochaine."
```

Règle : l'humour ne remplace jamais l'information. Il l'accompagne.
Règle 2 : jamais d'humour sur une vraie erreur critique ou un blocage client.

---

## Info-digest pour Augus (nouveau concept)

Augus veut tout savoir mais pas tout lire.
Solution : **l'info-digest** — une synthèse ultra-courte en fin de session.

```
🗞️ INFO-DIGEST [DATE]

Ce qu'on a fait :
→ [Action 1, résultat]
→ [Action 2, résultat]

Ce que ça change :
→ [Impact business concret]

Ce qui vient :
→ [Prochaine priorité]

Anecdote du jour : [fait intéressant ou observation pertinente — 1 ligne, peut être drôle]
```

L'info-digest remplace tous les détails. Si Augus veut creuser → il demande. Sinon il a l'essentiel.

---

## Routing des 50 agents vers les pipelines

> Référence complète : `personnalites/CASTING.md` + `directives/ORCHESTRATION_V2.md`
> Skills Tree : `directives/SKILLS_TREE.md`
> Système adaptatif C1→C5 — voir ORCHESTRATION_V2.md

```
Pipeline KDP :
  SCRIBE + PHILOMÈNE (fond) + NICHE (niche) + VOLT (si bottleneck)

Pipeline VENTE :
  CLOSER (closing) + PHILOMÈNE (forme) + ONYX (si premium)

Décision stratégique :
  SENTINEL (dispatch) + CORTEX (structure) + OMEGA (si complexe) + FRANKLIN (recul)

Innovation :
  GLITCH (disruption) + NICHE (niche) + VOLT (pipeline) + LEDGER (chiffres)

Audit & Performance :
  PULSE (setup + perf) + DATUM (KPIs)

Restitution complexe :
  [Agents pertinents] + FRANKLIN (résumé vulgarisé)
```

---

## Routing Tri-Pôle

> Référence complète : `directives/TRI_POLE.md`

### Routing par pôle — décision instantanée

| Intent détectée | Pôle principal | Pôles secondaires |
|----------------|---------------|-------------------|
| Analyse, niche, veille, data, stratégie | **R — RECON** | — |
| Créer, produire, coder, écrire, designer | **F — FORGE** | R fournit le brief |
| Vendre, publier, distribuer, closer, déployer | **D — DEPLOY** | F fournit le livrable |
| Projet complet (de A à Z) | **R → F → D** | Boucle complète |
| Bug, erreur, maintenance | **F — FORGE** (ANVIL + PULSE) | — |
| Bilan, KPIs, résultats | **R — RECON** (DATUM + PRISM) | D fournit les métriques |

### Communication inter-pôles
```
Format : [PÔLE_SOURCE → PÔLE_DEST] Type : "Message"

[R→F] Brief : "Niche X — scoring 8/7/9. Pipeline KDP. GO."
[F→D] Livrable : "Carnet X — 120p, cover, keywords. Prêt."
[D→R] Feedback : "Ventes J+30 : 47 unités. Suggestion variante."
```

### Escalade
```
Intra-pôle → Gouverneur du pôle résout
Inter-pôles → SENTINEL arbitre
Stratégie globale → OMEGA-CORE
Irréversible → Augus décide
```
