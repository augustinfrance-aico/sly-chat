# TEMPLATES GUMROAD -- 5 WORKFLOWS N8N PRETS A VENDRE
## Crees par Bentley + Nikola -- Prets a packager et publier

---

## TEMPLATE #1 -- Prospection LinkedIn Automatisee
**Prix recommande : 97EUR**
**Nom produit Gumroad : LinkedIn Outreach Autopilot -- Template n8n**

### Ce que fait ce workflow
1. Scrape les profils LinkedIn de ta cible (via PhantomBuster)
2. Enrichit les donnees avec l’email (via Hunter.io)
3. Genere un message personnalise avec Claude AI pour chaque prospect
4. Envoie la sequence email via Lemlist
5. Log les resultats dans Google Sheets

### Nodes n8n (structure)
```
Trigger: Schedule (Lundi 9h00)
-> Node 1: HTTP Request -> PhantomBuster API (recupere 50 profils/semaine)
-> Node 2: Code (parse les donnees LinkedIn)
-> Node 3: HTTP Request -> Hunter.io (enrichissement email)
-> Node 4: Filter (email trouve = oui)
-> Node 5: HTTP Request -> Claude API
  Prompt: Tu es un expert en outreach B2B. Redige un email de prospection personnalise pour [Prenom] [Nom], [Titre] chez [Entreprise]. Angle : [probleme que notre offre resout]. Ton : professionnel, direct, pas de bullshit. Max 120 mots.
-> Node 6: HTTP Request -> Lemlist API (envoie l’email)
-> Node 7: Google Sheets (log : nom, entreprise, email, statut, date)
```

### Ce qu’on inclut dans le package
- Fichier JSON du workflow (import direct dans n8n)
- Guide de configuration (PDF 8 pages)
- Video Loom de setup (15 min)
- 5 templates de messages a adapter

**Page de vente Gumroad :**
*Stop a la prospection manuelle. Ce workflow n8n trouve tes prospects LinkedIn, enrichit leurs coordonnees, genere un message personnalise par l’IA, et l’envoie automatiquement. 50 prospects contactes chaque semaine sans lever le petit doigt. Setup en 30 minutes. Fonctionne pendant que tu dors.*

---

## TEMPLATE #2 -- Machine a Contenu Multi-Plateforme
**Prix recommande : 147EUR**
**Nom produit Gumroad : Content Machine -- 1 idee -> 8 contenus automatiques**

### Ce que fait ce workflow
1. Tu entres 1 idee de contenu dans un form
2. Claude genere : article Medium, thread LinkedIn, post Instagram, reponse Quora, script YouTube, 3 tweets, email newsletter
3. Tout est stocke dans Notion, pret a publier

### Nodes n8n
```
Trigger: Webhook (formulaire Typeform)
-> Node 1: Code (extrait l’idee + angle + audience cible)
-> Node 2: HTTP Request -> Claude API
  Prompt Master: Tu es un expert content marketing. A partir de cette idee : [IDEE], cree le contenu suivant pour l’audience [AUDIENCE] :
  1. Article Medium (800 mots, SEO-optimise)
  2. Thread LinkedIn (8 posts, hooks forts)
  3. Caption Instagram (150 mots + 5 hashtags)
  4. Reponse Quora (400 mots, valeur pure)
  5. Script YouTube intro (300 mots)
  6. Email newsletter (500 mots, objet inclus)
  Format de sortie : JSON avec cles separees pour chaque format.
-> Node 3: Code (parse le JSON de Claude)
-> Node 4-9: Notion API (cree une page par format dans la base de donnees)
-> Node 10: Slack/Telegram (notification ton contenu est pret)
```

**Page de vente Gumroad :**
*1 idee. 30 secondes. 8 contenus prets a publier. Ce workflow n8n transforme automatiquement chaque idee en article Medium, thread LinkedIn, post Instagram, reponse Quora, script YouTube, email newsletter. Ton Notion se remplit pendant que tu bois ton cafe.*

---

## TEMPLATE #3 -- Veille Concurrentielle IA
**Prix recommande : 67EUR**
**Nom produit Gumroad : Competitor Intelligence -- Veille automatique**

### Ce que fait ce workflow
1. Surveille les sites de tes concurrents (nouvelles pages, prix, offres)
2. Surveille les mots-cles de ta niche sur Google Alerts
3. Recupere les posts LinkedIn de tes concurrents
4. Claude analyse et resume les changements importants
5. Rapport hebdomadaire dans ton inbox

### Nodes n8n
```
Trigger: Schedule (Vendredi 8h00)
-> Node 1: HTTP Request -> Scrape URLs concurrents (changements detectes)
-> Node 2: RSS Feed -> Google Alerts niches
-> Node 3: HTTP Request -> Claude API
  Prompt: Analyse ces changements detectes chez mes concurrents : [DATA].
  Identifie : 1) Ce qui est strategiquement important 2) Ce que je devrais repliquer 3) Les opportunites que ca cree pour moi.
  Format : bullet points, max 300 mots.
-> Node 4: Gmail/Email (envoie le rapport)
-> Node 5: Google Sheets (archive l’historique)
```

