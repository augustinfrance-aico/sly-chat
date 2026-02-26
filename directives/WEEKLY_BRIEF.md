# WEEKLY_BRIEF — Bilan Hebdomadaire Automatisé

> Chaque fin de semaine (vendredi ou dimanche), l'agent produit ce bilan sans qu'Augus le demande.
> Format : résultats chiffrés + ce qui a bloqué + plan semaine suivante.
> Langage : zéro jargon, uniquement business.

---

## Quand produire ce bilan

```
Déclencheur automatique :
  - Vendredi soir si KPI semaine atteint
  - Dimanche soir sinon (dernier moment)
  - Sur demande explicite d'Augus ("bilan", "où on en est", "résumé semaine")
```

---

## Template du bilan (à remplir et envoyer à Augus)

```
📊 BILAN SEMAINE — [DATE]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📚 KDP — CARNETS AMAZON
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Carnets publiés cette semaine : X / 10 (objectif)
  ✅ [niche] [langue] — publié le [date]
  ✅ [niche] [langue] — publié le [date]
  🔄 [niche] [langue] — en cours (étape : COVER)
  ❌ [niche] [langue] — bloqué ([raison simple])

Revenus estimés/mois si tout vendu : X€
Prochaine priorité : [niche + langue]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🖼️ STOCK — PHOTOS IA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Images générées cette semaine : X / 250 (objectif)
Images uploadées (toutes plateformes) : X
Taux d'acceptation Shutterstock : X%

Niche la plus productive : [niche] — X images acceptées
Niche la plus rejetée : [niche] — X% rejet ([raison])

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 LEADS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Leads qualifiés générés : X / 50-100 (objectif)
Campagne active : [OUI/NON] — [client]
Taux de réponse si campagne : X%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚡ CE QUI A BLOQUÉ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Si problème : 1 phrase simple, pas de technique]
[Si rien : "Aucun blocage cette semaine."]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📅 PLAN SEMAINE PROCHAINE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Priorité 1 : [action concrète]
Priorité 2 : [action concrète]
Priorité 3 : [action concrète]

Question pour toi : [1 seule question si décision requise — sinon rien]
```

---

## Comment l'agent remplit ce template

### Sources de données
```
Carnets publiés    ← agents/PIPELINE_STATE.md (colonne ✅)
Images générées    ← agents/PIPELINE_STATE.md + .tmp/run_history.json
Blocages           ← directives/ERRORS.md (entrées de la semaine) + run_state.json errors[]
Plan semaine suivante ← agents/PIPELINE_STATE.md (prochaines priorités) + KPI manquants
```

### Calcul du revenu estimé
```
Carnet KDP :
  Prix moyen : 7.99$ (EN) / 6.99€ (FR/DE)
  Royalty 60% : ~4.80$ par vente
  Ventes estimées mois 1 : 5-15 (conservateur)
  Revenu estimé par carnet/mois : 24-72$

Stock photo :
  Shutterstock : 0.25-0.38$ / téléchargement
  250 images × 2 téléchargements/image/mois = 125-190$/mois (hypothèse conservatrice)
```

### Règle de priorité semaine suivante
```
1. Finir les runs interrompus (run_state.json in_progress ou failed)
2. Atteindre le KPI si manqué (ex: 4/10 carnets → priorité KDP la semaine suivante)
3. Nouvelles niches selon ordre dans ROSTER.md
4. Nouveaux clients ou projets signalés par Augus
```

---

## Historique des bilans

| Semaine | KDP | STOCK | Leads | Note |
|---------|-----|-------|-------|------|
| 2026-W08 | 0/10 | 0/250 | 300 prêts | Semaine de setup système |

*Ce tableau se remplit automatiquement après chaque bilan.*
