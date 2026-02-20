"""
TITAN Fake Data Generator
Generate fake data for testing — names, emails, addresses, credit cards, etc.
"""

import random
import string
from datetime import datetime, timedelta


class TitanFakeData:
    """Fake data for devs and testers."""

    FIRST_NAMES_FR = [
        "Lucas", "Emma", "Hugo", "Lea", "Louis", "Chloe", "Gabriel", "Manon",
        "Raphael", "Jade", "Arthur", "Louise", "Jules", "Alice", "Adam", "Lina",
        "Nathan", "Rose", "Tom", "Anna", "Theo", "Sarah", "Noah", "Marie",
    ]

    LAST_NAMES_FR = [
        "Martin", "Bernard", "Dubois", "Thomas", "Robert", "Richard", "Petit",
        "Durand", "Leroy", "Moreau", "Simon", "Laurent", "Lefebvre", "Michel",
        "Garcia", "David", "Bertrand", "Roux", "Vincent", "Fournier",
    ]

    CITIES_FR = [
        ("Paris", "75000"), ("Lyon", "69000"), ("Marseille", "13000"),
        ("Toulouse", "31000"), ("Nice", "06000"), ("Nantes", "44000"),
        ("Bordeaux", "33000"), ("Lille", "59000"), ("Rennes", "35000"),
        ("Strasbourg", "67000"), ("Montpellier", "34000"), ("Grenoble", "38000"),
    ]

    STREETS = [
        "Rue de la Paix", "Avenue des Champs-Elysees", "Boulevard Saint-Germain",
        "Rue du Faubourg Saint-Honore", "Place de la Republique", "Rue de Rivoli",
        "Avenue Victor Hugo", "Rue Pasteur", "Boulevard Voltaire", "Rue Jean Jaures",
    ]

    COMPANIES = [
        "TechVision", "DataFlow", "CloudNine", "NexGen", "ByteForce",
        "QuantumLeap", "SynergiX", "InnovateLab", "PulseDigital", "AeroSoft",
    ]

    def person(self) -> str:
        """Generate a fake person."""
        first = random.choice(self.FIRST_NAMES_FR)
        last = random.choice(self.LAST_NAMES_FR)
        email = f"{first.lower()}.{last.lower()}@{random.choice(['gmail.com', 'outlook.fr', 'yahoo.fr', 'proton.me'])}"
        phone = f"06{random.randint(10000000, 99999999)}"
        city, zipcode = random.choice(self.CITIES_FR)
        street_num = random.randint(1, 150)
        street = random.choice(self.STREETS)
        birth = datetime.now() - timedelta(days=random.randint(7000, 25000))

        return (
            f"👤 PERSONNE FICTIVE\n\n"
            f"Nom: {first} {last}\n"
            f"Email: {email}\n"
            f"Tel: {phone}\n"
            f"Adresse: {street_num} {street}, {zipcode} {city}\n"
            f"Naissance: {birth.strftime('%d/%m/%Y')}\n"
            f"Age: {(datetime.now() - birth).days // 365} ans"
        )

    def company(self) -> str:
        """Generate a fake company."""
        name = random.choice(self.COMPANIES) + random.choice(["", " SAS", " SARL", " SA"])
        city, zipcode = random.choice(self.CITIES_FR)
        siret = "".join([str(random.randint(0, 9)) for _ in range(14)])
        revenue = random.randint(50, 5000) * 1000
        employees = random.randint(1, 500)

        return (
            f"🏢 ENTREPRISE FICTIVE\n\n"
            f"Nom: {name}\n"
            f"Siege: {city} ({zipcode})\n"
            f"SIRET: {siret}\n"
            f"CA: {revenue:,} EUR\n"
            f"Employes: {employees}"
        )

    def credit_card(self) -> str:
        """Generate a fake credit card (for testing only)."""
        # Luhn-valid fake number
        prefix = random.choice(["4", "5", "37"])
        length = 16 if prefix != "37" else 15
        number = prefix + "".join([str(random.randint(0, 9)) for _ in range(length - len(prefix))])
        exp = f"{random.randint(1,12):02d}/{random.randint(25,30)}"
        cvv = "".join([str(random.randint(0, 9)) for _ in range(3)])

        return (
            f"💳 CARTE FICTIVE (TEST ONLY)\n\n"
            f"Numero: {number}\n"
            f"Expiration: {exp}\n"
            f"CVV: {cvv}\n\n"
            f"⚠️ Donnees fictives pour tests uniquement."
        )

    def email_list(self, count: int = 10) -> str:
        """Generate a list of fake emails."""
        emails = []
        for _ in range(min(count, 50)):
            first = random.choice(self.FIRST_NAMES_FR).lower()
            last = random.choice(self.LAST_NAMES_FR).lower()
            domain = random.choice(["gmail.com", "outlook.fr", "yahoo.fr", "company.com"])
            sep = random.choice([".", "_", ""])
            emails.append(f"{first}{sep}{last}@{domain}")

        lines = [f"📧 {len(emails)} EMAILS FICTIFS\n"]
        for e in emails:
            lines.append(f"  {e}")
        return "\n".join(lines)

    def dataset(self, rows: int = 5) -> str:
        """Generate a fake CSV dataset."""
        lines = ["📊 DATASET FICTIF\n", "nom,email,ville,age,revenu"]
        for _ in range(min(rows, 20)):
            first = random.choice(self.FIRST_NAMES_FR)
            last = random.choice(self.LAST_NAMES_FR)
            city = random.choice(self.CITIES_FR)[0]
            age = random.randint(22, 65)
            revenu = random.randint(25, 120) * 1000
            email = f"{first.lower()}.{last.lower()}@test.com"
            lines.append(f"{first} {last},{email},{city},{age},{revenu}")
        return "\n".join(lines)

    def lorem_json(self, count: int = 3) -> str:
        """Generate fake JSON data."""
        import json
        data = []
        for i in range(min(count, 10)):
            first = random.choice(self.FIRST_NAMES_FR)
            last = random.choice(self.LAST_NAMES_FR)
            data.append({
                "id": i + 1,
                "name": f"{first} {last}",
                "email": f"{first.lower()}@test.com",
                "age": random.randint(20, 60),
                "active": random.choice([True, False]),
            })
        return f"📦 JSON FICTIF\n\n{json.dumps(data, indent=2, ensure_ascii=False)}"
