"""
AI News Video Generator - Genere un mini-journal video d'1 minute
avec voix synthetisee et visuels animes.

Utilise:
- gTTS pour la synthese vocale (gratuit, bonne qualite)
- Pillow pour les images/texte
- moviepy pour l'assemblage video
"""

import os
import sys
import math
import tempfile
from datetime import datetime
from typing import List, Tuple

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# Video settings
WIDTH = 1080
HEIGHT = 1920  # Format vertical (9:16) pour les shorts/reels
FPS = 30
BG_COLOR = (15, 15, 30)
PRIMARY_COLOR = (139, 92, 246)  # Violet
SECONDARY_COLOR = (236, 72, 153)  # Rose
ACCENT_COLOR = (6, 182, 212)  # Cyan
TEXT_COLOR = (248, 250, 252)  # Blanc
MUTED_COLOR = (148, 163, 184)  # Gris


def get_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    """Charge une police systeme."""
    font_paths = [
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/segoeuib.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]

    if bold:
        bold_paths = [
            "C:/Windows/Fonts/segoeuib.ttf",
            "C:/Windows/Fonts/arialbd.ttf",
        ]
        font_paths = bold_paths + font_paths

    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue

    return ImageFont.load_default()


def wrap_text(text: str, font: ImageFont.FreeTypeFont, max_width: int) -> List[str]:
    """Decoupe le texte en lignes qui tiennent dans la largeur donnee."""
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = f"{current_line} {word}".strip()
        bbox = font.getbbox(test_line)
        text_width = bbox[2] - bbox[0]

        if text_width <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines


def create_gradient_background(width: int, height: int, t: float = 0) -> Image.Image:
    """Cree un fond degrade anime."""
    img = Image.new("RGB", (width, height))
    pixels = img.load()

    for y in range(height):
        ratio = y / height
        # Degrade du haut vers le bas avec variation temporelle
        offset = math.sin(t * 0.5) * 0.1
        r = int(15 + ratio * 20 + math.sin(ratio * 3 + t) * 10)
        g = int(15 + ratio * 10)
        b = int(30 + ratio * 40 + math.sin(ratio * 2 + t * 0.7) * 15)
        pixels[0, y] = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))

    # Copier la premiere colonne sur toutes les autres
    for x in range(1, width):
        for y in range(height):
            pixels[x, y] = pixels[0, y]

    return img


def draw_rounded_rect(draw: ImageDraw.Draw, xy: Tuple, radius: int, fill: Tuple):
    """Dessine un rectangle arrondi."""
    x1, y1, x2, y2 = xy
    draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill)
    draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill)
    draw.pieslice([x1, y1, x1 + 2 * radius, y1 + 2 * radius], 180, 270, fill=fill)
    draw.pieslice([x2 - 2 * radius, y1, x2, y1 + 2 * radius], 270, 360, fill=fill)
    draw.pieslice([x1, y2 - 2 * radius, x1 + 2 * radius, y2], 90, 180, fill=fill)
    draw.pieslice([x2 - 2 * radius, y2 - 2 * radius, x2, y2], 0, 90, fill=fill)


