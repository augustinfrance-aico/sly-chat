"""Test PadelShot login + check dispos avec auth complete."""
import asyncio
import aiohttp
import os
import re
import json
import sys
import io
from datetime import datetime, timedelta
from dotenv import load_dotenv
from bs4 import BeautifulSoup

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
load_dotenv()


async def test_full_auth():
    email = os.getenv("PADELSHOT_EMAIL")
    pwd = os.getenv("PADELSHOT_PASSWORD")
    base = "https://padelshot-fr.matchpoint.com.es"
    headers_json = {"Content-Type": "application/json; charset=utf-8"}

    async with aiohttp.ClientSession() as s:
        # === STEP 1: Login ===
        print("=== LOGIN ===")
        async with s.get(f"{base}/Login.aspx") as r:
            html = await r.text()

        soup = BeautifulSoup(html, "html.parser")

        # Scrape ASP.NET fields
        form_data = {}
        for inp in soup.find_all("input", {"type": "hidden"}):
            name = inp.get("name", "")
            if name:
                form_data[name] = inp.get("value", "")

        # Add credentials
        form_data["ctl00$ContentPlaceHolderContenido$Login1$UserName"] = email
        form_data["ctl00$ContentPlaceHolderContenido$Login1$Password"] = pwd
        form_data["ctl00$ContentPlaceHolderContenido$Login1$LoginButton"] = "Entrer"

        print(f"Fields to POST: {len(form_data)}")

        async with s.post(f"{base}/Login.aspx", data=form_data, allow_redirects=True) as r:
            print(f"Status: {r.status}")
            print(f"URL: {r.url}")
            cookies = {c.key for c in s.cookie_jar}
            print(f"Cookies: {cookies}")

            body = await r.text()
            if ".ASPXAUTH" in cookies:
                print(">>> LOGIN OK (ASPXAUTH cookie)")
            elif "Login.aspx" not in str(r.url):
                print(">>> LOGIN OK (redirect)")
            else:
                # Check for error message
                soup2 = BeautifulSoup(body, "html.parser")
                err = soup2.find(id=re.compile(r".*Failure.*", re.I))
                if err:
                    print(f">>> ERREUR: {err.get_text(strip=True)}")
                else:
                    # Maybe the login worked but stayed on same page
                    # Check if there's a logged-in indicator
                    user_el = soup2.find(id=re.compile(r".*lblUser.*|.*UserName.*|.*NombreUsuario.*", re.I))
                    if user_el:
                        print(f">>> Logged in as: {user_el.get_text(strip=True)}")
                    else:
                        print(">>> Login status unclear")
                        # Dump a snippet around the form area for debugging
                        form_area = soup2.find("form")
                        if form_area:
                            inputs_after = form_area.find_all("input", {"type": ["text", "email"]})
                            print(f"   Text inputs still on page: {len(inputs_after)}")

        # === STEP 2: Get Grid.aspx ===
        print("\n=== GRID ===")
        async with s.get(f"{base}/Booking/Grid.aspx") as r:
            grid_html = await r.text()
            print(f"Grid URL: {r.url}")
            print(f"Grid length: {len(grid_html)}")

            # Check if we're redirected back to login
            if "Login.aspx" in str(r.url):
                print(">>> Redirected to login - NOT authenticated")
                return

            key_match = re.search(
                r"hl90njda2b89k\s*=\s*[\x27\x22]([^\x27\x22]+)[\x27\x22]", grid_html
            )
            if key_match:
                key = key_match.group(1)
                print(f"API Key: {key[:40]}...")
            else:
                print(">>> API Key not found")
                # Try alternative patterns
                for pattern in [
                    r"var\s+key\s*=\s*[\x27\x22]([^\x27\x22]+)",
                    r"ajax.*key.*[\x27\x22]([A-Za-z0-9+/=]{20,})[\x27\x22]",
                ]:
                    m = re.search(pattern, grid_html)
                    if m:
                        key = m.group(1)
                        print(f"API Key (alt): {key[:40]}...")
                        break
                else:
                    print("No key found at all")
                    return

        # === STEP 3: Get Courts ===
        print("\n=== COURTS ===")
        async with s.post(
            f"{base}/booking/srvc.aspx/ObtenerCuadros",
            json={"key": key},
            headers=headers_json,
        ) as r:
            data = await r.json()
            courts = data.get("d", [])
            print(f"Courts: {len(courts)}")
            for c in courts:
                print(f"  ID={c['Id']:3} {c['Nombre']}")

        # === STEP 4: Get availability - Padel Lyon (ID 6) ===
        print("\n=== DISPONIBILITES ===")
        today = datetime.now()
        for offset in [0, 1, 2, 3]:
            d = today + timedelta(days=offset)
            ds = d.strftime("%d/%m/%Y")
            day_name = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"][d.weekday()]

            async with s.post(
                f"{base}/booking/srvc.aspx/ObtenerCuadro",
                json={"idCuadro": 6, "fecha": ds, "key": key},
                headers=headers_json,
            ) as r:
                resp_text = await r.text()
                try:
                    resp = json.loads(resp_text)
                    grid = resp.get("d", {})
                except json.JSONDecodeError:
                    print(f"{day_name} {ds}: Response not JSON ({resp_text[:100]})")
                    continue

                if grid and grid.get("Columnas"):
                    cols = grid["Columnas"]
                    print(f"{day_name} {ds}: {len(cols)} pistes, {grid.get('StrHoraInicio')}-{grid.get('StrHoraFin')}")
                    for col in cols[:4]:
                        cname = col.get("TextoPrincipal", "?")
                        occs = col.get("Ocupaciones", [])
                        free_16 = not any(
                            o.get("StrHoraInicio", "") <= "16:00" < o.get("StrHoraFin", "")
                            for o in occs
                        )
                        free_17 = not any(
                            o.get("StrHoraInicio", "") <= "17:00" < o.get("StrHoraFin", "")
                            for o in occs
                        )
                        print(f"  {cname}: 16h={'LIBRE' if free_16 else 'OCCUPE'} | 17h={'LIBRE' if free_17 else 'OCCUPE'}")
                elif grid:
                    print(f"{day_name} {ds}: grid OK mais 0 colonnes (StrHoraInicio={grid.get('StrHoraInicio')})")
                    # Dump the full grid for debugging
                    print(f"  Keys: {list(grid.keys())[:10]}")
                else:
                    print(f"{day_name} {ds}: grid vide")
                    print(f"  Raw: {resp_text[:200]}")


if __name__ == "__main__":
    asyncio.run(test_full_auth())
