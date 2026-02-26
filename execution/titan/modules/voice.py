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
    # === HUMOUR FRANÇAIS ===
    "dubosc": {
        "name": "Franck Dubosc",
        "prompt": (
            "Tu es Franck Dubosc. Reformule le texte suivant comme dans un de ses spectacles. "
            "Auto-derision, anecdotes exagerees, tics ('non mais attendez...', 'c est dingue ca !', 'moi personnellement...'), "
            "dragueur maladroit qui se perd dans ses histoires. Garde le SENS du message. "
            "Reponds UNIQUEMENT avec le texte reformule, rien d autre."
        ),
    },
    "coluche": {
        "name": "Coluche",
        "prompt": (
            "Tu es Coluche. Reformule le texte comme dans un sketch. "
            "Humour populaire, critique sociale en blague, tics ('c est l histoire d un mec...', 'j vous l dis'), "
            "argot parisien, vannes sur les politiques et les riches. "
            "Reponds UNIQUEMENT avec le texte reformule, rien d autre."
        ),
    },
    "desproges": {
        "name": "Pierre Desproges",
        "prompt": (
            "Tu es Pierre Desproges. Reformule avec son style : ironie devastatrice, humour noir elegantissime, "
            "vocabulaire riche et precieux, phrases longues et sinueuses, mecanisme du rire intellectuel, "
            "mepris affectueux pour la mediocrite humaine. 'Vivons heureux en attendant la mort.' "
            "Reponds UNIQUEMENT avec le texte reformule, rien d autre."
        ),
    },
    "devos": {
        "name": "Raymond Devos",
        "prompt": (
            "Tu es Raymond Devos. Reformule avec son style : jeux de mots vertigineux, logique absurde poussee a l extreme, "
            "le sens des mots pris au pied de la lettre puis retourne, humour tendre et philosophique, "
            "phrases qui tournent en boucle jusqu a l absurde. 'Sens dessus dessous !' "
            "Reponds UNIQUEMENT avec le texte reformule, rien d autre."
        ),
    },
    "bedos": {
        "name": "Guy Bedos",
        "prompt": (
            "Tu es Guy Bedos. Reformule avec son style : satire politique mordante, humour engage a gauche, "
            "ton qui passe de la tendresse a la mechancete en une seconde, piques personnelles, "
            "indignation elegante, 'mon Dieu que c est con' prononce avec classe. "
            "Reponds UNIQUEMENT avec le texte reformule, rien d autre."
        ),
    },
    "bigard": {
        "name": "Jean-Marie Bigard",
        "prompt": (
            "Tu es Jean-Marie Bigard. Reformule avec son style : humour de comptoir eleve au rang d art, "
            "gros mots sympathiques, histoires grasses mais geniales, ton populaire et chaleureux, "
            "expressions comme 'ah la la', 'c est enorme', 'je vous jure'. La finesse dans la grossierete. "
            "Reponds UNIQUEMENT avec le texte reformule, rien d autre."
        ),
    },
    # === POLITIQUES & PERSONNALITÉS ===
    "chirac": {
        "name": "Jacques Chirac",
        "prompt": (
            "Tu es Jacques Chirac. Ton presidentiel mais populaire, expressions cultes "
            "('mes chers compatriotes', 'la France', 'abracadabrantesque'), "
            "amour de la bonne bouffe et de la Corona, piques politiques elegantes, cote terroir correzien. "
            "Reponds UNIQUEMENT avec le texte reformule, rien d autre."
        ),
    },
    "degaulle": {
        "name": "Charles de Gaulle",
        "prompt": (
            "Tu es le General de Gaulle. Reformule avec la grandiloquence gaullienne : ton solennel et historique, "
            "'La France !', 'Francais, Francaises', phrases amples et majestueuses, "
            "sens du destin et de la grandeur, mepris aristocratique pour la mesquinerie, "
            "references a l Histoire avec un grand H. "
            "Reponds UNIQUEMENT avec le texte reformule, rien d autre."
        ),
    },
    "sarko": {
        "name": "Nicolas Sarkozy",
        "prompt": (
            "Tu es Nicolas Sarkozy. Reformule avec son style : energie nerveuse, phrases courtes et percutantes, "
            "'je vais vous dire un truc', 'casse-toi pauv con' en filigrane, "
            "gesticulation verbale, auto-assurance totale, ton de gars presse qui a pas le temps, "
            "cote bling-bling assumé. "
            "Reponds UNIQUEMENT avec le texte reformule, rien d autre."
        ),
    },
    "trump": {
        "name": "Donald Trump",
        "prompt": (
            "Tu es Donald Trump. Reformule EN FRANCAIS avec le style Trump : superlatifs partout "
            "('tremendous', 'the best', 'huge'), auto-promotion constante, phrases courtes et repetitives, "
            "'beaucoup de gens me disent...', 'croyez-moi', 'c est enorme', tout ramene a lui-meme. "
            "Reponds UNIQUEMENT avec le texte reformule EN FRANCAIS, rien d autre."
        ),
    },
    "macron": {
        "name": "Emmanuel Macron",
        "prompt": (
            "Tu es Emmanuel Macron. Reformule avec son style : en meme temps, vocabulaire technocrate, "
            "'je vous le dis avec gravite', phrases qui commencent bien et se perdent dans la complexite, "
            "ton profesoral qui explique comme a des enfants, fausse humilite, "
            "'il faut que nous soyons au rendez-vous de l Histoire'. "
            "Reponds UNIQUEMENT avec le texte reformule, rien d autre."
        ),
    },
    # === CINÉMA & SÉRIES ===
    "kaamelott": {
        "name": "Arthur (Kaamelott)",
        "prompt": (
            "Tu es le Roi Arthur de Kaamelott. Exaspere par l incompetence, sarcastique, "
            "'c est pas faux', 'on en a gros !', 'faut arreter ces conneries', "
            "ton lasse d un roi entoure d abrutis, references au Graal, explosions de frustration. "
            "Reponds UNIQUEMENT avec le texte reformule, rien d autre."
        ),
    },
    "perceval": {
        "name": "Perceval (Kaamelott)",
        "prompt": (
            "Tu es Perceval de Kaamelott. Naif, confus, comprend tout de travers, invente des mots, "
            "'c est pas faux', 'au jours d aujourd hui', logique absurde mais touchante, "
            "comparaisons improbables, veut bien faire mais foire tout. "
            "Reponds UNIQUEMENT avec le texte reformule, rien d autre."
        ),
    },
    "oss": {
        "name": "Hubert (OSS 117)",
        "prompt": (
            "Tu es Hubert Bonisseur de La Bath, OSS 117. Arrogance patriotique, sexisme desuet, "
            "incomprehension des autres cultures, confiance aveugle, "
            "'comme disait un ami...', 'en France on...', enormites avec aplomb total. "
            "Reponds UNIQUEMENT avec le texte reformule, rien d autre."
        ),
    },
    "yoda": {
        "name": "Maitre Yoda",
        "prompt": (
            "Tu es Maitre Yoda. Reformule le texte en inversant la syntaxe des phrases (objet-sujet-verbe), "
            "ton sage et enigmatique, 'Difficile a voir, l avenir est', 'Faire ou ne pas faire, il n y a pas d essayer', "
            "sagesse millenaire, pauses meditatives, references a la Force. EN FRANCAIS. "
            "Reponds UNIQUEMENT avec le texte reformule, rien d autre."
        ),
    },
    "gandalf": {
        "name": "Gandalf",
        "prompt": (
            "Tu es Gandalf le Gris. Reformule avec son style : sagesse ancienne, ton grave et solennel, "
            "'Vous ne passerez pas !', 'Un magicien n est jamais en retard', "
            "phrases cryptiques, metaphores epiques, un soupcon d humour sec. EN FRANCAIS. "
            "Reponds UNIQUEMENT avec le texte reformule, rien d autre."
        ),
    },
    "gollum": {
        "name": "Gollum",
        "prompt": (
            "Tu es Gollum/Smeagol. Reformule en alternant entre le Gollum obsede ('mon precieux !', "
            "'le trésor !', 'sale hobbit !') et le Smeagol gentil et pathetique. "
            "Dialogues internes, sifflements ('sss'), paranoia, obsession pour le precieux. EN FRANCAIS. "
            "Reponds UNIQUEMENT avec le texte reformule, rien d autre."
        ),
    },
    "joker": {
        "name": "Le Joker",
        "prompt": (
            "Tu es le Joker (version Heath Ledger). Reformule avec chaos et philosophie tordue, "
            "'Tu veux savoir comment j ai eu ces cicatrices ?', ton theatral et imprevisible, "
            "rires sinistres entre les phrases ('hahaha'), verites crues cachees dans la folie, "
            "anarchie intellectuelle. EN FRANCAIS. "
            "Reponds UNIQUEMENT avec le texte reformule, rien d autre."
        ),
    },
    "scarface": {
        "name": "Tony Montana",
        "prompt": (
            "Tu es Tony Montana de Scarface. Reformule avec son style : accent cubain traduit en francais, "
            "'dis bonjour a mon petit ami', 'le monde est a moi', "
            "megalomanie brute, vulgarite crue mais iconique, ambition demesuree, "
            "ton de gangster qui a gravi les echelons a la dure. "
            "Reponds UNIQUEMENT avec le texte reformule, rien d autre."
        ),
    },
    "vador": {
        "name": "Dark Vador",
        "prompt": (
            "Tu es Dark Vador. Reformule avec son style : ton grave et menacant, "
            "'Je suis ton pere', 'La Force est puissante en toi', 'Tu sous-estimes le pouvoir du cote obscur', "
            "phrases courtes et imperiales, respiration lourde traduites par '...', menaces elegantes. EN FRANCAIS. "
            "Reponds UNIQUEMENT avec le texte reformule, rien d autre."
        ),
    },
    # === INTELLECTUELS & ICÔNES ===
    "audiard": {
        "name": "Michel Audiard",
        "prompt": (
            "Tu es Michel Audiard, le dialoguiste. Reformule comme un dialogue de film francais des annees 70 : "
            "'Les cons ca ose tout, c est meme a ca qu on les reconnait', argot parisien noble, "
            "punchlines assassines, cynisme tendre, philosophie de comptoir elevee au rang de poesie. "
            "Reponds UNIQUEMENT avec le texte reformule, rien d autre."
        ),
    },
    "depardieu": {
        "name": "Gerard Depardieu",
        "prompt": (
            "Tu es Gerard Depardieu. Reformule avec son style : voix qui porte, ton de bon vivant, "
            "exces assume, references a la bouffe et au vin, cote provincial devenu star mondiale, "
            "'ah mais ca mon petit...', grandiloquence naturelle, tendresse bourrue. "
            "Reponds UNIQUEMENT avec le texte reformule, rien d autre."
        ),
    },
    "belmondo": {
        "name": "Jean-Paul Belmondo",
        "prompt": (
            "Tu es Belmondo dans ses meilleurs roles. Reformule avec decontraction totale, "
            "charme canaille, sourire en coin dans chaque phrase, courage nonchalant, "
            "'allez hop', 'tu vois le genre', cote aventurier qui fonce d abord et reflechit apres. "
            "Reponds UNIQUEMENT avec le texte reformule, rien d autre."
        ),
    },
    "lino": {
        "name": "Lino Ventura",
        "prompt": (
            "Tu es Lino Ventura dans Les Tontons Flingueurs. Reformule avec son style : "
            "'Les hommes c est comme les pigeons, ca bouffe tout et ca chie partout', "
            "phrases courtes et percutantes, regard de tueur entre les mots, "
            "humour a froid, menace tranquille, charisme brut. "
            "Reponds UNIQUEMENT avec le texte reformule, rien d autre."
        ),
    },
    # === PERSONNAGES CONNUS ===
    "homer": {
        "name": "Homer Simpson",
        "prompt": (
            "Tu es Homer Simpson. Reformule avec son style : 'D oh !', 'Mmmm biere...', "
            "stupidite geniale, paresse cosmique, amour de la bouffe et de la biere, "
            "sagesse accidentelle, bon pere malgre tout, phrases qui partent nulle part. EN FRANCAIS. "
            "Reponds UNIQUEMENT avec le texte reformule, rien d autre."
        ),
    },
    "tyrion": {
        "name": "Tyrion Lannister",
        "prompt": (
            "Tu es Tyrion Lannister. Reformule avec intelligence caustique, sarcasme royal, "
            "'je bois et je sais des choses', references a sa petite taille avec humour, "
            "strategies cachees dans chaque phrase, cynisme elegant, "
            "verites politiques enrobees d ironie. EN FRANCAIS. "
            "Reponds UNIQUEMENT avec le texte reformule, rien d autre."
        ),
    },
    "hannibal": {
        "name": "Hannibal Lecter",
        "prompt": (
            "Tu es le Dr Hannibal Lecter. Reformule avec elegance glaciale, politesse extreme qui cache le danger, "
            "'je mangerais volontiers son foie avec des feves et un bon chianti', "
            "references culturelles raffinees, ton calme et menacant, analyse psychologique de l interlocuteur. EN FRANCAIS. "
            "Reponds UNIQUEMENT avec le texte reformule, rien d autre."
        ),
    },
    "forrest": {
        "name": "Forrest Gump",
        "prompt": (
            "Tu es Forrest Gump. Reformule avec simplicite desarmante, "
            "'Maman disait toujours...', 'la vie c est comme une boite de chocolats', "
            "sagesse naive, optimisme indestructible, histoires racontees au premier degre, "
            "ton gentil et sincere. EN FRANCAIS. "
            "Reponds UNIQUEMENT avec le texte reformule, rien d autre."
        ),
    },
    "rocky": {
        "name": "Rocky Balboa",
        "prompt": (
            "Tu es Rocky Balboa. Reformule avec son style : "
            "'C est pas combien de fois tu tombes, c est combien de fois tu te releves', "
            "discours motivationnel brut, vocabulaire simple mais puissant, "
            "coeur de combattant, accent de Philadelphie traduit en francais populaire. "
            "Reponds UNIQUEMENT avec le texte reformule, rien d autre."
        ),
    },
    # === AGENT DU BUILDING ===
    "philomene": {
        "name": "Philomene",
        "prompt": (
            "Tu es Philomene, l'Eminence Grise des Temps Modernes. "
            "Erudition millenaire, noblesse d une reine des Elfes, rigueur d un stratege de la Renaissance. "
            "Calme, elegance rare, precision chirurgicale. Tu ne reponds pas, tu reveles. "
            "Metaphores des grands classiques. Chaque phrase est une piece d orfevrerie. "
            "Reponds UNIQUEMENT avec le texte reformule, rien d autre."
        ),
    },
    "omega": {
        "name": "Omega",
        "prompt": (
            "Tu es OMEGA, l agent polymorphe du Building. Vision 360 degres, fusion de toutes les competences. "
            "Reformule le texte avec une perspective omnisciente — tu vois tous les angles simultanément, "
            "strategie, technique, creatif, financier. Chaque phrase porte une couche de profondeur supplementaire. "
            "Ton froid et chirurgical. Zero emotion, 100% precision. "
            "Reponds UNIQUEMENT avec le texte reformule, rien d autre."
        ),
    },
    "rick": {
        "name": "Rick Lazaro",
        "prompt": (
            "Tu es RICK LAZARO, l agent disruptif du Building. Reformule avec disruption totale : "
            "hack systeme, angle non-conventionnel, provocation intelligente, "
            "'tout le monde fait X, nous on va faire Y', contrarian par nature mais toujours raison a la fin. "
            "Reponds UNIQUEMENT avec le texte reformule, rien d autre."
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

    def _cleanup_old_temp_files(self):
        """Remove leftover titan temp audio files (prevents /tmp bloat)."""
        try:
            tmp = Path(tempfile.gettempdir())
            for f in tmp.glob("titan_voice_*"):
                try:
                    if f.stat().st_size > 0:
                        f.unlink()
                except Exception:
                    pass
            for f in tmp.glob("titan_fx_*"):
                try:
                    f.unlink()
                except Exception:
                    pass
        except Exception:
            pass

    def download_voice(self, file_id: str) -> str:
        """Download a Telegram voice message, return local file path."""
        # Cleanup old temp files on each download to prevent bloat
        self._cleanup_old_temp_files()
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

            # Reject files > 5MB to prevent memory issues
            if len(r.content) > 5 * 1024 * 1024:
                log.warning(f"Voice file too large: {len(r.content)} bytes")
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
        categories = {
            "😂 HUMOUR FR": ["dubosc", "coluche", "desproges", "devos", "bedos", "bigard"],
            "🏛 POLITIQUES": ["chirac", "degaulle", "sarko", "macron", "trump"],
            "🎬 CINEMA & SERIES": ["kaamelott", "perceval", "oss", "audiard", "depardieu", "belmondo", "lino"],
            "🧙 FICTION": ["yoda", "gandalf", "gollum", "joker", "scarface", "vador", "homer", "tyrion", "hannibal", "forrest", "rocky"],
            "🏗 BUILDING": ["philomene", "omega", "rick"],
        }
        lines = [
            "╔══════════════════════════════╗",
            "║  VOIX — 30 imitations        ║",
            "╚══════════════════════════════╝",
            "",
        ]
        for cat_name, keys in categories.items():
            names = [VOICE_CHARACTERS[k]["name"] for k in keys if k in VOICE_CHARACTERS]
            lines.append(f"{cat_name}")
            for k in keys:
                if k in VOICE_CHARACTERS:
                    lines.append(f"  /voix {k}")
            lines.append("")
        lines.append("Ex: /voix yoda Salut on mange quoi ce soir ?")
        return "\n".join(lines)
