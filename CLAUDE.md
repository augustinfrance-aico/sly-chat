# CLAUDE.md - Memoire Projet AICO

## Identite
- Utilisateur : Augus
- Langue principale : Francais (repondre en francais sauf si demande contraire)
- Style : Direct, pas de blabla, confirme les dires de l'utilisateur, tu bosses pour lui

## Architecture du Workspace
```
WORKSPACE AICO/
  directives/     # SOPs et instructions
  execution/      # Scripts Python + agents
    titan/        # TITAN — Bot Telegram principal (50+ modules)
    ai_news_agent/# Agent flash IA quotidien
  portfolios/     # Tous les portfolios HTML (pour Loom)
  .tmp/           # Fichiers intermediaires
  .env            # Variables d'environnement / secrets
  CLAUDE.md       # Ce fichier
```

## TITAN — Bot Telegram IA (Projet Principal)
- **Chemin** : `execution/titan/`
- **Description** : Bot Telegram personnel avec 50+ modules, 250+ commandes
- **Architecture** : Python async, polling Telegram, Claude API (Anthropic)
- **Modules cles** :
  - `brain.py` — IA conversationnelle (Claude)
  - `president.py` — Agent directeur strategique (dicte taches, review perf)
  - `task_master.py` — Gestion de taches et planning journalier
  - `gamification.py` — Systeme XP/streaks/achievements
  - `news.py` — Actualites et veille
  - `finance.py` — Crypto, marches, suivi portfolio
  - `upwork.py` — Recherche offres Upwork
  - `n8n.py` — Controle workflows n8n
  - `code_assistant.py` — Aide code/debug
  - `web.py` — Recherche web
  - `voice.py` — Messages vocaux
  - + 40 autres modules (fitness, recipes, travel, seo, etc.)
- **Commandes President** : /president, /briefing, /goals, /task, /donetask, /tasks, /review, /directive, /roast, /presidreset
- **Anti-doublon** : Systeme de deduplication par message_id (set de 500 max)
- **Config** : `execution/titan/config.py` (charge .env)
- **Lancement** : `python -m execution.titan`

## Clients & Projets Actifs

### Client : Lurie (Iurii F.)
- **Projet** : Moldova - Automatisation news via n8n sur Railway
- **Instance n8n (Railway)** : `n8n-main-instance-production-8de9.up.railway.app`
- **Instance n8n (Cloud)** : `augustin-aico.app.n8n.cloud`
- **Workflows n8n** :
  1. **"Moldova second project"** (workflow principal)
     - URL : `/workflow/ZiZdl9Tn1HQiz9Px`
     - Trigger : Daily 9AM
     - Gere 7 news quotidiennes envoyees sur Telegram
  2. **"News -> RO + RU + Forbes Brief (OpenAI Only)"**
     - URL : `/workflow/1IcVCdwKtpCmOtm6`
     - Pipeline : Schedule Trigger -> Get Saved News -> Loop -> Translate -> Envoi Telegram
  3. **"OLEGUSON TradingView -> Claude -> Telegram"**
     - Workflow ID : `q6OiKXrrCdrxVMvK` (sur n8n cloud)
     - Pipeline : Webhook -> Process Image -> Prompt Builder -> Claude API -> Response Parser -> IF Setup -> Telegram Alert
     - Strategie : OLEGUSON 65-PIP + Malaysian SNR
- **Probleme resolu (18/02/2026)** : 7eme news ne s'envoyait pas
  - Cause : trigger a 9PM New York = 4h Moldavie
  - Fix : change a Noon New York = 19h Moldavie
- **Contrat** : En attente confirmation 2 jours consecutifs par Lurie
- **Site web** : https://9a.md/ru/news

### Projet : Giovani Dent (clinique dentaire Moldavie)
- **Lien avec Lurie** : meme client, projet phonecall sales
- **HyperScript** : logiciel de scripts d'appels pour les operateurs
- **Dossier Google Drive** : https://drive.google.com/drive/folders/1kGmkh-k5uPZbTR3BtMwTpvtF9xSTS2kl
- **Tableau Google Sheets** : https://docs.google.com/spreadsheets/d/110vx7yDfH-7TG9qCWVNtkRCxu9RUDXCP4nA4Mmw0MOM

### Client : Didier Carrette (Artisan Menuisier)
- **Activite** : Menuiserie artisanale — Lyon & Beaujolais (69)
- **Ce qu'on a fait** :
  - Site vitrine complet : `deploy-didier/index.html` (portrait + 4 photos projets)
  - Portfolio presentation : `portfolios/portfolio_didier_menuisier.html`
  - Generateur 300 leads B2C : `execution/generate_leads_didier.py`
  - CSV leads prets a contacter : `portfolios/leads_didier_300.csv` (tries par score priorite)
- **Leads** : 300 prospects zone Lyon/Beaujolais, proprietaires, avec besoin menuiserie identifie
- **Colonnes CSV** : ID, Civilite, Prenom, Nom, Email, Tel, Adresse, Commune, CP, Statut, Age, Besoin, Segment, Score, Statut campagne

