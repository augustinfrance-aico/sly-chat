# TRI-PÔLE — Architecture Opérationnelle AICO

> 3 Pôles. 50 Agents. 1 Boucle infinie de profit.
> Ce fichier est le protocole opérationnel central du Building.
> Opération Expansion 27/02/2026 : 50 agents (1 nébuleuse + 3 leaders + 6 méta + 40 opérationnels).
> Roster complet et définitif : personnalites/CASTING.md (source de vérité unique).

---

## VISION

```
                         AUGUS (Suzerain)
                              │
                         OMEGA-CORE
                     (Cerveau stratégique)
                              │
               ┌──────────────┼──────────────┐
               │              │              │
         ╔═══════════╗  ╔═══════════╗  ╔═══════════╗
         ║  PÔLE R   ║  ║  PÔLE F   ║  ║  PÔLE D   ║
         ║  RECON    ║  ║  FORGE    ║  ║  DEPLOY   ║
         ╚═══════════╝  ╚═══════════╝  ╚═══════════╝
         Renseignement   Production     Distribution
         & Stratégie     & Création     & Opérations
```

**Principe** : Chaque demande entre par un Pôle, traverse les autres si nécessaire, et boucle.
**Règle** : Un agent appartient à UN pôle principal. Il peut être prêté temporairement à un autre.

---

## PÔLE R — RECON (Renseignement & Stratégie)

> "Trouve la cible. Quantifie le profit. Livre le brief."

### Gouverneurs
| Agent | Rôle gouverneur |
|-------|----------------|
| **CORTEX** | Structure, priorisation, architecture des décisions |
| **SIBYL** | Analyse prédictive, timing, tendances, vision 3-5 ans IA |

### Agents permanents
| Agent | Spécialité | Output type |
|-------|-----------|-------------|
| **NICHE** | Scanner niches, marchés, opportunités sous-exploitées | Rapport niche + scoring |
| **SPECTER** | Veille concurrentielle, intelligence business, reverse-engineering | Dossier concurrence |
| **PRISM** | Pricing, psychology des offres, tarification | Analyse chiffrée + recommandation prix |
| **DATUM** | Analyse de performance, KPIs, monitoring, alertes | Dashboard perf |
| **GLITCH** | Angles non-conventionnels, hacks système, brainstorm créatif | Concept disruptif |
| **NEXUS** | Synergies inter-projets, cascades, amplification | Carte des connexions |

### Déclencheurs d'activation
```
Mots-clés Augus → Pôle R activé :
"niche", "marché", "opportunité", "tendance", "data", "analyse",
"stratégie", "concurrent", "pricing", "idée", "hack", "et si on",
"qu'est-ce qui marche", "scanner", "veille", "prédiction", "synergie"
```

### Output standard du Pôle R
```
📡 [RECON] Brief Opportunité

Niche : [nom]
Marché : [taille, compétition, tendance]
Scoring : [1-10] potentiel / [1-10] faisabilité / [1-10] urgence
Angle recommandé : [description courte]
Action : [pipeline recommandé — KDP / STOCK / LEADS / AGENCE / CONTENU]

→ Envoyé au Pôle F pour production
```

### Coalitions internes fréquentes
- **NICHE + PRISM** : Niche identifiée → pricing validé
- **SPECTER + DATUM** : Concurrent détecté → benchmark chiffré
- **GLITCH + SIBYL** : Idée sauvage → projection temporelle
- **CORTEX + tout le pôle** : Décision stratégique complexe → priorisation

---

## PÔLE F — FORGE (Production & Création)

> "Transforme le brief en produit. Zéro erreur. Vitesse max."

### Gouverneurs
| Agent | Rôle gouverneur |
|-------|----------------|
| **VOLT** | Architecture technique, pipelines, automation |
| **PHILOMÈNE** | Qualité rédactionnelle, précision, élégance, traduction |

### Agents permanents
| Agent | Spécialité | Output type |
|-------|-----------|-------------|
| **ANVIL** | Exécution brute, code, déblocage, deadlines | Code + livrable technique |
| **FRESCO** | Créatif, storytelling visuel, branding, scripts vidéo | Assets visuels + direction artistique |
| **VIRAL** | Contenu social, engagement, tendances virales | Posts + calendrier éditorial |
| **PULSE** | Performance, latence, audit setup, workspace | Profiling + config optimisée |
| **PIXEL** | Gamification, UX interactive, pixel art | Interface + game design |

