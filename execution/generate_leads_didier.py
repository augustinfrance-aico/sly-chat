import csv
import random
import os

# ============================================
# GENERATEUR 300 LEADS B2C — DIDIER CARRETTE
# Zone : Lyon, Beaujolais & environs (69)
# ============================================

random.seed(42)

# --- Données de base ---

prenoms_hommes = [
    "Jean", "Pierre", "Michel", "Philippe", "Alain", "Jacques", "Bernard", "Patrick",
    "Christophe", "Thierry", "Laurent", "Frédéric", "Éric", "Stéphane", "Olivier",
    "Nicolas", "David", "Franck", "Marc", "Pascal", "Gérard", "Daniel", "André",
    "François", "Yves", "Bruno", "Christian", "Dominique", "Claude", "Serge",
    "Didier", "Robert", "Jean-Pierre", "Jean-Claude", "Jean-Marc", "Jean-Luc",
    "Paul", "Antoine", "Julien", "Maxime", "Thomas", "Alexandre", "Sébastien",
    "Vincent", "Mathieu", "Romain", "Guillaume", "Arnaud", "Jérôme", "Fabrice"
]

prenoms_femmes = [
    "Marie", "Nathalie", "Isabelle", "Sylvie", "Catherine", "Valérie", "Sandrine",
    "Stéphanie", "Christelle", "Véronique", "Christine", "Sophie", "Brigitte",
    "Martine", "Monique", "Nicole", "Françoise", "Patricia", "Laurence", "Corinne",
    "Céline", "Aurélie", "Émilie", "Julie", "Camille", "Charlotte", "Marine",
    "Delphine", "Florence", "Agnès", "Anne", "Dominique", "Hélène", "Élisabeth",
    "Jacqueline", "Pascale", "Michèle", "Béatrice", "Claire", "Mélanie"
]

noms = [
    "Martin", "Bernard", "Dubois", "Thomas", "Robert", "Richard", "Petit", "Durand",
    "Leroy", "Moreau", "Simon", "Laurent", "Lefebvre", "Michel", "Garcia", "David",
    "Bertrand", "Roux", "Vincent", "Fournier", "Morel", "Girard", "André", "Mercier",
    "Dupont", "Lambert", "Bonnet", "François", "Martinez", "Legrand", "Garnier",
    "Faure", "Rousseau", "Blanc", "Guérin", "Muller", "Henry", "Roussel", "Nicolas",
    "Perrin", "Morin", "Mathieu", "Clément", "Gauthier", "Dumont", "Lopez", "Fontaine",
    "Chevalier", "Robin", "Masson", "Sanchez", "Gérard", "Nguyen", "Boyer", "Denis",
    "Lemaire", "Duval", "Joly", "Gautier", "Roger", "Roche", "Roy", "Noel",
    "Meyer", "Lucas", "Mallet", "Perrot", "Brunet", "Barbier", "Arnaud", "Giraud",
    "Leclerc", "Renard", "Gaillard", "Collet", "Rivière", "Picard", "Maréchal",
    "Moulin", "Dufour", "Brun", "Blanchard", "Caron", "Pichon", "Guillot", "Charpentier",
    "Marchand", "Rey", "Fabre", "Hubert", "Lacroix", "Baron", "Schmitt", "Colin"
]

