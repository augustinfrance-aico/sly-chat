"""
TITAN Space Module
ISS tracker, astronomy facts, space news.
"""

import requests
from datetime import datetime


class TitanSpace:
    """Explore the cosmos."""

    def iss_location(self) -> str:
        """Get current ISS location."""
        try:
            resp = requests.get("http://api.open-notify.org/iss-now.json", timeout=10)
            data = resp.json()
            pos = data["iss_position"]
            lat = float(pos["latitude"])
            lon = float(pos["longitude"])

            return (
                f"🛸 ISS EN DIRECT\n\n"
                f"Latitude: {lat:.4f}\n"
                f"Longitude: {lon:.4f}\n"
                f"🗺 Maps: https://www.google.com/maps/@{lat},{lon},4z\n\n"
                f"Vitesse: ~28,000 km/h\n"
                f"Altitude: ~408 km"
            )
        except Exception as e:
            return f"ISS indisponible: {e}"

    def people_in_space(self) -> str:
        """Get people currently in space."""
        try:
            resp = requests.get("http://api.open-notify.org/astros.json", timeout=10)
            data = resp.json()
            people = data.get("people", [])

            lines = [f"👨‍🚀 {data.get('number', '?')} PERSONNES DANS L'ESPACE\n"]
            crafts = {}
            for p in people:
                craft = p.get("craft", "?")
                if craft not in crafts:
                    crafts[craft] = []
                crafts[craft].append(p.get("name", "?"))

            for craft, crew in crafts.items():
                lines.append(f"🚀 {craft}:")
                for name in crew:
                    lines.append(f"  • {name}")

            return "\n".join(lines)
        except Exception as e:
            return f"Erreur: {e}"

    def apod(self) -> str:
        """Get NASA Astronomy Picture of the Day (no API key needed for demo)."""
        try:
            resp = requests.get("https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY", timeout=10)
            data = resp.json()
            return (
                f"🌌 PHOTO ASTRONOMIQUE DU JOUR\n\n"
                f"📸 {data.get('title', '?')}\n"
                f"📅 {data.get('date', '?')}\n\n"
                f"{data.get('explanation', '')[:500]}\n\n"
                f"🔗 {data.get('url', '')}"
            )
        except Exception:
            return "Photo du jour indisponible."

    def next_launches(self) -> str:
        """Get upcoming rocket launches."""
        try:
            resp = requests.get("https://fdo.rocketlaunch.live/json/launches/next/5", timeout=10)
            data = resp.json()
            launches = data.get("result", [])

            if not launches:
                return "Pas de lancements a venir."

            lines = ["🚀 PROCHAINS LANCEMENTS\n"]
            for l in launches[:5]:
                name = l.get("name", "?")
                provider = l.get("provider", {}).get("name", "?")
                date = l.get("date_str", "?")
                lines.append(f"  🔹 {name}\n     {provider} | {date}")

            return "\n".join(lines)
        except Exception:
            return "Lancements indisponibles."

    def mars_weather(self) -> str:
        """Get Mars weather (when available)."""
        return (
            f"🔴 METEO MARS\n\n"
            f"Temperature: -60C (moyenne)\n"
            f"Pression: ~600 Pa (1% de la Terre)\n"
            f"Vent: ~30 km/h\n"
            f"Atmosphere: 95% CO2\n\n"
            f"Perseverance explore Jezero Crater."
        )

    def planet_facts(self, planet: str = "mars") -> str:
        """Facts about a planet."""
        planets = {
            "mercure": "☿ Mercure: Plus proche du Soleil. Temp: -180 a 430C. Annee: 88 jours.",
            "venus": "♀ Venus: Planete la plus chaude (465C). Tourne a l'envers. Pression: 90x Terre.",
            "terre": "🌍 Terre: Seule planete avec de l'eau liquide en surface. 8000 km de diametre.",
            "mars": "♂ Mars: La planete rouge. Olympus Mons: plus grand volcan du systeme solaire (21 km).",
            "jupiter": "♃ Jupiter: Plus grande planete. 318x la masse de la Terre. 95 lunes connues.",
            "saturne": "♄ Saturne: Ses anneaux s'etendent sur 282,000 km. Densite < eau.",
            "uranus": "♅ Uranus: Tourne sur le cote (98 degres). -224C. Decouverte en 1781.",
            "neptune": "♆ Neptune: Vents de 2100 km/h. Annee: 165 ans terrestres. Bleu methane.",
        }
        info = planets.get(planet.lower(), f"Planete inconnue. Disponibles: {', '.join(planets.keys())}")
        return f"🪐 PLANETE\n\n{info}"
