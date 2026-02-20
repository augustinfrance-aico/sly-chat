"""
TITAN Invoice Module
Generate professional invoices as text (for freelancers).
"""

from datetime import datetime, timedelta


class TitanInvoice:
    """Facture en 2 secondes."""

    def generate(self, client: str, items: str, rate: float = 0) -> str:
        """Generate a text invoice.
        items format: "description1:amount1,description2:amount2"
        """
        now = datetime.now()
        due = now + timedelta(days=30)
        inv_number = f"INV-{now.strftime('%Y%m%d')}-{now.strftime('%H%M')}"

        lines = [
            f"{'=' * 40}",
            f"         FACTURE",
            f"{'=' * 40}",
            f"",
            f"  De: AICO — Augustin",
            f"  A: {client}",
            f"  Date: {now.strftime('%d/%m/%Y')}",
            f"  Echeance: {due.strftime('%d/%m/%Y')}",
            f"  Numero: {inv_number}",
            f"",
            f"{'=' * 40}",
            f"  PRESTATIONS",
            f"{'=' * 40}",
        ]

        total = 0
        item_list = items.split(",")
        for item in item_list:
            parts = item.strip().split(":")
            if len(parts) == 2:
                desc = parts[0].strip()
                try:
                    amount = float(parts[1].strip())
                except ValueError:
                    amount = rate
            else:
                desc = parts[0].strip()
                amount = rate

            total += amount
            lines.append(f"  {desc:<25} {amount:>8.2f} EUR")

        tva = total * 0.20
        total_ttc = total + tva

        lines.extend([
            f"",
            f"{'=' * 40}",
            f"  Sous-total HT:         {total:>8.2f} EUR",
            f"  TVA (20%):             {tva:>8.2f} EUR",
            f"  TOTAL TTC:             {total_ttc:>8.2f} EUR",
            f"{'=' * 40}",
            f"",
            f"  Conditions: Paiement a 30 jours",
            f"  IBAN: FR76 XXXX XXXX XXXX XXXX",
            f"",
            f"  Merci pour votre confiance !",
            f"{'=' * 40}",
        ])

        return "\n".join(lines)

    def quick_invoice(self, client: str, description: str, amount: float) -> str:
        """Generate a quick single-item invoice."""
        return self.generate(client, f"{description}:{amount}")

    def estimate(self, client: str, items: str) -> str:
        """Generate a quote/estimate."""
        now = datetime.now()
        valid_until = now + timedelta(days=15)
        est_number = f"DEVIS-{now.strftime('%Y%m%d')}-{now.strftime('%H%M')}"

        lines = [
            f"{'=' * 40}",
            f"         DEVIS",
            f"{'=' * 40}",
            f"",
            f"  De: AICO — Augustin",
            f"  A: {client}",
            f"  Date: {now.strftime('%d/%m/%Y')}",
            f"  Valide jusqu'au: {valid_until.strftime('%d/%m/%Y')}",
            f"  Numero: {est_number}",
            f"",
            f"{'=' * 40}",
            f"  PRESTATIONS",
            f"{'=' * 40}",
        ]

        total = 0
        item_list = items.split(",")
        for item in item_list:
            parts = item.strip().split(":")
            if len(parts) == 2:
                desc = parts[0].strip()
                try:
                    amount = float(parts[1].strip())
                except ValueError:
                    amount = 0
            else:
                desc = parts[0].strip()
                amount = 0

            total += amount
            lines.append(f"  {desc:<25} {amount:>8.2f} EUR")

        tva = total * 0.20
        total_ttc = total + tva

        lines.extend([
            f"",
            f"{'=' * 40}",
            f"  Sous-total HT:         {total:>8.2f} EUR",
            f"  TVA (20%):             {tva:>8.2f} EUR",
            f"  TOTAL TTC:             {total_ttc:>8.2f} EUR",
            f"{'=' * 40}",
            f"",
            f"  Devis valable 15 jours.",
            f"{'=' * 40}",
        ])

        return "\n".join(lines)
