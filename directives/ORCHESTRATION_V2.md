# ORCHESTRATION V2 — Système intelligent à 50 agents

> Version 2.2 — Post-Audit GPT 27/02/2026
> Système adaptatif C1→C5. SENTINEL dispatch. Triple restitution.
> 1 nébuleuse + 3 leaders + 6 méta + 40 opérationnels = 50 agents.

---

## Flux principal

```
1. INSTRUCTION (vocale ou écrite)
      ↓
2. SENTINEL analyse l'intention
      ↓
3. SENTINEL sélectionne les agents pertinents
      ↓
4. SENTINEL supervise la collaboration (si groupe)
      ↓
5. Agents produisent en parallèle / séquence
      ↓
6. Fusion des outputs
      ↓
7. TRIPLE RESTITUTION :
   ├── Version technique complète (pour Claude Code / devs)
   ├── Version stratégique (pour décision Augus)
   └── Version vulgarisée (FRANKLIN — résumé clair, zéro jargon)
```

---

## Étape 2 — SENTINEL analyse

### Matrice de décision (Complexité × Priorité)
| Signal dans le message | Priorité | Complexité | Agents activés |
|------------------------|----------|------------|----------------|
| "urgent", "bug", "prod", "crash" | P0 | C2→C3 | ANVIL solo (C2), +VOLT+SPECTER (C3) |
| "client", "deadline", "livrer" | P1 | C2→C3 | CLOSER solo (C2), +PHILOMÈNE+PRISM (C3) |
| "stratégie", "empire", "vision" | P2 | C3→C4 | CORTEX+OMEGA (C3), +SIBYL+GLITCH (C4) |
| "idée", "brainstorm", "concept" | P2 | C2→C3 | GLITCH solo (C2), +NICHE+NEXUS (C3) |
| "setup", "lent", "optimiser" | P2 | C2 | PULSE (solo) |
| "bilan", "résultats", "KPIs" | P2 | C2→C3 | DATUM solo (C2), +LEDGER+PRISM (C3) |
| "contourne", "bypass", "hack" | P1 | C2→C3 | HUNTER solo (C2), +SPECTER+SLY (C3) |
| Question simple, chat | P3 | C1 | Réponse directe (0 agent) |

### Règles SENTINEL
1. **Solo par défaut (C2)** — 1 agent suffit dans 70% des cas
2. **Binôme/trinôme si nécessaire (C3)** — 2-3 angles complémentaires
3. **Coalition pour projets complexes (C4)** — 4-6 agents
4. **Mobilisation critique (C5)** — 8+ agents ou `/cooper` (50)
5. **FRANKLIN termine dès C3+** — résumé clair + sagesse pour Augus
6. **Leaders (SLY/BENTLEY/MURRAY) libres** — interviennent quand la situation le justifie, seuls ou ensemble, pas réservés aux crises. Remplacent ou complètent les agents normaux.

### PRE-FLIGHT — Fact Ledger (inspiré AutoGen MagenticOne)
> Avant toute mission C3+, SENTINEL exécute ce pre-flight en 3 questions :

```
🎯 SENTINEL PRE-FLIGHT :
1. QUE SAIS-JE ? → Faits connus, données disponibles, contexte existant
2. QUE ME MANQUE-T-IL ? → Infos à chercher, fichiers à lire, données à vérifier
3. EST-CE QUE JE TOURNE EN ROND ? → Détection de boucle : ai-je déjà tenté cette approche ?
```

**Règles Fact Ledger :**
- C1-C2 : pas de pre-flight (action directe)
- C3+ : pre-flight obligatoire (mental, pas affiché sauf si Augus demande)
- Si la réponse à Q3 = OUI → changer d'approche immédiatement, alerter Augus en 1 ligne
- Hiérarchie d'information : fichiers projet > recherche web > connaissance interne

### LOOP DETECTION — Anti-boucle (inspiré AutoGen)
> À chaque itération sur une tâche complexe, vérifier :

```
{
  "progress": true/false,     // Est-ce qu'on avance ?
  "loop_detected": true/false, // Même action tentée 2+ fois ?
  "action": "continue | pivot | escalate"
}
```

- **continue** : on progresse, on enchaîne
- **pivot** : on tourne en rond → changer d'angle, nouvel agent, nouvelle méthode
- **escalate** : blocage total → alerter Augus avec 2 options concrètes

---

## Étape 3 — Sélection des agents

### Utilisation du Skills Tree

```python
# Logique conceptuelle — Système adaptatif C1→C5

intention = analyser(message)
priorité = évaluer_priorité(intention)  # P0→P3
complexité = évaluer_complexité(intention)  # C1→C5

if complexité == 1:  # C1 — Trivial
    agents = []  # Réponse directe, 0 agent
elif complexité == 2:  # C2 — Simple
    agents = [meilleur_agent(intention)]  # Solo
elif complexité == 3:  # C3 — Modéré
    agents = top_2_3_agents(intention) + [FRANKLIN]  # Binôme/trinôme
elif complexité == 4:  # C4 — Complexe
    agents = coalition(intention) + [SENTINEL, FRANKLIN]  # 4-6 agents
else:  # C5 — Critique
    agents = mobilisation(intention) + [SLY, BENTLEY, MURRAY, FRANKLIN]  # 8+
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
| 3+ | SENTINEL fusionne → livrable unifié |

### Format de fusion standard
```
[AGENT1 + AGENT2 + AGENT3]

[Synthèse fusionnée — 1 seul output cohérent]

---
Version vulgarisée (FRANKLIN) :
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