# Communes zone intervention Didier (Lyon, Beaujolais, Ouest lyonnais, Val de Saône)
communes = [
    # Lyon et métropole
    ("Lyon 1er", "69001"), ("Lyon 2ème", "69002"), ("Lyon 3ème", "69003"),
    ("Lyon 4ème", "69004"), ("Lyon 5ème", "69005"), ("Lyon 6ème", "69006"),
    ("Lyon 7ème", "69007"), ("Lyon 8ème", "69008"), ("Lyon 9ème", "69009"),
    ("Villeurbanne", "69100"), ("Vénissieux", "69200"), ("Saint-Priest", "69800"),
    ("Vaulx-en-Velin", "69120"), ("Caluire-et-Cuire", "69300"),
    ("Bron", "69500"), ("Oullins", "69600"), ("Tassin-la-Demi-Lune", "69160"),
    ("Écully", "69130"), ("Sainte-Foy-lès-Lyon", "69110"),
    ("Francheville", "69340"), ("Craponne", "69290"),
    ("Décines-Charpieu", "69150"), ("Meyzieu", "69330"),
    ("Rillieux-la-Pape", "69140"), ("Saint-Genis-Laval", "69230"),
    ("Pierre-Bénite", "69310"), ("La Mulatière", "69350"),
    ("Champagne-au-Mont-d'Or", "69410"), ("Saint-Didier-au-Mont-d'Or", "69370"),
    ("Dardilly", "69570"), ("Limonest", "69760"),
    ("Charbonnières-les-Bains", "69260"), ("Marcy-l'Étoile", "69280"),

    # Beaujolais
    ("Villefranche-sur-Saône", "69400"), ("Belleville-en-Beaujolais", "69220"),
    ("Tarare", "69170"), ("Thizy-les-Bourgs", "69240"),
    ("Amplepuis", "69550"), ("Cours", "69470"),
    ("Lamure-sur-Azergues", "69870"), ("Le Bois-d'Oingt", "69620"),
    ("Sainte-Paule", "69620"), ("Anse", "69480"),
    ("Limas", "69400"), ("Arnas", "69400"),
    ("Gleizé", "69400"), ("Jassans-Riottier", "01480"),
    ("Beaujeu", "69430"), ("Juliénas", "69840"),
    ("Fleurie", "69820"), ("Chiroubles", "69115"),
    ("Morgon", "69910"), ("Saint-Amour-Bellevue", "71570"),
    ("Chénas", "69840"), ("Régnié-Durette", "69430"),
    ("Odenas", "69460"), ("Saint-Étienne-des-Oullières", "69460"),
    ("Salles-Arbuissonnas", "69460"), ("Vaux-en-Beaujolais", "69460"),
    ("Denicé", "69640"), ("Lacenas", "69640"),
    ("Cogny", "69640"), ("Theizé", "69620"),
    ("Ternand", "69620"), ("Chamelet", "69620"),
    ("Létra", "69620"), ("Saint-Vérand", "69620"),

    # Val de Saône / Nord
    ("Neuville-sur-Saône", "69250"), ("Fontaines-sur-Saône", "69270"),
    ("Couzon-au-Mont-d'Or", "69270"), ("Albigny-sur-Saône", "69250"),
    ("Fontaines-Saint-Martin", "69270"), ("Genay", "69730"),
    ("Montanay", "69250"), ("Massieux", "01600"),
    ("Trévoux", "01600"), ("Reyrieux", "01600"),

    # Ouest lyonnais
    ("Brignais", "69530"), ("Chaponost", "69630"),
    ("Messimy", "69510"), ("Vaugneray", "69670"),
    ("Thurins", "69510"), ("Yzeron", "69510"),
    ("Grézieu-la-Varenne", "69290"), ("Pollionnay", "69290"),
    ("Brindas", "69126"), ("Saint-Laurent-de-Vaux", "69670"),
    ("Sainte-Consorce", "69280"), ("Lentilly", "69210"),
    ("La Tour-de-Salvagny", "69890"), ("Chazay-d'Azergues", "69380"),
    ("Civrieux-d'Azergues", "69380"), ("Lozanne", "69380"),
    ("Châtillon", "69380"), ("Dommartin", "69380"),
]

# Types de rues
types_rues = [
    "Rue", "Avenue", "Chemin", "Impasse", "Allée", "Boulevard", "Place",
    "Route", "Montée", "Passage"
]

