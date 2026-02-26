# ORCHESTRATION V2 — Système intelligent à 30 agents

> Version 2 — Restructuration 26/02/2026
> Remplace le protocole d'orchestration simplifié.
> Intègre SENTINEL (dispatch), Skills Tree, et triple restitution.

---

## Flux principal

```
1. INSTRUCTION (vocale ou écrite)
      ↓
2. SENTINEL analyse l'intention
      ↓
3. SENTINEL sélectionne les agents pertinents
      ↓
4. BAGHEERA supervise la collaboration (si groupe)
      ↓
5. Agents produisent en parallèle / séquence
      ↓
6. Fusion des outputs
      ↓
7. TRIPLE RESTITUTION :
   ├── Version technique complète (pour Claude Code / devs)
   ├── Version stratégique (pour décision Augus)
   └── Version vulgarisée (LIMPIDE — résumé clair, zéro jargon)
```

---

## Étape 2 — SENTINEL analyse

### Matrice de décision
| Signal dans le message | Priorité | Mode | Agents activés |
|------------------------|----------|------|----------------|
| "urgent", "bug", "prod", "crash" | P0 | Focus | FORGE (solo) |
| "client", "deadline", "livrer" | P1 | Exécution rapide | Agent le plus pertinent |
| "stratégie", "empire", "vision" | P2 | Conseil | OMEGA + MURPHY + ORACLE |
| "idée", "brainstorm", "concept" | P2 | Débat créatif | RICK + BALOO + MAYA |
| "setup", "lent", "optimiser" | P2 | Focus | X-O1 + PULSE |
| "bilan", "résultats", "KPIs" | P2 | Analyse | CYPHER + NASH + GRIMALDI |
| Question simple, chat | P3 | Focus | Réponse directe (pas d'agent) |

### Règles SENTINEL
1. **Solo par défaut** — 1 agent suffit dans 70% des cas
2. **Binôme si nécessaire** — 2 angles complémentaires requis
3. **Trinôme max** — sauf projet complet (P0/P1 critique)
4. **Ne jamais activer plus de 5 agents** — bruit > signal
5. **Toujours finir par LIMPIDE** — résumé clair pour Augus

---

## Étape 3 — Sélection des agents

### Utilisation du Skills Tree

```python
# Logique conceptuelle (pas du code exécutable)

intention = analyser(message)
complexité = évaluer(intention)  # 1-5

if complexité <= 2:
    mode = "Focus"
    agents = [meilleur_agent(intention)]
elif complexité <= 3:
    mode = "Conseil"
    agents = top_2_agents(intention)
elif complexité <= 4:
    mode = "Débat"
    agents = top_3_agents(intention) + [LIMPIDE]
else:
    mode = "Coalition"
    agents = agents_par_pôle(intention) + [SENTINEL, BAGHEERA, LIMPIDE]
```

### Skills Tree activation
- Complexité 1-2 → Compétences principales uniquement
- Complexité 3 → Compétences principales + avancées
- Complexité 4-5 → Toutes compétences (y compris activables)

---

## Étape 6 — Fusion des outputs

### Règle de fusion
| Nombre agents | Méthode |
|---------------|---------|
| 1 | Pas de fusion — output direct |
| 2 | Header `[AGENT1 + AGENT2]` + synthèse |
| 3+ | BAGHEERA fusionne → livrable unifié |

### Format de fusion standard
```
[AGENT1 + AGENT2 + AGENT3]

[Synthèse fusionnée — 1 seul output cohérent]

---
Version vulgarisée (LIMPIDE) :
[Résumé en 3 phrases max, zéro jargon]
```

---

## Étape 7 — Triple restitution

### Quand activer la triple restitution
- **Toujours** pour les projets P0/P1
- **Sur demande** pour P2/P3
- **Jamais** pour les réponses simples (chat, questions rapides)

### Format
```
━━━ RESTITUTION ━━━

📋 TECHNIQUE :
[Détail complet — code, fichiers modifiés, architecture]

🎯 STRATÉGIQUE :
[Impact business, prochaines étapes, décisions à prendre]

💎 RÉSUMÉ CLAIR (LIMPIDE) :
[3 phrases. Ce qui a été fait. Pourquoi. Ce qui change pour toi.]
━━━━━━━━━━━━━━━━━━━
```

---

## Commandes vocales — Protocole voice-to-action

> Quand Augus parle dans le micro, le système doit :

```
1. Transcrire → texte brut
2. SENTINEL intercepte → analyse intention
3. Route vers le bon agent / mode
4. Agent(s) lisent le projet (fichiers pertinents)
5. Identifient les fichiers concernés
6. Exécutent l'action (code, refactor, test, doc)
7. Résumé vocal-friendly (phrases courtes, pas de jargon)
```

### Commandes vocales rapides
| Ce qu'Augus dit | Ce qui se passe |
|-----------------|-----------------|
| "Fixe le bug dans [fichier]" | FORGE → debug → fix → commit |
| "Résume ce qui s'est passé" | LIMPIDE → digest des dernières actions |
| "Priorise mes tâches" | SENTINEL → liste P0→P3 |
| "Montre-moi les KPIs" | CYPHER → dashboard rapide |
| "Clean le workspace" | ZEN → nettoyage .tmp, fichiers morts |
| "C'est quoi le plan ?" | MURPHY → état du projet structuré |
| "Quel agent pour [X] ?" | SENTINEL → routing + explication |

---

## Intégration avec les systèmes existants

### agent_router.py
- `route(message)` → retourne agents scorés par pertinence
- SENTINEL utilise ce routeur comme base, puis affine avec le Skills Tree

### brain.py (TITAN)
- Cameo système inchangé (~30% des messages)
- Nouvelle catégorie "simplification" avec LIMPIDE
- SENTINEL ajouté dans catégorie "strategie"
- PULSE ajouté dans catégorie "tech" et "setup"

### CASTING.md
- Registre complet des 30 agents
- Mis à jour avec la restructuration

---

## Règles d'or de l'orchestration V2

1. **Solo par défaut** — complexité minimale, toujours
2. **SENTINEL dispatch, BAGHEERA supervise** — jamais l'inverse
3. **LIMPIDE termine** — chaque output complexe finit par un résumé clair
4. **Zéro agent inutile** — si un agent n'apporte rien de nouveau, il ne participe pas
5. **Boucle R→F→D jamais interrompue** — le feedback revient toujours à R
6. **Le système devient plus fort après chaque cycle** — sinon le cycle n'est pas terminé
