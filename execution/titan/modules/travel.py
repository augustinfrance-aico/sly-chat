"""
TITAN Travel Module
City guides, packing lists, travel tips, time zone helper.
"""

import random
import requests

from ..ai_client import chat as ai_chat


class TitanTravel:
    """Explore the world."""

    def __init__(self):
        pass

    def country_info(self, country: str) -> str:
        """Get country information."""
        try:
            resp = requests.get(f"https://restcountries.com/v3.1/name/{country}", timeout=10)
            data = resp.json()[0]

            name = data.get("name", {}).get("common", country)
            capital = data.get("capital", ["?"])[0]
            population = data.get("population", 0)
            region = data.get("region", "?")
            languages = ", ".join(data.get("languages", {}).values())
            currencies = ", ".join(f"{v['name']} ({v['symbol']})" for v in data.get("currencies", {}).values())
            flag = data.get("flag", "")
            timezones = ", ".join(data.get("timezones", [])[:3])

            return (
                f"{flag} {name.upper()}\n"
                f"{'=' * 25}\n\n"
                f"🏛 Capitale: {capital}\n"
                f"👥 Population: {population:,}\n"
                f"🌍 Region: {region}\n"
                f"🗣 Langues: {languages}\n"
                f"💰 Monnaie: {currencies}\n"
                f"🕐 Fuseaux: {timezones}"
            )
        except Exception as e:
            return f"Pays non trouve: {e}"

    async def city_guide(self, city: str) -> str:
        """Generate a mini city guide."""
        return ai_chat("Expert assistant.", f"""Guide rapide de {city}: top 5 a voir, ou manger, transport, budget, et conseil insider.""", 1500)

    def packing_list(self, trip_type: str = "week", weather: str = "tempere") -> str:
        """Generate a packing list."""
        base = [
            "Passeport/CI", "Telephone + chargeur", "Batterie externe",
            "Ecouteurs", "Adaptateur prise", "Medicaments de base",
        ]

        clothes_map = {
            "chaud": ["T-shirts x5", "Shorts x3", "Maillot de bain", "Sandales", "Creme solaire", "Lunettes de soleil", "Chapeau"],
            "froid": ["Pull x3", "Manteau", "Echarpe", "Gants", "Bonnet", "Bottes", "Sous-vetements thermiques"],
            "tempere": ["T-shirts x4", "Pull x2", "Jean x2", "Veste legere", "Baskets", "Parapluie compact"],
        }

        clothes = clothes_map.get(weather.lower(), clothes_map["tempere"])

        lines = [
            f"🧳 PACKING LIST ({trip_type} / {weather})\n",
            "📋 ESSENTIELS",
        ]
        for item in base:
            lines.append(f"  ☐ {item}")

        lines.append("\n👕 VETEMENTS")
        for item in clothes:
            lines.append(f"  ☐ {item}")

        lines.append("\n🧴 TOILETTE")
        for item in ["Brosse a dents", "Dentifrice", "Shampoing mini", "Deodorant"]:
            lines.append(f"  ☐ {item}")

        return "\n".join(lines)

    def random_destination(self) -> str:
        """Suggest a random travel destination."""
        destinations = [
            ("Tokyo", "🇯🇵", "Culture, tech, gastronomie"),
            ("Lisbonne", "🇵🇹", "Soleil, pasteis, azulejos"),
            ("Bali", "🇮🇩", "Plages, temples, surf"),
            ("New York", "🇺🇸", "Urban, culture, food"),
            ("Marrakech", "🇲🇦", "Souks, riads, tajines"),
            ("Reykjavik", "🇮🇸", "Aurores boreales, geysers"),
            ("Bangkok", "🇹🇭", "Street food, temples, nightlife"),
            ("Prague", "🇨🇿", "Architecture, biere, histoire"),
            ("Cape Town", "🇿🇦", "Nature, vin, aventure"),
            ("Kyoto", "🇯🇵", "Temples, jardins zen, tradition"),
        ]
        city, flag, desc = random.choice(destinations)
        return f"✈️ DESTINATION ALEATOIRE\n\n{flag} {city}\n🌟 {desc}\n\nTape /cityguide {city} pour le guide."
