"""
TITAN ASCII Art Module
Generate ASCII art text and decorations.
"""


class TitanASCII:
    """Text art for the terminal generation."""

    FONTS = {
        "block": {
            "A": ["█▀█", "█▀█", "▀ ▀"], "B": ["█▀▄", "█▀▄", "▀▀ "], "C": ["█▀▀", "█  ", "▀▀▀"],
            "D": ["█▀▄", "█ █", "▀▀ "], "E": ["█▀▀", "█▀▀", "▀▀▀"], "F": ["█▀▀", "█▀▀", "▀  "],
            "G": ["█▀▀", "█ █", "▀▀▀"], "H": ["█ █", "█▀█", "▀ ▀"], "I": ["▀█▀", " █ ", " ▀ "],
            "J": ["  █", "  █", "▀▀ "], "K": ["█ █", "█▀▄", "▀ ▀"], "L": ["█  ", "█  ", "▀▀▀"],
            "M": ["█▄█", "█ █", "▀ ▀"], "N": ["█▀█", "█ █", "▀ ▀"], "O": ["█▀█", "█ █", "▀▀▀"],
            "P": ["█▀█", "█▀▀", "▀  "], "Q": ["█▀█", "█ █", " ▀▀"], "R": ["█▀█", "█▀▄", "▀ ▀"],
            "S": ["█▀▀", "▀▀█", "▀▀▀"], "T": ["▀█▀", " █ ", " ▀ "], "U": ["█ █", "█ █", "▀▀▀"],
            "V": ["█ █", "█ █", " ▀ "], "W": ["█ █", "█ █", "█▀█"], "X": ["█ █", " █ ", "█ █"],
            "Y": ["█ █", " █ ", " ▀ "], "Z": ["▀▀█", " █ ", "█▀▀"],
            " ": ["   ", "   ", "   "],
        }
    }

    def text_art(self, text: str) -> str:
        """Generate block text art."""
        font = self.FONTS["block"]
        text = text.upper()[:20]  # Limit length

        rows = ["", "", ""]
        for char in text:
            if char in font:
                for i in range(3):
                    rows[i] += font[char][i] + " "
            else:
                for i in range(3):
                    rows[i] += "   "

        return f"🎨 ASCII ART\n\n" + "\n".join(rows)

    def box(self, text: str) -> str:
        """Put text in a box."""
        lines = text.split("\n")
        max_len = max(len(l) for l in lines)

        result = ["╔" + "═" * (max_len + 2) + "╗"]
        for line in lines:
            result.append(f"║ {line:<{max_len}} ║")
        result.append("╚" + "═" * (max_len + 2) + "╝")

        return "\n".join(result)

    def banner(self, text: str) -> str:
        """Create a banner."""
        length = len(text) + 4
        return (
            f"{'*' * length}\n"
            f"* {text} *\n"
            f"{'*' * length}"
        )

    def divider(self, style: str = "default") -> str:
        """Decorative dividers."""
        dividers = {
            "default": "═" * 30,
            "stars": "★ " * 15,
            "dots": "• " * 15,
            "wave": "～" * 15,
            "arrows": "▸ " * 15,
            "blocks": "█░" * 15,
            "hearts": "♥ " * 15,
            "diamond": "◆ " * 15,
        }
        d = dividers.get(style.lower(), dividers["default"])
        return d

    def table(self, headers: list, rows: list) -> str:
        """Create an ASCII table."""
        col_widths = [max(len(str(h)), max((len(str(row[i])) for row in rows), default=0))
                      for i, h in enumerate(headers)]

        header = " | ".join(f"{h:<{col_widths[i]}}" for i, h in enumerate(headers))
        sep = "-+-".join("-" * w for w in col_widths)

        lines = [header, sep]
        for row in rows:
            line = " | ".join(f"{str(row[i]):<{col_widths[i]}}" for i in range(len(headers)))
            lines.append(line)

        return "\n".join(lines)

    def emoji_art(self, design: str = "heart") -> str:
        """Predefined emoji art."""
        designs = {
            "heart": (
                "  ❤️❤️   ❤️❤️\n"
                "❤️❤️❤️❤️❤️❤️❤️❤️\n"
                "❤️❤️❤️❤️❤️❤️❤️❤️\n"
                "  ❤️❤️❤️❤️❤️❤️\n"
                "    ❤️❤️❤️❤️\n"
                "      ❤️❤️\n"
                "        ❤️"
            ),
            "star": (
                "        ⭐\n"
                "      ⭐⭐⭐\n"
                "    ⭐⭐⭐⭐⭐\n"
                "  ⭐⭐⭐⭐⭐⭐⭐\n"
                "    ⭐⭐⭐⭐⭐\n"
                "   ⭐⭐   ⭐⭐"
            ),
            "rocket": (
                "      🔥\n"
                "     🔥🔥\n"
                "    🚀🚀🚀\n"
                "   🚀🚀🚀🚀\n"
                "    🚀🚀🚀\n"
                "     💨💨"
            ),
        }
        return designs.get(design.lower(), f"Design '{design}' inconnu. Disponibles: {', '.join(designs.keys())}")