### Déclencheurs d'activation
```
Mots-clés Augus → Pôle F activé :
"créer", "produire", "écrire", "coder", "design", "carnet", "KDP",
"photo", "stock", "template", "contenu", "newsletter", "vidéo",
"prompt", "rédiger", "construire", "automatiser", "pipeline"
```

### Output standard du Pôle F
```
🔨 [FORGE] Livrable Prêt

Produit : [nom + type]
Brief source : [réf brief Pôle R]
Qualité : [validé par PHILOMÈNE ✅ / FRESCO ✅]
Fichiers : [chemins des livrables]
Notes : [particularités, variantes possibles]

→ Envoyé au Pôle D pour distribution
```

### Coalitions internes fréquentes
- **ANVIL + VOLT** : Pipeline technique complet
- **PHILOMÈNE + FRESCO** : Contenu texte + visuel premium
- **VIRAL + PHILOMÈNE** : Contenu social + long-form coordonné
- **FRESCO + VIRAL** : Vidéo + distribution sociale

### Pipelines de production (hérités)
| Pipeline | Agents FORGE mobilisés | Directive source |
|----------|----------------------|-----------------|
| KDP | PHILOMÈNE (rédaction) + FRESCO (cover) + VOLT (pipeline) | agents/INDEX.md |
| STOCK | FRESCO (visuels) + VOLT (pipeline) | agents/INDEX.md |
| TEMPLATES | VOLT (architecture) + PHILOMÈNE (copy) + ANVIL (code) | directives/TEMPLATES_GUMROAD.md |
| CONTENU | VIRAL + PHILOMÈNE + FRESCO | directives/RUISSEAUX.md §4 |
| NEWSLETTER | PHILOMÈNE + VIRAL | directives/RUISSEAUX.md §5 |

---

## PÔLE D — DEPLOY (Distribution & Opérations)

> "Vends. Distribue. Maintiens. Zéro downtime. Revenus constants."

### Gouverneurs
| Agent | Rôle gouverneur |
|-------|----------------|
| **DREYFUS** | Discipline, cadence, contrôle qualité, zéro défaut |
| **CLOSER** | Closing, vente, onboarding, rétention |

### Agents permanents
| Agent | Spécialité | Output type |
|-------|-----------|-------------|
| **RACOON** | Growth hacking, cold outreach, acquisition low-cost | Campagnes growth + séquences |
| **KAISER** | Relations long terme, partenariats, diplomatie, négociation | Contrats + partnerships |
| **ONYX** | Positionnement premium, image haut de gamme | Packaging premium |
| **LEDGER** | Audit coûts, finances, projections, ROI | Rapports financiers |
| **FRANKLIN** | Simplification, vulgarisation, nettoyage, validation finale | Validation + résumé clair |

### Déclencheurs d'activation
```
Mots-clés Augus → Pôle D activé :
"vendre", "publier", "uploader", "distribuer", "closer", "client",
"deal", "leads", "outreach", "pitch", "partenariat", "premium",
"coûts", "finances", "setup", "TITAN", "serveur", "stabilité",
"maintenance", "erreur", "bug", "deploy"
```

### Output standard du Pôle D
```
🚀 [DEPLOY] Rapport Distribution

Livrable : [nom + source Pôle F]
Canal : [KDP / Gumroad / Upwork / LinkedIn / Direct]
Statut : [publié ✅ / en attente GO Augus 🟠 / bloqué ⛔]
Métriques J+X : [ventes / vues / leads / revenus]
Feedback : [ce qui marche, ce qui coince]

→ Feedback envoyé au Pôle R pour affinage
```

### Coalitions internes fréquentes
- **CLOSER + RACOON** : Outreach agressif + closing
- **KAISER + ONYX** : Client premium + relation long terme
- **LEDGER + PULSE** : Audit coûts + audit technique
- **FRANKLIN + DREYFUS** : Qualité + clarté avant livraison

---

## LA BOUCLE — Le Moteur Perpétuel

```
┌─────────────────────────────────────────────────┐
│                                                 │
│    PÔLE R ──Brief──→ PÔLE F ──Livrable──→ PÔLE D
│      ▲                                      │   │
│      │                                      │   │
│      └──────── Feedback + Métriques ────────┘   │
│                                                 │
└─────────────────────────────────────────────────┘
```

### Cycle standard d'un projet
```
1. [R] NICHE scanne → niche détectée
2. [R] PRISM + DATUM valident les chiffres
3. [R] CORTEX priorise → Brief envoyé à F
4. [F] VOLT conçoit le pipeline
5. [F] Agents de production exécutent
6. [F] PHILOMÈNE valide qualité → Livrable envoyé à D
7. [D] Canal de distribution choisi
8. [D] CLOSER/RACOON vendent
9. [D] LEDGER mesure le ROI
10. [D] FRANKLIN valide → Feedback envoyé à R
11. [R] Boucle : affiner, pivoter, ou scaler
```

