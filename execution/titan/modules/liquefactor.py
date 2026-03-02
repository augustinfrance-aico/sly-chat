"""
Content Liquefactor v2 — HTML page generator for reviews, news digests, breaking news.
Pipeline: content → LLM analysis → HTML page → GitHub Pages → Telegram link.

Literary theme: serif fonts, warm tones, editorial layout.
Three page types: review (long), digest (daily), breaking (alert).
"""

import hashlib
import html as html_module
import json
import logging
import os
import re
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

import feedparser

from ..ai_client import chat as ai_chat
from ..config import NEWS_FEEDS

log = logging.getLogger("titan.liquefactor")

MEMORY_DIR = Path(__file__).parent.parent / "memory"
LIQUEFACTOR_STATE = MEMORY_DIR / "liquefactor_state.json"
DEPLOY_DIR = Path(__file__).parent.parent.parent.parent / "reviews"
GITHUB_PAGES_BASE = "https://augustinfrance-aico.github.io/sly-command"

MONITORED_CHANNELS = {
    "UCbo-KbSjJDG6JWQ_MTZ_rNA": "Nick Saraev",
    "UCbRP3c757lWg9M-U7TyEkXA": "AI Jason",
    "UC4JX40jDee_tINbkjycV4Sg": "Matt Wolfe",
    "UCsBjURrPoezykLs9EqgamOA": "Fireship",
    "UCnUYZLuoy1rq1aVMwx4piYg": "Two Minute Papers",
    "UCX6OQ3DkcsbYNE6H8uQQuVA": "The AI Advantage",
}

# ─── CSS literary theme (shared across all page types) ───

LITERARY_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=Source+Serif+4:ital,wght@0,300;0,400;0,600;1,300;1,400&family=JetBrains+Mono:wght@400&display=swap');

