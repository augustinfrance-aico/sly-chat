"""
TITAN Deals Module
Find cheap flights, hotel deals, travel bargains.
Uses Skyscanner redirect links + Google Flights + free APIs.
"""

import requests
from datetime import datetime, timedelta
from urllib.parse import quote

from ..ai_client import chat as ai_chat


class TitanDeals:
    """Trouve les bons plans pour voyager sans se ruiner."""

    def __init__(self):
        pass

    def cheap_flights(self, origin: str = "PAR", destination: str = "", budget: str = "300") -> str:
        """Find cheap flights using Google Flights redirect + Skyscanner."""
        today = datetime.now()
        dates_depart = [(today + timedelta(days=i)).strftime("%Y-%m-%d") for i in [14, 21, 30, 45, 60]]

        lines = ["VOLS PAS CHERS\n"]
        lines.append(f"De: {origin.upper()} | Budget: {budget}E")

        if destination:
            lines.append(f"Vers: {destination.upper()}\n")
        else:
            lines.append("Vers: Partout (explore)\n")

        dest_part = f"/{destination.upper()}" if destination else ""
        gf_link = f"https://www.google.com/travel/flights?q=flights+from+{origin.upper()}+to+{destination.upper() if destination else 'anywhere'}+under+{budget}+euros"
        lines.append(f"Google Flights: {gf_link}")

        dest_sky = destination.lower() if destination else "anywhere"
        sky_link = f"https://www.skyscanner.fr/transport/vols/{origin.lower()}/{dest_sky}/"
        lines.append(f"Skyscanner: {sky_link}")

        kayak_link = f"https://www.kayak.fr/explore/{origin.upper()}"
        lines.append(f"Kayak Explore: {kayak_link}")

        kiwi_link = f"https://www.kiwi.com/fr/search/tiles/{origin.lower()}/anywhere/"
        lines.append(f"Kiwi.com: {kiwi_link}")

        lines.append(f"\nASTUCES TITAN:")
        lines.append(f"  * Mardi et mercredi = vols les moins chers")
        lines.append(f"  * Reserve 6-8 semaines a l'avance")
        lines.append(f"  * Active les alertes prix sur Skyscanner")
        lines.append(f"  * Aeroports secondaires = -30% en moyenne")

        return "\n".join(lines)

    def weekend_deals(self) -> str:
        """Find weekend getaway deals."""
        today = datetime.now()
        days_until_friday = (4 - today.weekday()) % 7
        if days_until_friday == 0:
            days_until_friday = 7
        friday = today + timedelta(days=days_until_friday)
        sunday = friday + timedelta(days=2)

        destinations = [
            {"city": "Barcelone", "code": "BCN", "price_range": "50-120E"},
            {"city": "Lisbonne", "code": "LIS", "price_range": "60-150E"},
            {"city": "Rome", "code": "FCO", "price_range": "40-110E"},
            {"city": "Amsterdam", "code": "AMS", "price_range": "50-130E"},
            {"city": "Berlin", "code": "BER", "price_range": "40-100E"},
            {"city": "Londres", "code": "LON", "price_range": "30-90E"},
            {"city": "Prague", "code": "PRG", "price_range": "35-95E"},
            {"city": "Marrakech", "code": "RAK", "price_range": "60-140E"},
            {"city": "Dublin", "code": "DUB", "price_range": "45-120E"},
            {"city": "Athenes", "code": "ATH", "price_range": "70-160E"},
        ]

        lines = [f"WEEKEND DEALS ({friday.strftime('%d/%m')} -> {sunday.strftime('%d/%m')})\n"]
        for d in destinations:
            sky_url = f"https://www.skyscanner.fr/transport/vols/pari/{d['code'].lower()}/{friday.strftime('%y%m%d')}/{sunday.strftime('%y%m%d')}/"
            lines.append(f"  {d['city']} -- {d['price_range']}")
            lines.append(f"     {sky_url}")

        lines.append(f"\nLes prix varient. Clique pour voir le prix reel du moment.")
        return "\n".join(lines)

    def hotel_deals(self, city: str, checkin: str = "", nights: str = "2") -> str:
        """Find hotel deals."""
        if not checkin:
            checkin = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")

        checkout_date = datetime.strptime(checkin, "%Y-%m-%d") + timedelta(days=int(nights))
        checkout = checkout_date.strftime("%Y-%m-%d")

        city_encoded = quote(city)

        lines = [f"HOTELS PAS CHERS -- {city.upper()}\n"]
        lines.append(f"Dates: {checkin} -> {checkout} ({nights} nuits)\n")

        booking_url = f"https://www.booking.com/searchresults.html?ss={city_encoded}&checkin={checkin}&checkout={checkout}&order=price"
        lines.append(f"Booking.com (par prix): {booking_url}")

        hw_url = f"https://www.hostelworld.com/st/hostels/{city_encoded}/"
        lines.append(f"Hostelworld: {hw_url}")

        airbnb_url = f"https://www.airbnb.fr/s/{city_encoded}/homes?checkin={checkin}&checkout={checkout}&price_max=80"
        lines.append(f"Airbnb (<80E/nuit): {airbnb_url}")

        gh_url = f"https://www.google.com/travel/hotels/{city_encoded}?q={city_encoded}+hotels&dates={checkin},{checkout}"
        lines.append(f"Google Hotels: {gh_url}")

        lines.append(f"\nCompare TOUJOURS les 4 plateformes.")
        return "\n".join(lines)

    def error_fares(self) -> str:
        """Find error fares and mistake deals."""
        lines = ["OU TROUVER LES ERREURS TARIFAIRES\n"]
        lines.append("Les compagnies se trompent parfois sur les prix. Voici ou guetter:\n")

        sites = [
            ("Secret Flying", "https://www.secretflying.com/posts/paris/", "Le meilleur pour les erreurs"),
            ("FlyDealFare", "https://www.flydealfare.com/", "Deals + erreurs US/EU"),
            ("The Flight Deal", "https://www.theflightdeal.com/", "Classique, verifie"),
            ("Fly4Free", "https://www.fly4free.com/", "Europe-focused"),
            ("Scott's Cheap Flights", "https://scottscheapflights.com/", "Newsletter premium top"),
            ("Jack's Flight Club", "https://jacksflightclub.com/", "Version UK/EU excellente"),
        ]

        for name, url, desc in sites:
            lines.append(f"  {name}")
            lines.append(f"     {desc}")
            lines.append(f"     {url}")

        lines.append(f"\nRegle d'or: reserve IMMEDIATEMENT. Les erreurs durent 2-6h max.")
        return "\n".join(lines)

    async def travel_advisor(self, request: str) -> str:
        """AI travel advisor for finding best deals."""
        return ai_chat("Expert assistant.", f"""En tant qu'expert voyage et bons plans, aide avec cette demande: "{request}" """, 1500)
