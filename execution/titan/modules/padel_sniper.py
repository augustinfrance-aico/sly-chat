"""
TITAN PadelSniper — Réservation automatique PadelShot Craponne
Stratégie : snipe à minuit J-16 + 1 scan annulations/jour à 12h30
Créneaux cibles : Ven 16h-18h / Sam 16h-18h / Dim 16h-18h
Mode discret : 1 seule piste réservée par créneau horaire
"""

import asyncio
import json
import logging
import os
from datetime import datetime, timedelta, time as dtime

import aiohttp

logger = logging.getLogger("titan.padel_sniper")

# --- Config ---
BASE_URL = "https://padelshot-fr.matchpoint.com.es"
COURT_ID = 6  # Padel Lyon (Craponne) — 7 pistes

# Créneaux cibles : (weekday, heure) — 4=ven, 5=sam, 6=dim
# Couverture 16h-18h = slots de 30 min : 16:00, 16:30, 17:00, 17:30
TARGET_SLOTS = [
    (4, "16:00"), (4, "16:30"), (4, "17:00"), (4, "17:30"),
    (5, "16:00"), (5, "16:30"), (5, "17:00"), (5, "17:30"),
    (6, "16:00"), (6, "16:30"), (6, "17:00"), (6, "17:30"),
]

JOURS_FR = {0: "Lundi", 1: "Mardi", 2: "Mercredi", 3: "Jeudi",
            4: "Vendredi", 5: "Samedi", 6: "Dimanche"}

# Fenêtre de réservation PadelShot = 16 jours calendaires, ouverture à minuit
BOOKING_WINDOW_DAYS = 16