:root {
  --bg: #FDFBF7; --bg-alt: #F5F0E8; --bg-card: #FFFFFF;
  --text: #1A1A1A; --text-body: #2D2D2D; --text-sec: #6B6B6B; --text-muted: #999;
  --accent: #8B4513; --accent-light: #A0522D; --gold: #B8860B;
  --border: #E5DDD0; --border-lt: #F0EBE0;
  --link: #2E5090; --link-h: #1A3560;
  --highlight: #FFF8DC; --shadow: rgba(0,0,0,0.06);
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #1A1815; --bg-alt: #242019; --bg-card: #2A2520;
    --text: #E8E0D0; --text-body: #D0C8B8; --text-sec: #A09888; --text-muted: #786858;
    --accent: #C4956A; --accent-light: #D4A57A; --gold: #D4A030;
    --border: #3A3530; --border-lt: #302B25;
    --link: #7AA0D0; --link-h: #90B0E0;
    --highlight: #2A2518; --shadow: rgba(0,0,0,0.2);
  }
}
* { margin:0; padding:0; box-sizing:border-box; }
body {
  font-family: 'Source Serif 4', Georgia, serif;
  background: var(--bg); color: var(--text-body);
  line-height: 1.85; font-size: 18px;
  -webkit-font-smoothing: antialiased;
}
.page-header {
  max-width: 720px; margin: 0 auto;
  padding: 60px 24px 40px; text-align: center;
  border-bottom: 1px solid var(--border);
}
.brand {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px; letter-spacing: 3px;
  text-transform: uppercase; color: var(--accent); margin-bottom: 24px;
}
.page-header h1 {
  font-family: 'Playfair Display', serif;
  font-size: clamp(28px, 5vw, 44px); font-weight: 700;
  line-height: 1.2; color: var(--text); margin-bottom: 20px;
}
.meta {
  font-size: 15px; color: var(--text-sec);
  display: flex; flex-wrap: wrap; justify-content: center; gap: 16px;
}
.meta a { color: var(--link); text-decoration: none; }
.meta a:hover { color: var(--link-h); text-decoration: underline; }
.reading-time {
  display: inline-block; background: var(--highlight);
  border: 1px solid var(--border); border-radius: 4px;
  padding: 2px 10px; font-size: 13px;
  color: var(--accent); font-weight: 600;
}
article {
  max-width: 680px; margin: 0 auto; padding: 48px 24px 80px;
}
article h2 {
  font-family: 'Playfair Display', serif;
  font-size: 28px; font-weight: 600; color: var(--text);
  margin: 56px 0 20px; padding-bottom: 12px;
  border-bottom: 2px solid var(--border);
}
article h3 {
  font-family: 'Playfair Display', serif;
  font-size: 22px; font-weight: 600; color: var(--text);
  margin: 40px 0 16px;
}
article p { margin-bottom: 20px; text-align: justify; hyphens: auto; }
article blockquote {
  margin: 32px 0; padding: 20px 24px;
  border-left: 3px solid var(--accent); background: var(--bg-alt);
  font-style: italic; color: var(--text-sec);
}
article table { width: 100%; border-collapse: collapse; margin: 24px 0; font-size: 15px; }
article th { text-align: left; padding: 12px; border-bottom: 2px solid var(--border); color: var(--accent); font-weight: 600; }
article td { padding: 10px 12px; border-bottom: 1px solid var(--border-lt); }
article ul, article ol { margin: 16px 0 24px 24px; }
article li { margin-bottom: 8px; padding-left: 8px; }
.video-embed {
  margin: 32px 0; border-radius: 8px; overflow: hidden;
  box-shadow: 0 4px 20px var(--shadow); aspect-ratio: 16/9;
}
.video-embed iframe { width: 100%; height: 100%; border: none; }
.schema-box {
  background: var(--bg-alt); border: 1px solid var(--border);
  border-radius: 8px; padding: 24px; margin: 24px 0;
  font-family: 'JetBrains Mono', monospace;
  font-size: 14px; line-height: 2; color: var(--accent); overflow-x: auto;
}
.news-card {
  background: var(--bg-card); border: 1px solid var(--border);
  border-radius: 8px; padding: 20px; margin-bottom: 20px;
  box-shadow: 0 2px 8px var(--shadow);
}
.news-card h3 { margin: 0 0 8px; font-size: 20px; }
.news-card .source { font-size: 13px; color: var(--accent); margin-bottom: 8px; }
.news-card img { width: 100%; border-radius: 6px; margin: 12px 0; max-height: 300px; object-fit: cover; }
.breaking-banner {
  background: linear-gradient(135deg, #8B0000, #B22222);
  color: #fff; text-align: center; padding: 12px;
  font-family: 'JetBrains Mono', monospace; font-size: 13px;
  letter-spacing: 3px; text-transform: uppercase;
}
footer {
  max-width: 680px; margin: 0 auto; padding: 32px 24px;
  border-top: 1px solid var(--border); text-align: center;
  font-size: 13px; color: var(--text-muted);
}
footer a { color: var(--link); text-decoration: none; }
@media (max-width: 600px) {
  body { font-size: 16px; }
  article { padding: 32px 16px 60px; }
  article h2 { font-size: 24px; margin-top: 40px; }
}
"""


class ContentLiquefactor:
    """Generates HTML pages for reviews, news digests, and breaking news."""

    # ─── Reading time targets ───

    @staticmethod
    def _reading_time_target(duration_sec: int) -> dict:
        minutes = duration_sec / 60
        if minutes < 15:
            read_min = 3
        elif minutes < 60:
            read_min = 5 + int((minutes - 15) / 15)
        elif minutes < 180:
            read_min = 10 + int((minutes - 60) / 60)
        else:
            read_min = 15 + int((minutes - 180) / 60)
        target_words = read_min * 250
        num_sections = max(3, target_words // 600)
        return {"read_minutes": read_min, "target_words": target_words, "num_sections": num_sections}

    # ─── Markdown → HTML converter ───

    @staticmethod
    def _md_to_html(text: str) -> str:
        lines = text.split("\n")
        parts, in_ul, in_table = [], False, False
        for raw in lines:
            s = raw.strip()
            if not s:
                if in_ul:
                    parts.append("</ul>"); in_ul = False
                if in_table:
                    parts.append("</tbody></table>"); in_table = False
                continue
            if s.startswith("## "):
                parts.append(f"<h2>{s[3:]}</h2>"); continue
            if s.startswith("### "):
                parts.append(f"<h3>{s[4:]}</h3>"); continue
            if s.startswith("> "):
                parts.append(f"<blockquote><p>{s[2:]}</p></blockquote>"); continue
            if s.startswith("---"):
                parts.append("<hr>"); continue
            if "|" in s and s.startswith("|"):
                cells = [c.strip() for c in s.split("|")[1:-1]]
                if all(set(c) <= set("-: ") for c in cells):
                    continue
                if not in_table:
                    parts.append("<table><thead><tr>" + "".join(f"<th>{c}</th>" for c in cells) + "</tr></thead><tbody>")
                    in_table = True
                else:
                    parts.append("<tr>" + "".join(f"<td>{c}</td>" for c in cells) + "</tr>")
                continue
            if s.startswith("- ") or s.startswith("* "):
                if not in_ul:
                    parts.append("<ul>"); in_ul = True
                c = s[2:]
                c = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", c)
                c = re.sub(r"\*(.+?)\*", r"<em>\1</em>", c)
                parts.append(f"<li>{c}</li>"); continue
            if in_ul:
                parts.append("</ul>"); in_ul = False
            p = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
            p = re.sub(r"\*(.+?)\*", r"<em>\1</em>", p)
            parts.append(f"<p>{p}</p>")
        if in_ul:
            parts.append("</ul>")
        if in_table:
            parts.append("</tbody></table>")
        return "\n".join(parts)

    # ─── Utility methods ───

    @staticmethod
    def _slugify(text: str) -> str:
        slug = re.sub(r"[^\w\s-]", "", text.lower())
        slug = re.sub(r"[-\s]+", "-", slug).strip("-")
        return slug[:60]

    @staticmethod
    def _fmt_duration(sec: int) -> str:
        if sec >= 3600:
            return f"{sec // 3600}h{(sec % 3600) // 60:02d}"
        return f"{sec // 60} min"

    def _load_state(self) -> dict:
        if LIQUEFACTOR_STATE.exists():
            with open(LIQUEFACTOR_STATE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"seen_video_ids": [], "seen_article_ids": [], "reviews": [], "digests": []}

    def _save_state(self, state: dict):
        MEMORY_DIR.mkdir(parents=True, exist_ok=True)
        with open(LIQUEFACTOR_STATE, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)

    # ─── Deploy to GitHub Pages ───

    def _deploy(self, html: str, filename: str, subdir: str = "reviews") -> str:
        deploy_dir = DEPLOY_DIR / subdir
        deploy_dir.mkdir(parents=True, exist_ok=True)
        filepath = deploy_dir / filename
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        log.info(f"Written {subdir}/{filename} ({len(html)} chars)")
        try:
            subprocess.run(["git", "add", "."], cwd=str(DEPLOY_DIR), capture_output=True, timeout=30)
            subprocess.run(
                ["git", "commit", "-m", f"Liquefactor: {subdir}/{filename}"],
                cwd=str(DEPLOY_DIR), capture_output=True, timeout=30,
            )
            subprocess.run(["git", "push", "origin", "main"], cwd=str(DEPLOY_DIR), capture_output=True, timeout=60)
            log.info(f"Deployed {subdir}/{filename}")
        except Exception as e:
            log.error(f"Git deploy error: {e}")
        return f"{GITHUB_PAGES_BASE}/{subdir}/{filename}"

    # ─── Telegram link sender ───

    def _telegram(self, title: str, url: str, page_type: str = "review"):
        import requests
        bot_token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
        chat_id = os.environ.get("TELEGRAM_CHAT_ID", "")
        if not bot_token or not chat_id:
            log.warning("Telegram credentials missing, skipping notification")
            return
        emojis = {"review": "\U0001f4d6", "digest": "\U0001f4f0", "breaking": "\U0001f6a8"}
        emoji = emojis.get(page_type, "\U0001f4c4")
        text = f"{emoji} {title}\n\n{url}"
        try:
            requests.post(
                f"https://api.telegram.org/bot{bot_token}/sendMessage",
                json={"chat_id": chat_id, "text": text, "disable_web_page_preview": False},
                timeout=10,
            )
        except Exception as e:
            log.error(f"Telegram error: {e}")

    # ═══════════════════════════════════════════════════
    # 1. YOUTUBE REVIEW — Long-form literary analysis
    # ═══════════════════════════════════════════════════

    def _sectioned_analysis(self, transcript: str, title: str, url: str, duration_sec: int) -> str:
        targets = self._reading_time_target(duration_sec)
        n = targets["num_sections"]
        dur_str = self._fmt_duration(duration_sec)

        chunk_size = max(1, len(transcript) // n)
        chunks = [transcript[i * chunk_size:(i + 1) * chunk_size] for i in range(n)]
        if len(transcript) > n * chunk_size:
            chunks[-1] += transcript[n * chunk_size:]

        system = (
            "Tu es un critique et rédacteur pour un magazine culturel et technologique français. "
            "Tu écris en français avec des accents corrects (é, è, à, ç, ê, etc.), JAMAIS d'entités HTML. "
            "Style littéraire, élégant, dense, informatif. Pas de jargon inutile. "
            "IMPORTANT : écris des textes LONGS et détaillés. Chaque section doit faire 800-1200 mots minimum. "
            "Développe les idées, donne des exemples, fais des comparaisons, contextualise."
        )

        sections = []
        for i, chunk in enumerate(chunks):
            if i == 0:
                prompt = (
                    f"Analyse cette PREMIÈRE PARTIE de la vidéo \"{title}\" ({dur_str}).\n\n"
                    f"Écris :\n"
                    f"## Fiche d'identité\n"
                    f"Titre, auteur, durée, score business /10 justifié.\n\n"
                    f"## Résumé exécutif\n"
                    f"3-4 paragraphes détaillés, pas de bullet points.\n\n"
                    f"## Les idées forces\n"
                    f"Développe chaque idée en un paragraphe complet (pas de tirets).\n\n"
                    f"Transcription (partie 1/{n}) :\n{chunk[:20000]}"
                )
            elif i == n - 1:
                prompt = (
                    f"Termine l'analyse de la vidéo \"{title}\" ({dur_str}).\n\n"
                    f"Écris :\n"
                    f"## Artillerie technique\n"
                    f"Tous les outils/APIs cités dans un tableau | Outil | Fonction | Accès |\n\n"
                    f"## Vulgarisation\n"
                    f"3 concepts complexes expliqués avec des analogies littéraires.\n\n"
                    f"## Plan d'action freelance\n"
                    f"Comment monétiser ces connaissances concrètement, avec prix.\n\n"
                    f"## Verdict final\n"
                    f"Synthèse, pour qui, limites, note.\n\n"
                    f"Transcription (partie {i + 1}/{n}) :\n{chunk[:20000]}"
                )
            else:
                prompt = (
                    f"Continue l'analyse de la vidéo \"{title}\" ({dur_str}).\n"
                    f"Cette section couvre la partie {i + 1}/{n}.\n\n"
                    f"Écris un chapitre thématique de 600-900 mots :\n"
                    f"- Identifie le THÈME PRINCIPAL de ce segment\n"
                    f"- Donne un TITRE de chapitre (## Titre)\n"
                    f"- Développe en paragraphes fluides, pas de listes\n"
                    f"- Cite les outils/concepts avec explications\n"
                    f"- Ajoute des analogies ou métaphores\n\n"
                    f"Transcription (partie {i + 1}/{n}) :\n{chunk[:20000]}"
                )

            try:
                result = ai_chat(system, prompt, max_tokens=6000)
                sections.append(result)
                log.info(f"Section {i + 1}/{n}: {len(result)} chars")
            except Exception as e:
                log.error(f"Section {i + 1} error: {e}")
                sections.append(f"*Section {i + 1} indisponible.*")
            time.sleep(2)  # rate limit buffer

        return "\n\n---\n\n".join(sections)

    def generate_review(self, url: str) -> dict:
        from .transcribe import transcribe_youtube_sync

        log.info(f"Liquefactor v2 review: {url}")
        t_data = transcribe_youtube_sync(url)
        transcript = t_data["transcript"]
        title = t_data["title"]
        duration = t_data["duration_sec"]
        video_id = t_data["video_id"]
        targets = self._reading_time_target(duration)
        dur_str = self._fmt_duration(duration)

        log.info(f"Target: {targets['read_minutes']} min lecture, {targets['num_sections']} sections")
        analysis = self._sectioned_analysis(transcript, title, url, duration)
        content_html = self._md_to_html(analysis)
        content_html = html_module.unescape(content_html)  # fix any remaining entities

        date_str = datetime.now().strftime("%d %B %Y")
        slug = self._slugify(title)
        filename = f"{slug}.html"

        full_html = (
            f'<!DOCTYPE html>\n<html lang="fr">\n<head>\n'
            f'<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
            f'<title>{title} — Content Liquefactor</title>\n'
            f'<style>{LITERARY_CSS}</style>\n</head>\n<body>\n'
            f'<div class="page-header">\n'
            f'  <div class="brand">Content Liquefactor</div>\n'
            f'  <h1>{title}</h1>\n'
            f'  <div class="meta">\n'
            f'    <span>{dur_str}</span>\n'
            f'    <span class="reading-time">{targets["read_minutes"]} min de lecture</span>\n'
            f'    <span><a href="{url}" target="_blank">Voir sur YouTube</a></span>\n'
            f'    <span>{date_str}</span>\n'
            f'  </div>\n</div>\n'
            f'<article>\n'
            f'  <div class="video-embed">\n'
            f'    <iframe src="https://www.youtube.com/embed/{video_id}" allowfullscreen loading="lazy"></iframe>\n'
            f'  </div>\n'
            f'  {content_html}\n'
            f'</article>\n'
            f'<footer>\n'
            f'  <p>Généré par le <a href="{GITHUB_PAGES_BASE}">Content Liquefactor</a> — Cooper Building</p>\n'
            f'  <p>Analyse automatique par IA — {date_str}</p>\n'
            f'</footer>\n</body>\n</html>'
        )

        page_url = self._deploy(full_html, filename, "reviews")
        self._telegram(f"Review : {title} ({dur_str})", page_url, "review")

        state = self._load_state()
        state["reviews"].append({"video_id": video_id, "title": title, "url": page_url, "date": datetime.now().isoformat()})
        state["seen_video_ids"] = list(set(state.get("seen_video_ids", []) + [video_id]))[-200:]
        self._save_state(state)

        return {"url": page_url, "filename": filename, "read_minutes": targets["read_minutes"],
                "title": title, "sections": targets["num_sections"]}

    # ═══════════════════════════════════════════════════
    # 2. DAILY AI NEWS DIGEST
    # ═══════════════════════════════════════════════════

    def generate_daily_digest(self) -> dict:
        log.info("Generating daily AI news digest...")
        articles = []
        ai_feeds = NEWS_FEEDS.get("ai", []) + NEWS_FEEDS.get("tech", [])[:3]
        for feed_url in ai_feeds:
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries[:5]:
                    thumb = ""
                    if hasattr(entry, "media_content") and entry.media_content:
                        thumb = entry.media_content[0].get("url", "")
                    elif hasattr(entry, "media_thumbnail") and entry.media_thumbnail:
                        thumb = entry.media_thumbnail[0].get("url", "")
                    articles.append({
                        "title": entry.get("title", ""),
                        "summary": re.sub(r"<[^>]+>", "", entry.get("summary", ""))[:300],
                        "link": entry.get("link", ""),
                        "source": feed.feed.get("title", "Unknown"),
                        "thumbnail": thumb,
                    })
            except Exception:
                continue

        if not articles:
            return {"error": "Aucun article trouvé"}

        # Dedup by title hash
        seen = set()
        unique = []
        for a in articles:
            h = hashlib.md5(a["title"].encode()).hexdigest()[:12]
            if h not in seen:
                seen.add(h)
                unique.append(a)
        articles = unique[:30]

        articles_text = "\n".join(f"- [{a['source']}] {a['title']}: {a['summary'][:150]}" for a in articles)
        system = (
            "Tu es un éditeur de magazine IA francophone. "
            "Écris en français avec des accents corrects (UTF-8), JAMAIS d'entités HTML."
        )
        prompt = (
            f"Voici les articles IA du jour. Sélectionne les 10 plus importants et "
            f"écris pour chacun un résumé de 3-4 phrases en français.\n"
            f"Format : ## Titre\nRésumé en paragraphe.\n\n"
            f"Articles :\n{articles_text}"
        )
        digest_text = ai_chat(system, prompt, max_tokens=4000)
        content_html = self._md_to_html(digest_text)
        content_html = html_module.unescape(content_html)

        # Add thumbnail images where we have them
        for a in articles[:10]:
            if a.get("thumbnail"):
                img = f'<div class="news-card"><img src="{a["thumbnail"]}" alt=""><div class="source">{a["source"]}</div></div>'
                # Insert before first occurrence of article title in HTML
                escaped_title = a["title"][:40]
                if escaped_title in content_html:
                    content_html = content_html.replace(
                        escaped_title,
                        f'{escaped_title}</p>{img}<p>',
                        1,
                    )

        date_str = datetime.now().strftime("%d %B %Y")
        slug = datetime.now().strftime("digest-%Y-%m-%d")
        filename = f"{slug}.html"

        full_html = (
            f'<!DOCTYPE html>\n<html lang="fr">\n<head>\n'
            f'<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
            f'<title>Digest IA — {date_str}</title>\n'
            f'<style>{LITERARY_CSS}</style>\n</head>\n<body>\n'
            f'<div class="page-header">\n'
            f'  <div class="brand">Digest IA Quotidien</div>\n'
            f'  <h1>Les nouvelles de l\'intelligence artificielle</h1>\n'
            f'  <div class="meta">\n'
            f'    <span>{date_str}</span>\n'
            f'    <span>{len(articles)} sources analysées</span>\n'
            f'  </div>\n</div>\n'
            f'<article>\n{content_html}\n</article>\n'
            f'<footer>\n'
            f'  <p>Généré par le <a href="{GITHUB_PAGES_BASE}">Content Liquefactor</a> — Cooper Building</p>\n'
            f'</footer>\n</body>\n</html>'
        )

        page_url = self._deploy(full_html, filename, "news")
        self._telegram(f"Digest IA du {date_str}", page_url, "digest")

        state = self._load_state()
        state["digests"].append({"date": date_str, "url": page_url, "articles": len(articles)})
        state["digests"] = state["digests"][-90:]
        self._save_state(state)

        return {"url": page_url, "article_count": len(articles)}

    # ═══════════════════════════════════════════════════
    # 3. BREAKING NEWS DETECTION
    # ═══════════════════════════════════════════════════

    def check_breaking_news(self) -> Optional[dict]:
        state = self._load_state()
        seen_ids = set(state.get("seen_article_ids", []))

        candidates = []
        for feed_url in NEWS_FEEDS.get("ai", []):
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries[:3]:
                    art_id = hashlib.md5(entry.get("title", "").encode()).hexdigest()[:12]
                    if art_id in seen_ids:
                        continue
                    candidates.append({
                        "id": art_id,
                        "title": entry.get("title", ""),
                        "summary": re.sub(r"<[^>]+>", "", entry.get("summary", ""))[:500],
                        "link": entry.get("link", ""),
                        "source": feed.feed.get("title", ""),
                    })
            except Exception:
                continue

        if not candidates:
            return None

        for c in candidates:
            seen_ids.add(c["id"])
        state["seen_article_ids"] = list(seen_ids)[-500:]
        self._save_state(state)

        cand_text = "\n".join(f"- [{c['source']}] {c['title']}: {c['summary'][:200]}" for c in candidates)
        score = ai_chat(
            "Tu es un éditeur en chef IA. Détermine si un article est une BREAKING NEWS "
            "(nouveau modèle majeur, percée scientifique, annonce qui change l'industrie).",
            f"Réponds UNIQUEMENT avec:\nBREAKING: [titre exact]\nou\nNOTHING\n\n"
            f"Sois strict — un blog post normal n'est PAS breaking.\n\nArticles:\n{cand_text}",
            max_tokens=200,
        )

        if "NOTHING" in score or "BREAKING" not in score:
            return None

        breaking_title = score.split("BREAKING:")[-1].strip()
        match = None
        for c in candidates:
            if c["title"].lower() in breaking_title.lower() or breaking_title.lower() in c["title"].lower():
                match = c
                break
        if not match:
            match = candidates[0] if candidates else None
        if not match:
            return None

        detail = ai_chat(
            "Tu es un journaliste tech. Écris en français avec accents corrects (UTF-8). "
            "Style : journalistique, factuel, engageant.",
            f"Écris un article de 500 mots sur cette breaking news IA.\n\n"
            f"Titre: {match['title']}\nSource: {match['source']}\nRésumé: {match['summary']}",
            max_tokens=2000,
        )

        content_html = self._md_to_html(detail)
        content_html = html_module.unescape(content_html)
        slug = self._slugify(match["title"])
        filename = f"breaking-{slug}.html"
        date_str = datetime.now().strftime("%d %B %Y à %Hh%M")

        full_html = (
            f'<!DOCTYPE html>\n<html lang="fr">\n<head>\n'
            f'<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
            f'<title>BREAKING — {match["title"]}</title>\n'
            f'<style>{LITERARY_CSS}</style>\n</head>\n<body>\n'
            f'<div class="breaking-banner">BREAKING NEWS</div>\n'
            f'<div class="page-header">\n'
            f'  <div class="brand">Alerte Content Liquefactor</div>\n'
            f'  <h1>{match["title"]}</h1>\n'
            f'  <div class="meta">\n'
            f'    <span>{match["source"]}</span>\n'
            f'    <span>{date_str}</span>\n'
            f'    <span><a href="{match["link"]}" target="_blank">Source originale</a></span>\n'
            f'  </div>\n</div>\n'
            f'<article>\n{content_html}\n</article>\n'
            f'<footer>\n'
            f'  <p>Généré par le <a href="{GITHUB_PAGES_BASE}">Content Liquefactor</a> — Cooper Building</p>\n'
            f'</footer>\n</body>\n</html>'
        )

        page_url = self._deploy(full_html, filename, "news")
        self._telegram(f"BREAKING : {match['title']}", page_url, "breaking")
        return {"url": page_url, "title": match["title"]}

    # ═══════════════════════════════════════════════════
    # 4. YOUTUBE CHANNEL MONITORING
    # ═══════════════════════════════════════════════════

    def check_youtube_channels(self) -> list[dict]:
        state = self._load_state()
        seen = set(state.get("seen_video_ids", []))
        new_videos = []

        for channel_id, channel_name in MONITORED_CHANNELS.items():
            rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
            try:
                feed = feedparser.parse(rss_url)
                for entry in feed.entries[:3]:
                    vid_id = entry.get("yt_videoid", "")
                    if not vid_id:
                        link = entry.get("link", "")
                        m = re.search(r"v=([a-zA-Z0-9_-]{11})", link)
                        vid_id = m.group(1) if m else ""
                    if vid_id and vid_id not in seen:
                        new_videos.append({
                            "video_id": vid_id,
                            "title": entry.get("title", ""),
                            "channel": channel_name,
                            "url": f"https://www.youtube.com/watch?v={vid_id}",
                        })
                        seen.add(vid_id)
            except Exception as e:
                log.warning(f"YouTube RSS error ({channel_name}): {e}")

        state["seen_video_ids"] = list(seen)[-200:]
        self._save_state(state)
        return new_videos