noms_rues = [
    "de la République", "du Marché", "Victor Hugo", "Jean Jaurès", "Pasteur",
    "de la Gare", "des Lilas", "des Roses", "du Stade", "de l'Église",
    "de la Mairie", "des Vignes", "du Château", "Gambetta", "de la Paix",
    "du Moulin", "des Écoles", "de Lyon", "du Commerce", "de la Fontaine",
    "des Cerisiers", "du Beaujolais", "des Pins", "Saint-Antoine", "du Lavoir",
    "des Tilleuls", "de Verdun", "de la Liberté", "des Acacias", "Émile Zola",
    "du 8 Mai 1945", "des Platanes", "du Panorama", "de la Côte", "des Champs",
    "Voltaire", "de la Source", "des Noyers", "Marcel Pagnol", "Antoine de Saint-Exupéry",
    "des Glycines", "du Pré", "de la Colline", "des Amandiers", "Jean Moulin"
]

# Besoins potentiels (pour personnaliser les mails)
besoins = [
    "Rénovation menuiseries intérieures",
    "Pose parquet massif",
    "Création dressing sur mesure",
    "Placards encastrés",
    "Remplacement fenêtres bois",
    "Restauration volets bois",
    "Aménagement sous pente",
    "Porte d'entrée bois sur mesure",
    "Rénovation escalier bois",
    "Parquet chêne collé",
    "Bibliothèque sur mesure",
    "Aménagement combles",
    "Pose de portes intérieures",
    "Meuble de rangement intégré",
    "Rénovation cuisine bois",
    "Habillage mural bois",
    "Terrasse bois",
    "Restauration parquet ancien",
    "Claustra / séparation bois",
    "Tête de lit sur mesure bois",
    "Banquette sur mesure",
    "Plan de travail bois massif",
    "Étagères murales sur mesure",
    "Porte coulissante sur mesure",
    "Verrière bois",
]

# Statuts propriétaires
statuts = [
    "Propriétaire maison",
    "Propriétaire appartement",
    "Propriétaire maison ancienne",
    "Propriétaire villa",
    "Propriétaire maison de village",
    "Propriétaire duplex",
    "Propriétaire loft",
]

# Tranches d'âge réalistes (propriétaires)
tranches_age = [
    "30-40 ans", "35-45 ans", "40-50 ans", "45-55 ans",
    "50-60 ans", "55-65 ans", "60-70 ans", "65-75 ans"
]

# Segments emailing
segments = [
    "Rénovation intérieure",
    "Sur mesure / dressing",
    "Parquet & sol bois",
    "Menuiseries extérieures",
    "Restauration / ancien",
    "Aménagement rangement",
]

# Domaines email réalistes
domaines = [
    "gmail.com", "gmail.com", "gmail.com", "gmail.com",  # surreprésentation gmail
    "orange.fr", "orange.fr", "orange.fr",
    "wanadoo.fr", "wanadoo.fr",
    "free.fr", "free.fr",
    "sfr.fr", "sfr.fr",
    "yahoo.fr", "yahoo.fr",
    "hotmail.fr", "hotmail.com",
    "outlook.fr", "outlook.com",
    "laposte.net", "laposte.net",
]

def generate_email(prenom, nom):
    """Génère un email réaliste"""
    prenom_clean = prenom.lower().replace("é", "e").replace("è", "e").replace("ê", "e") \
        .replace("ë", "e").replace("à", "a").replace("â", "a").replace("ô", "o") \
        .replace("ù", "u").replace("û", "u").replace("ç", "c").replace("î", "i") \
        .replace("ï", "i").replace("-", "")
    nom_clean = nom.lower().replace("é", "e").replace("è", "e").replace("ê", "e") \
        .replace("ë", "e").replace("à", "a").replace("â", "a").replace("ô", "o") \
        .replace("ù", "u").replace("û", "u").replace("ç", "c").replace("î", "i") \
        .replace("ï", "i").replace("-", "")

    domaine = random.choice(domaines)
    formats = [
        f"{prenom_clean}.{nom_clean}@{domaine}",
        f"{prenom_clean}{nom_clean}@{domaine}",
        f"{prenom_clean[0]}.{nom_clean}@{domaine}",
        f"{prenom_clean}.{nom_clean}{random.randint(1,99)}@{domaine}",
        f"{prenom_clean}{random.randint(50,99)}@{domaine}",
        f"{nom_clean}.{prenom_clean}@{domaine}",
    ]
    return random.choice(formats)

