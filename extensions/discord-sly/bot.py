"""
SLY — Discord Bot du Cooper Building
Assistant IA connecte a Groq (llama-3.3-70b-versatile)
Slash commands: /ask, /help, /status
Repond aussi aux @mentions
"""

import os
import sys
import signal
import asyncio
import time
from datetime import datetime, timezone

import aiohttp
import discord
from discord import app_commands
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY",
    "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",
)

GROQ_MODEL = "llama-3.3-70b-versatile"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

SYSTEM_PROMPT = (
    "Tu es SLY, un assistant IA du Cooper Building (50 agents specialises). "
    "Reponds en francais, concis et direct."
)

# Embed colours — Neural Sovereign palette
COLOR_BLUE = 0x1F6FFF
COLOR_RED = 0xFF3B5C
COLOR_GREEN = 0x1EFF8E

MAX_RESPONSE_LENGTH = 4000  # Discord embed description limit ~4096

# ---------------------------------------------------------------------------
# Bot setup
# ---------------------------------------------------------------------------

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

start_time: float = 0.0
http_session: aiohttp.ClientSession | None = None


# ---------------------------------------------------------------------------
# Groq API call
# ---------------------------------------------------------------------------

async def ask_groq(question: str) -> str:
    """Send a question to Groq and return the assistant reply."""
    global http_session
    if http_session is None or http_session.closed:
        http_session = aiohttp.ClientSession()

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question},
        ],
        "max_tokens": 1024,
        "temperature": 0.7,
    }

    try:
        async with http_session.post(
            GROQ_API_URL, json=payload, headers=headers, timeout=aiohttp.ClientTimeout(total=30)
        ) as resp:
            if resp.status != 200:
                error_body = await resp.text()
                return f"Erreur Groq (HTTP {resp.status}): {error_body[:300]}"
            data = await resp.json()
            return data["choices"][0]["message"]["content"]
    except asyncio.TimeoutError:
        return "Timeout — Groq n'a pas repondu dans les 30 secondes."
    except Exception as exc:
        return f"Erreur inattendue: {exc}"


# ---------------------------------------------------------------------------
# Embed builders
# ---------------------------------------------------------------------------

def build_response_embed(question: str, answer: str) -> discord.Embed:
    """Build a rich embed for a successful AI response."""
    # Truncate if needed
    if len(answer) > MAX_RESPONSE_LENGTH:
        answer = answer[:MAX_RESPONSE_LENGTH] + "\n\n*... (tronque)*"

    embed = discord.Embed(
        description=answer,
        color=COLOR_BLUE,
        timestamp=datetime.now(timezone.utc),
    )
    embed.set_author(name="SLY")
    embed.set_footer(text="SLY-COMMAND | Cooper Building")

    # Show the question as a field if it's not too long
    if len(question) <= 256:
        embed.title = question
    else:
        embed.add_field(name="Question", value=question[:1024], inline=False)

    return embed


def build_error_embed(message: str) -> discord.Embed:
    """Build an error embed in red."""
    embed = discord.Embed(
        title="Erreur",
        description=message,
        color=COLOR_RED,
        timestamp=datetime.now(timezone.utc),
    )
    embed.set_author(name="SLY")
    embed.set_footer(text="SLY-COMMAND | Cooper Building")
    return embed


# ---------------------------------------------------------------------------
# Events
# ---------------------------------------------------------------------------

@bot.event
async def on_ready():
    global start_time
    start_time = time.monotonic()

    # Sync slash commands globally
    try:
        synced = await tree.sync()
        print(f"[SLY] Slash commands synchronisees: {len(synced)}")
    except Exception as exc:
        print(f"[SLY] Erreur sync commands: {exc}")

    activity = discord.Activity(
        type=discord.ActivityType.watching,
        name="the Cooper Building",
    )
    await bot.change_presence(activity=activity)

    print(f"[SLY] Connecte en tant que {bot.user} (ID: {bot.user.id})")
    print(f"[SLY] Serveurs: {len(bot.guilds)}")
    print("[SLY] Bot pret.")


@bot.event
async def on_message(message: discord.Message):
    """Respond to @mentions with an AI answer."""
    # Ignore own messages
    if message.author == bot.user:
        return

    # Only respond to mentions
    if bot.user not in message.mentions:
        return

    # Strip the mention from the content
    question = message.content
    for mention_str in [f"<@{bot.user.id}>", f"<@!{bot.user.id}>"]:
        question = question.replace(mention_str, "")
    question = question.strip()

    if not question:
        await message.reply(embed=build_error_embed("Pose-moi une question apres le @mention."))
        return

    async with message.channel.typing():
        answer = await ask_groq(question)

    if answer.startswith("Erreur") or answer.startswith("Timeout"):
        await message.reply(embed=build_error_embed(answer))
    else:
        await message.reply(embed=build_response_embed(question, answer))


