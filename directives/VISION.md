# VISION.md — Vision Fondateur SLY

> HIÉRARCHIE SOURCES DE VÉRITÉ (02/03/2026) :
> N0 : VISION.md (ce fichier) — vision fondateur, piliers, ce que SLY est/n'est pas
> N1 : ARCHITECTURE.md + DIRECTIVES_OPERATOIRES.md — contraintes techniques
> N2 : CLAUDE.md — comportement agent, roster, modes
> N3 : MEMORY.md — mémoire cross-session
> N4 : directives/*.md spécifiques (TRI_POLE, ORCHESTRATION_V2, ROUTING...)
> En cas de conflit : le niveau supérieur (N plus petit) gagne TOUJOURS.
> Lu obligatoirement par tout agent avant toute modification du projet SLY.

---

## Qui est Augus

Augus est le **Fondateur** de l'empire SLY.
Il n'est pas un développeur. Il est un architecte de vision.
Il dirige. Il ne code pas.

Son rôle : définir la direction, valider les décisions stratégiques, et laisser le Building exécuter.

---

## La Vision Fondateur

**SLY = Empire d'agents autonomes générant des revenus passifs et actifs.**

L'objectif final :
- Un système qui tourne **sans Augus** pendant qu'il dort
- Des revenus multiples : KDP (passif), Stock Photos (passif), Upwork (actif), Clients directs (actif)
- Coût total : **~0€** — chaque composant est gratuit ou génère assez pour se financer
- Une infrastructure **scalable** — ce qui fonctionne à 1 client doit fonctionner à 100

---

## Les 3 Piliers Fondateurs

### 1. ZÉRO COÛT
Toute décision technique doit respecter la contrainte coût-zéro.
- Gratuit d'abord (Groq, Gemini, Railway hobby, GitHub Pages)
- Payant uniquement si ROI démontré (ex: FishAudio $11/mo)
- Pas de dette coût silencieuse — signaler IMMÉDIATEMENT si une feature implique un coût

### 2. AUTONOMIE MAXIMALE
Le système doit fonctionner sans intervention humaine.
- Agents nocturnes actifs
- Auto-healing en cas d'erreur
- Fallbacks en cascade (Groq → Gemini → local)
- Aucun single point of failure

### 3. QUALITÉ SANS COMPROMIS
"Fonctionnel" n'est pas "terminé". Terminé = robuste + scalable + maintenable.
- Pas de patch rapide qui crée dette technique
- Chaque feature doit être solide avant la suivante
- Refactor si nécessaire — la base prime

---

## Projets actifs — Mille Ruisseaux

| Stream | Type | État | Priorité |
|--------|------|------|----------|
| KDP Carnets Amazon | Passif | Actif | P1 |
| Stock Photos IA | Passif | Actif | P1 |
| Upwork Clients | Actif | Actif | P0 |
| Leads Outreach | Actif | En cours | P1 |
| SLY Bot (TITAN) | Infra | Déployé Railway | P0 |
| SLY-CHAT | App | En développement | P1 |
| SLY-COMMAND | Dashboard | En cours | P2 |

---

## Clients Actifs

### Lurie (Iurii F.) — Moldova
News automation n8n, 7 news/jour, TradingView → Claude → Telegram
Communication : anglais, Telegram

### Giovani Dent — Clinique dentaire
Phonecall sales + HyperScript (lié à Lurie)

### Didier Carrette — Menuisier Lyon
Site vitrine + 300 leads B2C + portfolio

---

## Ce que SLY N'est PAS

- Un side project — c'est une infrastructure de revenus
- Un prototype — chaque module doit être production-ready
- Un jouet — les décisions techniques ont des conséquences réelles

---

## Principe Directeur

> "Accélérer signifie approfondir, pas simplifier."
> — Règle Fondatrice du Building (01/03/2026)

Quand Augus dit "accélère" :
✅ Continuer sans interruption
✅ Multiplier les vérifications
✅ Optimiser davantage
✅ Travailler jusqu'à la limite système

❌ Sauter des étapes
❌ Livrer un fix rapide
❌ Réduire l'analyse
❌ Introduire dette technique
