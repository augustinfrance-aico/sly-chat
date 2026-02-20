"""
TITAN Color Palette Module
Generate color palettes, convert colors, brand color suggestions.
"""

import random


class TitanColors:
    """Colors for designers and devs."""

    PALETTES = {
        "modern": ["#1a1a2e", "#16213e", "#0f3460", "#e94560", "#533483"],
        "sunset": ["#ff6b6b", "#feca57", "#ff9ff3", "#54a0ff", "#5f27cd"],
        "nature": ["#2d6a4f", "#40916c", "#52b788", "#74c69d", "#95d5b2"],
        "ocean": ["#023e8a", "#0077b6", "#0096c7", "#00b4d8", "#48cae4"],
        "fire": ["#6a040f", "#9d0208", "#d00000", "#dc2f02", "#e85d04"],
        "pastel": ["#ffadad", "#ffd6a5", "#fdffb6", "#caffbf", "#9bf6ff"],
        "dark": ["#0d1117", "#161b22", "#21262d", "#30363d", "#484f58"],
        "neon": ["#00ff87", "#60efff", "#ff00e5", "#ff6b00", "#ffff00"],
        "minimal": ["#ffffff", "#f8f9fa", "#e9ecef", "#212529", "#495057"],
        "brand_tech": ["#0066ff", "#00c2ff", "#f0f0f0", "#1a1a1a", "#ff4444"],
    }

    def palette(self, style: str = "random") -> str:
        """Get a color palette."""
        if style.lower() in self.PALETTES:
            colors = self.PALETTES[style.lower()]
            name = style
        else:
            name = random.choice(list(self.PALETTES.keys()))
            colors = self.PALETTES[name]

        lines = [f"🎨 PALETTE: {name.upper()}\n"]
        for c in colors:
            block = "██████"
            lines.append(f"  {block} {c}")

        lines.append(f"\nCSS: {', '.join(colors)}")
        return "\n".join(lines)

    def hex_to_rgb(self, hex_color: str) -> str:
        """Convert HEX to RGB."""
        hex_color = hex_color.lstrip("#")
        try:
            r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
            return f"🎨 #{hex_color}\n  RGB: ({r}, {g}, {b})\n  HSL: ~approx"
        except Exception:
            return "Format invalide. Utilise #FF5733"

    def rgb_to_hex(self, r: int, g: int, b: int) -> str:
        """Convert RGB to HEX."""
        hex_color = f"#{r:02x}{g:02x}{b:02x}"
        return f"🎨 RGB({r}, {g}, {b})\n  HEX: {hex_color}"

    def random_color(self) -> str:
        """Generate a random color."""
        r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        hex_c = f"#{r:02x}{g:02x}{b:02x}"
        return f"🎲 COULEUR ALEATOIRE\n  HEX: {hex_c}\n  RGB: ({r}, {g}, {b})"

    def brand_colors(self, brand: str) -> str:
        """Get brand colors for famous companies."""
        brands = {
            "google": ["#4285F4", "#DB4437", "#F4B400", "#0F9D58"],
            "facebook": ["#1877F2", "#898F9C", "#F0F2F5"],
            "twitter": ["#1DA1F2", "#14171A", "#657786"],
            "spotify": ["#1DB954", "#191414", "#FFFFFF"],
            "netflix": ["#E50914", "#141414", "#FFFFFF"],
            "apple": ["#000000", "#A2AAAD", "#FFFFFF"],
            "amazon": ["#FF9900", "#232F3E", "#FFFFFF"],
            "stripe": ["#635BFF", "#0A2540", "#FFFFFF"],
            "slack": ["#4A154B", "#36C5F0", "#2EB67D", "#ECB22E", "#E01E5A"],
            "discord": ["#5865F2", "#EB459E", "#FEE75C", "#57F287", "#ED4245"],
        }

        brand_lower = brand.lower().strip()
        if brand_lower in brands:
            colors = brands[brand_lower]
            lines = [f"🏷 {brand.upper()} BRAND COLORS\n"]
            for c in colors:
                lines.append(f"  ██████ {c}")
            return "\n".join(lines)

        available = ", ".join(brands.keys())
        return f"Marque non trouvee. Disponibles: {available}"

    def gradient(self, color1: str, color2: str, steps: int = 5) -> str:
        """Generate a gradient between two colors."""
        try:
            c1 = color1.lstrip("#")
            c2 = color2.lstrip("#")
            r1, g1, b1 = int(c1[0:2], 16), int(c1[2:4], 16), int(c1[4:6], 16)
            r2, g2, b2 = int(c2[0:2], 16), int(c2[2:4], 16), int(c2[4:6], 16)

            lines = [f"🌈 GRADIENT: #{c1} -> #{c2}\n"]
            for i in range(steps):
                t = i / (steps - 1)
                r = int(r1 + (r2 - r1) * t)
                g = int(g1 + (g2 - g1) * t)
                b = int(b1 + (b2 - b1) * t)
                hex_c = f"#{r:02x}{g:02x}{b:02x}"
                lines.append(f"  ██████ {hex_c}")

            return "\n".join(lines)
        except Exception:
            return "Format: /gradient #FF0000 #0000FF"

    def list_palettes(self) -> str:
        """List available palettes."""
        lines = ["🎨 PALETTES DISPONIBLES\n"]
        for name in self.PALETTES:
            preview = " ".join(self.PALETTES[name][:3])
            lines.append(f"  • {name}: {preview}...")
        lines.append(f"\nUtilise /palette <nom>")
        return "\n".join(lines)
