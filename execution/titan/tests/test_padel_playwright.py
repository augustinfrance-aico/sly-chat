"""Test PadelShot login via Playwright — intercept API calls."""
import asyncio
import json
import os
import sys
import io
from datetime import datetime, timedelta
from dotenv import load_dotenv

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
load_dotenv()


async def test():
    from playwright.async_api import async_playwright

    email = os.getenv("PADELSHOT_EMAIL")
    pwd = os.getenv("PADELSHOT_PASSWORD")
    base = "https://padelshot-fr.matchpoint.com.es"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        # Intercepter les requetes API
        api_responses = []

        async def handle_response(response):
            url = response.url
            if "srvc.aspx" in url:
                try:
                    body = await response.json()
                    api_responses.append({"url": url, "data": body})
                except Exception:
                    pass

        page.on("response", handle_response)

        # === LOGIN ===
        print("=== LOGIN ===")
        await page.goto(f"{base}/Login.aspx", wait_until="networkidle")
        print(f"Page title: {await page.title()}")

        # Accept cookies banner first
        try:
            accept_btn = page.locator('input[value="Accepter"], button:has-text("Accepter")')
            if await accept_btn.count() > 0:
                await accept_btn.first.click(force=True)
                print("Cookie banner accepted")
                await asyncio.sleep(1)
        except Exception as e:
            print(f"Cookie banner: {e}")

        # If banner-block-screen still there, remove it via JS
        await page.evaluate("""
            () => {
                document.querySelectorAll('.banner-block-screen, .banner-cookies').forEach(el => el.remove());
            }
        """)

        # Fill login form
        await page.fill('input[type="text"]', email)
        await page.fill('input[type="password"]', pwd)
        await page.click('input[type="submit"][value="Entrer"]', force=True)

        # Wait for navigation
        await page.wait_for_load_state("networkidle")
        current_url = page.url
        print(f"After login URL: {current_url}")

        if "Login.aspx" in current_url:
            # Check for error
            error_el = await page.query_selector('[id*="Failure"]')
            if error_el:
                error_text = await error_el.inner_text()
                print(f"LOGIN ERROR: {error_text}")
            else:
                print("Still on login page but no visible error")
            await browser.close()
            return

        print(">>> LOGIN OK!")

        # === GRID ===
        print("\n=== NAVIGATING TO GRID ===")
        await page.goto(f"{base}/Booking/Grid.aspx", wait_until="networkidle")
        await asyncio.sleep(2)  # Let AJAX calls complete
        print(f"Grid URL: {page.url}")

        # Get API key from page
        key = await page.evaluate("() => typeof hl90njda2b89k !== 'undefined' ? hl90njda2b89k : null")
        print(f"API Key: {key[:40] if key else 'NOT FOUND'}...")

        # Check intercepted API calls
        print(f"\nIntercepted {len(api_responses)} API calls:")
        for resp in api_responses:
            url_short = resp["url"].split("/")[-1]
            d = resp["data"].get("d", "?")
            if isinstance(d, list):
                print(f"  {url_short}: {len(d)} items")
                for item in d[:3]:
                    if isinstance(item, dict):
                        print(f"    {item.get('Nombre', item.get('Id', '?'))}")
            elif isinstance(d, dict):
                cols = d.get("Columnas", [])
                print(f"  {url_short}: {len(cols)} colonnes")
            else:
                print(f"  {url_short}: {str(d)[:100]}")

        # === MANUAL API CALLS ===
        if key:
            print("\n=== MANUAL API CALLS ===")
            # Get courts via JS evaluation
            courts_json = await page.evaluate("""
                async () => {
                    const resp = await fetch('/booking/srvc.aspx/ObtenerCuadros', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json; charset=utf-8'},
                        body: JSON.stringify({key: hl90njda2b89k})
                    });
                    return await resp.json();
                }
            """)
            courts = courts_json.get("d", [])
            print(f"Courts: {len(courts)}")
            for c in courts:
                print(f"  ID={c['Id']:3} {c['Nombre']}")

            # Check availability for Padel Lyon (ID 6)
            today = datetime.now()
            for offset in [0, 1, 2]:
                d = today + timedelta(days=offset)
                ds = d.strftime("%d/%m/%Y")
                day_name = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"][d.weekday()]

                grid_json = await page.evaluate("""
                    async (params) => {
                        const resp = await fetch('/booking/srvc.aspx/ObtenerCuadro', {
                            method: 'POST',
                            headers: {'Content-Type': 'application/json; charset=utf-8'},
                            body: JSON.stringify({idCuadro: params.courtId, fecha: params.date, key: hl90njda2b89k})
                        });
                        return await resp.json();
                    }
                """, {"courtId": 6, "date": ds})

                grid = grid_json.get("d", {})
                cols = grid.get("Columnas", [])
                if cols:
                    print(f"\n{day_name} {ds}: {len(cols)} pistes")
                    for col in cols[:5]:
                        cname = col.get("TextoPrincipal", "?")
                        occs = col.get("Ocupaciones", [])
                        for h in ["16:00", "17:00"]:
                            busy = any(
                                o.get("StrHoraInicio", "") <= h < o.get("StrHoraFin", "")
                                for o in occs
                            )
                            print(f"  {cname} {h}: {'OCCUPE' if busy else 'LIBRE'}")
                else:
                    h_start = grid.get("StrHoraInicio")
                    print(f"\n{day_name} {ds}: 0 pistes (StrHoraInicio={h_start})")
                    if grid:
                        print(f"  Grid keys: {list(grid.keys())[:8]}")

        await browser.close()


if __name__ == "__main__":
    asyncio.run(test())
