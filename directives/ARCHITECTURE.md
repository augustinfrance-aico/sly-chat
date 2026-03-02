# ARCHITECTURE.md — Architecture Technique SLY

> HIÉRARCHIE N1 (voir VISION.md pour la hiérarchie complète).
> En cas de conflit avec N2/N3/N4 : ce document gagne.
> En cas de conflit avec VISION.md (N0) : VISION.md gagne.
> Lire avant toute modification de code, d'infrastructure ou d'architecture.

---

## Vue d'ensemble

```
WORKSPACE AICO/
│
├── execution/titan/          # SLY Bot — moteur principal (Python async)
│   ├── brain.py              # Cerveau IA — cascade Groq + Gemini
│   ├── president.py          # Directeur — orchestration des modules
│   ├── config.py             # Configuration centralisée (charge .env)
│   ├── scheduler.py          # Tâches automatiques 24/7
│   ├── command_server.py     # REST API locale (port 7777)
│   ├── requirements.txt      # Dépendances Python
│   └── modules/              # 70+ modules spécialisés
│
├── sly-chat/                 # SLY-CHAT — App mobile/web
│   ├── index.html            # App principale (4000+ lignes)
│   └── [assets]              # Images, modèles 3D, GLB
│
├── portfolios/               # SLY-COMMAND + portfolios clients
│   └── titan_command.html    # Dashboard web (12 tabs)
│
├── directives/               # SOPs, blueprints, orchestration
├── personnalites/            # 50 fiches agents Cooper Building
├── agents/                   # Pipelines KDP/STOCK/LEADS + profiles
├── Blueprint/                # Feuilles de route stratégiques
├── src/                      # Manuscrits KDP en cours
└── .env                      # Secrets (JAMAIS commité)
```

---

## SLY Bot — Architecture Interne

### Cascade IA (ordre de priorité)
```
1. Groq llama-3.3-70b        (primaire — le plus capable)
2. Groq llama-4-maverick      (fallback 1)
3. Groq llama-4-scout         (fallback 2)
4. Groq kimi-k2               (fallback 3)
5. Groq qwen3-32b             (fallback 4)
6. Groq llama-3.1-8b          (fallback 5 — le plus rapide)
7. Gemini (Google)            (fallback final — toujours dispo)
8. Ollama local               (optionnel, si dispo)
```

**Règle** : jamais de single point of failure. Si un modèle fail → suivant automatiquement.

### Transport
- **Polling Telegram** (pas webhook) — plus simple, plus robuste pour Railway
- Anti-doublon : `set processed_messages` (max 500, purge à 200)
- Timeout par message : 30 secondes max avant fallback

### Mémoire
- Fenêtre : 25 messages actifs
- Auto-facts : extraction automatique des infos importantes
- Profil perso + contacts persistants
- President state : `execution/titan/memory/president.json`

### Modules clés
| Module | Rôle |
|--------|------|
| brain.py | Cerveau IA — dispatch + cascade modèles |
| president.py | Directeur — état + priorités + décisions |
| voice.py | Transcription vocale + TTS |
| gamification.py | Système XP + achievements |
| finance.py | Crypto + portfolio |
| news.py | Agrégation + résumé news |
| upwork.py | Scanner offres Upwork |
| scheduler.py | Tâches automatiques (cron-like) |
| liquefactor.py | Content Liquefactor pipeline |
| transcribe.py | Transcription audio |

---

## SLY-CHAT — Architecture Cible

### Stack technique confirmé (blueprint `PROMPT_SLY_CHAT.md`)
```
Frontend : HTML/CSS/JS (index.html) → Capacitor 6 (iOS natif)
Backend  : Proxy endpoints sur SLY Bot Railway (pas de clés frontend)
IA       : Groq direct (fallback) → via proxy production
TTS      : ElevenLabs + FishAudio (voix clonées doubleurs FR)
3D       : Three.js + GLB Sketchfab (Sly Cooper model)
Push     : APNS via Capacitor (iOS natif)
```

### Ce qui est en place vs ce qui manque
✅ App web (4000+ lignes, 37 features)
✅ Chat IA fonctionnel (Groq direct)
✅ TTS ElevenLabs basique

❌ Proxy backend (clés API exposées en frontend — CRITIQUE)
❌ Capacitor 6 (pas d'app iOS native)
❌ Modèle 3D Sly Cooper (Three.js + GLB)
❌ WebSocket vers SLY Bot
❌ APNS push notifications
❌ Métriques/observabilité (TTFT, TTFA)
❌ Circuit Breaker pattern
❌ Mémoire 4 couches réelle

---

## SLY-COMMAND — Architecture

```
Interface  : portfolios/titan_command.html (12 tabs, PWA)
Backend    : execution/titan/command_server.py (port 7777, REST)
Deploy     : GitHub Pages (augustinfrance-aico/sly-command)
Chat IA    : Groq direct (clé frontend — à migrer vers proxy)
TTS        : ElevenLabs + FishAudio Plus ($11/mo, 200 min/mo)
```

---

## Déploiement Infrastructure

### Railway (production SLY Bot)
- Auto-deploy depuis GitHub (branche main)
- Dockerfile à la racine du projet
- `railway.toml` pour config
- Budget : $4-5/mois (hobby plan)

### GitHub Pages (frontends)
- sly-chat : `augustinfrance-aico/sly-chat` → https://augustinfrance-aico.github.io/sly-chat/
- sly-command : `augustinfrance-aico/sly-command`

### n8n (automatisations clients)
- Lurie : Railway instance + Cloud
- Workflows news : 7/jour, Moldova + RO + RU + Forbes
- Timezone : America/New_York (UTC-5), Moldavie = +7h

---

## Contraintes Architecture NON NÉGOCIABLES

1. **ZÉRO COÛT** sauf si ROI démontré — tout doit tenir sur les tiers gratuits
2. **Pas de single point of failure** — cascade + fallback PARTOUT
3. **Anti-regress** — ne pas casser ce qui fonctionne en prod
4. **Séparation des secrets** — clés API dans `.env` uniquement, jamais dans le code
5. **Encoding UTF-8** partout (Windows compatibility bug vécu)
6. **Blueprint first** — `PROMPT_SLY_CHAT.md` est la loi pour SLY-CHAT

---

## Décisions Techniques Figées

| Décision | Raison |
|----------|--------|
| Polling Telegram (pas webhook) | Simplicité + robustesse Railway |
| Groq primaire (pas OpenAI) | Gratuit, ultra-rapide |
| Gemini comme dernier fallback | Toujours dispo, gratuit |
| Railway pour SLY Bot | Auto-deploy, 5$/mo max |
| GitHub Pages pour frontends | Gratuit, CDN mondial |
| Python async pour SLY Bot | Perf + écosystème bot Telegram |

---

## Règles Architecture

### AVANT toute modification
1. Lire ce fichier complet
2. Identifier les fichiers impactés
3. Vérifier qui importe le module modifié
4. Vérifier la cascade IA si brain.py touché
5. Vérifier les secrets si config.py touché

### INTERDICTIONS
- Jamais commiter `.env`
- Jamais hardcoder une clé API dans le code
- Jamais casser la cascade Groq → Gemini
- Jamais ajouter une dépendance payante sans signaler à Augus
- Jamais modifier le polling Telegram sans test préalable

### OBLIGATIONS
- Tout changement dans `modules/` → vérifier `president.py` (qui orchestre)
- Tout changement dans `config.py` → vérifier le `.env` de prod Railway
- Tout changement frontend → tester localement avant GitHub Pages