def create_intro_frame(t: float) -> np.ndarray:
    """Cree une frame pour l'intro."""
    img = create_gradient_background(WIDTH, HEIGHT, t)
    draw = ImageDraw.Draw(img)

    # Logo / Titre
    title_font = get_font(72, bold=True)
    sub_font = get_font(36)

    # Animation d'entree
    alpha = min(1.0, t * 2)
    y_offset = int((1 - alpha) * 50)

    # Badge "FLASH IA"
    badge_y = 600 + y_offset
    draw_rounded_rect(draw, (300, badge_y, 780, badge_y + 80), 40, PRIMARY_COLOR)
    badge_font = get_font(40, bold=True)
    bbox = badge_font.getbbox("FLASH IA")
    text_w = bbox[2] - bbox[0]
    draw.text((540 - text_w // 2, badge_y + 18), "FLASH IA", font=badge_font, fill=(255, 255, 255))

    # Titre principal
    title_y = 720 + y_offset
    title = "Actualites IA"
    bbox = title_font.getbbox(title)
    text_w = bbox[2] - bbox[0]
    draw.text((540 - text_w // 2, title_y), title, font=title_font, fill=TEXT_COLOR)

    # Sous-titre
    sub_y = 820 + y_offset
    sub = "Votre resume hebdomadaire"
    bbox = sub_font.getbbox(sub)
    text_w = bbox[2] - bbox[0]
    draw.text((540 - text_w // 2, sub_y), sub, font=sub_font, fill=MUTED_COLOR)

    # Date
    date_y = 900 + y_offset
    date_str = datetime.now().strftime("%d/%m/%Y")
    date_font = get_font(32)
    bbox = date_font.getbbox(date_str)
    text_w = bbox[2] - bbox[0]
    draw.text((540 - text_w // 2, date_y), date_str, font=date_font, fill=ACCENT_COLOR)

    # Decorations - cercles lumineux
    for i in range(3):
        cx = 200 + i * 300
        cy = 1400
        radius = int(30 + math.sin(t * 2 + i) * 10)
        color = [PRIMARY_COLOR, SECONDARY_COLOR, ACCENT_COLOR][i]
        draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=color)

    return np.array(img)


def create_news_frame(t: float, news_text: str, news_num: int, total: int) -> np.ndarray:
    """Cree une frame pour afficher une news."""
    img = create_gradient_background(WIDTH, HEIGHT, t)
    draw = ImageDraw.Draw(img)

    # Header
    header_font = get_font(32, bold=True)
    draw_rounded_rect(draw, (60, 80, 400, 140), 30, PRIMARY_COLOR)
    draw.text((100, 90), f"ACTU {news_num}/{total}", font=header_font, fill=(255, 255, 255))

    # Barre de progression
    bar_width = WIDTH - 120
    bar_x = 60
    bar_y = 170
    draw.rectangle([bar_x, bar_y, bar_x + bar_width, bar_y + 6], fill=(40, 40, 60))
    progress = news_num / total
    draw.rectangle([bar_x, bar_y, bar_x + int(bar_width * progress), bar_y + 6], fill=ACCENT_COLOR)

    # Texte de la news
    text_font = get_font(44)
    padding = 80
    max_text_width = WIDTH - 2 * padding

    lines = wrap_text(news_text, text_font, max_text_width)

    # Card background
    card_top = 240
    line_height = 65
    card_height = len(lines) * line_height + 80
    draw_rounded_rect(
        draw,
        (padding - 20, card_top, WIDTH - padding + 20, card_top + card_height),
        20,
        (25, 25, 45)
    )

    # Texte
    y = card_top + 40
    for line in lines:
        draw.text((padding, y), line, font=text_font, fill=TEXT_COLOR)
        y += line_height

    # Icone micro animee en bas
    mic_y = 1600
    mic_scale = 1 + math.sin(t * 4) * 0.1
    mic_radius = int(40 * mic_scale)
    draw.ellipse(
        [540 - mic_radius, mic_y - mic_radius, 540 + mic_radius, mic_y + mic_radius],
        fill=SECONDARY_COLOR
    )
    mic_font = get_font(40)
    draw.text((522, mic_y - 22), "🎙", font=mic_font, fill=(255, 255, 255))

    return np.array(img)


def create_outro_frame(t: float) -> np.ndarray:
    """Cree une frame pour l'outro."""
    img = create_gradient_background(WIDTH, HEIGHT, t)
    draw = ImageDraw.Draw(img)

    alpha = min(1.0, t * 2)
    y_offset = int((1 - alpha) * 30)

    # Titre
    title_font = get_font(56, bold=True)
    title_y = 700 + y_offset
    title = "A la semaine"
    bbox = title_font.getbbox(title)
    text_w = bbox[2] - bbox[0]
    draw.text((540 - text_w // 2, title_y), title, font=title_font, fill=TEXT_COLOR)

    title2 = "prochaine!"
    bbox2 = title_font.getbbox(title2)
    text_w2 = bbox2[2] - bbox2[0]
    draw.text((540 - text_w2 // 2, title_y + 75), title2, font=title_font, fill=PRIMARY_COLOR)

    # Badge
    sub_font = get_font(32)
    sub_y = 900 + y_offset
    draw_rounded_rect(draw, (250, sub_y, 830, sub_y + 60), 30, (25, 25, 45))
    sub = "FLASH IA - Notaires & Innovation"
    bbox = sub_font.getbbox(sub)
    text_w = bbox[2] - bbox[0]
    draw.text((540 - text_w // 2, sub_y + 12), sub, font=sub_font, fill=MUTED_COLOR)

    return np.array(img)


def generate_tts(text: str, output_path: str, lang: str = "fr") -> str:
    """Genere un fichier audio TTS."""
    print(f"[TTS] Generation de la voix...")
    tts = gTTS(text=text, lang=lang, slow=False)
    tts.save(output_path)
    print(f"[OK] Audio: {output_path}")
    return output_path


def generate_video(script: str, output_dir: str = None) -> str:
    """
    Genere la video complete du mini-journal.

    Args:
        script: Le texte a lire/afficher
        output_dir: Dossier de sortie

    Returns:
        Chemin vers le fichier video MP4
    """
    from moviepy import ImageClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip

    if output_dir is None:
        output_dir = os.path.dirname(os.path.abspath(__file__))

    date_str = datetime.now().strftime("%Y-%m-%d")
    output_path = os.path.join(output_dir, f"flash_ia_{date_str}.mp4")

    # 1. Generer l'audio TTS
    print("\n[1/4] Generation de la voix...")
    audio_path = os.path.join(output_dir, f"flash_ia_{date_str}.mp3")
    generate_tts(script, audio_path)

    # Charger l'audio pour obtenir la duree
    audio_clip = AudioFileClip(audio_path)
    total_duration = audio_clip.duration
    print(f"       Duree audio: {total_duration:.1f}s")

    # 2. Decouper le script en sections
    print("[2/4] Preparation des sections...")
    sentences = [s.strip() for s in script.replace("!", "!|").replace(".", ".|").replace("?", "?|").split("|") if s.strip()]

    # Regrouper en 4-5 sections
    section_size = max(1, len(sentences) // 4)
    sections = []
    for i in range(0, len(sentences), section_size):
        section_text = " ".join(sentences[i:i + section_size])
        if section_text:
            sections.append(section_text)

    if len(sections) > 5:
        # Fusionner les dernieres
        sections = sections[:4] + [" ".join(sections[4:])]

    # 3. Creer les clips video
    print("[3/4] Generation des images...")
    clips = []

    # Durees par section
    intro_duration = 3.0
    outro_duration = 3.0
    news_total = total_duration - intro_duration - outro_duration
    section_duration = max(2.0, news_total / max(1, len(sections)))

    # Intro
    intro_frame = create_intro_frame(0.5)
    intro_clip = ImageClip(intro_frame).with_duration(intro_duration)
    clips.append(intro_clip)

    # Sections de news
    for i, section in enumerate(sections):
        frame = create_news_frame(0.5, section[:200], i + 1, len(sections))
        clip = ImageClip(frame).with_duration(section_duration)
        clips.append(clip)

    # Outro
    outro_frame = create_outro_frame(0.5)
    outro_clip = ImageClip(outro_frame).with_duration(outro_duration)
    clips.append(outro_clip)

    # 4. Assembler
    print("[4/4] Assemblage de la video...")
    video = concatenate_videoclips(clips, method="compose")

    # Ajuster la duree video a l'audio
    if video.duration > total_duration:
        video = video.subclipped(0, total_duration)

    # Ajouter l'audio
    video = video.with_audio(audio_clip)

    # Exporter
    video.write_videofile(
        output_path,
        fps=FPS,
        codec="libx264",
        audio_codec="aac",
        temp_audiofile=os.path.join(output_dir, "temp_audio.m4a"),
        remove_temp=True,
        logger="bar"
    )

    print(f"\n[OK] Video generee: {output_path}")
    print(f"     Duree: {total_duration:.1f}s")
    print(f"     Format: {WIDTH}x{HEIGHT} (vertical/shorts)")

    # Cleanup
    audio_clip.close()
    video.close()

    return output_path


if __name__ == "__main__":
    test_script = """Bonjour a tous! Bienvenue dans votre Flash IA de la semaine!
Cette semaine, OpenAI a lance un nouvel outil d'automatisation qui pourrait revolutionner la gestion documentaire.
Google a annonce des avancees majeures dans la reconnaissance de texte manuscrit, parfait pour numeriser les archives.
Cote notaires, l'IA peut desormais analyser un compromis de vente en quelques secondes et detecter les anomalies.
A la semaine prochaine pour votre prochain Flash IA!"""

    generate_video(test_script)
