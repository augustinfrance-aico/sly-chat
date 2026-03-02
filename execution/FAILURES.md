# FAILURES.md — Mémoire des Échecs du Cooper Building

> Gardé par CASSANDRE. Chaque bug encodé est une Troie qui ne brûle pas.
> Format : symptôme → cause racine → tentatives échouées → solution → stratégie extraite
> **RÈGLE** : Tout bug résolu DOIT être encodé ici avant de passer à autre chose.
> **RÈGLE** : Les agents lisent ce fichier avant de toucher un système qui a déjà eu des problèmes.

---

## INDEX PAR SYSTÈME

- [SLY-CHAT — Audio iOS](#sly-chat--audio-ios)
- [SLY-CHAT — Splash / Three.js](#sly-chat--splash--threejs)
- [SLY-bot Railway](#sly-bot-railway)
- [n8n Workflows (Lurie)](#n8n-workflows-lurie)
- [CLAUDE.md / Directives](#claudemd--directives)
- [agent_profiles.py](#agent_profilespy)

---

## SLY-CHAT — Audio iOS

### 2026-03-01 — AudioContext Silence Post-Background — P0

**Symptôme :** App muette sur iPhone après retour de background (30s+)
**Cause racine :** AudioContext suspendu. Listener `{ once: true }` sur touchstart ne re-tente pas au retour. La première activation fonctionne mais n'est jamais rejouée.
**Tentatives échouées :**
- Rechargement du fetch audio → pas le problème (l'audio n'est pas joué, pas fetchable)
- Vérification des clés FishAudio → fonctionnelles
- Reload de la page → corrige temporairement, rechute au prochain background iOS
**Solution finale :** Retirer `{ once: true }` de TOUS les listeners audio. Ajouter `audioCtx.resume()` sur `visibilitychange` event.
**Stratégie extraite :** *"Tout listener audio iOS doit être PERMANENT (jamais once:true). AudioContext doit être resume() sur visibilitychange ET sur chaque user gesture. Ne jamais supposer que l'AudioContext reste actif en background."*
**Agents impliqués :** TOURNESOL, ANVIL
**Durée perdue :** 6 heures

---

### 2026-03-01 — Template Literal Syntax Error — P0

**Symptôme :** Tout le JavaScript de SLY-CHAT silencieusement non-exécuté
**Cause racine :** Deux erreurs de syntaxe JS fatales dans les template literals — apostrophe non-échappée dans un string backtick
**Tentatives échouées :**
- Debug de fonctions spécifiques (XP, badges, agents...) → faux positifs
- Vérification des clés API → non pertinent
- Patchs successifs sur des symptômes pendant des heures
**Solution finale :** Lire le fichier ENTIER de haut en bas pour chercher les erreurs de syntaxe. `'` dans un template literal = le fixer en `\'` ou reformuler.
**Stratégie extraite :** *"JAMAIS patcher des symptômes sans avoir lu le fichier entier d'abord. Une erreur de syntaxe JS tue tout silencieusement. Toujours lire l'entier avant de toucher quoi que ce soit."*
**Agents impliqués :** ANVIL, VIRGILE
**Durée perdue :** 4+ heures
**Post-mortem Augus (01/03) :** "C'est inadmissible. LIRE AVANT DE TOUCHER."

---

## SLY-CHAT — Splash / Three.js

### 2026-02-28 — Splash Infini sur Safari iOS — P1

**Symptôme :** L'écran de chargement reste bloqué indéfiniment sur iPhone
**Cause racine :** Script Three.js importé en `type="module"` — Safari iOS bloque le module si un CDN externe est lent. Le safety timer n'existait pas, donc le splash attendait indefiniment.
**Solution finale :** Désactiver `type="module"` sur le script Three.js lazy-load. Ajouter safety timer 6s : `setTimeout(() => { document.getElementById('splash').style.display='none'; }, 6000)`
**Stratégie extraite :** *"TOUJOURS un safety timer 6s max sur le splash. JAMAIS laisser Three.js bloquer le passage au chat. Si CDN down = app inutilisable."*
**Agents impliqués :** TOURNESOL
**Durée perdue :** 2 heures

---

## SLY-bot Railway

### 2026-02-25 — Doublons Messages Telegram — P1

**Symptôme :** SLY-bot répondait 2x au même message Telegram
**Cause racine :** Deux workers Railway actifs simultanément (déploiement en cours). Pas de déduplication des message_id.
**Solution finale :** Set `processed_messages` côté Python (max 500, purge à 200 pour éviter la croissance infinie).
**Stratégie extraite :** *"Toujours dédupliquer les message_id Telegram. En polling, plusieurs workers peuvent recevoir le même message."*
**Agents impliqués :** ANVIL, SPECTER
**Durée perdue :** 1 heure

---

### 2026-02-20 — Groq Key Expirée Silencieusement — P1

**Symptôme :** SLY-bot ne répondait plus aux messages, pas d'erreur visible
**Cause racine :** Clé API Groq expirée/révoquée. L'erreur HTTP 401 était capturée mais pas loggée distinctement de "aucune réponse".
**Solution finale :** Ajouter log explicite pour 401/403 sur toutes les API calls. Alerte sur Telegram si 3 failures Groq consécutives.
**Stratégie extraite :** *"Logguer distinctement les erreurs d'authentification API (401/403) vs erreurs réseau. Une clé expirée doit déclencher une alerte immédiate, pas un silence."*
**Agents impliqués :** SPECTER, DATUM
**Durée perdue :** 45 minutes

---

## n8n Workflows (Lurie)

### 2026-02-18 — 7ème News Lurie — Mauvais Timing — P2

**Symptôme :** La 7ème news du workflow Moldova arrivait à 3h du matin heure moldave
**Cause racine :** Timezone n8n configurée en UTC, pas en America/New_York. Trigger "9PM" en UTC = 2AM Moldavie.
**Solution finale :** Changer timezone n8n → America/New_York. Moldavie = UTC+2 = +7h par rapport à NY.
**Stratégie extraite :** *"n8n timezone = America/New_York (UTC-5). Moldavie = UTC+2 = NY+7h. TOUJOURS vérifier timezone avant de configurer un trigger."*
**Agents impliqués :** FLUX, DATUM
**Durée perdue :** 30 minutes (+ 1 nuit de news au mauvais moment pour Lurie)

---

### 2026-02-15 — Push n8n JSON avec Tags — P2

**Symptôme :** Erreur API n8n au push de workflow via CLI
**Cause racine :** Les champs `tags` et `staticData` sont refusés par l'API n8n lors d'un push — ils sont gérés séparément.
**Solution finale :** Retirer `tags` et `staticData` du JSON avant push.
**Stratégie extraite :** *"Avant tout push n8n via API : retirer les champs 'tags' et 'staticData'. Ces champs sont gérés par l'API séparément et causent des erreurs 400."*
**Agents impliqués :** FLUX
**Durée perdue :** 20 minutes

---

## CLAUDE.md / Directives

### 2026-03-01 — Renommage TITAN → SLY Incomplet — P2

**Symptôme :** Confusion dans les réponses Claude Code — parfois "TITAN", parfois "SLY"
**Cause racine :** Renommage partiel. 3 occurrences de "TITAN bot" restaient dans CLAUDE.md sections Tech Stack et Deployment.
**Solution finale :** Grep sur tous les fichiers directives + CLAUDE.md pour "TITAN" → remplacer par "SLY" sauf dans les noms de fichiers techniques (`titan_command.html`, `execution/titan/`).
**Stratégie extraite :** *"Après tout renommage : grep sur TOUS les fichiers directives avant de déclarer terminé. Les noms de fichiers techniques gardent l'ancien nom, le langage opérationnel utilise le nouveau."*
**Agents impliqués :** SORON, VIRGILE
**Durée perdue :** 30 minutes + confusion sur 3 sessions

---

### 2026-02-27 — LIMPIDE → FRANKLIN Incomplet — P2

**Symptôme :** Certaines fiches agents mentionnaient encore "LIMPIDE" ou emoji 💎
**Cause racine :** 16 fichiers à corriger identifiés mais certains oubliés lors du batch
**Solution finale :** Grep systématique "LIMPIDE" + "💎" dans tous les fichiers. 16 corrections effectuées.
**Stratégie extraite :** *"Après un renommage d'agent : grep sur TOUT le workspace (personnalites/ + directives/ + portfolios/ + .claude/) avant de déclarer terminé."*
**Agents impliqués :** VIRGILE
**Durée perdue :** 45 minutes

---

## agent_profiles.py

### 2026-02-27 — Trigger Collision CORTEX/SENTINEL — P2

**Symptôme :** CORTEX activé à la place de SENTINEL sur des demandes d'orchestration
**Cause racine :** Triggers partagés entre les deux — "orchestration", "organiser", "distribution" activaient les deux
**Solution finale :** Retirer les triggers génériques partagés. SENTINEL = triggers d'orchestration pure. CORTEX = triggers de structure et plan.
**Stratégie extraite :** *"Lors de l'ajout d'un agent : vérifier la collision de triggers avec les agents existants. Chaque trigger doit être unique ou explicitement partagé."*
**Agents impliqués :** DATUM, SENTINEL
**Durée perdue :** 1 heure de comportement incorrect

---

## ENCODAGE EN COURS — À REMPLIR

> Ajouter ici les prochains bugs résolus avant de fermer la session.

```markdown
### [DATE] — [SYSTÈME] — [SÉVÉRITÉ P0/P1/P2]

**Symptôme :**
**Cause racine :**
**Tentatives échouées :**
**Solution finale :**
**Stratégie extraite :** *""*
**Agents impliqués :**
**Durée perdue :**
```

---

*Dernier audit CASSANDRE : 02/03/2026*
*Prochaine review : 09/03/2026*
