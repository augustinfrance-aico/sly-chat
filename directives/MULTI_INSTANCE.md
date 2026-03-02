# MULTI_INSTANCE.md — Protocole Anti-Conflit Claude Code

> *"Deux généraux peuvent mener la même guerre — s'ils ont des cartes différentes et ne se marchent pas dessus."*

---

## POURQUOI CE FICHIER EXISTE

Augus ouvre parfois **plusieurs instances Claude Code en même temps** sur le même workspace.

Sans règles claires = désastre :
- Instance A écrit dans `grimaldi.md` pendant qu'Instance B le lit → corruption
- Les deux instances créent des fichiers différents avec le même nom → collision
- Une instance supprime ce que l'autre vient de créer → perte de travail

Ce fichier = le **code de la route** pour les Claude en parallèle.

---

## RÈGLE #0 — VÉRIFIER AVANT D'AGIR

Avant toute modification d'un fichier, mentalement (ou en lisant) vérifier :

```
Est-ce que ce fichier est dans ma zone de travail assignée ?
Est-ce qu'une autre instance est susceptible d'y toucher aussi ?
```

Si oui aux deux → **ne pas modifier**. Attendre ou changer d'approche.

---

## LES 3 ZONES DE TRAVAIL

Quand plusieurs Claude tournent en parallèle, chacun reçoit une **zone nommée**.
Roster complet officiel : personnalites/CASTING.md (50 agents — mis à jour 02/03/2026)

### Zone A — Nébuleuse + Leaders + Méta + Stratégie
```
personnalites/omega.md
personnalites/sly.md
personnalites/bentley.md
personnalites/murray.md
personnalites/darwin.md
personnalites/shadow.md
personnalites/agora.md
personnalites/chronos.md
personnalites/havoc.md
personnalites/atlas.md
personnalites/sentinel.md
personnalites/cortex.md
personnalites/glitch.md
personnalites/sibyl.md
personnalites/nexus.md
```

### Zone B — Vente + Contenu + Ops + Marchés
```
personnalites/closer.md
personnalites/kaiser.md
personnalites/prism.md
personnalites/onyx.md
personnalites/ledger.md
personnalites/philomene.md
personnalites/fresco.md
personnalites/viral.md
personnalites/franklin.md
personnalites/anvil.md
personnalites/dreyfus.md
personnalites/specter.md
personnalites/datum.md
personnalites/pulse.md
personnalites/niche.md
personnalites/racoon.md
```

### Zone C — R&D + Nouveaux + Fichiers système
```
personnalites/cipher.md
personnalites/radar.md
personnalites/proto.md
personnalites/pixel.md
personnalites/aurora.md
personnalites/virgile.md
personnalites/gauss.md
personnalites/orpheus.md
personnalites/mercer.md
personnalites/turing.md
personnalites/flux.md
personnalites/hunter.md
personnalites/mirage.md
personnalites/justice.md
personnalites/echo.md
directives/*.md        ← fichiers de protocole
portfolios/*.html      ← portfolios HTML
execution/titan/*.py   ← code SLY bot
sly-chat/index.html    ← HIGH RISK — 1 seule instance à la fois
```

---

## FICHIERS PARTAGÉS — ZONE ROUGE

Ces fichiers sont **lus par tout le monde, modifiés par personne** sans concertation :

```
CLAUDE.md                        ← mémoire projet — lire OK, modifier AVEC PRÉCAUTION
personnalites/CASTING.md         ← roster officiel (50 agents) — SOURCE DE VÉRITÉ — lecture seule
.env                             ← secrets — ne jamais modifier en parallèle
execution/titan/config.py        ← config SLY bot — une instance à la fois
sly-chat/index.html              ← HIGH RISK — une seule instance à la fois
```

**Règle** : Si tu dois modifier un fichier Zone Rouge, annonce-le dans ta réponse à l'utilisateur avant d'agir.

---

## FICHIERS TEMPORAIRES — NOMMAGE ANTI-COLLISION

Chaque instance qui crée des fichiers temporaires utilise un **préfixe de session** :

```
Format : .tmp/[instance_id]_[nom_fichier]

Exemples :
  .tmp/instanceA_draft_portfolio.html
  .tmp/instanceB_test_output.txt
  .tmp/instanceC_rapport_audit.md
```

**Jamais** de fichiers `.tmp/temp.txt` ou `.tmp/output.json` sans préfixe → collision garantie.

---

## PROTOCOLE DE MERGE (EN CAS DE CONFLIT)

Si deux instances ont modifié le même fichier :

1. **Lire les deux versions** (git diff ou comparaison manuelle)
2. **Identifier les sections** : sont-elles différentes ou superposées ?
3. Si différentes → **merger les deux** (les deux ajouts sont valides)
4. Si superposées → **garder la plus complète**, signaler à Augus

**Ne jamais écraser silencieusement.** Toujours signaler le conflit dans la réponse.

---

## PATTERN DE TRAVAIL RECOMMANDÉ

### Pour Augus (l'orchestrateur humain)

Quand tu lances plusieurs Claude en parallèle :

```
Instance 1 : "Tu travailles sur la Zone A (agents 1-10)"
Instance 2 : "Tu travailles sur la Zone B (agents 11-20)"
Instance 3 : "Tu travailles sur la Zone C (agents 21-25 + system)"
```

Précise **explicitement la zone** dans ton premier message à chaque instance.

### Pour Claude (l'exécutant)

Au démarrage d'une session :
1. Vérifier ce fichier MULTI_INSTANCE.md
2. Identifier ta zone assignée
3. Rester dans ta zone sauf instruction explicite
4. Annoncer tout travail sur Zone Rouge avant d'agir

---

## SIGNAUX D'ALARME

