"""
TITAN SEO Module
SEO analysis, keyword ideas, meta tag generator, sitemap checker.
"""

import requests

from ..ai_client import chat as ai_chat


class TitanSEO:
    """Domine Google."""

    def __init__(self):
        pass

    def check_site(self, url: str) -> str:
        """Quick SEO check on a website."""
        try:
            resp = requests.get(url, timeout=15, headers={"User-Agent": "TitanBot/1.0"})
            html = resp.text[:5000]

            # Extract basic SEO elements
            title = ""
            desc = ""
            h1_count = html.lower().count("<h1")
            has_robots = "/robots.txt" in html or True
            has_sitemap = "sitemap" in html.lower()
            is_https = url.startswith("https")
            load_time = resp.elapsed.total_seconds()

            # Title
            import re
            title_match = re.search(r"<title>(.*?)</title>", html, re.IGNORECASE)
            if title_match:
                title = title_match.group(1)[:60]

            # Meta description
            desc_match = re.search(r'meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', html, re.IGNORECASE)
            if desc_match:
                desc = desc_match.group(1)[:160]

            score = 0
            checks = []

            if title:
                score += 20
                checks.append(f"✅ Title: {title[:50]}")
            else:
                checks.append("❌ Pas de title tag")

            if desc:
                score += 20
                checks.append(f"✅ Meta desc: {desc[:80]}...")
            else:
                checks.append("❌ Pas de meta description")

            if is_https:
                score += 15
                checks.append("✅ HTTPS actif")
            else:
                checks.append("❌ Pas de HTTPS")

            if h1_count == 1:
                score += 15
                checks.append("✅ Un seul H1")
            elif h1_count > 1:
                score += 5
                checks.append(f"⚠️ {h1_count} balises H1 (devrait etre 1)")
            else:
                checks.append("❌ Pas de H1")

            if load_time < 2:
                score += 15
                checks.append(f"✅ Temps de chargement: {load_time:.1f}s")
            elif load_time < 5:
                score += 8
                checks.append(f"⚠️ Temps de chargement: {load_time:.1f}s (lent)")
            else:
                checks.append(f"❌ Trop lent: {load_time:.1f}s")

            score += 15  # Base score

            return (
                f"🔍 SEO CHECK: {url}\n"
                f"{'=' * 25}\n"
                f"Score: {score}/100\n\n"
                + "\n".join(checks)
            )
        except Exception as e:
            return f"Erreur SEO check: {e}"

    async def keywords(self, topic: str) -> str:
        """Generate keyword ideas for a topic."""
        return ai_chat("Expert assistant.", f"""Genere 20 idees de mots-cles SEO pour: "{topic}" """, 1000)

    async def meta_tags(self, page_desc: str) -> str:
        """Generate optimized meta tags."""
        return ai_chat("Expert assistant.", f"""Genere des meta tags SEO optimises pour cette page: "{page_desc}" """, 500)
