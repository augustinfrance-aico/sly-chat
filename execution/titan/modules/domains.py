"""
TITAN Domain Checker Module
Check domain availability, WHOIS info, DNS lookup.
"""

import requests
import socket


class TitanDomains:
    """Find the perfect domain name."""

    def check(self, domain: str) -> str:
        """Check if a domain is available via DNS lookup."""
        results = []
        extensions = [".com", ".fr", ".io", ".co", ".dev", ".ai", ".app"]

        base = domain.replace("www.", "").split(".")[0]

        results.append(f"🌐 DOMAIN CHECK: {base}\n")

        for ext in extensions:
            full = f"{base}{ext}"
            try:
                socket.gethostbyname(full)
                results.append(f"  ❌ {full} — pris")
            except socket.gaierror:
                results.append(f"  ✅ {full} — disponible !")
            except Exception:
                results.append(f"  ❓ {full} — incertain")

        return "\n".join(results)

    def dns_lookup(self, domain: str) -> str:
        """DNS lookup for a domain."""
        try:
            ip = socket.gethostbyname(domain)
            lines = [f"🔍 DNS LOOKUP: {domain}\n"]
            lines.append(f"  IP: {ip}")

            try:
                hostname = socket.gethostbyaddr(ip)
                lines.append(f"  Hostname: {hostname[0]}")
            except Exception:
                pass

            # Check HTTP
            try:
                resp = requests.head(f"https://{domain}", timeout=5, allow_redirects=True)
                lines.append(f"  HTTPS: {resp.status_code}")
                lines.append(f"  Server: {resp.headers.get('server', '?')}")
            except Exception:
                try:
                    resp = requests.head(f"http://{domain}", timeout=5, allow_redirects=True)
                    lines.append(f"  HTTP: {resp.status_code}")
                except Exception:
                    lines.append("  HTTP: inaccessible")

            return "\n".join(lines)
        except socket.gaierror:
            return f"Domaine '{domain}' non resolu (probablement disponible)."

    def suggest(self, keyword: str) -> str:
        """Suggest domain names."""
        prefixes = ["", "get", "try", "use", "my", "the", "go"]
        suffixes = ["", "app", "hq", "io", "lab", "hub", "ai"]
        extensions = [".com", ".io", ".co", ".dev", ".ai"]

        suggestions = []
        for pre in prefixes:
            for suf in suffixes:
                name = f"{pre}{keyword}{suf}"
                if len(name) > 3 and len(name) < 20:
                    suggestions.append(name)

        # Deduplicate and limit
        seen = set()
        unique = []
        for s in suggestions:
            if s not in seen:
                seen.add(s)
                unique.append(s)

        lines = [f"💡 SUGGESTIONS DOMAINES: {keyword}\n"]
        for name in unique[:15]:
            ext = ".com"
            lines.append(f"  • {name}{ext}")

        lines.append(f"\nUtilise /domaincheck <nom> pour verifier la disponibilite.")
        return "\n".join(lines)
