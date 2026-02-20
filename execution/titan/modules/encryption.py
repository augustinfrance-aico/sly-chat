"""
TITAN Encryption Module
Hash, encode/decode, encrypt text.
"""

import hashlib
import base64
import secrets
import string


class TitanEncryption:
    """Security tools at your fingertips."""

    def hash_text(self, text: str, algo: str = "sha256") -> str:
        """Hash text with various algorithms."""
        algos = {
            "md5": hashlib.md5,
            "sha1": hashlib.sha1,
            "sha256": hashlib.sha256,
            "sha512": hashlib.sha512,
        }

        if algo.lower() not in algos:
            return f"Algorithmes: {', '.join(algos.keys())}"

        h = algos[algo.lower()](text.encode()).hexdigest()
        return f"🔐 HASH ({algo.upper()})\n\nInput: {text[:50]}\nHash: {h}"

    def hash_all(self, text: str) -> str:
        """Hash with all algorithms."""
        lines = [f"🔐 HASH ALL: {text[:30]}...\n"]
        for algo in ["md5", "sha1", "sha256", "sha512"]:
            h = hashlib.new(algo, text.encode()).hexdigest()
            lines.append(f"  {algo.upper()}: {h}")
        return "\n".join(lines)

    def base64_encode(self, text: str) -> str:
        """Encode text to Base64."""
        encoded = base64.b64encode(text.encode()).decode()
        return f"📦 BASE64 ENCODE\n\nInput: {text[:50]}\nOutput: {encoded}"

    def base64_decode(self, text: str) -> str:
        """Decode Base64 text."""
        try:
            decoded = base64.b64decode(text.encode()).decode()
            return f"📦 BASE64 DECODE\n\nInput: {text[:50]}\nOutput: {decoded}"
        except Exception:
            return "Erreur: texte Base64 invalide."

    def caesar_encrypt(self, text: str, shift: int = 3) -> str:
        """Caesar cipher encryption."""
        result = []
        for char in text:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                result.append(chr((ord(char) - base + shift) % 26 + base))
            else:
                result.append(char)
        encrypted = "".join(result)
        return f"🔑 CAESAR (shift={shift})\n\nOriginal: {text}\nChiffre: {encrypted}"

    def caesar_decrypt(self, text: str, shift: int = 3) -> str:
        """Caesar cipher decryption."""
        return self.caesar_encrypt(text, -shift)

    def generate_token(self, length: int = 32) -> str:
        """Generate a secure random token."""
        token = secrets.token_hex(length)
        url_safe = secrets.token_urlsafe(length)
        return (
            f"🔑 TOKENS GENERES\n\n"
            f"Hex ({length * 2} chars):\n{token}\n\n"
            f"URL-safe ({len(url_safe)} chars):\n{url_safe}"
        )

    def generate_api_key(self) -> str:
        """Generate a fake API key format."""
        prefix = "sk"
        part1 = secrets.token_hex(4)
        part2 = secrets.token_hex(8)
        part3 = secrets.token_hex(16)
        key = f"{prefix}-{part1}-{part2}-{part3}"
        return f"🔐 API KEY\n\n{key}\n\n(Ceci est un format fictif pour tests)"

    def rot13(self, text: str) -> str:
        """ROT13 encoding."""
        import codecs
        result = codecs.encode(text, 'rot_13')
        return f"🔄 ROT13\n\nInput: {text}\nOutput: {result}"

    def morse_encode(self, text: str) -> str:
        """Convert text to Morse code."""
        morse_dict = {
            'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
            'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
            'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
            'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
            'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---',
            '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...',
            '8': '---..', '9': '----.', ' ': '/',
        }
        morse = " ".join(morse_dict.get(c.upper(), c) for c in text)
        return f"📡 MORSE\n\n{text}\n{morse}"
