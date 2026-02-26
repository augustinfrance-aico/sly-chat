"""
TITAN Toolbox
Swiss army knife — calculators, converters, generators, random utils.
"""

import json
import math
import random
import string
import hashlib
from datetime import datetime, timedelta
from typing import Optional

import requests


class TitanToolbox:
    """Titan's utility belt."""

    # === CALCULATORS ===

    def calculate(self, expression: str) -> str:
        """Safe math calculator using AST — no eval()."""
        import ast
        import operator

        allowed = set("0123456789+-*/().% ")
        if not all(c in allowed for c in expression):
            return "Expression invalide. Utilise uniquement des chiffres et +-*/()."

        ops = {
            ast.Add: operator.add, ast.Sub: operator.sub,
            ast.Mult: operator.mul, ast.Div: operator.truediv,
            ast.Mod: operator.mod, ast.Pow: operator.pow,
            ast.USub: operator.neg, ast.UAdd: operator.pos,
        }

        def _eval(node):
            if isinstance(node, ast.Expression):
                return _eval(node.body)
            elif isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
                return node.value
            elif isinstance(node, ast.BinOp) and type(node.op) in ops:
                return ops[type(node.op)](_eval(node.left), _eval(node.right))
            elif isinstance(node, ast.UnaryOp) and type(node.op) in ops:
                return ops[type(node.op)](_eval(node.operand))
            else:
                raise ValueError("Expression non supportée")

        try:
            tree = ast.parse(expression, mode="eval")
            result = _eval(tree)
            return f"= {result}"
        except Exception as e:
            return f"Erreur: {e}"

    def percentage(self, value: float, total: float) -> str:
        """Calculate percentage."""
        if total == 0:
            return "Division par zero."
        pct = (value / total) * 100
        return f"{value} / {total} = {pct:.1f}%"

    def margin(self, cost: float, price: float) -> str:
        """Calculate profit margin."""
        if price == 0:
            return "Prix ne peut pas etre zero."
        margin_pct = ((price - cost) / price) * 100
        profit = price - cost
        return f"Cout: {cost} | Prix: {price} | Profit: {profit:.2f} | Marge: {margin_pct:.1f}%"

    def freelance_rate(self, annual_target: float, hours_per_week: int = 30, weeks: int = 46) -> str:
        """Calculate freelance hourly rate."""
        total_hours = hours_per_week * weeks
        hourly = annual_target / total_hours
        daily = hourly * 8
        monthly = annual_target / 12

        return (
            f"💰 TARIF FREELANCE\n"
            f"Objectif annuel: {annual_target:,.0f} EUR\n"
            f"Heures/semaine: {hours_per_week}h\n"
            f"Semaines/an: {weeks}\n"
            f"---\n"
            f"Taux horaire: {hourly:.0f} EUR/h\n"
            f"TJM: {daily:.0f} EUR/jour\n"
            f"Mensuel: {monthly:,.0f} EUR/mois"
        )

    # === CONVERTERS ===

    def convert_currency(self, amount: float, from_curr: str, to_curr: str) -> str:
        """Convert currency using free API."""
        try:
            url = f"https://api.exchangerate-api.com/v4/latest/{from_curr.upper()}"
            resp = requests.get(url, timeout=10)
            data = resp.json()
            rate = data["rates"].get(to_curr.upper())

            if rate:
                result = amount * rate
                return f"{amount:.2f} {from_curr.upper()} = {result:.2f} {to_curr.upper()} (taux: {rate:.4f})"
            return f"Devise '{to_curr}' non trouvee."

        except Exception as e:
            return f"Erreur conversion: {e}"

    def convert_timezone(self, time_str: str, from_tz: str, to_tz: str) -> str:
        """Simple timezone offset conversion."""
        offsets = {
            "paris": 1, "london": 0, "new_york": -5, "la": -8,
            "tokyo": 9, "dubai": 4, "sydney": 11, "bangkok": 7,
            "cet": 1, "est": -5, "pst": -8, "gmt": 0, "utc": 0,
        }

        from_offset = offsets.get(from_tz.lower().replace(" ", "_"))
        to_offset = offsets.get(to_tz.lower().replace(" ", "_"))

        if from_offset is None or to_offset is None:
            return f"Fuseau non reconnu. Disponibles: {', '.join(offsets.keys())}"

        try:
            hour, minute = map(int, time_str.split(":"))
            diff = to_offset - from_offset
            new_hour = (hour + diff) % 24
            return f"{time_str} ({from_tz}) = {new_hour:02d}:{minute:02d} ({to_tz})"
        except Exception:
            return "Format: HH:MM"

    def convert_units(self, value: float, from_unit: str, to_unit: str) -> str:
        """Convert common units."""
        conversions = {
            ("km", "miles"): 0.621371,
            ("miles", "km"): 1.60934,
            ("kg", "lbs"): 2.20462,
            ("lbs", "kg"): 0.453592,
            ("c", "f"): lambda v: v * 9/5 + 32,
            ("f", "c"): lambda v: (v - 32) * 5/9,
            ("m", "ft"): 3.28084,
            ("ft", "m"): 0.3048,
            ("l", "gal"): 0.264172,
            ("gal", "l"): 3.78541,
            ("eur", "usd"): 1.08,  # Approximate
        }

        key = (from_unit.lower(), to_unit.lower())
        factor = conversions.get(key)

        if factor is None:
            return f"Conversion {from_unit} -> {to_unit} non supportee."

        if callable(factor):
            result = factor(value)
        else:
            result = value * factor

        return f"{value} {from_unit} = {result:.2f} {to_unit}"

    # === GENERATORS ===

    def generate_password(self, length: int = 16) -> str:
        """Generate a secure password."""
        chars = string.ascii_letters + string.digits + "!@#$%&*"
        password = ''.join(random.SystemRandom().choice(chars) for _ in range(length))
        return f"🔑 {password}"

    def generate_uuid(self) -> str:
        """Generate a UUID."""
        import uuid
        return str(uuid.uuid4())

    def generate_lorem(self, words: int = 50) -> str:
        """Generate lorem ipsum text."""
        base = ("Lorem ipsum dolor sit amet consectetur adipiscing elit sed do "
                "eiusmod tempor incididunt ut labore et dolore magna aliqua Ut enim "
                "ad minim veniam quis nostrud exercitation ullamco laboris nisi ut "
                "aliquip ex ea commodo consequat Duis aute irure dolor in reprehenderit "
                "in voluptate velit esse cillum dolore eu fugiat nulla pariatur").split()

        result = []
        for i in range(words):
            result.append(random.choice(base))
        return " ".join(result) + "."

    # === QUICK INFO ===

    def ip_info(self) -> str:
        """Get current public IP and location."""
        try:
            resp = requests.get("https://ipinfo.io/json", timeout=5)
            data = resp.json()
            return (
                f"🌐 IP: {data.get('ip')}\n"
                f"Ville: {data.get('city')}\n"
                f"Region: {data.get('region')}\n"
                f"Pays: {data.get('country')}\n"
                f"FAI: {data.get('org')}"
            )
        except Exception as e:
            return f"Erreur: {e}"

    def weather(self, city: str = "Lyon") -> str:
        """Get weather (free API, no key needed)."""
        try:
            url = f"https://wttr.in/{city}?format=j1"
            resp = requests.get(url, timeout=10)
            data = resp.json()

            current = data["current_condition"][0]
            temp = current["temp_C"]
            feels = current["FeelsLikeC"]
            desc = current["weatherDesc"][0]["value"]
            humidity = current["humidity"]
            wind = current["windspeedKmph"]

            return (
                f"🌤 METEO {city.upper()}\n"
                f"Temp: {temp}C (ressenti {feels}C)\n"
                f"Ciel: {desc}\n"
                f"Humidite: {humidity}%\n"
                f"Vent: {wind} km/h"
            )
        except Exception as e:
            return f"Meteo indisponible: {e}"

    def countdown(self, event_name: str, date_str: str) -> str:
        """Calculate days until an event."""
        try:
            target = datetime.strptime(date_str, "%Y-%m-%d")
            delta = target - datetime.now()
            days = delta.days

            if days < 0:
                return f"{event_name} est passe il y a {abs(days)} jours."
            elif days == 0:
                return f"🎉 {event_name} c'est AUJOURD'HUI !"
            else:
                return f"⏳ {event_name}: dans {days} jours ({date_str})"
        except ValueError:
            return "Format date: YYYY-MM-DD"