Si tu détectes l'un de ces signes, **STOP et signale à Augus** :

```
🔴 STOP — Fichier modifié depuis ta dernière lecture (mtime changé)
🔴 STOP — Section déjà présente que tu allais créer
🔴 STOP — Contenu différent de ce que tu attendais dans un fichier
🔴 STOP — Deux instances éditent le même fichier simultanément
```

Le coût d'un arrêt = 30 secondes.
Le coût d'une collision = 30 minutes de repair.

---

## JOURNAL DE SESSION (OPTIONNEL)

Chaque instance peut créer un mini-journal de ce qu'elle fait :

```
.tmp/session_[timestamp]_log.txt

Contenu :
- Instance : [A/B/C]
- Zone : [agents 1-10 / 11-20 / etc]
- Fichiers touchés : [liste]
- Statut : [en cours / terminé]
```

Permet à Augus de tracker quelle instance a fait quoi.

---

## RÉSUMÉ EN 10 MOTS

> **Zone assignée → rester dedans → annoncer avant de toucher Zone Rouge.**

---

## RÈGLE CRITIQUE — MÊME PROMPT ENVOYÉ À PLUSIEURS FENÊTRES (01/03/2026)

> Augus envoie parfois le **même prompt identique** à 2-3 fenêtres Claude Code en parallèle.

### Est-ce que ça marche ? Réponse honnête :

**✅ Oui pour :** recherche, analyse, brainstorming, rédaction de directives, questions stratégiques.
→ Chaque fenêtre explore des angles différents. Augus garde le meilleur. Productivité réelle.

**⚠️ Dangereux pour :** modification de fichiers partagés, push git, modifications de code.
→ Deux fenêtres qui écrivent sur le même fichier = corruption garantie. Race condition.

### Protocole quand tu reçois un prompt et suspectes d'autres instances actives

1. **Lire `git status`** au démarrage de toute tâche de modification. Si des fichiers sont `M` sans que tu les aies touchés → autre fenêtre active.
2. **Vérifier les fichiers cibles** : si le fichier que tu vas modifier est dans la liste ci-dessous → ANNONCER avant d'agir.
3. **Ne JAMAIS écrire silencieusement** sur un fichier Zone Rouge sans signaler.

### Signal d'alerte à afficher SI SUSPICION

```
⚠️ MULTI-FENÊTRES DÉTECTÉ
Ce prompt a peut-être été envoyé à plusieurs instances Claude Code.
Si une autre fenêtre travaille sur [nom_fichier], STOP et confirme l'ordre des priorités.
Cette instance va : [décrire l'action prévue]
```

### Règle de coordination (quand même prompt, même fichier)

| Situation | Action |
|-----------|--------|
| Deux fenêtres reçoivent le même prompt de recherche | OK — chacune explore, Augus choisit |
| Deux fenêtres vont modifier le même fichier HTML/JS | STOP — une seule modifie, l'autre attend |
| Deux fenêtres vont modifier le même fichier .md | Merger les deux versions après, ne pas écraser |
| Deux fenêtres font un `git push` | DANGER — ne push qu'une seule. Sinon conflits remote. |

### Recommandation à Augus

Quand tu envoies le même prompt à plusieurs fenêtres :
- Pour des **tâches intellectuelles** (analyse, écriture, stratégie) → top, garde le meilleur
- Pour des **tâches de code sur le même fichier** → assigne des zones différentes à chaque fenêtre
- Format suggéré : "Fenêtre 1 : tu travailles sur le splash + CSS. Fenêtre 2 : tu travailles sur le JS IA cascade."

> **Résumé** : Même prompt = puissant pour la pensée parallèle. Dangereux si les deux touchent les mêmes fichiers. Toujours annoncer avant d'agir.

---

## RÈGLE CRITIQUE — FENÊTRES PARALLÈLES SUR UN PROJET ACTIF (01/03/2026)

> **Quand une autre fenêtre Claude Code travaille DÉJÀ sur un fichier, cette fenêtre NE TOUCHE PAS ce fichier.**

### Signaux d'alerte à vérifier AVANT toute modification

1. **Vérifier git status** : si un fichier est listé comme modifié (M) et que tu n'es pas celui qui l'a modifié → STOP.
2. **Vérifier mtime** : si le fichier a été modifié récemment et que ta session n'a rien fait → une autre fenêtre travaille dessus.
3. **Lire le fichier entier** : si le contenu ne correspond pas à ce que tu attendais (ajouts non planifiés) → autre fenêtre active.

### Fichiers actifs SLY-CHAT — ZONE ROUGE PARTAGÉE

```
sly-chat/index.html          ← fichier principal — UNE SEULE instance à la fois
sly-chat/manifest.json       ← config PWA
sly-chat/service-worker.js   ← SW
```

### Protocole si conflit détecté

```
1. STOP immédiat — ne pas écrire
2. Signaler à Augus : "⚠️ Conflit détecté — sly-chat/index.html modifié par autre fenêtre"
3. Attendre confirmation d'Augus sur qui continue
4. Si Augus dit "continue toi" → reprendre EN RELISANT le fichier entier d'abord
5. Merger les changements des deux fenêtres si possible, JAMAIS écraser silencieusement
```

### Coordination proactive

Sur CHAQUE réponse impliquant `sly-chat/index.html`, ANNONCER :
> "⚠️ Note : si une autre fenêtre Claude Code travaille sur index.html en ce moment, nous risquons un conflit. Confirme que cette fenêtre est seule à modifier ce fichier."

---

*Mis à jour le 01/03/2026 — Ajout protocole multi-fenêtres SLY-CHAT*

*Créé le 25/02/2026 — Protocole AICO Digital Workshop*
