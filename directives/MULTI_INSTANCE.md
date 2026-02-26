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

### Zone A — Agents 1-10
```
personnalites/omega.md
personnalites/murphy.md
personnalites/philomene.md
personnalites/rick.md
personnalites/nikola.md
personnalites/stanley.md
personnalites/vito.md
personnalites/maya.md
personnalites/basquiat.md
personnalites/zara.md
```

### Zone B — Agents 11-20
```
personnalites/grimaldi.md
personnalites/leon.md
personnalites/spartan.md
personnalites/oracle.md
personnalites/nash.md
personnalites/ghost.md
personnalites/cypher.md
personnalites/forge.md
personnalites/zen.md
personnalites/aladin.md
```

### Zone C — Agents 21-25 + Fichiers système
```
personnalites/sly.md
personnalites/bentley.md
personnalites/murray.md
personnalites/bagheera.md
personnalites/baloo.md
directives/*.md        ← fichiers de protocole
portfolios/*.html      ← portfolios HTML
execution/titan/*.py   ← code TITAN
```

---

## FICHIERS PARTAGÉS — ZONE ROUGE

Ces fichiers sont **lus par tout le monde, modifiés par personne** sans concertation :

```
CLAUDE.md                        ← mémoire projet — lire OK, modifier AVEC PRÉCAUTION
directives/AGENTS.md             ← roster officiel — lecture seule
personnalites/CASTING.md         ← routing — lecture seule
personnalites/ALL_AGENTS_PROMPTS.md  ← archive — lecture seule
.env                             ← secrets — ne jamais modifier en parallèle
execution/titan/config.py        ← config TITAN — une instance à la fois
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

*Créé le 25/02/2026 — Protocole AICO Digital Workshop*
