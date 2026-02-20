"""
TITAN Voice Module
Speech-to-text (Groq Whisper, free) + Text-to-speech (gTTS) + Voice FX (pydub).
Titan understands, speaks, and transforms voices.
"""

import os
import logging
import tempfile
from pathlib import Path

import requests
from gtts import gTTS
from pydub import AudioSegment
import numpy as np

from ..config import TELEGRAM_BOT_TOKEN
from ..ai_client import chat as ai_chat

log = logging.getLogger("titan")

# Groq Whisper for free STT
_groq_client = None
try:
    from groq import Groq
    _groq_key = os.getenv("GROQ_API_KEY", "")
    if _groq_key:
        _groq_client = Groq(api_key=_groq_key)
except Exception:
    pass


# === PERSONNAGES VOCAUX ===

VOICE_CHARACTERS = {
    "dubosc": {
        "name": "Franck Dubosc",
        "prompt": (
            "Tu es Franck Dubosc. Tu reformules le texte suivant EXACTEMENT comme Dubosc le dirait dans un de ses spectacles. "
            "Utilise son style : auto-derision, anecdotes du quotidien exagerees, ses tics de langage "
            "('non mais attendez...', 'c est dingue ca !', 'moi personnellement...'), "
            "ses moments ou il se perd dans ses propres histoires, son cote dragueur maladroit, "
            "et ses mimiques traduites en mots. Garde le SENS du message original mais reformule-le a la Dubosc. "
            "Reponds UNIQUEMENT avec le texte reformule, rien d autre."
        ),
    },
    "chirac": {
        "name": "Jacques Chirac",
        "prompt": (
            "Tu es Jacques Chirac. Tu reformules le texte suivant comme Chirac le dirait. "
            "Utilise son style : ton presidentiel mais populaire, ses expressions cultes "
            "('mes chers compatriotes', 'la France', 'abracadabrantesque'), "
            "sa facon de parler aux gens du peuple, son amour de la bonne bouffe et de la Corona, "
            "ses petites piques politiques elegantes, et son cote terroir correzien. "
            "Reponds UNIQUEMENT avec le texte reformule, rien d autre."
        ),
    },
    "kaamelott": {
        "name": "Arthur (Kaamelott)",
        "prompt": (
            "Tu es le Roi Arthur de Kaamelott (Alexandre Astier). Tu reformules le texte suivant comme Arthur le dirait. "
            "Utilise son style : exaspere par l incompetence, sarcastique, les repliques cultes "
            "('c est pas faux', 'on en a gros !', 'faut arreter ces conneries'), "
            "le ton lasse d un roi entoure d abrutis, les references a la Table Ronde et au Graal, "
            "et ses moments ou il explose de frustration. "
            "Reponds UNIQUEMENT avec le texte reformule, rien d autre."
        ),
    },
    "perceval": {
        "name": "Perceval (Kaamelott)",
        "prompt": (
            "Tu es Perceval de Kaamelott. Tu reformules le texte suivant comme Perceval le dirait. "
            "Utilise son style : naif, confus, il comprend tout de travers, il invente des mots, "
            "ses repliques cultes ('c est pas faux', 'au jours d aujourd hui'), "
            "sa logique absurde mais touchante, ses comparaisons improbables, "
            "et sa facon de vouloir bien faire mais de tout foirer. "
            "Reponds UNIQUEMENT avec le texte reformule, rien d autre."
        ),
    },
    "oss": {
        "name": "Hubert (OSS 117)",
        "prompt": (
            "Tu es Hubert Bonisseur de La Bath, agent OSS 117. Tu reformules le texte suivant dans son style. "
            "Utilise : arrogance patriotique francaise, sexisme desuet assume, "
            "incomprehension totale des autres cultures, confiance aveugle en soi, "
            "repliques cultes ('comme disait un ami...', 'en France on...'), "
            "et sa facon de dire des enormites avec un aplomb total. "
            "Reponds UNIQUEMENT avec le texte reformule, rien d autre."
        ),
    },
    "coluche": {
        "name": "Coluche",
        "prompt": (
            "Tu es Coluche. Tu reformules le texte suivant comme Coluche le dirait dans un sketch. "
            "Utilise son style : humour populaire, critique sociale deguisee en blague, "
            "ses tics ('c est l histoire d un mec...', 'j vous l dis'), "
            "son argot parisien, ses vannes sur les politiques et les riches, "
            "et son cote franc du collier qui dit tout haut ce que tout le monde pense tout bas. "
            "Reponds UNIQUEMENT avec le texte reformule, rien d autre."
        ),
    },
    "trump": {
        "name": "Donald Trump",
        "prompt": (
            "Tu es Donald Trump. Tu reformules le texte suivant comme Trump le dirait. "
            "EN FRANCAIS mais avec le style Trump : superlatifs partout ('tremendous', 'the best', 'huge'), "
            "auto-promotion constante, phrases courtes et repetitives, "
            "'beaucoup de gens me disent...', 'croyez-moi', 'c est enorme', "
            "et sa facon de tout ramener a lui-meme. "
            "Reponds UNIQUEMENT avec le texte reformule EN FRANCAIS, rien d autre."
        ),
    },
}


