"""
TITAN Email Generator
Write any type of email in seconds.
Cold outreach, follow-ups, proposals, newsletters, event promos.
"""

from ..ai_client import chat as ai_chat


class TitanEmailGen:
    """Titan writes emails like a pro copywriter."""

    def __init__(self):
        pass

    async def write_email(self, brief: str, style: str = "professional", lang: str = "fr") -> str:
        """Write any email from a brief."""
        lang_name = {"fr": "francais", "en": "anglais", "es": "espagnol"}.get(lang, lang)
        return ai_chat("Expert assistant.", f"""Redige un email en {lang_name}.\n\nBrief: {brief}\nStyle: {style}""", 1024)

    async def cold_outreach(self, target: str, offer: str, lang: str = "fr") -> str:
        """Generate a cold outreach email."""
        return await self.write_email(
            f"Email de prospection a froid pour {target}. On propose: {offer}. "
            f"Accroche personnalisee, pas de spam. Propose un call de 15 min.",
            style="direct, humain, pas corporate",
            lang=lang,
        )

    async def follow_up(self, context: str, attempt: int = 1, lang: str = "fr") -> str:
        """Generate a follow-up email."""
        urgency = {
            1: "Premier follow-up, poli, rappel doux",
            2: "Deuxieme relance, un peu plus direct, apporter de la valeur",
            3: "Derniere relance, creer l'urgence, proposer alternative",
        }.get(attempt, "Relance standard")
        return await self.write_email(
            f"Follow-up email. Contexte: {context}. Ton: {urgency}",
            style="conversationnel",
            lang=lang,
        )

    async def event_promo(self, event_name: str, details: str, lang: str = "fr") -> str:
        """Generate an event promotion email."""
        return await self.write_email(
            f"Email promotionnel pour l'evenement '{event_name}'. Details: {details}. "
            f"Creer de l'excitation, donner les infos cles (date, lieu, prix), CTA inscription.",
            style="enthousiaste mais pas over-the-top",
            lang=lang,
        )

    async def newsletter_section(self, topic: str, content_brief: str, lang: str = "fr") -> str:
        """Generate a newsletter section."""
        return await self.write_email(
            f"Section de newsletter sur le sujet: {topic}. Brief: {content_brief}. "
            f"Format: titre accrocheur + 3-4 phrases + CTA si pertinent.",
            style="informatif, engageant",
            lang=lang,
        )

    async def thank_you(self, context: str, lang: str = "fr") -> str:
        """Generate a thank you / post-meeting email."""
        return await self.write_email(
            f"Email de remerciement. Contexte: {context}. "
            f"Court, sincere, proposer la prochaine etape.",
            style="chaleureux, professionnel",
            lang=lang,
        )

    async def rewrite(self, original: str, instruction: str, lang: str = "fr") -> str:
        """Rewrite an existing email with specific instructions."""
        lang_name = {"fr": "francais", "en": "anglais"}.get(lang, lang)
        return ai_chat("Expert assistant.", f"""Reecris cet email en {lang_name} avec cette instruction: {instruction}\n\n{original}""", 1024)
