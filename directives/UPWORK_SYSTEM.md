# UPWORK_SYSTEM — Machine à Clients Autonome

> Upwork = le ruisseau actif le plus rentable à court terme.
> Ce système tourne en autonomie : recherche → candidature → suivi → closing.
> Augus dirige le closing. L'agent fait tout le reste.

---

## Positionnement (ce qu'on vend)

```
PAS : "Je fais de l'IA"  ← trop générique, 10 000 concurrents
OUI : "J'automatise vos process répétitifs avec des agents IA — vous économisez X heures/semaine"
```

**Niches où on gagne :**
- Bots Telegram avec IA (TITAN est notre démo vivante)
- Automatisation n8n (workflow, news, notifications)
- Dashboards + reporting automatisé
- Chatbots client (Telegram/WhatsApp)
- Pipelines de leads automatisés

**Proof of concept disponible immédiatement :**
- TITAN = bot Telegram 50+ modules (démo réelle)
- Workflow n8n Moldova Lurie (déjà en prod)
- 300 leads Didier générés en automatique
- 10 portfolios HTML déjà créés

---

## Processus de candidature autonome

### STEP 1 — Veille quotidienne (agent fait seul)
```
Chercher sur Upwork :
  Mots-clés : "telegram bot", "n8n automation", "AI chatbot", "workflow automation", "python bot"
  Filtre : < 24h, budget > $300, client avec historique

Trier par pertinence :
  ✅ Client avec reviews (sérieux)
  ✅ Budget aligné avec le service
  ✅ Besoin dans nos niches
  ❌ Ignorer : trop vague, client 0 review, budget < $100
```

### STEP 2 — Candidature (agent rédige, Augus approuve si > $500)
```
Structure d'une bonne candidature :

LIGNE 1 : Montrer qu'on a lu le brief (référence un détail spécifique)
LIGNE 2-3 : Notre expérience exactement alignée (exemple concret, pas générique)
LIGNE 4 : Ce qu'on ferait concrètement pour eux (mini-plan en 2-3 étapes)
LIGNE 5 : Appel à l'action simple ("Disponible pour un call de 15 min cette semaine ?")

Longueur cible : 150-200 mots max. Pas un roman.
Ton : confiant, direct, pas servile.
```

**Template de base (adapter à chaque job) :**
```
Hey [Prénom si dispo],

J'ai lu ton brief sur [sujet spécifique]. J'ai récemment [exemple concret aligné].

Pour ton projet, je ferais :
→ [Étape 1 concrète]
→ [Étape 2 concrète]
→ [Livrable final]

Délai estimé : [X jours]. Budget : [fourchette si demandé].

Dispo pour un call rapide cette semaine si ça t'intéresse.

[Augus]
```

### STEP 3 — Portfolio automatique (agent génère)
```
Si le client veut voir des exemples :
→ Agent sélectionne les 2-3 portfolios les plus proches dans portfolios/
→ Génère un message d'accompagnement adapté au job
→ Augus envoie

Portfolios disponibles :
- portfolio_travis.html (bot Telegram + Stripe + IA)
- portfolio_broker_bot.html (bot + dashboard)
- portfolio_babysitting.html (Google Sheets automation)
- + 7 autres dans portfolios/
```

### STEP 4 — Suivi (agent rappelle)
```
Si pas de réponse après 3 jours :
→ 1 relance courte (3 lignes max)
→ Puis laisser tomber — pas de harcèlement

Si réponse positive :
→ Augus prend la main pour le call/négociation
→ Agent prépare : brief du client + questions à poser + budget cible
```

---

## Objectifs et KPIs

| Métrique | Objectif semaine | Objectif mois |
|----------|-----------------|---------------|
| Jobs analysés | 20+ | 80+ |
| Candidatures envoyées | 5-8 | 20-30 |
| Taux de réponse cible | >15% | >15% |
| Calls planifiés | 2-3 | 8-10 |
| Clients signés | 1 | 3-4 |
| Revenu mensuel | 300-800€ | 1000-3000€ |

---

## Règles de pricing

```
Bot Telegram simple (commandes basiques) : 300-600€
Bot Telegram avancé (IA + modules) : 800-2000€
Workflow n8n basique : 200-400€
Workflow n8n complexe (multi-étapes + IA) : 500-1500€
Dashboard automatisé : 400-1000€
Maintenance mensuelle : 100-300€/mois

Règle : jamais en dessous de 150€ pour un projet.
En dessous = perte de temps > valeur générée.
```

---

## Gestion des clients (après signature)

```
Livraison :
→ Toujours livrer en avance ou à temps (jamais en retard)
→ Une démo avant la livraison finale (évite les surprises)
→ Documentation simple (pas technique) sur comment utiliser

Récurrence :
→ Toujours proposer une maintenance mensuelle à la fin
→ "Je peux surveiller que tout tourne et ajouter des features si besoin — X€/mois"
→ 2-3 clients récurrents = revenu stable sans acquisition constante

Feedback :
→ Demander une review Upwork dès le projet terminé
→ Les reviews = taux de conversion futur × 3
```

---

## Projets Upwork en cours

| Client | Projet | Statut | Prochaine action |
|--------|--------|--------|-----------------|
| Travis | Bot Telegram + Stripe | Portfolio envoyé | Relance si pas de réponse |
| Quiz Funnel | Typeform + Stan | Portfolio envoyé | Idem |
| Broker Bot | Bot + Dashboard | Portfolio envoyé | Idem |
| Flight | Texas→Australia | Portfolio envoyé | Idem |
| HubSpot | CRM Cleanup | Portfolio envoyé | Idem |
| Babysitting | Google Sheets | Portfolio envoyé | Idem |