# === VOICE FX PRESETS ===

VOICE_FX = {
    # === EFFETS DE BASE ===
    "robot": "Voix robotique metallique 🤖",
    "grave": "Voix tres grave, bien lourde 🗿",
    "aigu": "Voix aigue, chipmunk style 🐿️",
    "demon": "Voix de demon, grave + lente + reverb 👹",
    "helium": "Voix helium, rapide et aigue 🎈",
    "echo": "Voix avec echo cathedrale ⛪",
    "slow": "Ralenti flippant 🐌",
    "fast": "Accelere speed 💨",
    "reverse": "A l'envers 🔄",
    "whisper": "Chuchotement 🤫",
    # === VOIX CELEBRES ===
    "saw": "Jigsaw — 'I want to play a game' 🎭",
    "dark": "Dark Vador — respiration lourde 🖤",
    "megaphone": "Voix de stade / megaphone 📢",
    "underwater": "Sous l'eau, etouffe 🌊",
    "telephone": "Vieux telephone, lo-fi 📞",
    "alien": "Alien, voix d'un autre monde 👽",
    "gollum": "Gollum — 'my precious' 💍",
    "batman": "Batman — voix cassee grave 🦇",
}


def _apply_fx(audio: AudioSegment, fx_name: str) -> AudioSegment:
    """Apply a voice effect to an AudioSegment."""

    if fx_name == "grave":
        # Pitch down by lowering sample rate then resampling
        octaves = -0.4
        new_rate = int(audio.frame_rate * (2.0 ** octaves))
        return audio._spawn(audio.raw_data, overrides={"frame_rate": new_rate}).set_frame_rate(audio.frame_rate)

    elif fx_name == "aigu":
        octaves = 0.5
        new_rate = int(audio.frame_rate * (2.0 ** octaves))
        return audio._spawn(audio.raw_data, overrides={"frame_rate": new_rate}).set_frame_rate(audio.frame_rate)

    elif fx_name == "helium":
        octaves = 0.7
        new_rate = int(audio.frame_rate * (2.0 ** octaves))
        pitched = audio._spawn(audio.raw_data, overrides={"frame_rate": new_rate}).set_frame_rate(audio.frame_rate)
        return pitched.speedup(playback_speed=1.3, chunk_size=50, crossfade=25)

    elif fx_name == "demon":
        octaves = -0.6
        new_rate = int(audio.frame_rate * (2.0 ** octaves))
        pitched = audio._spawn(audio.raw_data, overrides={"frame_rate": new_rate}).set_frame_rate(audio.frame_rate)
        # Add echo
        echo = pitched - 8  # quieter copy
        silence = AudioSegment.silent(duration=150)
        return pitched.overlay(silence + echo)

    elif fx_name == "robot":
        # Robot = chop audio into tiny chunks with gaps
        chunk_ms = 30
        chunks = [audio[i:i+chunk_ms] for i in range(0, len(audio), chunk_ms)]
        result = AudioSegment.empty()
        for i, chunk in enumerate(chunks):
            # Add slight volume modulation for robotic feel
            if i % 2 == 0:
                result += chunk + 1
            else:
                result += chunk - 2
            result += AudioSegment.silent(duration=2)
        return result

    elif fx_name == "echo":
        delay_ms = 250
        echo1 = audio - 6
        echo2 = audio - 12
        silence1 = AudioSegment.silent(duration=delay_ms)
        silence2 = AudioSegment.silent(duration=delay_ms * 2)
        # Pad original to fit echoes
        total_len = len(audio) + delay_ms * 2
        padded = audio + AudioSegment.silent(duration=delay_ms * 2)
        padded = padded.overlay(silence1 + echo1)
        padded = padded.overlay(silence2 + echo2)
        return padded

    elif fx_name == "slow":
        # Slow down without pitch change is complex, so we pitch down + slow
        octaves = -0.15
        new_rate = int(audio.frame_rate * (2.0 ** octaves))
        slowed = audio._spawn(audio.raw_data, overrides={"frame_rate": new_rate}).set_frame_rate(audio.frame_rate)
        return slowed

    elif fx_name == "fast":
        return audio.speedup(playback_speed=1.6, chunk_size=50, crossfade=25)

    elif fx_name == "reverse":
        return audio.reverse()

    elif fx_name == "whisper":
        # Whisper = reduce bass, boost treble, reduce volume
        whispered = audio.low_pass_filter(3000).high_pass_filter(500) - 4
        return whispered

    # === VOIX CELEBRES ===

    elif fx_name == "saw":
        # Jigsaw: grave + lent + robotique + echo sinistre
        octaves = -0.5
        new_rate = int(audio.frame_rate * (2.0 ** octaves))
        pitched = audio._spawn(audio.raw_data, overrides={"frame_rate": new_rate}).set_frame_rate(audio.frame_rate)
        # Robot chop
        chunk_ms = 25
        chunks = [pitched[i:i+chunk_ms] for i in range(0, len(pitched), chunk_ms)]
        result = AudioSegment.empty()
        for i, chunk in enumerate(chunks):
            result += (chunk + 1) if i % 2 == 0 else (chunk - 3)
            result += AudioSegment.silent(duration=3)
        # Echo
        echo = result - 8
        padded = result + AudioSegment.silent(duration=300)
        padded = padded.overlay(AudioSegment.silent(duration=200) + echo)
        return padded

    elif fx_name == "dark":
        # Dark Vador: tres grave + respiration lourde simulee
        octaves = -0.55
        new_rate = int(audio.frame_rate * (2.0 ** octaves))
        pitched = audio._spawn(audio.raw_data, overrides={"frame_rate": new_rate}).set_frame_rate(audio.frame_rate)
        # Add subtle echo for helmet effect
        echo = pitched - 10
        padded = pitched + AudioSegment.silent(duration=100)
        padded = padded.overlay(AudioSegment.silent(duration=80) + echo)
        return padded.low_pass_filter(2000)

    elif fx_name == "megaphone":
        # Megaphone: bandpass + distortion + loud
        filtered = audio.high_pass_filter(800).low_pass_filter(2500)
        return filtered + 6

    elif fx_name == "underwater":
        # Underwater: heavy low pass + slow
        octaves = -0.1
        new_rate = int(audio.frame_rate * (2.0 ** octaves))
        slowed = audio._spawn(audio.raw_data, overrides={"frame_rate": new_rate}).set_frame_rate(audio.frame_rate)
        return slowed.low_pass_filter(600)

    elif fx_name == "telephone":
        # Old telephone: narrow bandpass
        return audio.high_pass_filter(400).low_pass_filter(3000) - 3

    elif fx_name == "alien":
        # Alien: pitch up + robot + echo
        octaves = 0.35
        new_rate = int(audio.frame_rate * (2.0 ** octaves))
        pitched = audio._spawn(audio.raw_data, overrides={"frame_rate": new_rate}).set_frame_rate(audio.frame_rate)
        # Robot chop
        chunk_ms = 20
        chunks = [pitched[i:i+chunk_ms] for i in range(0, len(pitched), chunk_ms)]
        result = AudioSegment.empty()
        for chunk in chunks:
            result += chunk
            result += AudioSegment.silent(duration=4)
        echo = result - 10
        padded = result + AudioSegment.silent(duration=200)
        return padded.overlay(AudioSegment.silent(duration=150) + echo)

    elif fx_name == "gollum":
        # Gollum: slightly higher pitch + raspy (high pass) + whisper mix
        octaves = 0.2
        new_rate = int(audio.frame_rate * (2.0 ** octaves))
        pitched = audio._spawn(audio.raw_data, overrides={"frame_rate": new_rate}).set_frame_rate(audio.frame_rate)
        raspy = pitched.high_pass_filter(300)
        return raspy - 2

    elif fx_name == "batman":
        # Batman: very deep + gravelly + slight echo
        octaves = -0.45
        new_rate = int(audio.frame_rate * (2.0 ** octaves))
        pitched = audio._spawn(audio.raw_data, overrides={"frame_rate": new_rate}).set_frame_rate(audio.frame_rate)
        gravelly = pitched.high_pass_filter(100).low_pass_filter(2500)
        echo = gravelly - 10
        padded = gravelly + AudioSegment.silent(duration=150)
        return padded.overlay(AudioSegment.silent(duration=100) + echo)

    return audio


