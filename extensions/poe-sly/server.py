"""
SLY on Poe — Cooper Building AI Assistant
Publishes SLY as a bot on poe.com marketplace.

Usage:
    pip install -r requirements.txt
    python server.py

Then on poe.com/create_bot → Server bot → URL: http://your-server:8080
"""

from __future__ import annotations

import os
import httpx
import fastapi_poe as fp

GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY",
    "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",
)
GROQ_MODEL = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = (
    "Tu es SLY, un assistant IA polyvalent du Cooper Building — "
    "une equipe de 50 agents IA specialises (strategie, code, vente, creatif, R&D). "
    "Reponds en francais sauf si l'utilisateur parle anglais. "
    "Sois concis, direct, utile. Pas de blabla. "
    "Ton createur est Augus, fondateur de l'empire AICO."
)

POE_ACCESS_KEY = os.getenv("POE_ACCESS_KEY", "")


class SlyBot(fp.PoeBot):
    """SLY bot for Poe marketplace."""

    async def get_response(self, request: fp.QueryRequest):
        # Build conversation history for Groq
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]

        for msg in request.query:
            role = "user" if msg.role == "user" else "assistant"
            messages.append({"role": role, "content": msg.content})

        # Call Groq API
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                resp = await client.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {GROQ_API_KEY}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": GROQ_MODEL,
                        "messages": messages,
                        "max_tokens": 1024,
                        "temperature": 0.7,
                    },
                )
                data = resp.json()

                if "choices" in data and data["choices"]:
                    answer = data["choices"][0]["message"]["content"]
                else:
                    error = data.get("error", {}).get("message", "Unknown error")
                    answer = f"Erreur Groq: {error}"

        except Exception as e:
            answer = f"Erreur de connexion: {e}"

        yield fp.PartialResponse(text=answer)

    async def get_settings(self, setting: fp.SettingsRequest) -> fp.SettingsResponse:
        return fp.SettingsResponse(
            server_bot_dependencies={},
            introduction_message=(
                "Salut ! Je suis **SLY**, assistant IA du Cooper Building.\n\n"
                "50 agents specialises a ton service : strategie, code, vente, creatif, R&D.\n\n"
                "Pose ta question, je m'en occupe."
            ),
        )


if __name__ == "__main__":
    bot = SlyBot()

    if not POE_ACCESS_KEY:
        print("=" * 60)
        print("SLY on Poe — Setup")
        print("=" * 60)
        print()
        print("1. Va sur https://poe.com/create_bot")
        print("2. Choisis 'Server bot'")
        print("3. Recupere ton Access Key")
        print("4. Lance avec: POE_ACCESS_KEY=xxx python server.py")
        print()
        print("Ou set la variable d'env POE_ACCESS_KEY dans .env")
        print("=" * 60)
        print()
        print("Mode dev: lancement sur port 8080 sans auth...")
        print()

    # Start the server
    fp.run(bot, access_key=POE_ACCESS_KEY or "dev", port=8080)