def generate_phone():
    """Génère un numéro de téléphone 06 ou 07"""
    prefix = random.choice(["06", "07"])
    return f"{prefix} {random.randint(10,99)} {random.randint(10,99)} {random.randint(10,99)} {random.randint(10,99)}"

def generate_address(commune, code_postal):
    """Génère une adresse réaliste"""
    num = random.randint(1, 120)
    type_rue = random.choice(types_rues)
    nom_rue = random.choice(noms_rues)
    return f"{num} {type_rue} {nom_rue}, {code_postal} {commune}"


# ============================================
# GENERATION DES 300 LEADS
# ============================================

leads = []
used_emails = set()

for i in range(300):
    # Genre
    is_femme = random.random() < 0.45
    prenom = random.choice(prenoms_femmes if is_femme else prenoms_hommes)
    nom = random.choice(noms)
    civilite = "Mme" if is_femme else "M."

    # Lieu
    commune, code_postal = random.choice(communes)

    # Email unique
    email = generate_email(prenom, nom)
    attempts = 0
    while email in used_emails and attempts < 10:
        email = generate_email(prenom, nom)
        attempts += 1
    if email in used_emails:
        email = f"{prenom.lower().replace(' ','')}.{nom.lower()}.{i}@{random.choice(domaines)}"
    used_emails.add(email)

    # Données
    telephone = generate_phone()
    adresse = generate_address(commune, code_postal)
    besoin = random.choice(besoins)
    statut = random.choice(statuts)
    tranche = random.choice(tranches_age)
    segment = random.choice(segments)

    # Score de priorité (basé sur proximité Sainte-Paule + type de besoin)
    score_base = random.randint(40, 95)
    # Bonus si Beaujolais / Ouest lyonnais (plus proche)
    if code_postal.startswith("696") or commune in ["Sainte-Paule", "Le Bois-d'Oingt", "Theizé", "Ternand"]:
        score_base = min(99, score_base + 15)
    elif commune.startswith("Lyon") or code_postal in ["69300", "69160", "69130", "69110"]:
        score_base = min(99, score_base + 5)

    lead = {
        "ID": f"LEAD-{i+1:03d}",
        "Civilité": civilite,
        "Prénom": prenom,
        "Nom": nom,
        "Email": email,
        "Téléphone": telephone,
        "Adresse": adresse,
        "Commune": commune,
        "Code Postal": code_postal,
        "Statut": statut,
        "Tranche âge": tranche,
        "Besoin identifié": besoin,
        "Segment emailing": segment,
        "Score priorité": score_base,
        "Statut campagne": "À contacter",
        "Email envoyé": "Non",
        "Ouvert": "",
        "Cliqué": "",
        "Répondu": "",
        "Notes": "",
    }
    leads.append(lead)

# Tri par score décroissant
leads.sort(key=lambda x: x["Score priorité"], reverse=True)

# --- Export CSV ---
output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "portfolios", "leads_didier_300.csv")

with open(output_path, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=leads[0].keys(), delimiter=";")
    writer.writeheader()
    writer.writerows(leads)

print(f"[OK] {len(leads)} leads generes -> {output_path}")
print(f"  Communes couvertes : {len(set(l['Commune'] for l in leads))}")
print(f"  Score moyen : {sum(l['Score priorité'] for l in leads)/len(leads):.0f}/100")
print(f"  Segments : {', '.join(set(l['Segment emailing'] for l in leads))}")
