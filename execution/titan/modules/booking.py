"""
TITAN Booking Module
Reserve sports sessions, gym, padel, badminton via Anybuddy and others.
"""

from urllib.parse import quote
from datetime import datetime, timedelta


class TitanBooking:
    """Réserve tes sessions de sport comme un pro."""

    # Popular cities with Anybuddy
    ANYBUDDY_CITIES = {
        "paris": "paris",
        "lyon": "lyon",
        "marseille": "marseille",
        "bordeaux": "bordeaux",
        "toulouse": "toulouse",
        "nantes": "nantes",
        "lille": "lille",
        "strasbourg": "strasbourg",
        "montpellier": "montpellier",
        "nice": "nice",
    }

    SPORTS = {
        "badminton": "badminton",
        "padel": "padel",
        "tennis": "tennis",
        "squash": "squash",
        "foot5": "football-5",
        "foot": "football-5",
        "basket": "basketball",
        "escalade": "climbing",
        "ping-pong": "table-tennis",
        "yoga": "yoga",
        "crossfit": "crossfit",
        "natation": "swimming",
        "muscu": "fitness",
        "boxe": "boxing",
    }

    def anybuddy(self, sport: str = "badminton", city: str = "paris") -> str:
        """Book a sport session on Anybuddy."""
        city_key = city.lower().strip()
        sport_key = sport.lower().strip()

        # Anybuddy deep link
        anybuddy_city = self.ANYBUDDY_CITIES.get(city_key, city_key)
        anybuddy_sport = self.SPORTS.get(sport_key, sport_key)

        # Build URLs
        anybuddy_url = f"https://www.anybuddy.com/fr/{anybuddy_city}/{anybuddy_sport}"

        # Alternative dates
        today = datetime.now()
        dates = []
        for i in range(7):
            d = today + timedelta(days=i)
            dates.append(d.strftime("%A %d/%m"))

        lines = [f"🏸 RÉSERVER {sport.upper()} — {city.upper()}\n"]
        lines.append(f"📱 Anybuddy: {anybuddy_url}")
        lines.append(f"   (Télécharge l'app Anybuddy pour réserver direct)\n")

        # Créneaux suggérés
        lines.append("📅 PROCHAINS CRÉNEAUX DISPO:")
        for d in dates[:5]:
            lines.append(f"  • {d} — 12h, 18h, 19h, 20h")

        lines.append(f"\n💡 ASTUCES:")
        lines.append(f"  • Réserve 2-3 jours avant pour les meilleurs créneaux")
        lines.append(f"  • Les créneaux de midi sont souvent moins chers")
        lines.append(f"  • L'app Anybuddy envoie des notifs pour les créneaux last-minute à -50%")

        return "\n".join(lines)

    def padel(self, city: str = "paris") -> str:
        """Book padel specifically."""
        return self._sport_booking("padel", city, [
            ("Anybuddy", f"https://www.anybuddy.com/fr/{city.lower()}/padel"),
            ("Padel Reference", f"https://www.padelreference.com/reserver-padel-{city.lower()}"),
            ("Ten'Up", "https://tenup.fft.fr/"),
        ])

    def tennis(self, city: str = "paris") -> str:
        """Book tennis."""
        return self._sport_booking("tennis", city, [
            ("Anybuddy", f"https://www.anybuddy.com/fr/{city.lower()}/tennis"),
            ("Ten'Up (FFT)", "https://tenup.fft.fr/"),
            ("Paris Tennis", "https://tennis.paris.fr/tennis/"),
        ])

    def foot5(self, city: str = "paris") -> str:
        """Book 5-a-side football."""
        return self._sport_booking("foot 5", city, [
            ("Anybuddy", f"https://www.anybuddy.com/fr/{city.lower()}/football-5"),
            ("Le Five", "https://www.lefive.fr/"),
            ("UrbanSoccer", "https://www.urbansoccer.fr/"),
        ])

    def escalade(self, city: str = "paris") -> str:
        """Book climbing."""
        return self._sport_booking("escalade", city, [
            ("Anybuddy", f"https://www.anybuddy.com/fr/{city.lower()}/climbing"),
            ("Climb Up", "https://www.climbup.fr/"),
            ("Arkose", "https://arkose.com/"),
            ("MurMur", "https://murmur.fr/"),
        ])

    def gym(self, city: str = "paris") -> str:
        """Find gym deals."""
        lines = [f"💪 SALLES DE SPORT — {city.upper()}\n"]

        gyms = [
            ("Basic-Fit", "https://www.basic-fit.com/fr-fr/salle-de-sport/", "19.99€/mois — le moins cher"),
            ("Fitness Park", "https://www.fitnesspark.fr/", "29.99€/mois — bon rapport qualité/prix"),
            ("Neoness", "https://www.neoness.fr/", "15-25€/mois — Paris surtout"),
            ("ClassPass", "https://classpass.com/", "Multi-salles, multi-sports, crédits"),
            ("Gymlib", "https://www.gymlib.com/", "Accès à 4000+ salles avec 1 abonnement"),
        ]

        for name, url, desc in gyms:
            lines.append(f"  🏋️ {name} — {desc}")
            lines.append(f"     {url}")

        lines.append(f"\n💡 Gymlib et ClassPass sont géniaux pour tester plein de salles différentes.")
        return "\n".join(lines)

    def sports_list(self) -> str:
        """List all bookable sports."""
        lines = ["🏆 SPORTS RÉSERVABLES\n"]
        lines.append("Via Anybuddy + autres plateformes:\n")

        sports_info = [
            ("🏸 Badminton", "/bookbad [ville]"),
            ("🎾 Padel", "/bookpadel [ville]"),
            ("🎾 Tennis", "/booktennis [ville]"),
            ("⚽ Foot 5", "/bookfoot [ville]"),
            ("🧗 Escalade", "/bookescalade [ville]"),
            ("🏋️ Salle de sport", "/bookgym [ville]"),
            ("🏐 Squash", "/bookany squash [ville]"),
            ("🏓 Ping-pong", "/bookany ping-pong [ville]"),
            ("🥊 Boxe", "/bookany boxe [ville]"),
            ("🧘 Yoga", "/bookany yoga [ville]"),
        ]

        for sport, cmd in sports_info:
            lines.append(f"  {sport} → {cmd}")

        lines.append(f"\n📱 Télécharge Anybuddy: https://www.anybuddy.com/fr")
        return "\n".join(lines)

    def _sport_booking(self, sport: str, city: str, platforms: list) -> str:
        """Generic sport booking template."""
        today = datetime.now()

        lines = [f"🏆 RÉSERVER {sport.upper()} — {city.upper()}\n"]

        lines.append("📱 PLATEFORMES:\n")
        for name, url in platforms:
            lines.append(f"  🔗 {name}: {url}")

        lines.append(f"\n📅 CETTE SEMAINE:")
        for i in range(7):
            d = today + timedelta(days=i)
            day_name = d.strftime("%A %d/%m")
            lines.append(f"  • {day_name}")

        lines.append(f"\n💡 Réserve sur Anybuddy pour comparer les prix de tous les centres.")
        return "\n".join(lines)
