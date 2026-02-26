# DIRECTIVE — R&D Lab AI

> Systeme de veille recherche IA automatise. 5 agents specialises. Zero cout.

---

## Vue d'ensemble

Le R&D Lab est compose de 5 agents dans le Pole R (RECON) :

| Agent | Role | Scheduling |
|-------|------|-----------|
| **ARXIV** | Veille papers (arXiv, Semantic Scholar, HuggingFace, GitHub) | Digest quotidien 7h30 |
| **SCOUT** | Detection innovations (startups, brevets, frameworks) | Alertes midi (si EXPLOSIVE) |
| **LABRAT** | Prototypage experimental (paper → code) | On-demand |
| **HORIZON** | Vision strategique 3-5 ans | Forecast mensuel (1er du mois) |
| **DOCTORANT** | Interface unifiee, hypotheses, dashboard | Hub permanent |

---

## Architecture

```
ARXIV ──┐
SCOUT ──┤
LABRAT ─┼──→ DOCTORANT ──→ Dashboard + Telegram
HORIZON ┘                   (/rdlab)
```

### Flux de donnees
1. ARXIV et SCOUT fetchent les sources (APIs gratuites)
2. Donnees stockees dans `execution/titan/memory/rdlab_*.json`
3. DOCTORANT agrege et sert via `/api/rdlab`
4. Dashboard dans tab "R&D Lab" de TITAN-COMMAND
5. LABRAT genere prototypes dans `experiments/`

---

## Commandes Telegram

| Commande | Action |
|----------|--------|
| `/rdlab` | Dashboard resume |
| `/rdlab papers` | Top 5 papers du jour |
| `/rdlab papers weekly` | Rapport hebdo |
| `/rdlab papers search <q>` | Recherche papers |
| `/rdlab scout` | Rapport innovations |
| `/rdlab scout alerts` | Alertes actives |
| `/rdlab scout stack` | Comparaison stack AICO |
| `/rdlab scout patents` | Brevets recents |
| `/rdlab experiment list` | Liste experiences |
| `/rdlab experiment proto <id>` | Click-to-prototype |
| `/rdlab horizon` | Dernier forecast |
| `/rdlab horizon obsolete` | Check obsolescence |
| `/rdlab hypothesis <question>` | Test d'hypothese |
| `/rdlab search <query>` | Recherche cross-sources |
| `/rdlab weekly` | Resume hebdo |

---

## APIs (zero cout)

| Source | API | Limite |
|--------|-----|--------|
| arXiv | `export.arxiv.org/api/query` | 1 req/3s |
| Semantic Scholar | `api.semanticscholar.org` | 5000/5min |
| GitHub | `api.github.com/search` | 60/h |
| HuggingFace | `huggingface.co/api/daily_papers` | Illimite |
| PatentsView | `api.patentsview.org` | Illimite |
| HackerNews | Firebase API | Illimite |
| RSS feeds | feedparser | Illimite |

---

## Fichiers

### Modules
- `execution/titan/modules/rdlab_digestor.py`
- `execution/titan/modules/rdlab_scout.py`
- `execution/titan/modules/rdlab_experiment.py`
- `execution/titan/modules/rdlab_horizon.py`
- `execution/titan/modules/rdlab_doctorant.py`

### Memoire
- `execution/titan/memory/rdlab_papers.json`
- `execution/titan/memory/rdlab_innovations.json`
- `execution/titan/memory/rdlab_experiments.json`
- `execution/titan/memory/rdlab_horizon.json`
- `execution/titan/memory/rdlab_dashboard.json`

### Personnalites
- `personnalites/arxiv.md`
- `personnalites/scout.md`
- `personnalites/labrat.md`
- `personnalites/horizon.md`
- `personnalites/doctorant.md`

---

## Click-to-Prototype (LABRAT)

1. ARXIV trouve un paper (score > 7/10)
2. `/rdlab experiment proto <paper_id>`
3. LABRAT genere spec + code Python (<100 lignes)
4. Sauve dans `experiments/{id}_prototype.py`
5. **PAS d'auto-execution** — Augus review et lance manuellement
6. Status : `proposed → generated → tested → adopted / rejected`

---

## Integration

- **Scheduler** : 3 taches auto (digest 7h30, alertes 12h, forecast mensuel)
- **Brain cameos** : categorie "rdlab" dans CAMEO_TRIGGERS
- **TITAN-COMMAND** : tab "R&D Lab" avec 5 sections
- **API** : `/api/rdlab/*` endpoints dans command_server.py
- **Tri-Pole** : agents en Pole R (RECON), LABRAT flottant R↔F