class PadelSniper:
    """Réservation automatique PadelShot via Playwright."""

    def __init__(self):
        self.email = os.getenv("PADELSHOT_EMAIL", "")
        self.password = os.getenv("PADELSHOT_PASSWORD", "")
        self.telegram_token = os.getenv("TELEGRAM_BOT_TOKEN", "")
        self.telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID", "")  # Augus
        self.charlotte_chat_id = os.getenv("CHARLOTTE_TELEGRAM_CHAT_ID", "")  # Charlotte
        self._alerted: set[str] = set()
        # Heure du scan quotidien d'annulations (12h30 = pause dej, pic d'annulations)
        self.daily_scan_hour = 12
        self.daily_scan_minute = 30

    # ── Login ──

    async def _login(self, page) -> bool:
        """Login MatchPoint via Playwright."""
        try:
            await page.goto(f"{BASE_URL}/Login.aspx", wait_until="networkidle")
            await page.evaluate(
                "document.querySelectorAll('.banner-block-screen,.banner-cookies,[class*=cookie]').forEach(e=>e.remove())"
            )
            await asyncio.sleep(0.3)
            await page.fill("input[type=text]", self.email)
            await page.fill("input[type=password]", self.password)
            await page.click("input[type=submit]", force=True)
            await page.wait_for_load_state("networkidle")

            if "Login.aspx" not in page.url:
                logger.info("Login OK")
                return True
            logger.error("Login FAIL")
            return False
        except Exception as e:
            logger.error(f"Login error: {e}")
            return False

    async def _goto_grid(self, page) -> bool:
        """Naviguer vers Grid.aspx et vérifier l'API key."""
        await page.goto(f"{BASE_URL}/Booking/Grid.aspx", wait_until="networkidle")
        await asyncio.sleep(1)
        has_key = await page.evaluate("() => typeof hl90njda2b89k !== 'undefined'")
        return has_key

    # ── Disponibilités ──

    async def _get_grid(self, page, date_str: str) -> dict:
        """Récupère la grille complète pour une date (DD/MM/YYYY)."""
        try:
            return await page.evaluate("""
                async (params) => {
                    const r = await fetch('/booking/srvc.aspx/ObtenerCuadro', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json; charset=utf-8'},
                        body: JSON.stringify({
                            idCuadro: params.courtId,
                            fecha: params.date,
                            key: hl90njda2b89k
                        })
                    });
                    return (await r.json()).d;
                }
            """, {"courtId": COURT_ID, "date": date_str}) or {}
        except Exception as e:
            logger.error(f"Get grid error: {e}")
            return {}

    def _find_free_courts(self, grid: dict, target_hour: str) -> list[dict]:
        """Retourne les pistes libres avec leurs infos (index, id, nom)."""
        free = []
        for idx, col in enumerate(grid.get("Columnas", [])):
            occs = col.get("Ocupaciones", [])
            busy = any(
                o.get("StrHoraInicio", "") <= target_hour < o.get("StrHoraFin", "")
                for o in occs
            )
            if not busy:
                free.append({
                    "index": idx,
                    "id": col.get("Id"),
                    "name": col.get("TextoPrincipal", "?"),
                    "modalidad": col.get("IdModalidadFijaParaReservas"),
                })
        return free

    # ── Réservation via clic navigateur ──

    async def _book_slot(self, page, date_str: str, hour: str, court_info: dict) -> bool:
        """
        Réserve un créneau en simulant le parcours utilisateur complet.
        1. Charge la grille au bon jour
        2. Clique sur le créneau libre
        3. Accepte les conditions
        4. Confirme la réservation
        """
        try:
            # S'assurer qu'on est sur Grid.aspx
            if "Grid.aspx" not in page.url:
                await self._goto_grid(page)

            # Sélectionner "Padel Lyon" dans le dropdown si besoin
            await page.evaluate("""() => {
                var sel = document.querySelector('#ddlCuadros, select');
                if (sel) {
                    for (var i = 0; i < sel.options.length; i++) {
                        if (sel.options[i].value == '6') {
                            sel.selectedIndex = i;
                            sel.dispatchEvent(new Event('change'));
                            break;
                        }
                    }
                }
            }""")
            await asyncio.sleep(0.5)

            # Changer la date via le datepicker
            await page.evaluate(f"""() => {{
                var dp = document.querySelector('#fechaTabla');
                if (dp && $.fn.datepicker) {{
                    var parts = '{date_str}'.split('/');
                    var d = new Date(parts[2], parts[1]-1, parts[0]);
                    $(dp).datepicker('setDate', d);
                    $(dp).trigger('change');
                }}
            }}""")
            await asyncio.sleep(1)

            # Charger la grille
            await page.evaluate(f"""() => {{
                if (typeof obtenerCuadro === 'function') {{
                    obtenerCuadro('{date_str}', 6, {{
                        success: prepararSvg,
                        beforeSend: function(){{}}
                    }});
                }}
            }}""")
            await asyncio.sleep(2)

            # Cliquer sur le créneau libre
            # Le créneau est identifié par sa position dans la grille SVG
            col_index = court_info["index"]
            clicked = await page.evaluate(f"""() => {{
                // Trouver le slot libre dans le SVG
                // Les slots libres sont des rectangles cliquables
                var svgEl = document.querySelector('#svgTabla, svg');
                if (!svgEl) return 'no_svg';

                // Appeler la fonction AJAX directement (plus fiable que cliquer sur le SVG)
                if (typeof ajaxObtenerInformacionHuecoLibre === 'function') {{
                    ajaxObtenerInformacionHuecoLibre('{hour}', {col_index});
                    return 'clicked';
                }}
                return 'no_function';
            }}""")

            if clicked != "clicked":
                logger.error(f"Click failed: {clicked}")
                return False

            await asyncio.sleep(2)

            # Vérifier si le dialogue de réservation est ouvert
            dialog_open = await page.evaluate("""() => {
                var dlg = document.querySelector('#dialogReserva');
                return dlg && dlg.style.display !== 'none';
            }""")

            if not dialog_open:
                # Peut-être que le slot n'a pas d'options (hors horaires)
                logger.warning("Dialog not open — slot may not be bookable")
                return False

            # Chercher le bouton de réservation dans le dialogue
            # Le flow MatchPoint redirige vers Mediator.aspx avec un token
            booked = await page.evaluate("""() => {
                // Chercher les liens/boutons de réservation dans le SVG du dialog
                var links = document.querySelectorAll('#dialogReserva a, #dialogReserva [onclick]');
                for (var el of links) {
                    var onclick = el.getAttribute('onclick') || '';
                    var href = el.getAttribute('href') || '';
                    if (onclick.includes('Mediator') || href.includes('Mediator')) {
                        // Simuler le clic
                        el.click();
                        return 'mediator_clicked';
                    }
                }
                // Chercher aussi dans les SVG rect/text
                var svgTexts = document.querySelectorAll('#dialogReserva text, #dialogReserva rect');
                for (var el of svgTexts) {
                    var onclick = el.getAttribute('onclick') || '';
                    if (onclick.includes('Mediator') || onclick.includes('location.href')) {
                        eval(onclick.replace('$:', ''));
                        return 'svg_clicked';
                    }
                }
                return 'no_booking_button';
            }""")

            if booked in ("mediator_clicked", "svg_clicked"):
                # Attendre la page Mediator
                await page.wait_for_load_state("networkidle")
                logger.info(f"Mediator page: {page.url}")

                # Sur Mediator.aspx, accepter les conditions et confirmer
                # Cocher la checkbox des conditions si elle existe
                checkbox = page.locator('input[type=checkbox]')
                if await checkbox.count() > 0:
                    await checkbox.first.check(force=True)

                # Cliquer sur le bouton de confirmation
                confirm_btn = page.locator('input[type=submit], button[type=submit], .btnConfirmar, [id*=Confirm], [id*=Reservar]')
                if await confirm_btn.count() > 0:
                    await confirm_btn.first.click(force=True)
                    await page.wait_for_load_state("networkidle")
                    logger.info(f"Booking confirmed! URL: {page.url}")
                    return True
                else:
                    # Peut-être paiement en ligne requis
                    logger.warning(f"No confirm button on Mediator: {page.url}")
                    return False

            logger.warning(f"Booking button not found: {booked}")
            return False

        except Exception as e:
            logger.error(f"Book slot error: {e}")
            return False

    # ── Alertes Telegram ──

    async def _send_telegram_to(self, chat_id: str, message: str):
        """Envoie un message Telegram à un chat_id spécifique."""
        if not self.telegram_token or not chat_id:
            return
        try:
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            async with aiohttp.ClientSession() as http:
                await http.post(url, json={
                    "chat_id": chat_id,
                    "text": message,
                })
        except Exception as e:
            logger.error(f"Telegram error ({chat_id}): {e}")

    async def _send_telegram(self, message: str):
        """Envoie un message Telegram à Augus."""
        await self._send_telegram_to(self.telegram_chat_id, message)

    async def _notify_all(self, message: str):
        """Envoie un message à Augus ET Charlotte (pour les réservations)."""
        await self._send_telegram_to(self.telegram_chat_id, message)
        if self.charlotte_chat_id and self.charlotte_chat_id != self.telegram_chat_id:
            await self._send_telegram_to(self.charlotte_chat_id, message)

    # ── Scan (surveillance) ──

    async def scan(self) -> list[dict]:
        """Scan les créneaux cibles sur 16 jours."""
        from playwright.async_api import async_playwright

        results = []
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            if not await self._login(page):
                await browser.close()
                return results

            if not await self._goto_grid(page):
                await browser.close()
                return results

            today = datetime.now()
            for offset in range(BOOKING_WINDOW_DAYS):
                d = today + timedelta(days=offset)
                weekday = d.weekday()

                for target_wd, target_hour in TARGET_SLOTS:
                    if weekday != target_wd:
                        continue

                    date_str = d.strftime("%d/%m/%Y")
                    jour = JOURS_FR[weekday]
                    grid = await self._get_grid(page, date_str)
                    free = self._find_free_courts(grid, target_hour)

                    if free:
                        slot_key = f"{date_str}_{target_hour}"
                        results.append({
                            "date": date_str,
                            "jour": jour,
                            "hour": target_hour,
                            "free_courts": free,
                            "is_new": slot_key not in self._alerted,
                        })
                        self._alerted.add(slot_key)

                    await asyncio.sleep(0.2)

            await browser.close()
        return results

    # ── Snipe (réservation à l'ouverture) ──

    async def snipe(self, target_date: datetime = None):
        """
        Mode sniper : attend minuit J-16 et réserve instantanément.
        Si target_date est None, calcule automatiquement le prochain créneau cible.
        """
        from playwright.async_api import async_playwright

        if target_date is None:
            target_date = self._next_target_date()
            if target_date is None:
                logger.info("Aucun créneau cible dans les prochains jours")
                return

        # Calculer quand le créneau s'ouvre (minuit, 16 jours avant)
        opening_time = datetime.combine(
            target_date.date() - timedelta(days=BOOKING_WINDOW_DAYS),
            dtime(0, 0, 0)
        )

        # Déterminer les heures cibles pour ce jour
        target_hours = [h for wd, h in TARGET_SLOTS if wd == target_date.weekday()]
        date_str = target_date.strftime("%d/%m/%Y")
        jour = JOURS_FR[target_date.weekday()]

        logger.info(
            f"SNIPE: {jour} {date_str} @ {', '.join(target_hours)}"
            f" — ouverture à {opening_time.strftime('%d/%m %H:%M')}"
        )

        # Attendre jusqu'à 1 minute avant l'ouverture
        now = datetime.now()
        wait_until = opening_time - timedelta(minutes=1)
        if now < wait_until:
            wait_seconds = (wait_until - now).total_seconds()
            logger.info(f"Attente {wait_seconds/3600:.1f}h avant le snipe...")
            await self._send_telegram(
                f"🏸 SNIPE programme\n"
                f"Cible: {jour} {date_str} @ {', '.join(target_hours)}\n"
                f"Ouverture dans {wait_seconds/3600:.1f}h"
            )
            await asyncio.sleep(wait_seconds)

        # Se connecter 1 minute avant
        logger.info("Login pre-snipe...")
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            if not await self._login(page):
                await self._send_telegram("❌ SNIPE ECHEC — login impossible")
                await browser.close()
                return

            if not await self._goto_grid(page):
                await self._send_telegram("❌ SNIPE ECHEC — grille inaccessible")
                await browser.close()
                return

            # Attendre minuit pile
            now = datetime.now()
            if now < opening_time:
                wait = (opening_time - now).total_seconds()
                logger.info(f"Attente {wait:.0f}s avant minuit...")
                await asyncio.sleep(max(0, wait))

            # GO — tenter de réserver chaque heure cible
            booked = []
            for target_hour in target_hours:
                logger.info(f"Tentative: {date_str} {target_hour}...")

                # Rafraîchir la grille
                grid = await self._get_grid(page, date_str)
                free = self._find_free_courts(grid, target_hour)

                if not free:
                    logger.warning(f"Aucune piste libre à {target_hour}")
                    continue

                # Essayer chaque piste libre
                for court in free:
                    logger.info(f"  Réservation {court['name']} {target_hour}...")
                    success = await self._book_slot(page, date_str, target_hour, court)
                    if success:
                        booked.append(f"{court['name']} {target_hour}")
                        logger.info(f"  RESERVE! {court['name']} {target_hour}")
                        break
                    else:
                        logger.warning(f"  Echec {court['name']}, next...")
                        # Recharger Grid pour retry
                        await self._goto_grid(page)

                # Un seul créneau par heure suffit
                if any(target_hour in b for b in booked):
                    continue

            await browser.close()

        # Rapport — envoyé à tout le monde si réservation, sinon juste Augus
        if booked:
            msg = (
                f"✅ SNIPE REUSSI!\n\n"
                f"PadelShot Craponne — {jour} {date_str}\n"
                + "\n".join(f"  🏸 {b}" for b in booked)
            )
            await self._notify_all(msg)
        else:
            msg = (
                f"❌ SNIPE ECHEC\n\n"
                f"{jour} {date_str} — tous les creneaux pris\n"
                f"Les {', '.join(target_hours)} étaient déjà réservés."
            )
            await self._send_telegram(msg)
        logger.info(msg)

    def _next_target_date(self) -> datetime | None:
        """Retourne la prochaine date cible (Ven/Sam/Dim) dans la fenêtre de réservation."""
        today = datetime.now()
        target_weekdays = {wd for wd, _ in TARGET_SLOTS}
        for offset in range(1, BOOKING_WINDOW_DAYS + 7):
            d = today + timedelta(days=offset)
            if d.weekday() in target_weekdays:
                return datetime.combine(d.date(), dtime(0, 0))
        return None

    def _next_snipe_targets(self) -> list[tuple[datetime, datetime]]:
        """
        Retourne TOUS les prochains snipes : (target_date, opening_time).
        Inclut chaque Ven/Sam/Dim qui s'ouvre dans les 7 prochains jours.
        """
        targets = []
        today = datetime.now()

        for days_ahead in range(7):
            opening_midnight = datetime.combine(
                today.date() + timedelta(days=days_ahead),
                dtime(0, 0, 0)
            )
            # Quel jour s'ouvre à ce minuit ?
            target_date = opening_midnight.date() + timedelta(days=BOOKING_WINDOW_DAYS)
            if target_date.weekday() in (4, 5, 6):  # Ven, Sam, Dim
                # Seulement si l'ouverture est dans le futur
                if opening_midnight > today:
                    targets.append((
                        datetime.combine(target_date, dtime(0, 0)),
                        opening_midnight,
                    ))
        return targets

    # ── Auto-book (réservation depuis scan) ──

    async def _auto_book_slots(self, free_slots: list[dict]):
        """
        Réserve les créneaux libres détectés.
        Mode discret : 1 seule piste par créneau horaire (pas de spam).
        """
        from playwright.async_api import async_playwright

        if not free_slots:
            return

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            if not await self._login(page) or not await self._goto_grid(page):
                await browser.close()
                return

            for s in free_slots:
                # 1 seule piste par créneau — prendre la première dispo
                court = s["free_courts"][0]
                success = await self._book_slot(page, s["date"], s["hour"], court)
                if success:
                    await self._notify_all(
                        f"✅ RESERVE!\n"
                        f"PadelShot Craponne\n"
                        f"{s['jour']} {s['date']} {s['hour']}\n"
                        f"Piste: {court['name']}"
                    )
                else:
                    logger.warning(f"Auto-book echec: {s['date']} {s['hour']} {court['name']}")

                # Délai entre chaque tentative (discret)
                await asyncio.sleep(3)

            await browser.close()

    # ── Scheduler (boucle continue) ──

    async def run_scheduler(self):
        """
        Boucle infinie avec 2 modes :
        1. SNIPE : à chaque minuit, réserve les créneaux qui viennent d'ouvrir (J-16)
        2. SCAN : 1x/jour à 12h30, surveille les annulations et auto-book
        Mode discret : 1 piste par créneau, délais entre requêtes.
        """
        logger.info("PadelSniper scheduler actif (snipe minuit + scan 12h30)")

        snipe_targets = self._next_snipe_targets()
        target_info = "\n".join(
            f"  {JOURS_FR[t.weekday()]} {t.strftime('%d/%m')} (ouvre {o.strftime('%d/%m %H:%M')})"
            for t, o in snipe_targets
        ) if snipe_targets else "  Aucun dans les 7 prochains jours"

        await self._send_telegram(
            f"🏸 PadelSniper actif\n"
            f"Mode: SNIPE minuit + SCAN 12h30\n"
            f"1 scan/jour, 1 piste/creneau (discret)\n\n"
            f"Prochains snipes:\n{target_info}"
        )

        last_scan_date = None  # Pour ne scanner qu'1x/jour

        while True:
            try:
                now = datetime.now()

                # --- SNIPE : vérifier si un minuit approche ---
                snipe_targets = self._next_snipe_targets()
                for target_date, opening_time in snipe_targets:
                    time_until = (opening_time - now).total_seconds()

                    if 0 < time_until <= 90:
                        logger.info(f"SNIPE imminent: {target_date.strftime('%d/%m')} dans {time_until:.0f}s")
                        await self.snipe(target_date)
                        await asyncio.sleep(5)
                        break

                # --- SCAN QUOTIDIEN : 12h30, 1x/jour ---
                today_date = now.date()
                scan_time_reached = (
                    now.hour > self.daily_scan_hour
                    or (now.hour == self.daily_scan_hour and now.minute >= self.daily_scan_minute)
                )

                if scan_time_reached and last_scan_date != today_date:
                    logger.info("Scan quotidien 12h30 — recherche annulations...")
                    slots = await self.scan()
                    last_scan_date = today_date

                    if slots:
                        new_slots = [s for s in slots if s.get("is_new")]
                        if new_slots:
                            lines = ["🏸 ANNULATION DETECTEE!\n"]
                            for s in new_slots:
                                names = ", ".join(c["name"] for c in s["free_courts"])
                                lines.append(
                                    f"✅ {s['jour']} {s['date']} {s['hour']}\n"
                                    f"   Pistes: {names}"
                                )
                            await self._send_telegram("\n".join(lines))

                            # Auto-book (1 piste par créneau, discret)
                            await self._auto_book_slots(new_slots)

                        logger.info(f"Scan: {len(slots)} libres, {len([s for s in slots if s.get('is_new')])} nouveaux")
                    else:
                        logger.info("Scan quotidien: aucun creneau libre")
                        await self._send_telegram(
                            f"🏸 Scan quotidien {now.strftime('%d/%m %H:%M')}\n"
                            f"Aucun creneau libre Ven/Sam/Dim 16h-18h"
                        )

                # --- Calcul du prochain réveil ---
                # Prochain événement = soit minuit (snipe), soit 12h30 (scan)
                next_wake = None

                # Prochain snipe
                for _, opening_time in self._next_snipe_targets():
                    secs = (opening_time - datetime.now()).total_seconds()
                    if secs > 90:
                        next_wake = secs - 60  # Se réveiller 1 min avant
                        break
                    elif secs > 0:
                        next_wake = 10
                        break

                # Prochain scan quotidien
                if last_scan_date == today_date:
                    # Déjà scanné aujourd'hui → prochain scan demain 12h30
                    tomorrow_scan = datetime.combine(
                        today_date + timedelta(days=1),
                        dtime(self.daily_scan_hour, self.daily_scan_minute)
                    )
                else:
                    # Pas encore scanné → scan à 12h30 aujourd'hui (ou immédiat si passé)
                    today_scan = datetime.combine(
                        today_date,
                        dtime(self.daily_scan_hour, self.daily_scan_minute)
                    )
                    tomorrow_scan = today_scan if today_scan > datetime.now() else datetime.combine(
                        today_date + timedelta(days=1),
                        dtime(self.daily_scan_hour, self.daily_scan_minute)
                    )

                scan_secs = (tomorrow_scan - datetime.now()).total_seconds()
                if scan_secs > 0:
                    if next_wake is None or scan_secs < next_wake:
                        next_wake = scan_secs

                # Minimum 60s, maximum 6h entre les réveils
                sleep_time = max(60, min(next_wake or 3600, 21600))
                logger.info(f"Prochain reveil dans {sleep_time/60:.0f}min")
                await asyncio.sleep(sleep_time)

            except Exception as e:
                logger.error(f"Scheduler error: {e}")
                await self._send_telegram(f"⚠️ PadelSniper erreur: {e}")
                await asyncio.sleep(300)

    # ── Entry points ──

    async def run_once(self) -> str:
        """Scan unique — retourne résumé texte."""
        slots = await self.scan()

        if not slots:
            # Info sur le prochain snipe
            target = self._next_target_date()
            if target:
                opening = datetime.combine(
                    target.date() - timedelta(days=BOOKING_WINDOW_DAYS),
                    dtime(0, 0)
                )
                jour = JOURS_FR[target.weekday()]
                hours = [h for wd, h in TARGET_SLOTS if wd == target.weekday()]
                return (
                    f"🏸 PADEL SNIPER — Scan termine\n\n"
                    f"❌ Aucun creneau libre Ven/Sam/Dim 16h-18h\n\n"
                    f"Prochain snipe: {jour} {target.strftime('%d/%m/%Y')} "
                    f"@ {', '.join(hours)}\n"
                    f"Ouverture: {opening.strftime('%d/%m/%Y')} a minuit"
                )
            return "🏸 PADEL SNIPER — Aucun creneau libre"

        lines = ["🏸 PADEL SNIPER — Creneaux trouves!\n"]
        for slot in slots:
            names = ", ".join(c["name"] for c in slot["free_courts"])
            lines.append(
                f"✅ {slot['jour']} {slot['date']} {slot['hour']}\n"
                f"   Pistes: {names}"
            )
        return "\n".join(lines)


# --- Entry points pour TITAN / CLI ---
async def padel_scan() -> str:
    sniper = PadelSniper()
    return await sniper.run_once()

async def padel_snipe():
    sniper = PadelSniper()
    await sniper.snipe()

async def padel_scheduler():
    sniper = PadelSniper()
    await sniper.run_scheduler()