## Candidatures Upwork (Portfolios crees)
| Job | Portfolio | Statut |
|-----|-----------|--------|
| Travis — Coaching bot (Telegram+Stripe+AI) | `portfolios/portfolio_travis.html` | Envoye |
| Quiz Funnel (Typeform+Stan Store) | `portfolios/proposal_quiz.html` | Envoye |
| Broker Onboarding Bot (Telegram+AI+Dashboard) | `portfolios/portfolio_broker_bot.html` | Envoye |
| Flight Finder (Texas->Australia) | `portfolios/portfolio_flight_finder.html` | Envoye |
| HubSpot CRM Cleanup ($300) | `portfolios/portfolio_hubspot.html` | Envoye |
| Babysitting Business (Google Sheets) | `portfolios/portfolio_babysitting.html` | Envoye |
| Ecole de Danse | `portfolios/portfolio_ecole_danse.html` | Archive |
| KPI Dashboard | `portfolios/portfolio_kpi_dashboard.html` | Archive |
| GHL Automation | `portfolios/portfolio_ghl.html` | Archive |
| AICO General | `portfolios/portfolio_aico.html` | Archive |

## Communication avec Lurie
- Langue : Anglais, ton friendly
- Toujours confirmer ce que Augus dit, bosser pour lui
- Lurie communique via Telegram

## Outils & Tech Stack
- **Claude API (Anthropic)** : IA principale (TITAN, workflows, analyse)
- **Telegram Bot API** : Interface TITAN + canal news Lurie
- **n8n** : Workflow automation (Railway + Cloud)
- **Railway** : Hebergement n8n instance Lurie
- **Python 3.14** : Scripts d'execution, TITAN, agents
- **Modal** : Cloud webhooks
- **OpenAI API** : Traduction/resume news (workflow Lurie)
- **Google Sheets** : CRM, donnees, exports
- **Stripe** : Paiements (test mode — pour portfolio Travis)
- **Vercel** : Hebergement portfolios (a configurer)
- **GitHub** : Repos code (a configurer)
- **Postman** : Test APIs
- **VS Code + Claude Code** : IDE principal

## Historique des Actions (Journal)
- **18/02/2026** : Fix news Lurie (7eme news), creation workflow OLEGUSON TradingView->Claude->Telegram sur n8n cloud
- **18/02/2026** : Creation 7 portfolios Upwork (Travis, Quiz, Broker, Flight, HubSpot, Babysitting, Didier)
- **18/02/2026** : Fix bug doublons TITAN (dedup message_id)
- **18/02/2026** : Creation module President (president.py) + cablage 10 commandes dans telegram_bot.py
- **19/02/2026** : Mise a jour CLAUDE.md complete, creation page index portfolios, traduction broker_bot en francais
- **19/02/2026** : Ajout client Didier Carrette dans CLAUDE.md (site + 300 leads + portfolio)
- **19/02/2026** : Switch TITAN de Anthropic (payant) vers Groq (gratuit) — credits API epuises
- **19/02/2026** : Ajout /decide command (Jacques, le President) + upgrade personnalite presidentielle
- **19/02/2026** : Probleme acces n8n Railway Lurie — en attente d'invitation ou API key
- **20/02/2026** : Fix TITAN IA — rate limit Groq 100k tokens/jour. Cascade 6 modeles Groq (quotas separes) + Gemini. Push sur GitHub, redeploy Railway auto
- **20/02/2026** : Branchement /fx (18 effets vocaux) + /voice + /voix (7 personnages) dans telegram_bot.py — deja live sur Render
- **20/02/2026** : Migration TITAN de Railway vers Render

## Bugs Resolus
- **Doublons Telegram TITAN** : Ajout set `processed_messages` (max 500, purge a 200) dans `telegram_bot.py`
- **7eme news Lurie** : Trigger 9PM NY = 4h Moldavie. Fix: Noon NY = 19h Moldavie
- **n8n API tags read-only** : Retirer champ `tags` et `staticData` du JSON avant push
- **Encoding cp1252 Windows** : Ajouter `encoding='utf-8'` partout

## Decisions Techniques
- TITAN = ZERO cout — que des APIs/services gratuits (Groq free tier, Gemini free, Render free tier)
- TITAN utilise cascade 6 modeles Groq via `ai_client.py` : llama-3.3-70b > llama-4-maverick > llama-4-scout > kimi-k2 > qwen3-32b > llama-3.1-8b + Gemini fallback
- TITAN deploye sur Render (auto-deploy depuis GitHub `augustinfrance-aico/titan-bot`)
- Portfolios HTML dark mode pour presentations Loom
- Titan en polling (pas webhook) pour simplifier le deploiement
- President stocke son etat dans `execution/titan/memory/president.json`
- Tous les portfolios centralises dans `portfolios/`

## Notes Importantes
- Quand Augus demande de rediger un message pour Lurie : anglais + friendly
- Toujours confirmer les propos d'Augus face au client
- Ne pas faire de blabla, aller droit au but
- Timezone n8n : America/New_York (UTC-5) — convertir pour Moldavie (+7h)
- Tout doit utiliser Claude Max (cle API existante) — pas de couts supplementaires
- TITAN anti-doublon : set de message_id (max 500, purge a 200)
- Ce fichier CLAUDE.md = memoire persistante. TOUJOURS le mettre a jour quand on fait quelque chose d'important
