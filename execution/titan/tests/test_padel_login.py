"""Test login MatchPoint PadelShot + check dispos."""
import asyncio
import aiohttp
import os
import re
import json
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

load_dotenv()


async def test_login():
    email = os.getenv("PADELSHOT_EMAIL")
    pwd = os.getenv("PADELSHOT_PASSWORD")
    base = "https://padelshot-fr.matchpoint.com.es"

    print(f"Email: {email}")
    print(f"Password: {'*' * len(pwd) if pwd else 'MISSING'}")

    async with aiohttp.ClientSession() as s:
        # Step 1: GET login page
        async with s.get(f"{base}/Login.aspx") as r:
            html = await r.text()

        soup = BeautifulSoup(html, "html.parser")
        vs = soup.find("input", {"name": "__VIEWSTATE"})["value"]
        ev = soup.find("input", {"name": "__EVENTVALIDATION"})["value"]
        vg = soup.find("input", {"name": "__VIEWSTATEGENERATOR"})["value"]

        # Step 2: POST login
        data = {
            "__VIEWSTATE": vs,
            "__EVENTVALIDATION": ev,
            "__VIEWSTATEGENERATOR": vg,
            "__EVENTTARGET": "",
            "__EVENTARGUMENT": "",
            "ctl00$ContentPlaceHolderContenido$Login1$UserName": email,
            "ctl00$ContentPlaceHolderContenido$Login1$Password": pwd,
            "ctl00$ContentPlaceHolderContenido$Login1$LoginButton": "Entrer",
        }

        async with s.post(f"{base}/Login.aspx", data=data, allow_redirects=True) as r:
            print(f"\nStatus: {r.status}")
            print(f"URL finale: {r.url}")
            cookies = {c.key: c.value[:30] for c in s.cookie_jar}
            print(f"Cookies: {list(cookies.keys())}")

            if ".ASPXAUTH" in cookies:
                print(">>> LOGIN OK!")
            else:
                body = await r.text()
                soup2 = BeautifulSoup(body, "html.parser")
                err = soup2.find(id=re.compile(r".*FailureText.*"))
                if err:
                    print(f"Erreur: {err.get_text(strip=True)}")
                else:
                    print(f"Login.aspx dans URL: {'Login.aspx' in str(r.url)}")

        # Step 3: Grid.aspx
        async with s.get(f"{base}/Booking/Grid.aspx") as r:
            grid_html = await r.text()
            print(f"\nGrid.aspx status: {r.status}")
            print(f"Grid URL: {r.url}")

            pattern = r"hl90njda2b89k\s*=\s*['\x22]([^'\x22]+)['\x22]"
            match = re.search(pattern, grid_html)
            if match:
                key = match.group(1)
                print(f"API KEY: {key[:40]}...")

                # Step 4: Get courts
                headers = {"Content-Type": "application/json; charset=utf-8"}
                async with s.post(
                    f"{base}/booking/srvc.aspx/ObtenerCuadros",
                    json={"key": key},
                    headers=headers,
                ) as r2:
                    resp_data = await r2.json()
                    courts = resp_data.get("d", [])
                    print(f"\nCourts: {json.dumps(courts, indent=2)[:500]}")

                    if courts:
                        # Step 5: Check dispo samedi prochain
                        today = datetime.now()
                        for i in range(7):
                            d = today + timedelta(days=i)
                            if d.weekday() == 5:  # Samedi
                                ds = d.strftime("%d/%m/%Y")
                                print(f"\n=== DISPO SAMEDI {ds} ===")
                                court_id = courts[0].get("Id", 1)
                                async with s.post(
                                    f"{base}/booking/srvc.aspx/ObtenerCuadro",
                                    json={"idCuadro": court_id, "fecha": ds, "key": key},
                                    headers=headers,
                                ) as r3:
                                    grid = (await r3.json()).get("d", {})
                                    print(f"Heures: {grid.get('StrHoraInicio')} - {grid.get('StrHoraFin')}")
                                    for col in grid.get("Columnas", []):
                                        name = col.get("TextoPrincipal", "?")
                                        occs = col.get("Ocupaciones", [])
                                        for h in ["16:00", "16:30", "17:00", "17:30"]:
                                            busy = any(
                                                o.get("StrHoraInicio", "") <= h < o.get("StrHoraFin", "")
                                                for o in occs
                                            )
                                            status = "OCCUPE" if busy else "LIBRE"
                                            print(f"  {name} {h}: {status}")
                                break
            else:
                print("API KEY introuvable")
                if "Login.aspx" in str(r.url):
                    print("Redirige vers login - auth echouee")


if __name__ == "__main__":
    asyncio.run(test_login())