### Temps de cycle cible
| Type de projet | Cycle R→F→D | Boucle complète |
|---------------|-------------|-----------------|
| KDP carnet | R: 30min, F: 2h, D: 24h | 1 jour |
| Stock photos | R: 15min, F: 1h, D: 1h | 3h |
| Template Gumroad | R: 1h, F: 4h, D: 2h | 1 jour |
| Client Agence | R: 2h, F: 1-5j, D: ongoing | 1 semaine |
| Campagne contenu | R: 1h, F: 3h, D: ongoing | 1 jour + itération |

---

## HANDOFF SUMMARIZER — Zéro perte de contexte (inspiré CrewAI)

> À chaque passage de pôle (R→F, F→D, D→R), le pôle sortant produit un résumé structuré :

```
📋 HANDOFF [PÔLE_SOURCE → PÔLE_DEST]

1. MISSION : Quoi ? (objectif en 1 phrase)
2. ÉTAT : Où on en est ? (ce qui est fait, ce qui reste)
3. DÉCOUVERTES : Infos clés trouvées (faits, chiffres, données critiques)
4. NEXT : Quoi faire ensuite ? (action précise pour le pôle suivant)
5. CONTEXTE : Ce qu'il faut garder (URLs, noms, valeurs, chemins de fichiers)
```

**Règles :**
- Chaque section = 1-2 lignes MAX
- Pas de résumé si la tâche tient en 1 message (C1-C2)
- Obligatoire pour tout projet multi-étapes (C3+)
- Le pôle récepteur ne demande JAMAIS "c'est quoi le contexte ?" — tout est dans le handoff

---

## COMMUNICATION INTER-PÔLES

### Format obligatoire
```
[PÔLE_SOURCE → PÔLE_DEST] Type : "Message court"
```

### Exemples réels
```
[R→F] Brief : "Niche glucose tracking EN — 4.2K rech/mois,
       compétition faible. Template carnet A5. Scoring 8/7/9. GO."

[F→D] Livrable : "Carnet glucose EN — 120p, cover pro,
       7 keywords optimisés. Fichiers dans .tmp/. Prêt upload KDP."

[D→R] Feedback : "Ventes J+30 : 47 unités, 329€.
       Suggestion NICHE : variante A4 + version ES (marché 2x plus gros)."

[R→F] Brief itération : "Glucose tracker ES — reprendre EN,
       adapter PHILOMÈNE ES, nouvelle cover FRESCO ton chaud. GO."
```

### Escalade entre pôles
```
Problème intra-pôle → Gouverneur du pôle résout
Problème inter-pôles → SENTINEL arbitre
Problème stratégique global → OMEGA-CORE + Augus
Problème irréversible → Augus décide (ROUGE dans ROUTING.md)
```

---

## OMEGA-CORE — Le Cerveau Au-dessus des Pôles

OMEGA n'appartient à aucun pôle. Il les supervise tous.

### Rôle
- Vision 360° quand un problème touche 2+ pôles simultanément
- Arbitrage final si les gouverneurs ne s'accordent pas
- Activation sur demande d'Augus ou sur détection automatique de conflit
- Peut temporairement "posséder" n'importe quel agent de n'importe quel pôle

### Activation OMEGA
```
Automatique si :
- 2 gouverneurs envoient des recommandations contradictoires
- Un projet touche les 3 pôles avec interdépendances
- Augus dit "stratégie", "empire", "building", "vision"
- Situation de crise (3+ incidents simultanés)

Manuel :
- Augus dit "OMEGA" ou "vision globale"
```

---

## AGENTS FLOTTANTS

Certains agents ne sont pas assignés à un pôle fixe. Ils circulent selon le besoin :

| Agent | Pôle habituel | Peut flotter vers | Condition |
|-------|--------------|-------------------|-----------|
| **OMEGA** | Au-dessus | R / F / D | Problème multi-pôle |
| **GLITCH** | R (disruption) | F | Idée à prototyper directement |
| **NEXUS** | R (synergies) | F / D | Connexion inter-pôle détectée |
| **FRANKLIN** | D (validation) | R | Résumé de brief complexe |

