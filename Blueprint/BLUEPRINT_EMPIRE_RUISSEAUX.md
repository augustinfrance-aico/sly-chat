# BLUEPRINT — L'EMPIRE DES PETITS RUISSEAUX
*Par Augus × OMEGA — Business Plan Semaine Pro*

---

## VISION EN UNE LIGNE

Deux machines à cash passives (KDP + Stock Media) lancées cette semaine. Coût total : 0€. Revenus cibles : 500€/mois en 30 jours, 3 000€/mois en 90 jours.

---

## FLUX 1 — KDP (Kindle Direct Publishing)

### Principe
Créer des carnets/journaux sur Amazon KDP. L'IA génère le contenu. Amazon imprime à la demande. Marge nette : 30-70% par vente. Zéro stock, zéro logistique, zéro intervention après publication.

### Niches prioritaires (ordre d'attaque)

| Priorité | Produit | Audience | Prix cible | Potentiel/mois |
|----------|---------|----------|------------|----------------|
| 1 | Carnet suivi glycémie | 537M diabétiques | 8-12€ | 200-500€ |
| 2 | Carnet tension artérielle | 1.3B hypertendus | 8-12€ | 150-400€ |
| 3 | Journal intolérance alimentaire (FODMAP/gluten) | 15-20% population | 10-15€ | 100-300€ |
| 4 | Planificateur TDAH | En explosion | 12-18€ | 100-250€ |
| 5 | Journal sobriété (alcool/addiction) | Sous-servi | 10-15€ | 80-200€ |
| 6 | Carnet suivi grossesse | Achat émotionnel | 12-20€ | 100-200€ |

### Multiplicateur x6
Chaque carnet traduit en : FR / EN / ES / DE / PT / JA = 6 produits distincts = 6 flux indépendants.
**1 carnet créé = 6 ASINs sur Amazon.**

### Stack technique (coût : 0€)
- **Contenu** : Claude Max (déjà payé) génère les pages intérieures
- **Mise en page** : Canva gratuit ou Google Docs → export PDF
- **Cover** : Canva gratuit ou Midjourney (si dispo)
- **Publication** : kdp.amazon.com (gratuit)
- **Keyword research** : Publisher Rocket (à tester) ou Google Keyword Planner (gratuit)

### Plan d'exécution semaine pro

**Lundi** :
- [ ] Créer compte KDP (si pas fait)
- [ ] Générer contenu carnet glycémie EN (Claude) — 50 pages intérieures
- [ ] Design cover Canva (template simple, médical, propre)
- [ ] Publier sur KDP Amazon US

**Mardi** :
- [ ] Traduire carnet glycémie EN → FR, ES, DE (Claude)
- [ ] Publier 3 versions supplémentaires
- [ ] Commencer carnet tension artérielle

**Mercredi** :
- [ ] Publier carnet tension (EN + FR minimum)
- [ ] Commencer carnet FODMAP/intolérance
- [ ] Optimiser les descriptions avec mots-clés (Claude génère)

**Jeudi** :
- [ ] 2 nouveaux carnets publiés
- [ ] Keyword research : vérifier les termes qui rankent
- [ ] A+ Content sur les premiers carnets

**Vendredi** :
- [ ] Bilan : combien de carnets publiés, premières vues
- [ ] Identifier le carnet le plus prometteur → le dupliquer x3 niches similaires
- [ ] Setup alertes KDP dans TITAN

### Objectifs KDP
- Fin semaine 1 : 8-12 carnets publiés (2-3 niches × 3-4 langues)
- Fin mois 1 : 30+ carnets, premières ventes
- Fin mois 3 : 100+ carnets, 500-1500€/mois passif

---

## FLUX 2 — STOCK MEDIA (Photos IA)

### Principe
Générer des photos IA dans des niches sous-servies → uploader sur Shutterstock, Adobe Stock, Getty, Alamy. Chaque download = 0.25€ à 2€. Volume = revenus passifs.

### Niches prioritaires (trous noirs du marché)

