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

import requests

from .config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, TITAN_NAME
from .modules.brain import TitanBrain
from .modules.news import TitanNews
from .modules.web import TitanWeb
from .modules.finance import TitanFinance
from .modules.upwork import TitanUpwork
from .modules.n8n import TitanN8N
from .modules.email_gen import TitanEmailGen
from .modules.code_assistant import TitanCode
from .modules.portfolio_gen import TitanPortfolio
from .modules.calendar import TitanCalendar
from .modules.voice import TitanVoice
from .modules.toolbox import TitanToolbox
from .modules.gamification import TitanGamification
from .modules.dashboard import TitanDashboard
from .modules.memes import TitanMemes
from .modules.motivation import TitanMotivation
from .modules.wiki import TitanWiki
from .modules.qrcode_gen import TitanQRCode
from .modules.horoscope import TitanHoroscope
from .modules.movies import TitanMovies
from .modules.fitness import TitanFitness
from .modules.riddles import TitanRiddles
from .modules.ai_prompt import TitanAIPrompt
from .modules.crypto_defi import TitanDeFi
from .modules.seo import TitanSEO
from .modules.domains import TitanDomains
from .modules.colors import TitanColors
from .modules.encryption import TitanEncryption
from .modules.invoice import TitanInvoice
from .modules.social_media import TitanSocial
from .modules.fake_data import TitanFakeData
from .modules.learning import TitanLearning
from .modules.ascii_art import TitanASCII
from .modules.recipes import TitanRecipes
from .modules.music import TitanMusic
from .modules.json_tools import TitanJSON
from .modules.startup import TitanStartup
from .modules.travel import TitanTravel
from .modules.writing import TitanWriting
from .modules.space import TitanSpace
from .modules.productivity import TitanProductivity
from .modules.deals import TitanDeals
from .modules.booking import TitanBooking
from .modules.bible import TitanBible
from .modules.ai_watch import TitanAIWatch
from .modules.strategic import TitanStrategic
from .modules.sport_pro import TitanSportPro
from .modules.culture import TitanCulture
from .modules.task_master import TitanTaskMaster
from .modules.personal import TitanPersonal
from .modules.president import TitanPresident
from .modules import memory

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
        self.boot_timestamp = int(time.time())
        self.processed_messages = set()  # Track processed message IDs to prevent duplicates
        self._msg_lock = asyncio.Lock()  # Prevent parallel message processing
        self._president_session = False  # True = Jacques is talking, stays active

        # === Core ===
        self.brain = TitanBrain()

        # === Modules ===
        self.news = TitanNews()
        self.web = TitanWeb()
        self.finance = TitanFinance()
        self.upwork = TitanUpwork()
        self.n8n = TitanN8N()
        self.email = TitanEmailGen()
        self.code = TitanCode()
        self.portfolio = TitanPortfolio()
        self.calendar = TitanCalendar()
        self.voice = TitanVoice()
        self.toolbox = TitanToolbox()
        self.gamification = TitanGamification()
        self.dashboard = TitanDashboard()
        self.memes = TitanMemes()
        self.motivation = TitanMotivation()
        self.wiki = TitanWiki()
        self.qrcode = TitanQRCode()
        self.horoscope = TitanHoroscope()
        self.movies = TitanMovies()
        self.fitness = TitanFitness()
        self.riddles = TitanRiddles()
        self.ai_prompt = TitanAIPrompt()
        self.defi = TitanDeFi()
        self.seo = TitanSEO()
        self.domains = TitanDomains()
        self.colors = TitanColors()
        self.encryption = TitanEncryption()
        self.invoice_gen = TitanInvoice()
        self.social = TitanSocial()
        self.fake_data = TitanFakeData()
        self.learning = TitanLearning()
        self.ascii = TitanASCII()
        self.recipes = TitanRecipes()
        self.music = TitanMusic()
        self.json_tools = TitanJSON()
        self.startup = TitanStartup()
        self.travel = TitanTravel()
        self.writing = TitanWriting()
        self.space = TitanSpace()
        self.productivity = TitanProductivity()
        self.deals = TitanDeals()
        self.booking = TitanBooking()
        self.bible = TitanBible()
        self.ai_watch = TitanAIWatch()
        self.strategic = TitanStrategic()
        self.sport_pro = TitanSportPro()
        self.culture = TitanCulture()
        self.task_master = TitanTaskMaster()
        self.president = TitanPresident()

        # Register modules in brain
        self.brain.register_module("news", self.news)
        self.brain.register_module("web", self.web)
        self.brain.register_module("finance", self.finance)
        self.brain.register_module("upwork", self.upwork)
        self.brain.register_module("n8n", self.n8n)
        self.brain.register_module("email", self.email)
        self.brain.register_module("code", self.code)
        self.brain.register_module("portfolio", self.portfolio)

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

    def _send_single(self, chat_id: str, text: str, parse_mode: str = None) -> dict:
        """Send a single message."""
        data = {"chat_id": chat_id, "text": text}
        if parse_mode:
            data["parse_mode"] = parse_mode

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

            # Ignore old messages from before boot (prevents spam on restart)
            msg_date = message.get("date", 0)
            if msg_date < self.boot_timestamp:
                log.info(f"[SKIP] Old message from {user}: {text[:50]}")
                return

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

                    # Vocal commence par "claude" → fichier prompt vocaux
                    if text.lower().startswith("claude"):
                        instruction = text[6:].strip().lstrip(",:").strip()
                        self._write_claude_task(instruction)
                        self.send_message(chat_id, f"Transmis a Claude Code.\n\n\"{instruction[:300]}\"")
                        return
                    # Sinon → traitement normal (brain)

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

            # Gamification (silently in background, no footer)
            self.gamification.add_xp(action_type, module=module_used)
            self.gamification.check_daily_challenge()

            # Track in dashboard (silent)
            elapsed = time.time() - start_time
            self.dashboard.log_interaction(module_used, text[:50], elapsed)

            # Send text response only (skip if None — e.g. voice already sent)
            if response:
                log.info(f"[SENDING] len={len(response)} chars to {chat_id}")
                self.send_message(chat_id, response)
                log.info(f"[SENT OK] {response[:80]}...")

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

        if text == "/start":
            return self._get_welcome()

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

        # ===============
        # === FINANCE ===
        # ===============

        if text == "/crypto":
            self.gamification.track_action("market_check")
            prices = self.finance.get_crypto_prices()
            return self.finance.format_crypto_brief(prices)

        if text == "/stocks":
            self.gamification.track_action("market_check")
            return await self.finance.get_stocks_brief()

        if text == "/market":
            self.gamification.track_action("market_check")
            return await self.finance.analyze_market()

        # ============
        # === WEB ====
        # ============

        if text.startswith("/search "):
            self.gamification.track_action("search")
            return await self.web.search(text[8:].strip())

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

        if text.startswith("/voice "):
            voice_text = text[7:].strip()
            result = await self.voice.speak_and_send(chat_id, voice_text)
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

        # ==============
        # === MEMES ====
        # ==============

        if text == "/meme":
            return self.memes.random_meme()
        if text == "/funfact":
            return self.memes.fun_fact()
        if text == "/dadjoke":
            return self.memes.dad_joke()
        if text == "/thisday":
            return self.memes.this_day()

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

        # ================
        # === WIKIPEDIA ==
        # ================

        if text.startswith("/wiki "):
            return self.wiki.search(text[6:].strip())
        if text == "/randomwiki":
            return self.wiki.random_article()

        # ==============
        # === QRCODE ===
        # ==============

        if text.startswith("/qr "):
            return self.qrcode.generate(text[4:].strip())
        if text.startswith("/qrwifi "):
            parts = text[8:].split("|")
            if len(parts) >= 2:
                return self.qrcode.wifi(parts[0].strip(), parts[1].strip())
            return "Format: /qrwifi SSID | password"

        # =================
        # === HOROSCOPE ===
        # =================

        if text.startswith("/horoscope "):
            return self.horoscope.daily(text[11:].strip())
        if text.startswith("/compat "):
            parts = text[8:].split()
            if len(parts) == 2:
                return self.horoscope.compatibility(parts[0], parts[1])
            return "Format: /compat belier lion"

        # ==============
        # === MOVIES ===
        # ==============

        if text == "/trending":
            return self.movies.trending()
        if text.startswith("/moviesearch "):
            return self.movies.search(text[13:].strip())
        if text.startswith("/recommend "):
            return self.movies.recommend(text[11:].strip())
        if text == "/randommovie":
            return self.movies.random_movie()

        # ===============
        # === FITNESS ===
        # ===============

        if text.startswith("/workout"):
            group = text[9:].strip() if len(text) > 9 else "full"
            return self.fitness.workout(group)
        if text.startswith("/bmi "):
            parts = text[5:].split()
            if len(parts) == 2:
                try:
                    return self.fitness.bmi(float(parts[0]), float(parts[1]))
                except ValueError:
                    pass
            return "Format: /bmi 75 180 (kg cm)"
        if text.startswith("/calories "):
            parts = text[10:].split()
            if len(parts) >= 3:
                try:
                    return self.fitness.calories(float(parts[0]), float(parts[1]), int(parts[2]))
                except ValueError:
                    pass
            return "Format: /calories 75 180 25 (kg cm age)"
        if text == "/stretch":
            return self.fitness.stretch()
        if text == "/7min":
            return self.fitness.challenge_7min()

        # ===============
        # === RIDDLES ===
        # ===============

        if text == "/riddle":
            return self.riddles.riddle()
        if text == "/trivia":
            return self.riddles.trivia_api()
        if text == "/wyr":
            return self.riddles.would_you_rather()
        if text == "/mathchallenge":
            return self.riddles.math_challenge()

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

        # ================
        # === DEFI/CRYPTO =
        # ================

        if text.startswith("/token "):
            return self.defi.token_info(text[7:].strip())
        if text == "/feargreed":
            return self.defi.fear_greed()
        if text == "/trendingcrypto":
            return self.defi.trending_coins()
        if text == "/gas":
            return self.defi.gas_tracker()

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

        # ==============
        # === COLORS ===
        # ==============

        if text.startswith("/palette"):
            style = text[9:].strip() if len(text) > 9 else "random"
            return self.colors.palette(style)
        if text == "/palettes":
            return self.colors.list_palettes()
        if text == "/randomcolor":
            return self.colors.random_color()
        if text.startswith("/brandcolors "):
            return self.colors.brand_colors(text[13:].strip())
        if text.startswith("/gradient "):
            parts = text[10:].split()
            if len(parts) == 2:
                return self.colors.gradient(parts[0], parts[1])
            return "Format: /gradient #FF0000 #0000FF"

        # ==================
        # === ENCRYPTION ===
        # ==================

        if text.startswith("/hash "):
            return self.encryption.hash_all(text[6:].strip())
        if text.startswith("/base64 "):
            return self.encryption.base64_encode(text[8:].strip())
        if text.startswith("/base64d "):
            return self.encryption.base64_decode(text[9:].strip())
        if text.startswith("/morse "):
            return self.encryption.morse_encode(text[7:].strip())
        if text == "/gentoken":
            return self.encryption.generate_token()
        if text == "/apikey":
            return self.encryption.generate_api_key()

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

        # =================
        # === FAKE DATA ===
        # =================

        if text == "/fakeperson":
            return self.fake_data.person()
        if text == "/fakecompany":
            return self.fake_data.company()
        if text == "/fakecard":
            return self.fake_data.credit_card()
        if text.startswith("/fakeemails"):
            count = 10
            parts = text.split()
            if len(parts) > 1:
                try:
                    count = int(parts[1])
                except ValueError:
                    pass
            return self.fake_data.email_list(count)
        if text == "/fakejson":
            return self.fake_data.lorem_json()
        if text == "/fakedataset":
            return self.fake_data.dataset()

        # ================
        # === LEARNING ===
        # ================

        if text.startswith("/learn "):
            return await self.learning.explain(text[7:].strip())
        if text.startswith("/flashcards "):
            return await self.learning.flashcards(text[12:].strip())
        if text.startswith("/cheatsheet "):
            return await self.learning.cheatsheet(text[12:].strip())
        if text.startswith("/studyplan "):
            return await self.learning.study_plan(text[11:].strip())
        if text.startswith("/eli5 "):
            return await self.learning.eli5(text[6:].strip())
        if text.startswith("/quiz "):
            return await self.learning.quiz(text[6:].strip())

        # ================
        # === ASCII ART ==
        # ================

        if text.startswith("/ascii "):
            return self.ascii.text_art(text[7:].strip())
        if text.startswith("/box "):
            return self.ascii.box(text[5:].strip())
        if text.startswith("/banner "):
            return self.ascii.banner(text[8:].strip())

        # ===============
        # === RECIPES ===
        # ===============

        if text == "/quickmeal":
            return self.recipes.quick_meal()
        if text.startswith("/recipe "):
            return await self.recipes.recipe(text[8:].strip())
        if text.startswith("/mealplan"):
            goal = text[10:].strip() if len(text) > 10 else "equilibre"
            return await self.recipes.meal_plan(goal)
        if text.startswith("/ingredients "):
            return await self.recipes.with_ingredients(text[13:].strip())

        # =============
        # === MUSIC ===
        # =============

        if text.startswith("/playlist "):
            return self.music.playlist(text[10:].strip())
        if text == "/playlists":
            return self.music.genres()
        if text == "/albumreco":
            return self.music.album_reco()
        if text == "/songofday":
            return self.music.song_of_day()
        if text.startswith("/artist "):
            return self.music.artist_search(text[8:].strip())

        # ============
        # === JSON ===
        # ============

        if text.startswith("/jsonformat "):
            return self.json_tools.format(text[12:].strip())
        if text.startswith("/jsonvalidate "):
            return self.json_tools.validate(text[14:].strip())
        if text.startswith("/jsonsample"):
            structure = text[12:].strip() if len(text) > 12 else "user"
            return self.json_tools.sample(structure)

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

        # ==============
        # === TRAVEL ===
        # ==============

        if text.startswith("/country "):
            return self.travel.country_info(text[9:].strip())
        if text.startswith("/cityguide "):
            return await self.travel.city_guide(text[11:].strip())
        if text.startswith("/packing"):
            return self.travel.packing_list()
        if text == "/destination":
            return self.travel.random_destination()

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

        # =============
        # === SPACE ===
        # =============

        if text == "/iss":
            return self.space.iss_location()
        if text == "/astronauts":
            return self.space.people_in_space()
        if text == "/apod":
            return self.space.apod()
        if text.startswith("/planet "):
            return self.space.planet_facts(text[8:].strip())

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

        # ==============
        # === MOVIES v2 ==
        # ==============

        if text.startswith("/movietop"):
            cat = text[10:].strip() if len(text) > 10 else "all_time"
            return self.movies.top(cat)
        if text.startswith("/moviereco "):
            return self.movies.recommend(text[11:].strip())
        if text.startswith("/movieai "):
            return await self.movies.ai_recommend(text[9:].strip())
        if text.startswith("/rt "):
            return self.movies.rt_search(text[4:].strip())
        if text == "/whatson":
            return self.movies.whats_on()

        # =====================
        # === MUSIC v2 ========
        # =====================

        if text.startswith("/discover "):
            return await self.music.discover(text[10:].strip())
        if text.startswith("/similar "):
            return await self.music.similar_to(text[9:].strip())
        if text.startswith("/topalbums"):
            genre = text[11:].strip() if len(text) > 11 else "all"
            return self.music.top_albums(genre)
        if text == "/newmusic":
            return self.music.new_releases_links()

        # ==============
        # === DEALS ====
        # ==============

        if text.startswith("/flights"):
            parts = text[9:].strip().split() if len(text) > 9 else []
            origin = parts[0] if len(parts) > 0 else "PAR"
            dest = parts[1] if len(parts) > 1 else ""
            budget = parts[2] if len(parts) > 2 else "300"
            return self.deals.cheap_flights(origin, dest, budget)
        if text == "/weekenddeals":
            return self.deals.weekend_deals()
        if text.startswith("/hotels "):
            parts = text[8:].strip().split("|")
            city = parts[0].strip()
            checkin = parts[1].strip() if len(parts) > 1 else ""
            nights = parts[2].strip() if len(parts) > 2 else "2"
            return self.deals.hotel_deals(city, checkin, nights)
        if text == "/errorfares":
            return self.deals.error_fares()
        if text.startswith("/traveladvice "):
            return await self.deals.travel_advisor(text[14:].strip())

        # ================
        # === BOOKING ====
        # ================

        if text.startswith("/bookbad"):
            city = text[9:].strip() if len(text) > 9 else "paris"
            return self.booking.anybuddy("badminton", city)
        if text.startswith("/bookpadel"):
            city = text[11:].strip() if len(text) > 11 else "paris"
            return self.booking.padel(city)
        if text.startswith("/booktennis"):
            city = text[12:].strip() if len(text) > 12 else "paris"
            return self.booking.tennis(city)
        if text.startswith("/bookfoot"):
            city = text[10:].strip() if len(text) > 10 else "paris"
            return self.booking.foot5(city)
        if text.startswith("/bookescalade"):
            city = text[14:].strip() if len(text) > 14 else "paris"
            return self.booking.escalade(city)
        if text.startswith("/bookgym"):
            city = text[9:].strip() if len(text) > 9 else "paris"
            return self.booking.gym(city)
        if text.startswith("/bookany "):
            parts = text[9:].strip().split()
            sport = parts[0] if parts else "badminton"
            city = parts[1] if len(parts) > 1 else "paris"
            return self.booking.anybuddy(sport, city)
        if text == "/sports":
            return self.booking.sports_list()

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

        # ================
        # === PERSONAL ===
        # ================

        if text == "/myprofile":
            return self.brain.personal.get_profile_summary()
        if text.startswith("/profileset "):
            parts = text[12:].strip().split(" ", 1)
            if len(parts) == 2:
                return self.brain.personal.update_profile(parts[0], parts[1])
            return "Format: /profileset champ valeur"
        if text.startswith("/profileclear "):
            return self.brain.personal.clear_field(text[14:].strip())

        # ===================
        # === PRESIDENT ===
        # ===================

        if text == "/president" or text == "/pres":
            return (
                "JACQUES — Le President\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n"
                "/briefing — Briefing presidentiel du matin\n"
                "/goals <texte> — Definir objectifs semaine\n"
                "/task <texte> — Assigner une tache\n"
                "/donetask <n> — Marquer tache completee\n"
                "/tasks — Voir les taches en cours\n"
                "/review — Revue de performance\n"
                "/directive <sujet> — Directive sur un sujet\n"
                "/decide <question> — DECISION ULTIME de Jacques\n"
                "/roast — Se faire roaster\n"
                "/presidreset — Reset complet"
            )

        if text == "/briefing":
            return await self.president.morning_briefing()

        if text.startswith("/goals "):
            return await self.president.set_weekly_goals(text[7:].strip())

        if text.startswith("/task "):
            return await self.president.assign_task(text[6:].strip())

        if text.startswith("/donetask "):
            try:
                idx = int(text[10:].strip())
                return await self.president.complete_task(idx)
            except ValueError:
                return "Format: /donetask <numero>"

        if text == "/tasks":
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
        score = state_data.get("performance_score", 50)
        recent = memory.get_conversation_context(5)

        prompt = f"""Augustin te parle directement. Il dit: "{text}"

CONTEXTE: Freelance AI/automation, score {score}/100, objectifs: {json.dumps(goals, ensure_ascii=False) if goals else 'Aucun'}

REGLE ABSOLUE: Reponds en 2-5 phrases MAX. Conversationnel, direct, presidentiel. Pas de listes, pas de format structure. Parle comme dans une vraie conversation — court et tranchant."""

        reply = self.president._ai(prompt, max_tokens=400, mode="decide")
        memory.save_conversation(text, reply, "president")
        return reply

    # === BRIEF GENERATOR ===

    async def _generate_brief(self) -> str:
        """Generate the daily brief."""
        now = datetime.now()
        sections = [
            f"{'=' * 30}",
            f"  BRIEF TITAN",
            f"  {now.strftime('%A %d %B %Y')}",
            f"{'=' * 30}\n",
        ]

        # News
        try:
            news = await self.news.get_ai_summary()
            sections.append(f"📰 ACTUALITES\n{news}\n")
        except Exception as e:
            sections.append(f"📰 News indisponibles: {e}\n")

        # Crypto
        try:
            crypto = await self.finance.get_crypto_brief()
            sections.append(f"{crypto}\n")
        except Exception as e:
            sections.append(f"🪙 Crypto indisponible: {e}\n")

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

        # Daily challenge
        try:
            daily = self.gamification.get_daily_status()
            sections.append(f"\n{daily}\n")
        except Exception:
            pass

        # TaskMaster proactive check
        try:
            task_alert = self.task_master.proactive_check()
            if task_alert:
                sections.append(f"\n{task_alert}\n")
        except Exception:
            pass

        # Bible verse
        try:
            verse = self.bible.verse_of_day()
            sections.append(f"\n{verse}\n")
        except Exception:
            pass

        # Culture fact
        try:
            fact = self.culture.fact_of_day()
            sections.append(f"\n{fact}\n")
        except Exception:
            pass

        # Mindset
        try:
            mindset = self.strategic.mindset()
            sections.append(f"\n{mindset}\n")
        except Exception:
            pass

        sections.append("Bonne journée boss. Go conquérir le monde. 💪")
        return "\n".join(sections)

    # === HELPERS ===

    def _detect_module(self, text: str) -> str:
        """Detect which module was used for tracking."""
        cmd = text.split()[0].lower() if text.startswith("/") else ""

        module_map = {
            "/news": "news", "/newsai": "news", "/searchnews": "news",
            "/crypto": "finance", "/stocks": "finance", "/market": "finance",
            "/search": "web", "/url": "web", "/translate": "web",
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

        # New modules
        module_map.update({
            "/movietop": "movies", "/moviereco": "movies", "/movieai": "movies",
            "/rt": "movies", "/whatson": "movies",
            "/discover": "music", "/similar": "music", "/topalbums": "music", "/newmusic": "music",
            "/flights": "deals", "/weekenddeals": "deals", "/hotels": "deals",
            "/errorfares": "deals", "/traveladvice": "deals",
            "/bookbad": "booking", "/bookpadel": "booking", "/booktennis": "booking",
            "/bookfoot": "booking", "/bookescalade": "booking", "/bookgym": "booking",
            "/bookany": "booking", "/sports": "booking",
            "/verse": "bible", "/bibletheme": "bible", "/biblebook": "bible",
            "/proverb": "bible", "/devotion": "bible", "/versesearch": "bible",
            "/aitools": "ai_watch", "/ainews": "ai_watch", "/aitrends": "ai_watch",
            "/notaireia": "ai_watch", "/aibusiness": "ai_watch", "/aidigest": "ai_watch",
            "/intel": "strategic", "/wealthplan": "strategic", "/bizidea": "strategic",
            "/marketanalysis": "strategic", "/negotiate": "strategic",
            "/weeklyreview": "strategic", "/mindset": "strategic", "/sidehustles": "strategic",
            "/sportlog": "sport", "/sportstats": "sport", "/sportprog": "sport",
            "/nutrition": "sport", "/customworkout": "sport", "/sportmotiv": "sport",
            "/fact": "culture", "/mentalmodel": "culture", "/bookreco": "culture",
            "/booklist": "culture", "/deeptopic": "culture", "/debate": "culture", "/vocabulary": "culture",
            "/taskadd": "taskmaster", "/tasklist": "taskmaster", "/taskdone": "taskmaster",
            "/taskdelete": "taskmaster", "/taskweek": "taskmaster", "/planday": "taskmaster",
        })
        return module_map.get(cmd, "brain")

    def _get_welcome(self) -> str:
        """Welcome message — stylish."""
        return (
            f"{'=' * 30}\n"
            f"  🏛 TITAN v2.0\n"
            f"  L'Empereur des Agents IA\n"
            f"{'=' * 30}\n\n"
            f"Ah, te voilà boss. J'ai cru que t'allais me laisser m'ennuyer.\n\n"
            f"🧠 Intelligence artificielle\n"
            f"📰 News & Veille IA\n"
            f"💰 Finance, Crypto & Stratégie\n"
            f"✈️ Deals voyage & Bons plans\n"
            f"🏸 Réservation sport (Anybuddy)\n"
            f"🎬 Films & Séries (Rotten Tomatoes)\n"
            f"🎵 Découverte musicale IA\n"
            f"📖 Bible & Dévotion\n"
            f"🏋️ Coach sportif\n"
            f"📚 Culture & Savoir\n"
            f"🎯 TaskMaster proactif\n"
            f"💡 Business & Side Hustles\n"
            f"+ 40 autres modules\n\n"
            f"50 modules. 250+ commandes. 0 excuse.\n\n"
            f"Tape /help pour les commandes.\n"
            f"Ou parle-moi, je comprends tout."
        )

    def _get_help(self) -> str:
        """Complete help — all commands."""
        return (
            f"🏛 TITAN v2.0 — L'EMPEREUR\n"
            f"{'=' * 30}\n\n"

            f"🧠 INTELLIGENCE\n"
            f"  (parle-moi) — IA conversationnelle\n"
            f"  /brief — Brief quotidien\n\n"

            f"🎯 STRATÉGIE & BUSINESS\n"
            f"  /intel — Brief stratégique du matin\n"
            f"  /bizidea [domaine] — Idée business\n"
            f"  /wealthplan <situation> — Plan enrichissement\n"
            f"  /marketanalysis <marché> — Analyse marché\n"
            f"  /negotiate <contexte> — Stratégie négo\n"
            f"  /sidehustles — Side hustles tech\n"
            f"  /weeklyreview — Revue stratégique\n"
            f"  /mindset — Mindset du jour\n\n"

            f"🤖 VEILLE IA\n"
            f"  /aitools [cat] — Meilleurs outils IA\n"
            f"  /ainews — Sources veille IA\n"
            f"  /aitrends — Tendances IA actuelles\n"
            f"  /aidigest — Digest IA hebdo\n"
            f"  /notaireia — IA pour notaires\n"
            f"  /aibusiness — Opportunités IA\n\n"

            f"📋 TASKMASTER\n"
            f"  /taskadd titre [|prio|date|cat]\n"
            f"  /tasklist — Voir tâches\n"
            f"  /taskdone <id> — Compléter\n"
            f"  /taskweek — Bilan hebdo\n"
            f"  /planday — Plan du jour IA\n\n"

            f"✈️ DEALS & VOYAGES\n"
            f"  /flights [origin dest budget]\n"
            f"  /weekenddeals — Weekends pas chers\n"
            f"  /hotels ville [|checkin|nuits]\n"
            f"  /errorfares — Erreurs tarifaires\n"
            f"  /traveladvice <demande>\n\n"

            f"🏸 RÉSERVATION SPORT\n"
            f"  /bookbad [ville] — Badminton\n"
            f"  /bookpadel [ville] — Padel\n"
            f"  /booktennis [ville] — Tennis\n"
            f"  /bookfoot [ville] — Foot 5\n"
            f"  /bookescalade [ville] — Escalade\n"
            f"  /bookgym [ville] — Salle\n"
            f"  /sports — Liste complète\n\n"

            f"🏋️ SPORT PRO\n"
            f"  /sportlog sport [|durée|notes]\n"
            f"  /sportstats — Mes stats\n"
            f"  /sportprog [sport] — Programme\n"
            f"  /nutrition [timing] — Nutrition\n"
            f"  /customworkout <objectif>\n"
            f"  /sportmotiv — Motivation\n\n"

            f"🎬 FILMS & SÉRIES\n"
            f"  /trending — Tendances\n"
            f"  /moviesearch <nom> — Chercher\n"
            f"  /movietop [cat] — Top listes\n"
            f"  /moviereco <mood> — Par humeur\n"
            f"  /movieai <goûts> — Reco IA\n"
            f"  /rt <film> — Rotten Tomatoes\n"
            f"  /whatson — Streaming\n\n"

            f"🎵 MUSIQUE\n"
            f"  /playlist <mood> — Playlist\n"
            f"  /discover <goûts> — Découverte IA\n"
            f"  /similar <artiste> — Similaires\n"
            f"  /topalbums [genre] — Top albums\n"
            f"  /songofday — Chanson du jour\n"
            f"  /newmusic — Nouveautés\n\n"

            f"📖 BIBLE\n"
            f"  /verse — Verset du jour\n"
            f"  /bibletheme <thème> — Par thème\n"
            f"  /proverb — Proverbe\n"
            f"  /devotion [sujet] — Dévotion IA\n"
            f"  /versesearch <mot>\n\n"

            f"📚 CULTURE & SAVOIR\n"
            f"  /fact — Fait du jour\n"
            f"  /mentalmodel — Modèle mental\n"
            f"  /bookreco — Livre à lire\n"
            f"  /deeptopic <sujet> — Deep dive\n"
            f"  /debate <sujet> — Débat\n"
            f"  /vocabulary — Mot du jour\n\n"

            f"👔 LE PRESIDENT\n"
            f"  /president — Menu President\n"
            f"  /briefing — Briefing du matin\n"
            f"  /goals <texte> — Objectifs semaine\n"
            f"  /task <texte> — Assigner tache\n"
            f"  /donetask <n> — Completer tache\n"
            f"  /tasks — Voir taches\n"
            f"  /review — Revue performance\n"
            f"  /directive <sujet> — Directive\n"
            f"  /roast — Se faire roaster\n"
            f"  /decide <question> — DECISION ULTIME\n\n"

            f"Tape /help2 pour les commandes avancées."
        )

    def _get_help2(self) -> str:
        """Advanced help — more commands."""
        return (
            f"🏛 TITAN — COMMANDES AVANCÉES\n"
            f"{'=' * 30}\n\n"

            f"📰 NEWS & FINANCE\n"
            f"  /news /newsai /searchnews\n"
            f"  /crypto /stocks /market\n\n"

            f"🌐 WEB & SEARCH\n"
            f"  /search /url /translate\n\n"

            f"💼 UPWORK\n"
            f"  /analyze /proposal /loom\n\n"

            f"📧 EMAILS\n"
            f"  /email /coldemail /followup /rewrite\n\n"

            f"💻 CODE\n"
            f"  /code /debug /explain /review /regex /sql\n\n"

            f"🔧 TOOLBOX\n"
            f"  /calc /convert /currency /timezone\n"
            f"  /password /uuid /weather /ip /countdown\n\n"

            f"🎨 CRÉATIF\n"
            f"  /midjourney /dalle /sdprompt /promptgen\n"
            f"  /blogpost /copywriting /story /slogan\n"
            f"  /linkedin /thread /caption /hashtags\n"
            f"  /ascii /banner /palette /colors\n\n"

            f"🧰 OUTILS DEV\n"
            f"  /seocheck /keywords /metatags\n"
            f"  /domaincheck /dns /domainsuggest\n"
            f"  /hash /base64 /morse /gentoken\n"
            f"  /jsonformat /jsonvalidate /jsonsample\n"
            f"  /invoice /estimate\n\n"

            f"🎤 VOICE & FX\n"
            f"  /voice <texte> — Vocal TTS\n"
            f"  /voix <perso> <texte> — Vocal style perso\n"
            f"  /voix list — Liste personnages\n"
            f"  /fx <effet> — Effet sur dernier vocal\n"
            f"  /fx list — Liste effets\n\n"

            f"🎲 FUN\n"
            f"  /meme /funfact /dadjoke /riddle\n"
            f"  /trivia /horoscope /randomwiki\n"
            f"  /iss /astronauts /apod\n\n"

            f"🧠 MEMOIRE\n"
            f"  /remember /recall /memories /forget\n"
            f"  /contact /contacts\n\n"

            f"🏅 GAMIFICATION\n"
            f"  /profile /achievements /daily /leaderboard\n"
            f"  /dashboard /weekly /heatmap"
        )

    # === MAIN LOOP ===

    async def run(self):
        """Main bot loop — Titan is alive."""
        self.running = True

        log.info("=" * 50)
        log.info(f"  {TITAN_NAME} v1.0 — ONLINE")
        log.info(f"  Modules: 50 modules actifs — L'Empereur est en ligne")
        log.info(f"  Memory: loaded")
        log.info(f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        log.info("=" * 50)

        # No boot message — silent start, no spam

        while self.running:
            updates = self.get_updates()

            for update in updates:
                self.offset = update["update_id"] + 1

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
