"""
TITAN JSON Tools Module
Format, validate, query, convert JSON.
"""

import json


class TitanJSON:
    """JSON power tools."""

    def format(self, raw: str) -> str:
        """Pretty-print JSON."""
        try:
            data = json.loads(raw)
            formatted = json.dumps(data, indent=2, ensure_ascii=False)
            return f"📦 JSON FORMATE\n\n{formatted[:3000]}"
        except json.JSONDecodeError as e:
            return f"❌ JSON invalide: {e}"

    def validate(self, raw: str) -> str:
        """Validate JSON."""
        try:
            data = json.loads(raw)
            obj_type = type(data).__name__
            if isinstance(data, list):
                info = f"Array de {len(data)} elements"
            elif isinstance(data, dict):
                info = f"Object avec {len(data)} cles: {', '.join(list(data.keys())[:10])}"
            else:
                info = f"Type: {obj_type}"
            return f"✅ JSON VALIDE\n\n{info}"
        except json.JSONDecodeError as e:
            return f"❌ JSON INVALIDE\n\nErreur: {e}\nLigne: {e.lineno}, Col: {e.colno}"

    def minify(self, raw: str) -> str:
        """Minify JSON."""
        try:
            data = json.loads(raw)
            minified = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
            return f"📦 JSON MINIFIE\n\n{minified[:3000]}"
        except json.JSONDecodeError as e:
            return f"❌ JSON invalide: {e}"

    def to_csv(self, raw: str) -> str:
        """Convert JSON array to CSV."""
        try:
            data = json.loads(raw)
            if not isinstance(data, list) or not data:
                return "Le JSON doit etre un array d'objets."

            headers = list(data[0].keys())
            lines = [",".join(headers)]
            for item in data[:50]:
                row = [str(item.get(h, "")) for h in headers]
                lines.append(",".join(row))

            return f"📊 CSV\n\n" + "\n".join(lines)
        except Exception as e:
            return f"Erreur: {e}"

    def extract_keys(self, raw: str) -> str:
        """Extract all keys from JSON."""
        try:
            data = json.loads(raw)
            keys = set()

            def walk(obj, prefix=""):
                if isinstance(obj, dict):
                    for k, v in obj.items():
                        full = f"{prefix}.{k}" if prefix else k
                        keys.add(full)
                        walk(v, full)
                elif isinstance(obj, list) and obj:
                    walk(obj[0], f"{prefix}[]")

            walk(data)
            lines = ["🔑 CLES JSON\n"]
            for k in sorted(keys):
                lines.append(f"  • {k}")
            return "\n".join(lines)
        except Exception as e:
            return f"Erreur: {e}"

    def sample(self, structure: str = "user") -> str:
        """Generate sample JSON."""
        samples = {
            "user": {"id": 1, "name": "John Doe", "email": "john@example.com", "age": 30, "active": True},
            "product": {"id": 1, "name": "Widget", "price": 29.99, "currency": "EUR", "stock": 150, "category": "Tech"},
            "api_response": {"status": "success", "data": [{"id": 1, "value": "test"}], "meta": {"page": 1, "total": 42}},
            "config": {"app_name": "MyApp", "version": "1.0", "debug": False, "database": {"host": "localhost", "port": 5432}},
        }

        data = samples.get(structure.lower(), samples["user"])
        return f"📦 SAMPLE JSON: {structure}\n\n{json.dumps(data, indent=2, ensure_ascii=False)}"