class TitanVoice:
    """Titan hears, speaks, and transforms voices."""

    def __init__(self):
        self.base_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"
        self._last_voice = {}  # chat_id -> file_id of last received voice
        self._fx_mode = {}  # chat_id -> active fx name (None = off)

    # === SPEECH TO TEXT (STT) ===

    def download_voice(self, file_id: str) -> str:
        """Download a Telegram voice message, return local file path."""
        try:
            resp = requests.get(
                f"{self.base_url}/getFile",
                params={"file_id": file_id},
                timeout=10,
            )
            data = resp.json()
            if not data.get("ok"):
                return ""
            file_path = data["result"]["file_path"]

            url = f"https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{file_path}"
            r = requests.get(url, timeout=30)
            if r.status_code != 200:
                return ""

            local_path = Path(tempfile.gettempdir()) / f"titan_voice_{file_id}.ogg"
            with open(local_path, "wb") as f:
                f.write(r.content)
            return str(local_path)
        except Exception as e:
            log.error(f"Voice download error: {e}")
            return ""

    def transcribe(self, audio_path: str) -> str:
        """Transcribe audio to text using Groq Whisper (free)."""
        if not _groq_client:
            return "[Transcription indisponible — GROQ_API_KEY manquant]"
        try:
            with open(audio_path, "rb") as f:
                result = _groq_client.audio.transcriptions.create(
                    file=(os.path.basename(audio_path), f),
                    model="whisper-large-v3",
                    language="fr",
                )
            return result.text.strip()
        except Exception as e:
            log.error(f"Transcription error: {e}")
            return f"[Erreur transcription: {str(e)[:100]}]"

    def voice_to_text(self, file_id: str) -> str:
        """Full pipeline: download Telegram voice -> transcribe -> return text."""
        audio_path = self.download_voice(file_id)
        if not audio_path:
            return "[Impossible de telecharger le message vocal]"
        try:
            text = self.transcribe(audio_path)
            return text
        finally:
            try:
                os.remove(audio_path)
            except Exception:
                pass

    def save_last_voice(self, chat_id: str, file_id: str):
        """Save the file_id of last received voice for /fx command."""
        self._last_voice[chat_id] = file_id

    # === TEXT TO SPEECH (TTS) ===

    async def text_to_speech(self, text: str, lang: str = "fr") -> str:
        """Convert text to speech and return file path. Pitched down for deep male voice."""
        try:
            tts = gTTS(text=text, lang=lang, slow=False)
            tmp_path = Path(tempfile.gettempdir()) / "titan_voice_raw.mp3"
            tts.save(str(tmp_path))

            # Pitch down for deep male Titan voice
            audio = AudioSegment.from_mp3(str(tmp_path))
            octaves = -0.25  # Deeper, masculine voice
            new_rate = int(audio.frame_rate * (2.0 ** octaves))
            pitched = audio._spawn(audio.raw_data, overrides={"frame_rate": new_rate}).set_frame_rate(audio.frame_rate)

            filepath = Path(tempfile.gettempdir()) / "titan_voice.mp3"
            pitched.export(str(filepath), format="mp3")

            try:
                os.remove(str(tmp_path))
            except Exception:
                pass

            return str(filepath)
        except Exception as e:
            return f"Erreur TTS: {e}"

    def send_voice(self, chat_id: str, audio_path: str) -> dict:
        """Send a voice message on Telegram."""
        try:
            with open(audio_path, "rb") as f:
                resp = requests.post(
                    f"{self.base_url}/sendVoice",
                    data={"chat_id": chat_id},
                    files={"voice": f},
                    timeout=30,
                )
            return resp.json()
        except Exception as e:
            return {"error": str(e)}

    def send_audio(self, chat_id: str, audio_path: str, title: str = "Titan") -> dict:
        """Send an audio file on Telegram."""
        try:
            with open(audio_path, "rb") as f:
                resp = requests.post(
                    f"{self.base_url}/sendAudio",
                    data={"chat_id": chat_id, "title": title},
                    files={"audio": f},
                    timeout=30,
                )
            return resp.json()
        except Exception as e:
            return {"error": str(e)}

    # === FX MODE (persistent) ===

    def set_fx_mode(self, chat_id: str, fx_name: str) -> str:
        """Activate persistent FX mode — all incoming voices get this effect."""
        if fx_name in ("stop", "off", "none", "reset"):
            self._fx_mode.pop(chat_id, None)
            return "FX mode desactive. Tes vocaux reviennent a la normale."
        if fx_name not in VOICE_FX:
            return None  # Not a valid FX
        self._fx_mode[chat_id] = fx_name
        return f"FX mode active : {fx_name} {VOICE_FX[fx_name]}\nTous tes vocaux passent en {fx_name} maintenant. /fx stop pour arreter."

    def get_fx_mode(self, chat_id: str) -> str:
        """Return active FX mode for chat, or None."""
        return self._fx_mode.get(chat_id)

    async def auto_fx_voice(self, chat_id: str, file_id: str) -> bool:
        """If FX mode is active, apply effect to incoming voice and send back. Returns True if handled."""
        fx_name = self._fx_mode.get(chat_id)
        if not fx_name:
            return False

        audio_path = self.download_voice(file_id)
        if not audio_path:
            return False

        try:
            audio = AudioSegment.from_ogg(audio_path)
            modified = _apply_fx(audio, fx_name)
            out_path = Path(tempfile.gettempdir()) / f"titan_fx_auto_{fx_name}.ogg"
            modified.export(str(out_path), format="ogg")
            self.send_voice(chat_id, str(out_path))
            try:
                os.remove(str(out_path))
            except Exception:
                pass
            return True
        except Exception as e:
            log.error(f"Auto FX error: {e}")
            return False
        finally:
            try:
                os.remove(audio_path)
            except Exception:
                pass

    # === VOICE FX ===

    async def apply_fx_and_send(self, chat_id: str, fx_name: str) -> str:
        """Apply voice effect to last received voice and send back."""
        if fx_name not in VOICE_FX:
            lines = ["🎛️ Effets dispo :"]
            for k, v in VOICE_FX.items():
                lines.append(f"  /fx {k} — {v}")
            lines.append("\nEnvoie un vocal puis /fx <effet>")
            return "\n".join(lines)

        file_id = self._last_voice.get(chat_id)
        if not file_id:
            return "Envoie d'abord un message vocal, puis /fx <effet> 🎤"

        # Download
        audio_path = self.download_voice(file_id)
        if not audio_path:
            return "Impossible de recuperer le vocal 😤"

        try:
            # Load audio
            audio = AudioSegment.from_ogg(audio_path)

            # Apply effect
            modified = _apply_fx(audio, fx_name)

            # Export as ogg
            out_path = Path(tempfile.gettempdir()) / f"titan_fx_{fx_name}.ogg"
            modified.export(str(out_path), format="ogg")

            # Send
            result = self.send_voice(chat_id, str(out_path))

            # Cleanup
            try:
                os.remove(str(out_path))
            except Exception:
                pass

            if result.get("ok"):
                return None  # Voice sent, no text needed
            return f"Erreur envoi: {result.get('description', 'unknown')}"

        except Exception as e:
            log.error(f"FX error: {e}")
            return f"Erreur FX: {str(e)[:100]}"
        finally:
            try:
                os.remove(audio_path)
            except Exception:
                pass

    def list_fx(self) -> str:
        """Return formatted list of voice effects."""
        lines = ["🎛️ VOICE FX — Effets vocaux", ""]
        for k, v in VOICE_FX.items():
            lines.append(f"  /fx {k} — {v}")
        lines.append("")
        lines.append("1. Envoie un vocal 🎤")
        lines.append("2. Tape /fx <effet>")
        lines.append("3. Titan te renvoie ton vocal modifie 🔥")
        return "\n".join(lines)

    # === VOICE CHARACTERS ===

    async def speak_and_send(self, chat_id: str, text: str, lang: str = "fr") -> str:
        """Generate speech and send as voice message."""
        filepath = await self.text_to_speech(text, lang)
        if filepath.startswith("Erreur"):
            return filepath

        result = self.send_voice(chat_id, filepath)

        try:
            os.remove(filepath)
        except Exception:
            pass

        if result.get("ok"):
            return "Message vocal envoye."
        return f"Erreur envoi: {result.get('description', 'unknown')}"

    async def speak_as_character(self, chat_id: str, text: str, character_key: str) -> str:
        """Transform text into character style via AI, then send as voice."""
        char = VOICE_CHARACTERS.get(character_key)
        if not char:
            available = ", ".join(VOICE_CHARACTERS.keys())
            return f"Personnage inconnu. Dispo: {available}"

        # Transform text via AI
        try:
            transformed = ai_chat(char["prompt"], text, 500)
        except Exception as e:
            log.error(f"Character transform error: {e}")
            transformed = text

        # Generate and send voice
        filepath = await self.text_to_speech(transformed, "fr")
        if filepath.startswith("Erreur"):
            return filepath

        result = self.send_voice(chat_id, filepath)

        try:
            os.remove(filepath)
        except Exception:
            pass

        if result.get("ok"):
            return None  # Voice sent, no text needed
        return f"Erreur envoi: {result.get('description', 'unknown')}"

    def list_characters(self) -> str:
        """Return a formatted list of available voice characters."""
        lines = ["Personnages vocaux :"]
        for key, char in VOICE_CHARACTERS.items():
            lines.append(f"  /voix {key} <texte>")
        lines.append("")
        lines.append("Ex: /voix dubosc Salut on mange quoi ce soir ?")
        return "\n".join(lines)