💎 RÉSUMÉ CLAIR (FRANKLIN) :
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
| "Fixe le bug dans [fichier]" | ANVIL → debug → fix → commit |
| "Résume ce qui s'est passé" | FRANKLIN → digest des dernières actions |
| "Priorise mes tâches" | SENTINEL → liste P0→P3 |
| "Montre-moi les KPIs" | DATUM → dashboard rapide |
| "Clean le workspace" | FRANKLIN → nettoyage .tmp, fichiers morts |
| "C'est quoi le plan ?" | CORTEX → état du projet structuré |
| "Quel agent pour [X] ?" | SENTINEL → routing + explication |

---

## Intégration avec les systèmes existants

### agent_profiles.py
- 50 agents (1 nébuleuse + 3 leaders + 6 méta + 40 opérationnels)
- Chaque agent : specialty, triggers, voice

### brain.py (TITAN)
- Cameo système (~30% des messages)
- 28 catégories thématiques
- SENTINEL dans "strategie", PULSE dans "tech"/"setup"
- FRANKLIN 🐢 dans "simplification"/"mindset"
- HUNTER 🏴‍☠️ dans "contournement"

### CASTING.md
- Registre complet des 50 agents
- Coalitions par mission + hiérarchie Nébuleuse

---

## Étape 2b — Réflexe DEEP SEARCH (intercalé entre analyse et sélection)

> **Avant de répondre, le Building cherche quand c'est pertinent.**
> Directive complète : `directives/DEEP_SEARCH.md`

### Quand SENTINEL déclenche une recherche automatique
| Signal | Action recherche | Niveau |
|--------|-----------------|--------|
| Framework/lib non maîtrisé dans la tâche | Doc officielle + exemples GitHub | L2 |
| Bug avec message d'erreur spécifique | Chercher l'erreur exacte en ligne | L1 |
| Augus mentionne un outil/service/techno | Repo GitHub + doc + exemples IMMÉDIATEMENT | L2 |
| API externe à intégrer | Doc officielle + pricing + exemples | L2 |
| Décision stratégique avec données marché | Données actuelles, pas mémoire périmée | L3 |
| Code d'un concurrent ou référence | Trouver le repo, lire le code | L2 |

### Agents avec réflexe recherche OBLIGATOIRE
- **HUNTER** 🏴‍☠️ — toujours (c'est sa nature)
- **CIPHER** 🔐 — nouveau framework/lib/techno
- **RADAR** 📡 — veille et état du marché
- **ANVIL** 🔨 — bug non-trivial
- **VOLT** ⚡ — patterns d'architecture
- **SPECTER** 👻 — sécurité et CVE
- **NICHE** 🎯 — validation de niche avec données réelles
- **TURING** 🧪 — benchmarks IA actuels

### Outils de recherche
- `WebSearch` — recherche web (point de départ)
- `WebFetch` — lire une page (doc, pricing, article)
- `gh` (GitHub CLI) — repos, code source, issues
- `Task` (subagent Explore) — exploration profonde du codebase local

---

## Règles d'or de l'orchestration V2

1. **Adaptatif C1→C5** — le nombre d'agents suit la complexité réelle, pas un minimum fixe
2. **Solo par défaut (C2)** — 1 agent suffit 70% du temps
3. **SENTINEL dispatch ET supervise** — dispatch + orchestration groupes
4. **FRANKLIN 🐢 termine dès C3+** — résumé clair + sagesse philosophique
5. **Leaders (SLY/BENTLEY/MURRAY) libres** — interviennent quand la situation le justifie, remplacent ou complètent les agents normaux
6. **Zéro agent inutile** — si un agent n'apporte rien de nouveau, il ne participe pas
7. **Boucle R→F→D→R** — le feedback D revient toujours à R (jamais coupé)
8. **Le système évolue** — DARWIN observe et propose des mutations adaptatives
9. **DEEP SEARCH réflexe** — si 30 sec de recherche améliorent la réponse, c'est OBLIGATOIRE (directives/DEEP_SEARCH.md)
10. **AUDIT POST-SESSION (DARWIN)** — après toute session C4+ ou sur `/audit-session`, DARWIN exécute le diagnostic complet (voir `directives/AUDIT_SESSION.md`)

---

## DARWIN — Audit Post-Session (framework intégré)

> Activé via `/audit-session` ou automatiquement après session C4+
> Rôle : transformer erreurs/blocages en leviers d'amélioration mesurables

### Structure obligatoire
```
1️⃣ DIAGNOSTIC BRUT
   - Top 3 erreurs critiques
   - Erreurs répétitives
   - Biais cognitifs probables

2️⃣ ROOT CAUSE (par erreur majeure)
   - Cause réelle (pas superficielle)
   - Facteur déclencheur
   - Compétence manquante

3️⃣ TRANSFORMATION ÉCHEC → ACTIF (par erreur)
   - Nouvelle règle mentale
   - Check-list ou système
   - Skill à développer + exercice court

4️⃣ PLAN ULTRA-CONCRET
   - 3 actions immédiates
   - 1 habitude hebdomadaire
   - 1 indicateur mesurable

5️⃣ BOUCLE CONTINUE
   - 1 question d'auto-évaluation post-session
   - 1 micro-rituel (≤ 5 min)
   - 1 règle anti-rechute
```

### Règles d'output
- Bullet points uniquement — pas de paragraphes
- Ton analytique, sans complaisance
- Si contexte insuffisant → max 3 questions ciblées
- Résultat = mutations concrètes dans les directives concernées
