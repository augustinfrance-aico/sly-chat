"""Test if PadelShot grid works WITHOUT login (anonymous access)."""
import asyncio
import os
import sys
import io
import json
from dotenv import load_dotenv

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
load_dotenv()


async def test_anonymous():
    from playwright.async_api import async_playwright
    from datetime import datetime, timedelta

    portals = [
        ("https://padelshot-fr.matchpoint.com.es", "Craponne", [6, 7]),  # 6=Padel Lyon, 7=Bad Lyon
        ("https://padelshotsaintgenislaval-fr.matchpoint.com.es", "Saint-Genis", [4]),  # 4=Padel
    ]

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        for base_url, name, court_ids in portals:
            print(f"\n{'='*50}")
            print(f"{name} - ANONYMOUS ACCESS")
            print(f"{'='*50}")

            page = await browser.new_page()

            # Go directly to Grid.aspx without login
            await page.goto(f"{base_url}/Booking/Grid.aspx", wait_until="networkidle")
            await asyncio.sleep(2)

            final_url = page.url
            print(f"URL: {final_url}")

            if "Login.aspx" in final_url:
                print(">>> Redirected to login - anonymous NOT allowed")
                await page.close()
                continue

            # Get API key
            key = await page.evaluate(
                "() => typeof hl90njda2b89k !== 'undefined' ? hl90njda2b89k : null"
            )
            if not key:
                print(">>> No API key found")
                await page.close()
                continue

            print(f"API Key: {key[:30]}...")

            # Get courts
            courts = await page.evaluate("""async () => {
                const r = await fetch('/booking/srvc.aspx/ObtenerCuadros', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json; charset=utf-8'},
                    body: JSON.stringify({key: hl90njda2b89k})
                });
                const data = await r.json();
                return data.d;
            }""")
            print(f"\nCourts ({len(courts)}):")
            for c in courts:
                print(f"  ID={c['Id']} {c['Nombre']}")

            # Check availability
            today = datetime.now()
            for court_id in court_ids:
                court_name = next(
                    (c["Nombre"] for c in courts if c["Id"] == court_id),
                    f"ID={court_id}",
                )
                print(f"\n--- {court_name} (ID={court_id}) ---")

                for offset in [0, 1, 2, 3, 4, 5, 6]:
                    d = today + timedelta(days=offset)
                    ds = d.strftime("%d/%m/%Y")
                    day_name = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"][
                        d.weekday()
                    ]

                    grid = await page.evaluate(
                        """async (params) => {
                        const r = await fetch('/booking/srvc.aspx/ObtenerCuadro', {
                            method: 'POST',
                            headers: {'Content-Type': 'application/json; charset=utf-8'},
                            body: JSON.stringify({idCuadro: params.courtId, fecha: params.date, key: hl90njda2b89k})
                        });
                        const data = await r.json();
                        return data.d;
                    }""",
                        {"courtId": court_id, "date": ds},
                    )

                    if grid and grid.get("Columnas") and len(grid["Columnas"]) > 0:
                        cols = grid["Columnas"]
                        h_start = grid.get("StrHoraInicio", "?")
                        h_end = grid.get("StrHoraFin", "?")
                        print(f"\n  {day_name} {ds}: {len(cols)} pistes ({h_start}-{h_end})")

                        for col in cols:
                            cname = col.get("TextoPrincipal", "?")
                            occs = col.get("Ocupaciones", [])
                            slots_info = []
                            for h in ["16:00", "17:00"]:
                                busy = any(
                                    o.get("StrHoraInicio", "") <= h < o.get("StrHoraFin", "")
                                    for o in occs
                                )
                                slots_info.append(
                                    f"{h}={'X' if busy else 'OK'}"
                                )
                            print(f"    {cname}: {' | '.join(slots_info)} ({len(occs)} occ total)")
                    else:
                        # Check what we got
                        if grid:
                            fecha_min = grid.get("StrFechaMin", "?")
                            fecha_max = grid.get("StrFechaMax", "?")
                            print(f"  {day_name} {ds}: 0 pistes (fechaMin={fecha_min}, fechaMax={fecha_max})")
                        else:
                            print(f"  {day_name} {ds}: empty response")

            await page.close()

        await browser.close()


if __name__ == "__main__":
    asyncio.run(test_anonymous())
