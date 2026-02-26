# AGENT PUBLISHER — Formatage PDF + Publication KDP

## Mission
Formater les contenus en PDF print-ready, uploader sur KDP, optimiser les métadonnées et mots-clés pour le ranking Amazon.

## Stack
- **Formatage** : Python (reportlab / fpdf2) ou Pandoc
- **Upload** : Interface KDP manuelle (API KDP non publique)
- **Métadonnées** : Claude génère les descriptions optimisées
- **Coût** : 0€

## Spécifications PDF intérieur KDP

```
Taille page : 6" × 9" (15.24cm × 22.86cm)
Marges :
  - Intérieure (gutter) : 0.75" si < 300 pages
  - Extérieure : 0.5"
  - Haut/Bas : 0.75"
Police corps : 11-12pt, lisible
Police titres : 14-16pt
Interligne : 1.15-1.5
Format : PDF/X-1a ou PDF standard
Noir et blanc = moins cher à imprimer = prix vente plus bas = plus de ventes
```

## Script Python — Générateur PDF

```python
# publisher.py — Génération PDF carnet KDP
from fpdf import FPDF

class KDPPublisher:
    def __init__(self, title, subtitle, pages=120, lang="en"):
        self.title = title
        self.subtitle = subtitle
        self.pages = pages
        self.lang = lang
        self.pdf = FPDF(unit="in", format=(6, 9))

    def add_cover_page(self):
        self.pdf.add_page()
        self.pdf.set_font("Helvetica", "B", 24)
        self.pdf.cell(0, 1, self.title, align="C")

    def add_log_page(self, day_number, columns):
        """Ajoute une page de log quotidien avec tableau."""
        self.pdf.add_page()
        self.pdf.set_font("Helvetica", "B", 10)
        self.pdf.cell(0, 0.3, f"Day {day_number}", ln=True)
        # Tableau colonnes
        col_width = 5.5 / len(columns)
        for col in columns:
            self.pdf.cell(col_width, 0.25, col, border=1, align="C")
        self.pdf.ln()
        # Lignes vides
        for _ in range(15):
            for _ in columns:
                self.pdf.cell(col_width, 0.3, "", border=1)
            self.pdf.ln()

    def export(self, filename):
        self.pdf.output(filename)
        print(f"PDF généré : {filename}")
```

## Métadonnées KDP — Template par niche

### Carnet glycémie (exemple)
```
TITRE : Blood Sugar Log Book | Daily Glucose Tracker
SOUS-TITRE : 120-Day Diabetes Management Journal with Meal & Medication Notes
DESCRIPTION :
Track your blood sugar levels efficiently with this comprehensive daily log book.
Designed for people with Type 1 and Type 2 diabetes, pre-diabetes, and anyone
monitoring their glucose levels.

✓ 120 days of daily tracking
✓ Morning, afternoon, evening and bedtime readings
✓ Meal and carb intake notes
✓ Medication dosage tracking
✓ Weekly summary pages
✓ A1C progress notes

Perfect size (6"x9") fits in any bag. Simple, clean layout designed by healthcare professionals.

CATÉGORIES :
1. Books > Health, Fitness & Dieting > Diseases & Physical Ailments > Diabetes
2. Books > Self-Help > Personal Transformation

MOTS-CLÉS (7 max) :
blood sugar log book, glucose tracker journal, diabetes management notebook,
diabetic diary, blood glucose monitoring log, sugar level tracker, diabetes journal
```

## Checklist publication KDP

- [ ] PDF intérieur vérifié (pas d'erreurs, marges ok)
- [ ] Cover PDF en haute résolution
- [ ] Titre < 200 caractères
- [ ] Sous-titre < 200 caractères
- [ ] Description 150-4000 caractères avec bullet points
- [ ] 7 mots-clés optimisés (longue traîne)
- [ ] 2 catégories choisies (les plus spécifiques possible)
- [ ] Prix : 6.99-12.99$ (selon nb pages)
- [ ] Prix paperback vérifié (royalty > 0€)
- [ ] Territories : All territories

## Calcul prix / royalties

```
Royalty paperback = Prix × 60% - Coût impression
Coût impression = 0.85$ + (0.012$ × nb_pages) [noir/blanc US]

Exemple carnet 120 pages à 8.99$ :
= 8.99 × 60% - (0.85 + 0.012 × 120)
= 5.394 - (0.85 + 1.44)
= 5.394 - 2.29
= 3.10$ de royalty par vente
```

## Délais KDP
- Review : 24-72h
- Publication : après approbation
- Changements : 24-72h pour prise en compte
