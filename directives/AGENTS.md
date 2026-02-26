# AGENTS DU BUILDING — Directive de Connectivité

> 30 agents. Un écosystème. Zéro silo.
> Restructuration 26/02/2026 : DREYFUS→SPARTAN, FLEMMARD→ZEN, VERSO→ZARA, +SENTINEL, +PULSE, +LIMPIDE

---

## Architecture 3 couches

**Layer 1: Directive** (quoi faire)
- SOPs dans `directives/`
- Fiches agents dans `personnalites/`

**Layer 2: Orchestration** (qui décide)
- SENTINEL dispatch + arbitrage priorités → BAGHEERA supervise groupes → ALADIN coordonne tickets
- CASTING.md = registre d'activation (30 agents)
- GROUPES_TRAVAIL.md = binômes/trinômes
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
- 12 binômes naturels documentés dans GROUPES_TRAVAIL.md
- Formation : agent évalue seul → identifie angle mort → ping partenaire
- Dissolution : automatique à la livraison

### Règle 4 — Trinômes pour projets complexes
9 trinômes situationnels pour 3+ domaines simultanés.
- Supervision BAGHEERA obligatoire
- Ticket ALADIN obligatoire
- Audit GRIMALDI si tokens élevés

### Règle 5 — Pas de silo
- Tout agent peut communiquer avec tout agent
- BAGHEERA détecte les silos et force les connexions
- Un agent inutilisé >7 jours = alerte automatique

---

## Agents clés et leurs connexions

```
                    BAGHEERA (orchestration)
                         |
            ┌────────────┼────────────┐
            |            |            |
         OMEGA        MURPHY       ALADIN
       (polymorphe)  (structure)  (coordination)
            |            |            |
    ┌───────┤     ┌──────┤     ┌──────┤
    |       |     |      |     |      |
  RICK  PHILOMÈNE NIKOLA LÉON  GRIMALDI SPARTAN
(disrupt) (mots) (infra) (compta) (audit) (discipline)
    |       |     |
  BENTLEY BASQUIAT GHOST
  (agents) (art)  (sécu)
    |
  X-O1
(setup/audit)
```

## Flux standard d'un projet

```
1. Augus envoie une demande
2. Signaux détectés → agents activés (CASTING.md)
3. Si 1 agent suffit → solo
4. Si 2+ domaines → binôme/trinôme (GROUPES_TRAVAIL.md)
5. BAGHEERA supervise si groupe formé
6. Livraison → dissolution automatique
7. GRIMALDI audite si livrable externe
```

## Agents permanents (fond de réponse)
| Agent | Apport permanent |
|-------|-----------------|
| MURPHY | Structure dans chaque réponse |
| PHILOMÈNE | Précision des mots |
| ZEN | Recul et pas de panique |

## Agents spéciaux
| Agent | Rôle unique |
|-------|------------|
| OMEGA | Peut endosser N'IMPORTE quel rôle — réservé aux problèmes complexes |
| BAGHEERA | Méta-agent — orchestre mais ne fait PAS le travail |
| X-O1 | Audite le setup, les extensions, TITAN — consultant externe permanent |
| BALOO | Vulgarisation — rend compréhensible tout livrable |

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
| R — RECON | MURPHY + ORACLE | Maya, Ghost, Nash, Cypher, Rick |
| F — FORGE | NIKOLA + PHILOMÈNE | Forge, Basquiat, Zara, Murray, Léon, Baloo |
| D — DEPLOY | BAGHEERA + SPARTAN | Belfort, Stanley, Sly, Vito, Bentley, Grimaldi, X-O1, Zen |
| OMEGA-CORE | OMEGA | Au-dessus — arbitrage inter-pôle |

La Moon Tower (6 niveaux) reste en référence culturelle dans CASTING.md.
Le Tri-Pôle est le protocole d'exécution opérationnel.

---

## Self-annealing (auto-amélioration)
1. Problème détecté
2. Fix appliqué
3. Outil/script mis à jour
4. Directive mise à jour
5. Système plus fort qu'avant

---

*Directive maintenue par BAGHEERA & ALADIN. Validée GRIMALDI.*