### Règle de prêt
```
1. L'agent finit sa mission dans son pôle d'origine
2. Gouverneur du pôle demandeur envoie une requête
3. Gouverneur du pôle source valide le prêt
4. Prêt = temporaire. Retour automatique après livraison.
5. Un agent ne peut pas être prêté si son pôle est en charge critique
```

---

## MAPPING PIPELINES → PÔLES

| Pipeline existant | Pôle R (brief) | Pôle F (production) | Pôle D (distribution) |
|-------------------|---------------|--------------------|-----------------------|
| **KDP** | NICHE (niche) + PRISM (data) | PHILOMÈNE + FRESCO + VOLT | Upload KDP + LEDGER (ROI) |
| **STOCK** | NICHE (niche) + SPECTER (concurrence) | FRESCO + VOLT | Upload Shutterstock + LEDGER |
| **LEADS** | SPECTER (veille) + DATUM (scoring) | ANVIL (scraping) + PHILOMÈNE (templates) | RACOON + CLOSER (outreach) |
| **AGENCE** | SIBYL (timing) + PRISM (pricing) | VOLT (architecture) + ANVIL (dev) | CLOSER (closing) + KAISER (relation) |
| **TEMPLATES** | NICHE (marché) + GLITCH (angle) | VOLT + PHILOMÈNE + ANVIL | CLOSER (Gumroad) + RACOON (promo) |
| **CONTENU** | NICHE (trend) + GLITCH (angle) | VIRAL + PHILOMÈNE + FRESCO | RACOON (distribution) + VIRAL (social) |
| **NEWSLETTER** | DATUM (métriques) + NICHE (sujets) | PHILOMÈNE + VIRAL | Distribution Beehiiv + LEDGER |
| **TITAN** | PULSE (audit) + DATUM (perf) | ANVIL + VOLT (dev) | PULSE (deploy) + FRANKLIN (stabilité) |

---

## SELF-ANNEALING PAR PÔLE

Chaque pôle a son propre cycle d'amélioration :

### Pôle R — Amélioration du renseignement
```
1. Brief envoyé à F
2. F produit le livrable
3. D mesure les résultats
4. R analyse l'écart entre prédiction et réalité
5. R ajuste ses modèles de scoring
→ Briefs de plus en plus précis au fil du temps
```

### Pôle F — Amélioration de la production
```
1. Livrable produit
2. D mesure la qualité perçue (ventes, feedback)
3. F analyse les patterns de succès/échec
4. F ajuste ses templates et processus
→ Livrables de plus en plus efficaces
```

### Pôle D — Amélioration de la distribution
```
1. Livrable distribué
2. Métriques collectées (ventes, conversion, coûts)
3. D identifie les canaux les plus performants
4. D optimise le mix distribution
→ Revenus croissants à effort constant
```

---

## RÈGLES D'OR DU TRI-PÔLE

1. **Chaque agent sait à quel pôle il appartient** — pas de confusion
2. **Les gouverneurs décident au sein de leur pôle** — pas de micro-management
3. **OMEGA intervient uniquement si inter-pôle ou crise** — pas de surcharge
4. **La boucle R→F→D→R ne s'arrête jamais** — c'est le moteur de l'empire
5. **Format de communication standardisé** — `[PÔLE→PÔLE] Type : "message"`
6. **Solo par défaut au sein du pôle** — coalitions uniquement si nécessaire
7. **Augus reçoit des résultats, pas des process** — le Tri-Pôle est invisible pour lui sauf s'il demande
8. **Coût total : 0€** — contrainte maintenue, aucun pôle ne dépense sans GO explicite
9. **Feedback obligatoire** — D envoie TOUJOURS un retour à R après distribution
10. **Le système devient plus fort après chaque boucle** — sinon la boucle n'est pas terminée

---

## COMPATIBILITÉ

| Système existant | Statut | Relation avec Tri-Pôle |
|-----------------|--------|----------------------|
| Moon Tower (CASTING.md) | Actif — référence culturelle | Les 7 niveaux se mappent dans les 3 pôles |
| ORCHESTRATION_V2.md | Actif — système de dispatch | SENTINEL dispatch au-dessus des pôles |
| ROUTING.md | Actif — table de routing | Enrichie avec le routage par pôle |
| META_AGENTS.md | Actif — couche évolutive | 6 méta-agents au-dessus des 3 pôles |
| CONTEXT_BOOT.md | Actif — séquence boot | Inchangé, Tri-Pôle consulté à STEP 4 |

---

*Directive créée par OMEGA + CORTEX + GLITCH + VOLT + SENTINEL.*
*Validée LEDGER. Protégée FRANKLIN. Exécution immédiate.*
