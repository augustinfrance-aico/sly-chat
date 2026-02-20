"""
TITAN QR Code Generator
Generate QR codes for URLs, text, WiFi, contacts.
"""

import requests
import os
import tempfile


class TitanQRCode:
    """Generate QR codes instantly."""

    def generate(self, data: str, size: int = 300) -> str:
        """Generate a QR code image URL."""
        encoded = requests.utils.quote(data)
        url = f"https://api.qrserver.com/v1/create-qr-code/?size={size}x{size}&data={encoded}"
        return f"📱 QR CODE\n\nContenu: {data[:100]}\n🔗 {url}"

    def wifi(self, ssid: str, password: str, security: str = "WPA") -> str:
        """Generate WiFi QR code."""
        wifi_string = f"WIFI:T:{security};S:{ssid};P:{password};;"
        encoded = requests.utils.quote(wifi_string)
        url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={encoded}"
        return (
            f"📶 QR CODE WIFI\n\n"
            f"Reseau: {ssid}\n"
            f"Securite: {security}\n"
            f"🔗 {url}\n\n"
            f"Scanne pour se connecter automatiquement."
        )

    def vcard(self, name: str, phone: str = "", email: str = "", company: str = "") -> str:
        """Generate vCard QR code."""
        vcard = f"BEGIN:VCARD\\nVERSION:3.0\\nFN:{name}"
        if phone:
            vcard += f"\\nTEL:{phone}"
        if email:
            vcard += f"\\nEMAIL:{email}"
        if company:
            vcard += f"\\nORG:{company}"
        vcard += "\\nEND:VCARD"

        encoded = requests.utils.quote(vcard)
        url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={encoded}"
        return f"👤 QR VCARD: {name}\n🔗 {url}"

    def url(self, link: str) -> str:
        """Generate URL QR code."""
        return self.generate(link)
