"""
TITAN Telegram Bot
The interface — talk to Titan from anywhere.

Usage:
    python -m titan.telegram_bot

Features:
    - All Titan modules accessible via Telegram
    - Slash commands for quick access
    - Natural language for everything else
    - Voice messages
    - Gamification (XP, levels, achievements)
    - Dashboard & analytics
    - Auto daily brief
"""

import asyncio
import json
import logging
import time
from datetime import datetime
from pathlib import Path

import requests

from .config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, TITAN_NAME

# === CORE MODULES (always loaded — used every session) ===
from .modules.brain import TitanBrain
from .modules.voice import TitanVoice
from .modules.gamification import TitanGamification
from .modules.dashboard import TitanDashboard
from .modules.president import TitanPresident
from .modules import memory

# === LAZY LOADING — modules loaded on first use only ===
# Saves ~30 imports at boot, faster startup, less memory
_lazy_cache = {}

def _lazy(module_path: str, class_name: str):
    """Import and instantiate a module class on first use, then cache it."""
    key = f"{module_path}.{class_name}"
    if key not in _lazy_cache:
        import importlib
        mod = importlib.import_module(module_path, package="execution.titan")
        cls = getattr(mod, class_name)
        _lazy_cache[key] = cls()
    return _lazy_cache[key]

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [TITAN] %(message)s")
log = logging.getLogger("titan")