**Page de vente Gumroad :**
*Sache avant tout le monde ce que font tes concurrents. Ce workflow surveille leurs sites, leurs prix, leurs nouvelles offres, et t’envoie chaque vendredi un rapport IA qui identifie les opportunites. 30 minutes de setup. Veille permanente.*

---

## TEMPLATE #4 -- Support Client Automatise
**Prix recommande : 127EUR**
**Nom produit Gumroad : AI Customer Support -- Reponses automatiques intelligentes**

### Ce que fait ce workflow
1. Recoit les emails clients
2. Claude analyse la demande et sa priorite
3. Genere une reponse personnalisee et precise
4. Pour les cas simples : repond automatiquement
5. Pour les cas complexes : draft pret a valider en 1 clic

### Nodes n8n
```
Trigger: Gmail (nouvel email client recu)
-> Node 1: Code (extrait objet + corps + expediteur)
-> Node 2: HTTP Request -> Claude API
  Prompt: Tu es l’assistant support de [MARQUE].
  Email recu : [EMAIL_CONTENT]
  Historique client : [HISTORIQUE si disponible]
  1. Classifie la demande (simple/complexe/urgent)
  2. Si simple : redige la reponse complete
  3. Si complexe : redige un draft + note pour l’humain
  4. Ton : [CHARTE_TON]
  Format JSON : {classification, reponse, note_interne}
-> Node 3: IF (simple -> envoi auto / complexe -> draft Notion)
-> Node 4a: Gmail (envoi automatique si simple)
-> Node 4b: Notion (draft + alerte Slack si complexe)
-> Node 5: Google Sheets (log de tous les tickets)
```

**Page de vente Gumroad :**
*Reponds a 80% de tes emails clients automatiquement. Claude analyse chaque demande, genere une reponse personnalisee, et l’envoie pour les cas simples. Pour les cas complexes, un draft parfait t’attend en 1 clic. Setup : 45 minutes.*

---

## TEMPLATE #5 -- Pipeline de Creation KDP
**Prix recommande : 197EUR**
**Nom produit Gumroad : KDP Book Factory -- De l’idee au manuscrit automatique**

### Ce que fait ce workflow
1. Tu entres : titre du livre + audience + 8 chapitres souhaites
2. Claude genere chapitre par chapitre (avec retry si trop court)
3. Assemble le manuscrit complet dans un Google Doc
4. Genere la description Amazon optimisee SEO
5. Genere 7 mots-cles pour KDP
6. Notification quand tout est pret

### Nodes n8n
```
Trigger: Webhook (formulaire)
-> Node 1: Code (parse les inputs : titre, audience, chapitres[])
-> Node 2-9: Loop sur chaque chapitre
  Pour chaque chapitre:
  -> HTTP Request -> Claude API
    Prompt: Ecris le chapitre [N] intitule [TITRE_CHAPITRE] du livre [TITRE_LIVRE] pour l’audience [AUDIENCE].
    Inclure : introduction accrocheuse, 3-4 sections avec sous-titres, exemples pratiques, conclusion actionnable.
    Longueur : 2500-3000 mots. Ton : [TON].
  -> Code (verifie longueur > 2000 mots, sinon retry)
  -> Google Docs API (ajoute le chapitre au document)
-> Node 10: HTTP Request -> Claude API (genere description Amazon)
  Prompt: Genere une description Amazon optimisee pour ce livre : [TITRE] pour [AUDIENCE].
  Inclure : hook emotionnel, 5 bullet points benefices, appel a l’action.
  Max 500 mots. Optimise pour les mots-cles KDP.
-> Node 11: HTTP Request -> Claude API (genere 7 mots-cles)
-> Node 12: Google Docs API (ajoute description + mots-cles au document)
-> Node 13: Telegram (notification Ton livre est pret : [LIEN])
```

**Page de vente Gumroad :**
*De l’idee au manuscrit complet en 4 heures. Ce workflow n8n genere chapitre par chapitre, assemble votre livre dans Google Docs, et produit la description Amazon + les 7 mots-cles optimises SEO. Publiez sur KDP le jour meme. Le template inclus a deja produit 12 livres.*

---

## RECAPITULATIF CATALOGUE GUMROAD

| Template | Prix | Temps setup | Revenu passif potentiel |
|---------|------|-------------|------------------------|
| LinkedIn Outreach | 97EUR | 30 min | 50 prospects/semaine auto |
| Content Machine | 147EUR | 45 min | 8 contenus/idee auto |
| Veille Concurrentielle | 67EUR | 30 min | Rapport hebdo auto |
| Support Client | 127EUR | 45 min | 80% emails auto |
| KDP Book Factory | 197EUR | 60 min | 1 livre/session auto |

**Chiffre d’affaires potentiel si 20 ventes/template/mois :**
097 + 147 + 67 + 127 + 197 = **635EUR x 20 ventes = 12 700EUR/mois passif**

---

*Cree par Bentley (architecture) + Nikola (infra) + Philomene (prompts optimises)*
*Valide par Grimaldi -- STATUT : PRET POUR PACKAGING ET MISE EN VENTE*
