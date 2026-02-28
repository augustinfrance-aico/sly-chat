# AGENTS DU BUILDING — Directive de Connectivité

> 30 agents opérationnels + 6 méta-agents. Un écosystème. Zéro silo.
> Opération Ascension 27/02/2026 : 46→30 agents, compétences absorbées, noms stylés.

---

## Architecture 3 couches

**Layer 1: Directive** (quoi faire)
- SOPs dans `directives/`
- Fiches agents dans `personnalites/`

**Layer 2: Orchestration** (qui décide)
- SENTINEL dispatch + arbitrage priorités + orchestration groupes
- CASTING.md = registre d'activation (30+6 agents)
- ORCHESTRATION_V2.md = protocole d'orchestration intelligent
- SKILLS_TREE.md = compétences activables par contexte

**Layer 3: Exécution** (qui fait)
- Scripts Python dans `execution/`
- TITAN bot = interface Telegram (53 modules)
- `.env` pour les secrets

---

## Protocole de Connectivité Inter-Agents

### Règle 1 — Activation par signal
Chaque message d'Augus contient des **signaux** qui activent les agents pertinents.
```
Message → Signaux détectés → Agents activés → Réponse fusionnée
```
Référence signaux : table dans `CLAUDE.md` (section AGENTS DU BUILDING)

### Règle 2 — CAMEO dans TITAN (~30% des messages)
TITAN intègre automatiquement des agents du Building dans ses réponses.
- `brain.py` → `AGENT_CAMEOS` dict + `CAMEO_TRIGGERS`
- Catégories : stratégie, vente, création, tech, croissance, mindset, créatif, business, recherche, setup, simplification
- L'agent parle avec SA voix, son emoji, 1-2 phrases max

### Règle 3 — Binômes situationnels
Les agents se regroupent PAR NÉCESSITÉ, pas par confort.
- Formation : agent évalue seul → identifie angle mort → ping partenaire
- Dissolution : automatique à la livraison

### Règle 4 — Trinômes pour projets complexes
Pour 3+ domaines simultanés.
- Supervision SENTINEL obligatoire
- Audit LEDGER si tokens élevés

### Règle 5 — Pas de silo
- Tout agent peut communiquer avec tout agent
- SENTINEL détecte les silos et force les connexions
- Un agent inutilisé >7 jours = alerte automatique

---

## Agents clés et leurs connexions

```
                    SENTINEL (dispatch + orchestration)
                         |
            ┌────────────┼────────────┐
            |            |            |
         OMEGA        CORTEX       DREYFUS
       (polymorphe)  (structure)  (discipline/qualité)
            |            |            |
    ┌───────┤     ┌──────┤     ┌──────┤
    |       |     |      |     |      |
  GLITCH PHILOMÈNE VOLT  LEDGER CLOSER FRANKLIN
(disrupt) (mots) (infra) (audit) (vente) (clarté)
    |       |     |
  ONYX   FRESCO  SPECTER
 (agents) (art)  (veille)
    |
  PULSE
(perf/setup)
```

## Flux standard d'un projet

```
1. Augus envoie une demande
2. Signaux détectés → agents activés (CASTING.md)
3. Si 1 agent suffit → solo
4. Si 2+ domaines → binôme/trinôme
5. SENTINEL supervise si groupe formé
6. Livraison → dissolution automatique
7. LEDGER audite si livrable externe
```

## Agents permanents (fond de réponse)
| Agent | Apport permanent |
|-------|-----------------|
| CORTEX | Structure dans chaque réponse |
| PHILOMÈNE | Précision des mots |
| FRANKLIN | Recul, nettoyage, clarté |

## Agents spéciaux
| Agent | Rôle unique |
|-------|------------|
| OMEGA | Peut endosser N'IMPORTE quel rôle — réservé aux problèmes complexes |
| SENTINEL | Dispatch + orchestration groupes — ne fait PAS le travail |
| PULSE | Audit setup, performance, workspace — consultant perf permanent |
| FRANKLIN | Vulgarisation — rend compréhensible tout livrable |

## Architecture Tri-Pôle (protocole opérationnel)

> Référence complète : `directives/TRI_POLE.md`

```
                    AUGUS (Suzerain)
                         │
                    OMEGA-CORE
                         │
          ┌──────────────┼──────────────┐
          │              │              │
     PÔLE R (RECON)  PÔLE F (FORGE)  PÔLE D (DEPLOY)
     Renseignement   Production      Distribution
     & Stratégie     & Création      & Opérations
```

### Boucle perpétuelle
```
R (brief) → F (livrable) → D (vente + métriques) → R (feedback) → ...
```

### Mapping rapide
| Pôle | Gouverneurs | Agents |
|------|------------|--------|
| R — RECON | CORTEX + SIBYL | NICHE, SPECTER, PRISM, DATUM, GLITCH, NEXUS |
| F — FORGE | VOLT + PHILOMÈNE | ANVIL, FRESCO, VIRAL, PULSE, PIXEL |
| D — DEPLOY | DREYFUS + CLOSER | RACOON, KAISER, ONYX, LEDGER, FRANKLIN |
| OMEGA-CORE | OMEGA + SENTINEL | Au-dessus — arbitrage inter-pôle |

La Moon Tower (7 niveaux) reste en référence culturelle dans CASTING.md.
Le Tri-Pôle est le protocole d'exécution opérationnel.

---

## Self-annealing (auto-amélioration)
1. Problème détecté
2. Fix appliqué
3. Outil/script mis à jour
4. Directive mise à jour
5. Système plus fort qu'avant

---

*Directive maintenue par SENTINEL. Validée LEDGER.*