# ---------------------------------------------------------------------------
# Slash commands
# ---------------------------------------------------------------------------

@tree.command(name="ask", description="Pose une question a SLY (IA du Cooper Building)")
@app_commands.describe(question="Ta question pour SLY")
async def cmd_ask(interaction: discord.Interaction, question: str):
    """Main AI question command."""
    await interaction.response.defer(thinking=True)

    answer = await ask_groq(question)

    if answer.startswith("Erreur") or answer.startswith("Timeout"):
        await interaction.followup.send(embed=build_error_embed(answer))
    else:
        await interaction.followup.send(embed=build_response_embed(question, answer))


@tree.command(name="help", description="Affiche les commandes disponibles de SLY")
async def cmd_help(interaction: discord.Interaction):
    """Show available commands."""
    embed = discord.Embed(
        title="Commandes SLY",
        description="Voici ce que je sais faire :",
        color=COLOR_BLUE,
        timestamp=datetime.now(timezone.utc),
    )
    embed.set_author(name="SLY")

    embed.add_field(
        name="/ask `question`",
        value="Pose une question a l'IA — reponse instantanee via Groq.",
        inline=False,
    )
    embed.add_field(
        name="/help",
        value="Affiche cette liste de commandes.",
        inline=False,
    )
    embed.add_field(
        name="/status",
        value="Uptime du bot, modele IA, latence.",
        inline=False,
    )
    embed.add_field(
        name="@SLY `question`",
        value="Mentionne-moi avec une question — je reponds directement.",
        inline=False,
    )

    embed.set_footer(text="SLY-COMMAND | Cooper Building")
    await interaction.response.send_message(embed=embed)


@tree.command(name="status", description="Statut du bot SLY — uptime, modele, latence")
async def cmd_status(interaction: discord.Interaction):
    """Show bot status."""
    uptime_seconds = int(time.monotonic() - start_time)
    hours, remainder = divmod(uptime_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    uptime_str = f"{hours}h {minutes}m {seconds}s"

    latency_ms = round(bot.latency * 1000, 1)
    guild_count = len(bot.guilds)

    embed = discord.Embed(
        title="Statut SLY",
        color=COLOR_GREEN,
        timestamp=datetime.now(timezone.utc),
    )
    embed.set_author(name="SLY")

    embed.add_field(name="Uptime", value=uptime_str, inline=True)
    embed.add_field(name="Latence", value=f"{latency_ms} ms", inline=True)
    embed.add_field(name="Serveurs", value=str(guild_count), inline=True)
    embed.add_field(name="Modele IA", value=GROQ_MODEL, inline=True)
    embed.add_field(name="API", value="Groq (gratuit)", inline=True)
    embed.add_field(name="Python", value=f"{sys.version_info.major}.{sys.version_info.minor}", inline=True)

    embed.set_footer(text="SLY-COMMAND | Cooper Building")
    await interaction.response.send_message(embed=embed)


# ---------------------------------------------------------------------------
# Graceful shutdown
# ---------------------------------------------------------------------------

async def shutdown():
    """Clean shutdown: close HTTP session and bot."""
    print("\n[SLY] Arret en cours...")
    if http_session and not http_session.closed:
        await http_session.close()
    await bot.close()
    print("[SLY] Deconnecte. A plus.")


def handle_sigint(*_):
    """Handle Ctrl+C gracefully."""
    asyncio.get_event_loop().create_task(shutdown())


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    if not DISCORD_TOKEN:
        print("=" * 60)
        print("  ERREUR : DISCORD_TOKEN manquant !")
        print("=" * 60)
        print()
        print("  1. Va sur https://discord.com/developers/applications")
        print("  2. Cree une application (ou selectionne la tienne)")
        print("  3. Onglet 'Bot' → clique 'Reset Token' → copie le token")
        print("  4. Cree un fichier .env dans ce dossier avec :")
        print()
        print("     DISCORD_TOKEN=ton_token_ici")
        print()
        print("  5. Pour inviter le bot sur ton serveur :")
        print("     Onglet 'OAuth2' → 'URL Generator'")
        print("     Scopes: bot, applications.commands")
        print("     Permissions: Send Messages, Use Slash Commands,")
        print("                  Embed Links, Read Message History")
        print("     → copie l'URL et ouvre-la dans ton navigateur")
        print()
        print("  6. Relance : python bot.py")
        print("=" * 60)
        sys.exit(1)

    # Register SIGINT handler for graceful shutdown
    signal.signal(signal.SIGINT, handle_sigint)

    print("[SLY] Demarrage du bot Discord...")
    print(f"[SLY] Modele IA : {GROQ_MODEL}")
    bot.run(DISCORD_TOKEN, log_handler=None)


if __name__ == "__main__":
    main()