| Niche | Pourquoi c'est vide | Plateformes demandeuses |
|-------|--------------------|-----------------------|
| Business professionals noirs/africains | 95% du stock est caucasien | Corporate, presse, pubs |
| Seniors utilisant la tech (naturels) | Photos actuelles quasi inexistantes | Silver economy, santé |
| Familles musulmanes en contexte premium | Quasi rien de qualitatif | 1.8B musulmans, pubs |
| Handicap en contexte professionnel positif | Demande ESG/RSE explose | Réglementaire, corporate |
| Coworking Afrique/Asie | Stock = bureaux occidentaux | Startups locales, médias |
| Agriculture moderne / permaculture | Entre cliché ferme et labo | Médias, éducation |
| Personnes non-binaires en milieu pro | Demande explose, offre = 0 | Pubs inclusives |
| Cuisine Asie du Sud-Est plating pro | Tout est amateur | Food blogs, restaurants |

### Stack technique (coût : 0€ ou quasi)
- **Génération** : Midjourney (si dispo) / DALL-E / Stable Diffusion (gratuit local)
- **Upscaling** : Topaz Gigapixel (ou équivalent gratuit)
- **Upload en masse** : scripts Python (TITAN peut faire ça)
- **Plateformes** : Shutterstock Contributor + Adobe Stock + Alamy (tous gratuits à l'entrée)

### Plan d'exécution semaine pro

**Lundi** :
- [ ] Créer comptes contributeur : Shutterstock + Adobe Stock
- [ ] Générer batch 50 images niche "Business professionals africains"
- [ ] Uploader premier batch avec métadonnées optimisées

**Mardi** :
- [ ] Générer 50 images niche "Seniors tech"
- [ ] Uploader batch 2
- [ ] Créer prompt template pour chaque niche (réutilisable)

**Mercredi** :
- [ ] Générer 50 images niche "Familles musulmanes"
- [ ] Vérifier review/approbation premiers uploads
- [ ] Ajuster style si refus

**Jeudi** :
- [ ] Niche "Handicap professionnel positif" — 50 images
- [ ] Créer script Python d'upload automatique (semi-auto)

**Vendredi** :
- [ ] Bilan : combien approuvées, premières stats
- [ ] Identifier la niche qui performe → doubler la production
- [ ] Setup monitoring dans TITAN

### Objectifs Stock Media
- Fin semaine 1 : 200+ images uploadées sur 2 plateformes
- Fin mois 1 : 500+ images, premières ventes
- Fin mois 3 : 2000+ images, 200-800€/mois passif

---

## ARCHITECTURE OMEGA — Les 2 Flux en Parallèle

```
SEMAINE PRO
├── MATIN (2h) → KDP : créer + publier 2 carnets/jour
└── APRÈS-MIDI (2h) → Stock Media : générer + uploader 50 images/jour

TOTAL : 4h/jour pendant 5 jours
RÉSULTAT : 10 carnets KDP + 250 images stock = 2 flux actifs
```

---

## RÈGLES OMEGA APPLIQUÉES

- **Coût** : 0€ (Claude Max déjà payé, KDP gratuit, plateformes stock gratuites)
- **Intervention** : 0 après publication — Amazon vend, Shutterstock distribue
- **Duplication** : 1 carnet → 6 langues en 30 min. 1 prompt → 50 images en 1h
- **Premier euro** : KDP possible sous 7 jours. Stock sous 2-3 semaines
- **Indépendance** : Si Amazon change ses règles → Stock continue. Si Shutterstock réduit les royalties → KDP continue

---

## TITAN INTÉGRATION (Semaine 2)

Une fois les flux lancés, TITAN automatise le monitoring :
- `/kdp` — stats ventes du jour
- `/stock` — nouveaux downloads, revenus
- Alerte si un carnet passe en top 100 BSR → dupliquer immédiatement
- Rapport hebdo automatique : revenus KDP + Stock Media

---

## MÉTRIQUES DE SUCCÈS

| Métrique | Semaine 1 | Mois 1 | Mois 3 |
|----------|-----------|--------|--------|
| Carnets KDP publiés | 10+ | 30+ | 100+ |
| Images stock uploadées | 200+ | 500+ | 2000+ |
| Revenus KDP | 0-20€ | 50-200€ | 500-1500€ |
| Revenus Stock | 0€ | 20-100€ | 200-800€ |
| **TOTAL** | **0-20€** | **70-300€** | **700-2300€** |

---

## DÉCISION OMEGA

> Ces 2 flux respectent toutes les contraintes : coût nul, zéro intervention, duplicables, premier euro < 7 jours, indépendants l'un de l'autre.
>
> **Lundi matin → on lance les deux en parallèle. Pas de réflexion supplémentaire.**

*"Un ruisseau s'assèche ? On s'en fout. Il y en a 99 autres."*