class TitanTelegram:
    """Titan's Telegram interface — fully gamified."""

    def __init__(self):
        self.token = TELEGRAM_BOT_TOKEN
        self.base_url = f"https://api.telegram.org/bot{self.token}"
        self.offset = 0
        self.running = False
        self.processed_messages = set()  # Track processed message IDs to prevent duplicates
        self._msg_lock = asyncio.Lock()  # Prevent parallel message processing
        self._president_session = False  # True = Jacques is talking, stays active
        self._prompt_mode = False  # True = tous les vocaux vont dans prompt vocaux/ sans réponse IA

        # === CORE (always loaded — stored with _ prefix to not conflict with properties) ===
        self._brain = TitanBrain()
        self._voice = TitanVoice()
        self._gamification = TitanGamification()
        self._dashboard = TitanDashboard()
        self._president = TitanPresident()

    # === CORE MODULE ACCESSORS (always loaded) ===
    @property
    def brain(self):
        return self._brain

    @property
    def voice(self):
        return self._voice

    @property
    def gamification(self):
        return self._gamification

    @property
    def dashboard(self):
        return self._dashboard

    @property
    def president(self):
        return self._president

    # === LAZY MODULE PROPERTIES — loaded on first use ===
    @property
    def news(self):
        return _lazy(".modules.news", "TitanNews")

    @property
    def web(self):
        return _lazy(".modules.web", "TitanWeb")

    @property
    def perplexity(self):
        return _lazy(".modules.perplexity", "TitanPerplexity")

    @property
    def upwork(self):
        return _lazy(".modules.upwork", "TitanUpwork")

    @property
    def n8n(self):
        return _lazy(".modules.n8n", "TitanN8N")

    @property
    def email(self):
        return _lazy(".modules.email_gen", "TitanEmailGen")

    @property
    def code(self):
        return _lazy(".modules.code_assistant", "TitanCode")

    @property
    def portfolio(self):
        return _lazy(".modules.portfolio_gen", "TitanPortfolio")

    @property
    def calendar(self):
        return _lazy(".modules.calendar", "TitanCalendar")

    @property
    def toolbox(self):
        return _lazy(".modules.toolbox", "TitanToolbox")

    # memes — REMOVED (bloat)

    @property
    def motivation(self):
        return _lazy(".modules.motivation", "TitanMotivation")

    # wiki, qrcode, horoscope, movies, fitness, riddles — REMOVED (bloat)

    @property
    def ai_prompt(self):
        return _lazy(".modules.ai_prompt", "TitanAIPrompt")

    @property
    def seo(self):
        return _lazy(".modules.seo", "TitanSEO")

    @property
    def domains(self):
        return _lazy(".modules.domains", "TitanDomains")

    # colors, encryption — REMOVED (bloat)

    @property
    def invoice_gen(self):
        return _lazy(".modules.invoice", "TitanInvoice")

    @property
    def social(self):
        return _lazy(".modules.social_media", "TitanSocial")

    # fake_data, learning, ascii_art, recipes, music, json_tools — REMOVED (bloat)

    @property
    def startup(self):
        return _lazy(".modules.startup", "TitanStartup")

    # travel — REMOVED (bloat)

    @property
    def writing(self):
        return _lazy(".modules.writing", "TitanWriting")

    # space — REMOVED (bloat)

    @property
    def productivity(self):
        return _lazy(".modules.productivity", "TitanProductivity")

    # deals, booking — REMOVED (bloat)

    @property
    def bible(self):
        return _lazy(".modules.bible", "TitanBible")

    @property
    def ai_watch(self):
        return _lazy(".modules.ai_watch", "TitanAIWatch")

    # === BUILDING LIFE MODULES (Tri-Pôle creative suite) ===

    @property
    def journal(self):
        return _lazy(".modules.journal", "TitanJournal")

    @property
    def aggregator(self):
        return _lazy(".modules.aggregator", "TitanAggregator")

    @property
    def coach(self):
        return _lazy(".modules.coach", "TitanCoach")

    @property
    def auto_healer(self):
        return _lazy(".modules.auto_healer", "TitanAutoHealer")

    @property
    def morning_digest_mod(self):
        return _lazy(".modules.morning_digest", "TitanMorningDigest")

    @property
    def mega_prompt(self):
        return _lazy(".modules.mega_prompt", "TitanMegaPrompt")

    @property
    def film(self):
        return _lazy(".modules.film_building", "TitanFilm")

    @property
    def clones(self):
        return _lazy(".modules.clones", "TitanClones")

    @property
    def portfolio_live(self):
        return _lazy(".modules.portfolio_live", "TitanPortfolioLive")

    @property
    def empire_visual(self):
        return _lazy(".modules.empire_visual", "TitanEmpireVisual")

    @property
    def library(self):
        return _lazy(".modules.library", "TitanLibrary")

    @property
    def strategic(self):
        return _lazy(".modules.strategic", "TitanStrategic")

    @property
    def sport_pro(self):
        return _lazy(".modules.sport_pro", "TitanSportPro")

    @property
    def culture(self):
        return _lazy(".modules.culture", "TitanCulture")

    @property
    def task_master(self):
        return _lazy(".modules.task_master", "TitanTaskMaster")

    # personal — REMOVED (bloat)

    # === R&D LAB MODULES ===

    @property
    def rdlab_doctorant(self):
        return _lazy(".modules.rdlab_doctorant", "TitanRDLabDoctorant")

    @property
    def rdlab_digestor(self):
        return _lazy(".modules.rdlab_digestor", "TitanRDLabDigestor")

    @property
    def rdlab_scout(self):
        return _lazy(".modules.rdlab_scout", "TitanRDLabScout")

    @property
    def rdlab_experiment(self):
        return _lazy(".modules.rdlab_experiment", "TitanRDLabExperiment")

    @property
    def rdlab_horizon(self):
        return _lazy(".modules.rdlab_horizon", "TitanRDLabHorizon")

    # === CLAUDE BRIDGE ===

    def _get_claude_session_file(self):
        """Return path to current session file in 'prompt vocaux/' folder."""
        from pathlib import Path
        folder = Path(__file__).parent.parent.parent / "prompt vocaux"
        folder.mkdir(exist_ok=True)
        # One file per day
        from datetime import datetime
        date_str = datetime.now().strftime("%Y-%m-%d")
        return folder / f"session_{date_str}.md"

    def _write_claude_task(self, instruction: str) -> str:
        """Append a transcription to today's session file in 'prompt vocaux/'."""
        from datetime import datetime
        task_file = self._get_claude_session_file()
        timestamp = datetime.now().strftime("%H:%M:%S")

        # Create file with header if new
        if not task_file.exists():
            with open(task_file, "w", encoding="utf-8") as f:
                f.write(f"# Session vocale — {datetime.now().strftime('%Y-%m-%d')}\n\n")

        with open(task_file, "a", encoding="utf-8") as f:
            f.write(f"\n[{timestamp}] {instruction}\n")

        log.info(f"[CLAUDE BRIDGE] Written to {task_file.name}: {instruction[:80]}")
        return str(task_file)

    # === TELEGRAM API ===

    def send_message(self, chat_id: str, text: str, parse_mode: str = None) -> dict:
        """Send a message via Telegram. Truncate if too long instead of chunking."""
        # NEVER split into multiple messages — truncate instead
        if len(text) > 4000:
            text = text[:3950] + "\n\n[...]"
            log.warning(f"Message truncated from {len(text)} chars")
        return self._send_single(chat_id, text, parse_mode)

    def _send_single(self, chat_id: str, text: str, parse_mode: str = None, reply_markup: dict = None) -> dict:
        """Send a single message. Supports inline keyboards and WebApp buttons."""
        data = {"chat_id": chat_id, "text": text}
        if parse_mode:
            data["parse_mode"] = parse_mode
        if reply_markup:
            data["reply_markup"] = reply_markup

        try:
            resp = requests.post(f"{self.base_url}/sendMessage", json=data, timeout=10)
            return resp.json()
        except Exception as e:
            log.error(f"Send error: {e}")
            return {"error": str(e)}

    def send_typing(self, chat_id: str):
        """Show typing indicator."""
        try:
            requests.post(
                f"{self.base_url}/sendChatAction",
                json={"chat_id": chat_id, "action": "typing"},
                timeout=5,
            )
        except Exception:
            pass

    def get_updates(self) -> list:
        """Get new messages."""
        try:
            params = {
                "offset": self.offset,
                "timeout": 30,
                "allowed_updates": ["message"],
            }
            resp = requests.get(f"{self.base_url}/getUpdates", params=params, timeout=35)
            data = resp.json()
            return data.get("result", [])
        except Exception as e:
            log.error(f"Update error: {e}")
            return []

    # === GAMIFICATION HELPERS ===

    def _xp_footer(self, result: dict) -> str:
        """Create XP footer for messages."""
        notif = self.gamification.format_xp_notification(result)
        if not notif:
            return ""
        return f"\n\n{'~' * 25}\n{notif}"

    # === MESSAGE HANDLER ===

    async def handle_message(self, message: dict):
        """Process an incoming message. Lock ensures ONE response per message."""
        chat_id = str(message["chat"]["id"])
        text = message.get("text", "")
        user = message.get("from", {}).get("first_name", "Unknown")
        msg_id = message.get("message_id", 0)
        is_voice = False

        # DUPLICATE FIX: Skip if already processed this message (BEFORE any processing)
        if msg_id in self.processed_messages:
            log.info(f"[SKIP-DUP] Already processed message {msg_id}")
            return

        # Lock — only one message processed at a time, prevents double sends
        async with self._msg_lock:
            # Double-check after acquiring lock (another coroutine may have processed it)
            if msg_id in self.processed_messages:
                return
            self.processed_messages.add(msg_id)

            # Keep set from growing forever (max 500 recent messages)
            if len(self.processed_messages) > 500:
                self.processed_messages = set(sorted(self.processed_messages)[-200:])

            # Voice message — transcribe to text (INSIDE lock to prevent duplicate sends)
            voice = message.get("voice")
            if voice and not text:
                file_id = voice.get("file_id", "")
                if file_id:
                    # Save for /fx command
                    self.voice.save_last_voice(chat_id, file_id)

                    # FX MODE: if active, apply effect and send back (skip transcription)
                    if self.voice.get_fx_mode(chat_id):
                        self.send_typing(chat_id)
                        log.info(f"[{user}] FX mode active ({self.voice.get_fx_mode(chat_id)}), applying...")
                        handled = await self.voice.auto_fx_voice(chat_id, file_id)
                        if handled:
                            return
                        # If FX failed, fall through to normal transcription

                    self.send_typing(chat_id)
                    log.info(f"[{user}] Voice message received, transcribing...")
                    text = self.voice.voice_to_text(file_id)
                    is_voice = True
                    if text.startswith("["):
                        # Transcription failed
                        self.send_message(chat_id, text)
                        return
                    log.info(f"[{user}] Transcribed: {text[:80]}")

                    # MODE PROMPT : écrire dans fichier sans réponse IA
                    if self._prompt_mode:
                        self._write_claude_task(text)
                        self.send_message(chat_id, f"✍️ {text[:300]}")
                        return
                    # Sinon : laisser le vocal passer comme message texte normal → réponse IA

            if not text:
                return

            log.info(f"[{user}] {text}")
            self.send_typing(chat_id)

            # Security: only respond to authorized chat
            if TELEGRAM_CHAT_ID and chat_id != TELEGRAM_CHAT_ID:
                self.send_message(chat_id, "Acces non autorise. Titan est reserve a son proprietaire.")
                return

            # Track interaction
            start_time = time.time()
            module_used = "brain"
            action_type = "message"

            try:
                # Check if user wants to exit president session
                if self._president_session and self._is_president_exit(text):
                    self._president_session = False
                    response = "Jacques raccroche. Titan reprend la main, boss."
                    module_used = "president"
                    action_type = "message"
                # President session active — everything goes to Jacques
                elif not text.startswith("/") and (self._president_session or self._is_president_talk(text)):
                    if not self._president_session:
                        self._president_session = True
                    response = await self._president_conversation(text)
                    module_used = "president"
                    action_type = "message"
                # Slash commands always go to normal routing (even during president session)
                elif text.startswith("/"):
                    response = await self._route_command(text, chat_id)
                    module_used = self._detect_module(text)
                    action_type = "command"
                else:
                    response = await self._route_command(text, chat_id)
                    module_used = self._detect_module(text)
                    action_type = "message"
            except Exception as e:
                log.error(f"Error: {e}")
                response = f"Erreur: {str(e)[:200]}"
                # Auto-healer: log and attempt fix
                try:
                    fix_msg = self.auto_healer.log_error(e, context=text[:100])
                    if fix_msg:
                        response += f"\n\n{fix_msg}"
                except Exception:
                    pass

            # === BUILDING LIFE AUTO-FEATURES (silent) ===
            # Coach: log activity for pattern detection
            try:
                self.coach.log_activity()
            except Exception:
                pass

            # Library: auto-extract gems from conversation
            if response and not text.startswith("/"):
                try:
                    self.library.auto_extract(text, response)
                except Exception:
                    pass

            # Auto-healer: log errors if any occurred
            # (errors are caught above and logged separately)

            # Gamification (silently in background, no footer)
            self.gamification.add_xp(action_type, module=module_used)
            self.gamification.check_daily_challenge()

            # Track in dashboard (silent)
            elapsed = time.time() - start_time
            self.dashboard.log_interaction(module_used, text[:50], elapsed)

            # Coach nudge — désactivé (spam non-demandé)
            # Augus peut le réactiver via /coach manuellement

            # Journal: intercept answers if journal is waiting
            if self.journal.is_waiting() and not text.startswith("/"):
                journal_reply = self.journal.receive_answer(text)
                if journal_reply:
                    response = journal_reply

            # Send text response only (skip if None — e.g. voice already sent)
            if response:
                log.info(f"[SENDING] len={len(response)} chars to {chat_id}")
                self.send_message(chat_id, response)
                log.info(f"[SENT OK] {response[:80]}...")

    # === NIGHTSHIFT HANDLER ===

    NIGHTSHIFT_FILE = Path(__file__).parent / "memory" / "nightshift.json"

    def _load_nightshift(self) -> dict:
        try:
            with open(self.NIGHTSHIFT_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"enabled": False, "tasks": [], "history": []}

    def _save_nightshift(self, data: dict):
        with open(self.NIGHTSHIFT_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _handle_nightshift(self, text: str) -> str:
        """Handle /nightshift commands."""
        from .scheduler import TitanScheduler

        arg = text[len("/nightshift"):].strip().lower()
        config = self._load_nightshift()
        catalog = TitanScheduler.NIGHTSHIFT_CATALOG

        # /nightshift (no arg) → show status
        if not arg or arg == "list":
            status = "ON" if config.get("enabled") else "OFF"
            tasks = config.get("tasks", [])
            lines = [f"🌙 NIGHTSHIFT — {status}\n"]
            if tasks:
                for t in tasks:
                    meta = catalog.get(t, {})
                    lines.append(f"  {meta.get('emoji', '⚙️')} {meta.get('label', t)} ({meta.get('hour', '?')}h)")
            else:
                lines.append("  Aucune tache configuree.")
            lines.append(f"\n📋 CATALOGUE DISPO:")
            for tid, meta in catalog.items():
                marker = " ✅" if tid in tasks else ""
                lines.append(f"  {meta['emoji']} {tid} — {meta['label']} ({meta['hour']}h){marker}")
            lines.append(f"\n/nightshift on|off\n/nightshift add <id>\n/nightshift remove <id>\n/nightshift clear")
            return "\n".join(lines)

        # /nightshift on
        if arg == "on":
            config["enabled"] = True
            self._save_nightshift(config)
            tasks = config.get("tasks", [])
            if not tasks:
                return "🌙 Nightshift ACTIVE — mais aucune tache configuree.\nUtilise /nightshift add <id> pour ajouter."
            return f"🌙 Nightshift ACTIVE — {len(tasks)} taches programmees."

        # /nightshift off
        if arg == "off":
            config["enabled"] = False
            self._save_nightshift(config)
            return "🔴 Nightshift desactive."

        # /nightshift clear
        if arg == "clear":
            config["tasks"] = []
            config["history"] = []
            self._save_nightshift(config)
            return "🗑️ Toutes les taches nightshift supprimees."

        # /nightshift add <task_id>
        if arg.startswith("add "):
            task_id = arg[4:].strip()
            if task_id not in catalog:
                available = ", ".join(catalog.keys())
                return f"Tache inconnue: {task_id}\nDisponibles: {available}"
            tasks = config.get("tasks", [])
            if task_id in tasks:
                return f"{task_id} deja dans le nightshift."
            tasks.append(task_id)
            config["tasks"] = tasks
            self._save_nightshift(config)
            meta = catalog[task_id]
            return f"{meta['emoji']} {meta['label']} ajoute au nightshift ({meta['hour']}h)."

        # /nightshift remove <task_id>
        if arg.startswith("remove ") or arg.startswith("rm "):
            task_id = arg.split(" ", 1)[1].strip()
            tasks = config.get("tasks", [])
            if task_id not in tasks:
                return f"{task_id} n'est pas dans le nightshift."
            tasks.remove(task_id)
            config["tasks"] = tasks
            self._save_nightshift(config)
            return f"Tache {task_id} retiree du nightshift."

        return "Commande inconnue. /nightshift pour voir les options."

    async def _route_command(self, text: str, chat_id: str) -> str:
        """Route message to the right module."""

        # =====================
        # === HELP & STATUS ===
        # =====================

        # =====================
        # === CLAUDE BRIDGE ===
        # =====================

        if text.startswith("/claude"):
            arg = text[7:].strip()

            if arg.lower() == "clear":
                from datetime import datetime
                task_file = self._get_claude_session_file()
                with open(task_file, "w", encoding="utf-8") as f:
                    f.write(f"# Session vocale — {datetime.now().strftime('%Y-%m-%d')}\n\n")
                return "Session du jour remise a zero."

            # Texte direct → ajouter au fichier
            if arg:
                self._write_claude_task(arg)
                return f"Ajoute : \"{arg[:300]}\""

            task_file = self._get_claude_session_file()
            return f"Tous tes vocaux sont enregistres automatiquement.\n\nFichier : prompt vocaux/{task_file.name}\n\n/claude <texte> — ajouter du texte\n/claude clear — vider la session"

        # === /prompt — Mode dictée vocale vers fichier ===
        if text.startswith("/prompt"):
            arg = text[7:].strip().lower()

            if arg in ("stop", "off", "fin", "end"):
                self._prompt_mode = False
                task_file = self._get_claude_session_file()
                return f"🔴 Mode dictée désactivé.\nFichier : prompt vocaux/{task_file.name}"

            if arg == "clear":
                task_file = self._get_claude_session_file()
                with open(task_file, "w", encoding="utf-8") as f:
                    f.write(f"# Session — {datetime.now().strftime('%Y-%m-%d')}\n\n")
                return "Session vidée."

            if arg == "show":
                task_file = self._get_claude_session_file()
                if task_file.exists():
                    content = task_file.read_text(encoding="utf-8")
                    return content[:3500] if content.strip() else "Fichier vide."
                return "Aucune session aujourd'hui."

            # Activer le mode
            self._prompt_mode = True
            task_file = self._get_claude_session_file()
            return f"🟢 Mode dictée activé.\nParle — chaque vocal sera transcrit dans :\nprompt vocaux/{task_file.name}\n\n/prompt stop — désactiver\n/prompt show — voir le contenu\n/prompt clear — vider"

        if text == "/start":
            return self._get_welcome()

        if text == "/webapp":
            # Open SLY-COMMAND dashboard as Telegram Mini App
            webapp_url = "https://sly-command.netlify.app"
            markup = {
                "inline_keyboard": [[{
                    "text": "\U0001f3ae SLY-COMMAND HQ",
                    "web_app": {"url": webapp_url}
                }]]
            }
            self._send_single(chat_id, "\U0001f3af Ouvre ton QG, Commandant.", reply_markup=markup)
            return None  # Already sent with markup

        if text == "/help":
            return self._get_help()

        if text == "/help2":
            return self._get_help2()

        # ==================
        # === GAMIFICATION ==
        # ==================

        if text in ("/profile", "/xp"):
            return self.gamification.get_profile()

        if text == "/achievements":
            return self.gamification.get_achievements_display()

        if text == "/daily":
            return self.gamification.get_daily_status()

        if text == "/leaderboard":
            return self.gamification.get_leaderboard_position()

        # =================
        # === DASHBOARD ===
        # =================

        if text in ("/dashboard", "/stats"):
            return self.dashboard.get_overview()

        if text == "/weekly":
            return self.dashboard.get_weekly_report()

        if text == "/heatmap":
            return self.dashboard.get_heatmap()

        # ===================
        # === NIGHTSHIFT ===
        # ===================

        if text.startswith("/nightshift"):
            return self._handle_nightshift(text)

        # ================
        # === R&D LAB ===
        # ================

        if text.startswith("/rdlab"):
            self.gamification.track_action("rdlab")
            return self.rdlab_doctorant.handle_command(text)

        # ============
        # === NEWS ===
        # ============

        if text == "/news":
            self.gamification.track_action("news_check")
            return await self.news.get_brief()

        if text == "/newsai":
            self.gamification.track_action("news_check")
            return await self.news.get_ai_summary()

        if text.startswith("/searchnews "):
            self.gamification.track_action("search")
            return await self.news.search_news(text[12:].strip())

        # =======================
        # === WEB & RECHERCHE ===
        # =======================

        if text.startswith("/search ") or text.startswith("/perplexity "):
            self.gamification.track_action("search")
            query = text.split(" ", 1)[1].strip() if " " in text else ""
            return await self.perplexity.search(query)

        if text == "/searchhistory":
            return self.perplexity.get_history()

        if text.startswith("/url "):
            self.gamification.track_action("search")
            return await self.web.get_url_summary(text[5:].strip())

        if text.startswith("/translate "):
            self.gamification.track_action("translate")
            parts = text[11:].split(" ", 1)
            if len(parts) == 2:
                return await self.web.translate(parts[1], parts[0])
            return await self.web.translate(parts[0])

        # ==============
        # === UPWORK ===
        # ==============

        if text.startswith("/analyze "):
            return await self.upwork.analyze_job(text[9:])

        if text.startswith("/proposal "):
            self.gamification.track_action("email_write")
            return await self.upwork.generate_proposal(text[10:])

        if text.startswith("/loom "):
            return await self.upwork.generate_loom_script(text[6:])

        # ============
        # === N8N ====
        # ============

        if text == "/n8n":
            return await self.n8n.get_status()

        if text.startswith("/workflow "):
            self.gamification.track_action("workflow_create")
            return await self.n8n.create_workflow(text[10:])

        # =============
        # === EMAIL ===
        # =============

        if text.startswith("/email "):
            self.gamification.track_action("email_write")
            return await self.email.write_email(text[7:])

        if text.startswith("/coldemail "):
            self.gamification.track_action("email_write")
            parts = text[11:].split("|", 1)
            if len(parts) == 2:
                return await self.email.cold_outreach(parts[0].strip(), parts[1].strip())
            return "Format: /coldemail cible | offre"

        if text.startswith("/followup "):
            self.gamification.track_action("email_write")
            parts = text[10:].split("|", 1)
            attempt = 1
            context = parts[0].strip()
            if len(parts) == 2:
                try:
                    attempt = int(parts[1].strip())
                except ValueError:
                    pass
            return await self.email.follow_up(context, attempt)

        if text.startswith("/rewrite "):
            return await self.email.rewrite(text[9:], "ameliore le ton et la clarte")

        # ============
        # === CODE ===
        # ============

        if text.startswith("/code "):
            self.gamification.track_action("code_generate")
            parts = text[6:].split("|", 1)
            lang = "python"
            desc = parts[0].strip()
            if len(parts) == 2:
                lang = parts[0].strip()
                desc = parts[1].strip()
            return await self.code.generate(desc, lang)

        if text.startswith("/debug "):
            self.gamification.track_action("code_generate")
            return await self.code.debug(text[7:])

        if text.startswith("/explain "):
            return await self.code.explain(text[9:])

        if text.startswith("/review "):
            return await self.code.review(text[8:])

        if text.startswith("/regex "):
            return await self.code.regex(text[7:])

        if text.startswith("/sql "):
            return await self.code.sql(text[5:])

        # =================
        # === PORTFOLIO ===
        # =================

        if text.startswith("/portfolio "):
            return await self.portfolio.generate(text[11:])

        if text.startswith("/clientproposal "):
            parts = text[16:].split("|", 1)
            if len(parts) == 2:
                return await self.portfolio.generate_proposal(parts[0].strip(), parts[1].strip())
            return "Format: /clientproposal nom client | description projet"

        # ================
        # === CALENDAR ===
        # ================

        if text.startswith("/task "):
            parts = text[6:].split("|")
            task = parts[0].strip()
            priority = parts[1].strip() if len(parts) > 1 else "normal"
            due = parts[2].strip() if len(parts) > 2 else None
            return self.calendar.add_task(task, priority, due)

        if text.startswith("/done "):
            self.gamification.track_action("task_complete")
            try:
                task_id = int(text[6:].strip())
                return self.calendar.complete_task(task_id)
            except ValueError:
                return "Usage: /done <numero>"

        if text.startswith("/deltask "):
            try:
                task_id = int(text[9:].strip())
                return self.calendar.delete_task(task_id)
            except ValueError:
                return "Usage: /deltask <numero>"

        if text == "/tasks":
            return self.calendar.list_tasks()

        if text in ("/today", "/plan"):
            return self.calendar.get_today_plan()

        if text.startswith("/habit "):
            return self.calendar.add_habit(text[7:].strip())

        if text.startswith("/checkhabit "):
            self.gamification.track_action("task_complete")
            return self.calendar.check_habit(text[12:].strip())

        if text == "/habits":
            return self.calendar.list_habits()

        if text == "/pomodoro" or text.startswith("/pomodoro "):
            task = text[10:].strip() if len(text) > 10 else "focus"
            return self.calendar.pomodoro_start(task)

        if text == "/break":
            return self.calendar.pomodoro_break()

        # =============
        # === VOICE ===
        # =============

        if text == "/voice" or text == "/voice list":
            return self.voice.list_elevenlabs_voices()

        if text.startswith("/voice "):
            args = text[7:].strip()
            parts = args.split(None, 1)
            # Check if first word is a voice name
            from .modules.voice import ELEVENLABS_VOICES
            if len(parts) >= 2 and parts[0].lower() in ELEVENLABS_VOICES:
                voice_name = parts[0].lower()
                voice_text = parts[1]
            else:
                voice_name = None
                voice_text = args
            result = await self.voice.speak_elevenlabs(chat_id, voice_text, voice_name)
            if result and result.startswith("Erreur"):
                return result
            return None

        # /voix <personnage> <texte> — Voice with character personality
        if text.startswith("/voix"):
            args = text[5:].strip()
            if not args or args == "list":
                return self.voice.list_characters()
            parts = args.split(None, 1)
            if len(parts) < 2:
                return self.voice.list_characters()
            character_key = parts[0].lower()
            voice_text = parts[1]
            result = await self.voice.speak_as_character(chat_id, voice_text, character_key)
            if result and result.startswith("Erreur"):
                return result
            if result and result.startswith("Personnage"):
                return result
            return None

        # /fx <effet> — Activate persistent FX mode OR apply to last voice
        if text.startswith("/fx"):
            args = text[3:].strip()
            if not args or args == "list":
                return self.voice.list_fx()
            fx_arg = args.lower()
            # /fx stop — desactive le mode
            if fx_arg in ("stop", "off", "none", "reset"):
                return self.voice.set_fx_mode(chat_id, "stop")
            # Activate persistent FX mode
            mode_result = self.voice.set_fx_mode(chat_id, fx_arg)
            if mode_result:
                # Also apply to last voice if available
                await self.voice.apply_fx_and_send(chat_id, fx_arg)
                return mode_result
            # Unknown FX
            result = await self.voice.apply_fx_and_send(chat_id, fx_arg)
            return result

        # ===============
        # === TOOLBOX ===
        # ===============

        if text.startswith("/calc "):
            return self.toolbox.calculate(text[6:].strip())

        if text.startswith("/convert "):
            parts = text[9:].split()
            if len(parts) == 3:
                try:
                    return self.toolbox.convert_units(float(parts[0]), parts[1], parts[2])
                except ValueError:
                    return "Format: /convert 100 km miles"
            return "Format: /convert <valeur> <de> <vers>"

        if text.startswith("/currency "):
            parts = text[10:].split()
            if len(parts) == 3:
                try:
                    return self.toolbox.convert_currency(float(parts[0]), parts[1], parts[2])
                except ValueError:
                    return "Format: /currency 100 EUR USD"
            return "Format: /currency <montant> <de> <vers>"

        if text.startswith("/timezone "):
            parts = text[10:].split()
            if len(parts) == 3:
                return self.toolbox.convert_timezone(parts[0], parts[1], parts[2])
            return "Format: /timezone 14:00 paris new_york"

        if text == "/password":
            return self.toolbox.generate_password()

        if text == "/uuid":
            return self.toolbox.generate_uuid()

        if text.startswith("/weather"):
            city = text[9:].strip() if len(text) > 9 else "Lyon"
            return self.toolbox.weather(city)

        if text == "/ip":
            return self.toolbox.ip_info()

        if text.startswith("/countdown "):
            parts = text[11:].split("|")
            if len(parts) == 2:
                return self.toolbox.countdown(parts[0].strip(), parts[1].strip())
            return "Format: /countdown nom | YYYY-MM-DD"

        if text.startswith("/freelance "):
            try:
                amount = float(text[11:].strip())
                return self.toolbox.freelance_rate(amount)
            except ValueError:
                return "Format: /freelance 60000"

        # ==============
        # === MEMORY ===
        # ==============

        if text.startswith("/remember "):
            self.gamification.track_action("memory_save")
            parts = text[10:].split(":", 1)
            if len(parts) == 2:
                return memory.remember(parts[0].strip(), parts[1].strip())
            return memory.remember("note", text[10:])

        if text.startswith("/recall "):
            return memory.recall(text[8:].strip())

        if text == "/memories":
            mems = memory.list_memories()
            if mems:
                lines = [f"🧠 MEMOIRE ({len(mems)} entrees)\n"]
                for m in mems:
                    lines.append(f"  [{m['category']}] {m['key']}: {m['value']}")
                return "\n".join(lines)
            return "Memoire vide."

        if text.startswith("/forget "):
            return memory.forget(text[8:].strip())

        if text == "/contacts":
            contacts = memory.list_contacts()
            if contacts:
                lines = [f"👥 CONTACTS ({len(contacts)})\n"]
                for c in contacts:
                    lines.append(f"  {c['name']} -- {c.get('role', '')} {c.get('context', '')}")
                return "\n".join(lines)
            return "Aucun contact en memoire."

        if text.startswith("/contact "):
            parts = text[9:].split("|")
            if len(parts) >= 2:
                name = parts[0].strip()
                info = {"role": parts[1].strip() if len(parts) > 1 else ""}
                if len(parts) > 2:
                    info["context"] = parts[2].strip()
                return memory.save_contact(name, info)
            else:
                contact = memory.get_contact(parts[0].strip())
                if contact:
                    response = f"👤 {contact['name']}\n"
                    for k, v in contact.items():
                        if k not in ["name", "saved_at"]:
                            response += f"  {k}: {v}\n"
                    return response
                return f"Contact '{parts[0].strip()}' pas trouve."

        if text == "/memstatus":
            facts = memory.get_auto_facts(50)
            manual = memory.list_memories()
            lines = [f"🧠 MEMOIRE TITAN\n"]
            lines.append(f"Faits auto ({len(facts)}) :")
            for f in facts[-20:]:
                lines.append(f"  [{f['category']}] {f['fact'][:80]}")
            if manual:
                lines.append(f"\nMémoire manuelle ({len(manual)}) :")
                for m in manual[:10]:
                    lines.append(f"  [{m['category']}] {m['key']}: {m['value'][:60]}")
            return "\n".join(lines) if len(lines) > 2 else "Mémoire vide."

        if text.startswith("/forgetfact "):
            return memory.forget_auto_fact(text[12:].strip())

        # memes — REMOVED

        # ==================
        # === MOTIVATION ===
        # ==================

        if text == "/motivation":
            return self.motivation.morning_motivation()
        if text == "/quote":
            return self.motivation.quote()
        if text == "/affirmation":
            return self.motivation.affirmation()
        if text == "/stoic":
            return self.motivation.stoic()
        if text == "/hustle":
            return self.motivation.hustle()
        if text == "/reflect":
            return self.motivation.weekly_reflection()

        # wiki, qrcode, horoscope, movies, fitness, riddles — REMOVED

        # =================
        # === AI PROMPT ===
        # =================

        if text.startswith("/midjourney "):
            return await self.ai_prompt.midjourney(text[12:].strip())
        if text.startswith("/dalle "):
            return await self.ai_prompt.dalle(text[7:].strip())
        if text.startswith("/sdprompt "):
            return await self.ai_prompt.stable_diffusion(text[10:].strip())
        if text.startswith("/promptgen "):
            return await self.ai_prompt.chatgpt_prompt(text[11:].strip())
        if text.startswith("/improvePrompt "):
            return await self.ai_prompt.improve_prompt(text[15:].strip())

        # ===========
        # === SEO ===
        # ===========

        if text.startswith("/seocheck "):
            return self.seo.check_site(text[10:].strip())
        if text.startswith("/keywords "):
            return await self.seo.keywords(text[10:].strip())
        if text.startswith("/metatags "):
            return await self.seo.meta_tags(text[10:].strip())

        # ===============
        # === DOMAINS ===
        # ===============

        if text.startswith("/domaincheck "):
            return self.domains.check(text[13:].strip())
        if text.startswith("/dns "):
            return self.domains.dns_lookup(text[5:].strip())
        if text.startswith("/domainsuggest "):
            return self.domains.suggest(text[15:].strip())

        # colors, encryption — REMOVED

        # ===============
        # === INVOICE ===
        # ===============

        if text.startswith("/invoice "):
            parts = text[9:].split("|", 1)
            if len(parts) == 2:
                return self.invoice_gen.generate(parts[0].strip(), parts[1].strip())
            return "Format: /invoice Client | prestation1:prix1, prestation2:prix2"
        if text.startswith("/estimate "):
            parts = text[10:].split("|", 1)
            if len(parts) == 2:
                return self.invoice_gen.estimate(parts[0].strip(), parts[1].strip())
            return "Format: /estimate Client | prestation1:prix1"

        # ====================
        # === SOCIAL MEDIA ===
        # ====================

        if text.startswith("/linkedin "):
            return await self.social.linkedin_post(text[10:].strip())
        if text.startswith("/thread "):
            return await self.social.twitter_thread(text[8:].strip())
        if text.startswith("/caption "):
            return await self.social.instagram_caption(text[9:].strip())
        if text.startswith("/hashtags "):
            return await self.social.hashtags(text[10:].strip())
        if text.startswith("/bio "):
            parts = text[5:].split("|", 1)
            if len(parts) == 2:
                return await self.social.bio(parts[0].strip(), parts[1].strip())
            return "Format: /bio plateforme | description"
        if text.startswith("/contentcal "):
            return await self.social.content_calendar(text[12:].strip())

        # fake_data, learning, ascii_art, recipes, music, json_tools — REMOVED

        # ===============
        # === STARTUP ===
        # ===============

        if text.startswith("/startupname "):
            return self.startup.name_generator(text[13:].strip())
        if text.startswith("/pitch "):
            return await self.startup.elevator_pitch(text[7:].strip())
        if text.startswith("/businessmodel "):
            return await self.startup.business_model(text[15:].strip())
        if text.startswith("/competitors "):
            return await self.startup.competitor_analysis(text[13:].strip())
        if text.startswith("/pricing "):
            return await self.startup.pricing_strategy(text[9:].strip())

        # travel — REMOVED

        # ===============
        # === WRITING ===
        # ===============

        if text.startswith("/blogpost "):
            return await self.writing.blog_post(text[10:].strip())
        if text.startswith("/copywriting "):
            return await self.writing.copywriting(text[13:].strip())
        if text.startswith("/story "):
            return await self.writing.story(text[7:].strip())
        if text.startswith("/summarize "):
            return await self.writing.summarize(text[11:].strip())
        if text.startswith("/paraphrase "):
            return await self.writing.paraphrase(text[12:].strip())
        if text.startswith("/slogan "):
            return await self.writing.slogan(text[8:].strip())

        # space — REMOVED

        # ====================
        # === PRODUCTIVITY ===
        # ====================

        if text.startswith("/eisenhower "):
            return self.productivity.eisenhower(text[12:].strip())
        if text.startswith("/smartgoal "):
            return await self.productivity.smart_goal(text[11:].strip())
        if text.startswith("/timeblock "):
            return self.productivity.time_block(text[11:].strip())
        if text.startswith("/pareto "):
            return self.productivity.pareto(text[8:].strip())
        if text == "/ruleof3":
            return self.productivity.rule_of_three()

        # movies_v2, music_v2, deals, booking — REMOVED

        # =============
        # === BIBLE ====
        # =============

        if text == "/verse":
            return self.bible.verse_of_day()
        if text.startswith("/bibletheme "):
            return self.bible.verse_theme(text[12:].strip())
        if text.startswith("/biblebook "):
            return self.bible.book_info(text[11:].strip())
        if text == "/proverb":
            return self.bible.proverb()
        if text.startswith("/devotion"):
            topic = text[10:].strip() if len(text) > 10 else ""
            return await self.bible.devotion(topic)
        if text.startswith("/versesearch "):
            return self.bible.search_verse(text[13:].strip())

        # ================
        # === AI WATCH ===
        # ================

        if text.startswith("/aitools"):
            cat = text[9:].strip() if len(text) > 9 else ""
            return self.ai_watch.tools(cat)
        if text == "/ainews":
            return self.ai_watch.news_sources()
        if text == "/aitrends":
            return await self.ai_watch.trend_analysis()
        if text == "/notaireia":
            return await self.ai_watch.notaire_ia()
        if text == "/aibusiness":
            return await self.ai_watch.business_opportunities()
        if text == "/aidigest":
            return await self.ai_watch.weekly_digest()

        # ==================
        # === STRATEGIC ====
        # ==================

        if text == "/intel":
            return await self.strategic.morning_intel()
        if text.startswith("/wealthplan "):
            return await self.strategic.wealth_plan(text[12:].strip())
        if text.startswith("/bizidea"):
            interest = text[9:].strip() if len(text) > 9 else ""
            return await self.strategic.business_idea(interest)
        if text.startswith("/marketanalysis "):
            return await self.strategic.market_analysis(text[16:].strip())
        if text.startswith("/negotiate "):
            return await self.strategic.negotiate_tips(text[11:].strip())
        if text == "/weeklyreview":
            return await self.strategic.weekly_review()
        if text == "/mindset":
            return self.strategic.mindset()
        if text == "/sidehustles":
            return await self.strategic.side_hustles()

        # =================
        # === SPORT PRO ===
        # =================

        if text.startswith("/sportlog "):
            parts = text[10:].strip().split("|")
            sport = parts[0].strip()
            duration = parts[1].strip() if len(parts) > 1 else "60"
            notes = parts[2].strip() if len(parts) > 2 else ""
            return self.sport_pro.log_session(sport, duration, notes)
        if text == "/sportstats":
            return self.sport_pro.stats()
        if text.startswith("/sportprog"):
            sport = text[11:].strip() if len(text) > 11 else "badminton"
            return self.sport_pro.program(sport)
        if text.startswith("/nutrition"):
            timing = text[11:].strip() if len(text) > 11 else "all"
            return self.sport_pro.nutrition_advice(timing)
        if text.startswith("/customworkout "):
            return await self.sport_pro.custom_program(text[15:].strip())
        if text == "/sportmotiv":
            return self.sport_pro.motivation_sport()

        # ===============
        # === CULTURE ===
        # ===============

        if text == "/fact":
            return self.culture.fact_of_day()
        if text == "/mentalmodel":
            return self.culture.mental_model()
        if text == "/bookreco":
            return self.culture.book_reco()
        if text == "/booklist":
            return self.culture.book_list()
        if text.startswith("/deeptopic "):
            return await self.culture.learn(text[11:].strip())
        if text.startswith("/debate "):
            return await self.culture.debate(text[8:].strip())
        if text == "/vocabulary":
            return self.culture.vocabulary()

        # ==================
        # === TASKMASTER ===
        # ==================

        if text.startswith("/taskadd "):
            parts = text[8:].strip().split("|")
            title = parts[0].strip()
            priority = parts[1].strip() if len(parts) > 1 else "medium"
            due = parts[2].strip() if len(parts) > 2 else ""
            category = parts[3].strip() if len(parts) > 3 else "general"
            return self.task_master.add(title, priority, due, category)
        if text == "/tasklist":
            return self.task_master.list_tasks()
        if text.startswith("/taskdone "):
            self.gamification.track_action("task_complete")
            return self.task_master.done(text[10:].strip())
        if text.startswith("/taskdelete "):
            return self.task_master.delete(text[12:].strip())
        if text == "/taskweek":
            return self.task_master.weekly_summary()
        if text == "/planday":
            return await self.task_master.plan_day()

        # personal — REMOVED

        # ===================
        # === PRESIDENT ===
        # ===================

        if text == "/president" or text == "/pres":
            return (
                "🏛 JACQUES — Le Président\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                "/briefing — Briefing présidentiel\n"
                "/goals <texte> — Objectifs semaine\n"
                "/ptask <texte> — Assigner une tâche\n"
                "/pdone <n> — Compléter tâche\n"
                "/ptasks — Voir les tâches\n"
                "/review — Revue de performance\n"
                "/directive <sujet> — Directive\n"
                "/decide <question> — DÉCISION ULTIME\n"
                "/roast — Se faire roaster\n"
                "/presidreset — Reset complet"
            )

        if text == "/briefing":
            return await self.president.morning_briefing()

        if text.startswith("/goals "):
            return await self.president.set_weekly_goals(text[7:].strip())

        if text.startswith("/ptask "):
            return await self.president.assign_task(text[7:].strip())

        if text.startswith("/pdone "):
            try:
                idx = int(text[7:].strip())
                return await self.president.complete_task(idx)
            except ValueError:
                return "Format: /pdone <numero>"

        if text == "/ptasks":
            return await self.president.get_tasks()

        if text == "/review":
            return await self.president.review_performance()

        if text.startswith("/directive "):
            return await self.president.get_directive(text[11:].strip())

        if text == "/roast":
            return await self.president.roast()

        if text.startswith("/decide "):
            return await self.president.decide(text[8:].strip())

        if text == "/presidreset":
            return await self.president.reset()

        # ==============
        # === BRIEF ====
        # ==============

        if text == "/brief":
            self.gamification.track_action("news_check")
            self.gamification.track_action("market_check")
            return await self._generate_brief()

        # ======================================
        # === BUILDING LIFE MODULES (12 new) ===
        # ======================================

        # Journal du Suzerain
        if text.startswith("/journal") or text == "/j":
            if self.journal.is_waiting():
                return self.journal.receive_answer(text)
            return self.journal.handle_command(text)

        # Agrégateur Personnel
        if text in ("/digest", "/agreg") or text.startswith("/digest "):
            return await self.aggregator.generate_daily_digest()

        # Coach Invisible (stats)
        if text.startswith("/coach") or text == "/stats":
            if text == "/stats":
                pass  # Let dashboard handle /stats above
            else:
                return self.coach.handle_command(text)

        # Auto-Healer
        if text in ("/health", "/healer") or text.startswith("/healer "):
            return self.auto_healer.handle_command(text)

        # Morning Digest (manual trigger)
        if text == "/morningdigest":
            return await self.morning_digest_mod.generate()

        # Mega-Prompt
        if text.startswith("/megaprompt") or text.startswith("/mega"):
            return self.mega_prompt.handle_command(text)

        # Film du Building
        if text.startswith("/film") or text == "/script":
            return self.film.handle_command(text)

        # Armée de Clones
        if text.startswith("/clone"):
            if text.lower().startswith("/clone ") and len(text) > 7:
                idea = text[7:].strip()
                return await self.clones.generate_clones(idea)
            return self.clones.handle_command(text)

        # Portfolio Vivant
        if text.startswith("/folio") or (text.startswith("/portfolio") and "add" in text.lower()):
            return self.portfolio_live.handle_command(text)

        # Empire Visuel
        if text.startswith("/visual") or text == "/brand":
            return self.empire_visual.handle_command(text)

        # Bibliothèque d'Augus
        if text.startswith("/library") or text == "/biblio":
            return self.library.handle_command(text)

        # =======================
        # === GRAND CONSEIL ===
        # =======================

        if text.startswith("/conseil"):
            self.gamification.track_action("council")
            try:
                from .classroom.council_engine import handle_command
                cmd_parts = text.split(" ", 1)
                cmd = cmd_parts[0].replace("/conseil-", "").replace("/conseil", "start")
                args = cmd_parts[1] if len(cmd_parts) > 1 else ""
                return await handle_command(cmd, args)
            except Exception as e:
                return f"❌ Grand Conseil erreur : {str(e)[:200]}"

        # =======================
        # === CLASSROOM ===
        # =======================

        if text.startswith("/classroom"):
            self.gamification.track_action("classroom")
            try:
                from .classroom.classroom_engine import handle_command as cr_handle
                cmd_parts = text.split(" ", 1)
                cmd = cmd_parts[0].replace("/classroom-", "").replace("/classroom", "start")
                args = cmd_parts[1] if len(cmd_parts) > 1 else ""
                return await cr_handle(cmd, args)
            except Exception as e:
                return f"❌ Classroom erreur : {str(e)[:200]}"

        # ===============================
        # === DEFAULT: BRAIN (AI) ===
        # ===============================

        return await self.brain.think(text, context="telegram")

    # === PRESIDENT AUTO-DETECT ===

    _PRESIDENT_KEYWORDS = [
        "président", "president", "jacques",
        "le pres", "le président", "le president",
        "dis jacques", "hé jacques", "hey jacques", "eh jacques",
        "jacques dit", "jacques pense", "demande à jacques", "demande a jacques",
        "avis du président", "avis du president",
        "qu'en pense jacques", "qu en pense jacques",
        "parle au président", "parle au president",
        "appelle jacques", "appelle le président", "appelle le president",
    ]

    _PRESIDENT_EXIT_KEYWORDS = [
        "merci jacques", "salut jacques", "ciao jacques",
        "ok merci", "c'est bon", "c est bon",
        "titan", "parle a titan", "parle à titan",
        "retour titan", "switch titan", "stop président", "stop president",
        "au revoir jacques", "bye jacques", "fini",
    ]

    def _is_president_talk(self, text: str) -> bool:
        """Detect if user is talking to/about the President Jacques."""
        lower = text.lower().strip()
        return any(kw in lower for kw in self._PRESIDENT_KEYWORDS)

    def _is_president_exit(self, text: str) -> bool:
        """Detect if user wants to end the president session."""
        lower = text.lower().strip()
        return any(kw in lower for kw in self._PRESIDENT_EXIT_KEYWORDS)

    async def _president_conversation(self, text: str) -> str:
        """Route natural language to Jacques the President."""
        from .modules import memory
        from .modules.president import _load_state
        # Always reload fresh state from disk
        state_data = _load_state()
        self.president.state = state_data
        goals = state_data.get("weekly_goals", [])
        recent = memory.get_conversation_context(5)

        prompt = f"""L'Empereur te parle directement. Il dit: "{text}"

CONTEXTE: Freelance AI/automation, objectifs: {json.dumps(goals, ensure_ascii=False) if goals else 'Aucun'}

REGLE ABSOLUE: Reponds en 2-5 phrases MAX. Conversationnel, direct, presidentiel. Pas de listes, pas de format structure. Parle comme dans une vraie conversation — court et tranchant. JAMAIS de scores ou de points. JAMAIS de questions."""

        reply = self.president._ai(prompt, max_tokens=400, mode="decide")
        memory.save_conversation(text, reply, "president")
        return reply

    # === BRIEF GENERATOR ===

    async def _generate_brief(self) -> str:
        """Generate the daily brief."""
        now = datetime.now()
        sections = [
            "╔══════════════════════════════╗",
            "║  T.I.T.A.N. — BRIEF         ║",
            f"║  {now.strftime('%d %B %Y'):^28} ║",
            "╚══════════════════════════════╝\n",
        ]

        # News
        try:
            news = await self.news.get_ai_summary()
            sections.append(f"📰 ACTUALITES\n{news}\n")
        except Exception as e:
            sections.append(f"📰 News indisponibles: {e}\n")

        # Tasks
        try:
            tasks = self.calendar.list_tasks()
            sections.append(f"✅ TACHES\n{tasks}\n")
        except Exception:
            pass

        # Habits
        try:
            habits = self.calendar.list_habits()
            if habits and "Aucune" not in habits:
                sections.append(f"🔄 HABITUDES\n{habits}\n")
        except Exception:
            pass

        # Mindset
        try:
            mindset = self.strategic.mindset()
            sections.append(f"\n{mindset}\n")
        except Exception:
            pass

        sections.append("⚡ Systèmes en ligne. L'Empire attend tes ordres, Sire.")
        return "\n".join(sections)

    # === HELPERS ===

    def _detect_module(self, text: str) -> str:
        """Detect which module was used for tracking."""
        cmd = text.split()[0].lower() if text.startswith("/") else ""

        module_map = {
            "/news": "news", "/newsai": "news", "/searchnews": "news",
            "/search": "perplexity", "/perplexity": "perplexity", "/searchhistory": "perplexity",
            "/url": "web", "/translate": "web",
            "/analyze": "upwork", "/proposal": "upwork", "/loom": "upwork",
            "/n8n": "n8n", "/workflow": "n8n",
            "/email": "email", "/coldemail": "email", "/followup": "email", "/rewrite": "email",
            "/code": "code", "/debug": "code", "/explain": "code", "/review": "code",
            "/regex": "code", "/sql": "code",
            "/portfolio": "portfolio", "/clientproposal": "portfolio",
            "/task": "calendar", "/done": "calendar", "/tasks": "calendar",
            "/today": "calendar", "/plan": "calendar", "/habit": "calendar",
            "/checkhabit": "calendar", "/habits": "calendar",
            "/pomodoro": "calendar", "/break": "calendar",
            "/voice": "voice", "/voix": "voice", "/fx": "voice",
            "/calc": "toolbox", "/convert": "toolbox", "/currency": "toolbox",
            "/timezone": "toolbox", "/password": "toolbox", "/uuid": "toolbox",
            "/weather": "toolbox", "/ip": "toolbox", "/countdown": "toolbox",
            "/freelance": "toolbox",
            "/profile": "gamification", "/xp": "gamification",
            "/achievements": "gamification", "/daily": "gamification",
            "/leaderboard": "gamification",
            "/dashboard": "dashboard", "/stats": "dashboard",
            "/weekly": "dashboard", "/heatmap": "dashboard",
            "/remember": "memory", "/recall": "memory", "/memories": "memory",
            "/forget": "memory", "/contacts": "memory", "/contact": "memory",
            "/brief": "brief",
        }

        # Extended modules (kept after audit)
        module_map.update({
            "/verse": "bible", "/bibletheme": "bible", "/biblebook": "bible",
            "/proverb": "bible", "/devotion": "bible", "/versesearch": "bible",
            "/aitools": "ai_watch", "/ainews": "ai_watch", "/aitrends": "ai_watch",
            "/notaireia": "ai_watch", "/aibusiness": "ai_watch", "/aidigest": "ai_watch",
            "/intel": "strategic", "/wealthplan": "strategic", "/bizidea": "strategic",
            "/marketanalysis": "strategic", "/negotiate": "strategic",
            "/weeklyreview": "strategic", "/mindset": "strategic", "/sidehustles": "strategic",
            "/sportlog": "sport", "/sportstats": "sport", "/sportprog": "sport",
            "/nutrition": "sport", "/customworkout": "sport", "/sportmotiv": "sport",
            # Building Life modules
            "/journal": "journal", "/j": "journal",
            "/digest": "aggregator", "/agreg": "aggregator",
            "/coach": "coach",
            "/health": "healer", "/healer": "healer",
            "/morningdigest": "morning_digest",
            "/megaprompt": "mega_prompt", "/mega": "mega_prompt",
            "/film": "film", "/script": "film",
            "/clone": "clones", "/clones": "clones",
            "/folio": "portfolio_live",
            "/visual": "empire_visual", "/brand": "empire_visual",
            "/library": "library", "/biblio": "library",
            "/fact": "culture", "/mentalmodel": "culture", "/bookreco": "culture",
            "/booklist": "culture", "/deeptopic": "culture", "/debate": "culture", "/vocabulary": "culture",
            "/taskadd": "taskmaster", "/tasklist": "taskmaster", "/taskdone": "taskmaster",
            "/taskdelete": "taskmaster", "/taskweek": "taskmaster", "/planday": "taskmaster",
            "/linkedin": "social", "/thread": "social", "/caption": "social",
            "/hashtags": "social", "/bio": "social", "/contentcal": "social",
            "/blogpost": "writing", "/copywriting": "writing", "/story": "writing",
            "/summarize": "writing", "/paraphrase": "writing", "/slogan": "writing",
            "/midjourney": "ai_prompt", "/dalle": "ai_prompt", "/sdprompt": "ai_prompt",
            "/promptgen": "ai_prompt", "/improvePrompt": "ai_prompt",
            "/seocheck": "seo", "/keywords": "seo", "/metatags": "seo",
            "/domaincheck": "domains", "/dns": "domains", "/domainsuggest": "domains",
            "/invoice": "invoice", "/estimate": "invoice",
            "/startupname": "startup", "/pitch": "startup", "/businessmodel": "startup",
            "/competitors": "startup", "/pricing": "startup",
            "/motivation": "motivation", "/quote": "motivation", "/affirmation": "motivation",
            "/stoic": "motivation", "/hustle": "motivation", "/reflect": "motivation",
            "/president": "president", "/briefing": "president", "/goals": "president",
            "/ptask": "president", "/pdone": "president", "/ptasks": "president",
            "/directive": "president", "/decide": "president", "/roast": "president",
        })
        return module_map.get(cmd, "brain")

    def _get_welcome(self) -> str:
        """Welcome message — futuristic HUD style."""
        return (
            "╔══════════════════════════════╗\n"
            "║  T.I.T.A.N. v3.0            ║\n"
            "║  Tactical Intelligence &     ║\n"
            "║  Total Autonomous Network    ║\n"
            "╚══════════════════════════════╝\n\n"
            "⚡ SYSTÈME INITIALISÉ\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            "▸ 32 modules — zero bloat\n"
            "▸ 150+ commandes actives\n"
            "▸ Cascade IA : 6 modèles\n"
            "▸ Coût opérationnel : 0€\n"
            "━━━━━━━━━━━━━━━━━━━━━\n\n"
            "🧠 IA libre\n"
            "📰 Veille IA       🎯 Stratégie\n"
            "💻 Code & Dev      🏛 Président\n"
            "🎤 20+ Voix        📚 Culture\n"
            "📧 Outreach        🏅 Sport\n\n"
            "Commandant. Systèmes prêts.\n"
            "/help → commandes  |  Parle-moi → IA"
        )

    def _get_help(self) -> str:
        """Help — futuristic HUD."""
        return (
            "╔══════════════════════════════╗\n"
            "║   T.I.T.A.N. — COMMANDES    ║\n"
            "╚══════════════════════════════╝\n\n"

            "⚡ CORE\n"
            "  (parle-moi) → IA libre\n"
            "  /brief → Brief quotidien\n\n"

            "🎯 STRATÉGIE & BUSINESS\n"
            "  /intel  /bizidea  /wealthplan\n"
            "  /marketanalysis  /negotiate\n"
            "  /sidehustles  /mindset\n"
            "  /pitch  /businessmodel  /pricing\n\n"

            "🤖 VEILLE IA\n"
            "  /aitools  /ainews  /aitrends\n"
            "  /aidigest  /aibusiness\n\n"

            "📋 TÂCHES\n"
            "  /task <texte>  /done <n>  /tasks\n"
            "  /habit <nom>  /pomodoro  /planday\n\n"

            "🏛 PRÉSIDENT JACQUES\n"
            "  /president  /briefing  /goals\n"
            "  /ptask  /pdone  /decide  /roast\n\n"

            "🎤 VOIX — 20+ imitations\n"
            "  /voix → liste des personnages\n"
            "  /voix <perso> <texte>\n"
            "  /fx → 18 effets vocaux\n\n"

            "📖 BIBLE  |  📚 CULTURE\n"
            "  /verse  /devotion  /fact\n"
            "  /bookreco  /debate\n\n"

            "🧠 MÉMOIRE\n"
            "  /remember  /recall  /contact\n\n"

            "/help2 → commandes avancées"
        )

    def _get_help2(self) -> str:
        """Advanced commands — HUD style."""
        return (
            "╔══════════════════════════════╗\n"
            "║  T.I.T.A.N. — AVANCÉ        ║\n"
            "╚══════════════════════════════╝\n\n"

            "📰 NEWS\n"
            "  /news  /newsai  /searchnews\n\n"

            "🌐 WEB & RECHERCHE\n"
            "  /search  /perplexity  /searchhistory\n"
            "  /url  /translate\n\n"

            "💼 UPWORK & CLIENTS\n"
            "  /analyze  /proposal  /loom\n"
            "  /portfolio  /invoice  /estimate\n\n"

            "📧 OUTREACH\n"
            "  /email  /coldemail  /followup\n"
            "  /linkedin  /thread  /caption\n\n"

            "💻 CODE\n"
            "  /code  /debug  /explain\n"
            "  /review  /regex  /sql\n\n"

            "🔧 TOOLBOX\n"
            "  /calc  /convert  /currency\n"
            "  /weather  /password  /countdown\n\n"

            "✍️ ÉCRITURE\n"
            "  /blogpost  /copywriting  /slogan\n"
            "  /summarize  /paraphrase\n\n"

            "🎨 PROMPTS IA\n"
            "  /midjourney  /dalle  /sdprompt\n"
            "  /promptgen  /improvePrompt\n\n"

            "📊 SEO & DOMAINES\n"
            "  /seocheck  /keywords  /metatags\n"
            "  /domaincheck  /dns\n\n"

            "🏅 SPORT & STATS\n"
            "  /sportlog  /sportstats  /sportprog\n"
            "  /dashboard  /weekly  /heatmap\n\n"

            "💪 MOTIVATION\n"
            "  /motivation  /quote  /stoic  /hustle"
        )

    # === MAIN LOOP ===

    def _load_offset(self) -> int:
        """Load persisted offset from disk to survive restarts."""
        from pathlib import Path
        offset_file = Path(__file__).parent / "memory" / "offset.txt"
        try:
            if offset_file.exists():
                return int(offset_file.read_text().strip())
        except Exception:
            pass
        return 0

    def _save_offset(self, offset: int):
        """Persist offset to disk."""
        from pathlib import Path
        offset_file = Path(__file__).parent / "memory" / "offset.txt"
        try:
            offset_file.write_text(str(offset))
        except Exception:
            pass

    async def run(self):
        """Main bot loop — Titan is alive."""
        self.running = True

        # Register lazy modules in brain (triggers lazy load only for these core ones)
        for name in ("news", "web", "upwork", "n8n", "email", "code", "portfolio"):
            self.brain.register_module(name, getattr(self, name))

        # Load persisted offset — prevents reprocessing on restart
        self.offset = self._load_offset()

        # On startup: drop pending updates to avoid replaying old messages
        # This also kicks out any other polling instance (Render etc.) — only 1 can poll at a time
        try:
            requests.post(
                f"{self.base_url}/deleteWebhook",
                json={"drop_pending_updates": True},
                timeout=5
            )
            log.info("  Startup: pending updates dropped (anti-doublon)")
        except Exception:
            pass

        # If offset is 0 (fresh start), get the latest update_id to skip old messages
        if self.offset == 0:
            try:
                resp = requests.get(
                    f"{self.base_url}/getUpdates",
                    params={"offset": -1, "limit": 1, "timeout": 0},
                    timeout=5
                )
                results = resp.json().get("result", [])
                if results:
                    self.offset = results[-1]["update_id"] + 1
                    self._save_offset(self.offset)
                    log.info(f"  Fresh start — offset set to {self.offset}")
            except Exception:
                pass

        log.info("=" * 50)
        log.info(f"  T.I.T.A.N. v3.0 — ONLINE")
        log.info(f"  32 modules — zero bloat")
        log.info(f"  Offset: {self.offset}")
        log.info(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        log.info("=" * 50)

        # No boot message — silent start, no spam

        while self.running:
            updates = self.get_updates()

            for update in updates:
                next_offset = update["update_id"] + 1
                # Persist offset BEFORE processing — even if handler crashes, won't replay
                if next_offset > self.offset:
                    self.offset = next_offset
                    self._save_offset(self.offset)

                if "message" in update:
                    await self.handle_message(update["message"])

            await asyncio.sleep(0.5)

    def stop(self):
        """Shutdown Titan."""
        self.running = False
        if TELEGRAM_CHAT_ID:
            self.send_message(TELEGRAM_CHAT_ID, "🔴 Titan hors ligne. A bientot boss.")
        log.info("Titan shutdown complete.")


async def main():
    """Entry point."""
    bot = TitanTelegram()
    try:
        await bot.run()
    except KeyboardInterrupt:
        bot.stop()


if __name__ == "__main__":
    asyncio.run(main())
