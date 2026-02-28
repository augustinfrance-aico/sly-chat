"""Test dispo PadelShot Craponne sur plusieurs dates."""
import asyncio
import aiohttp
import re
import json
import sys
import io
from datetime import datetime, timedelta

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


async def test_dates():
    base = "https://padelshot-fr.matchpoint.com.es"
    async with aiohttp.ClientSession() as s:
        async with s.get(f"{base}/Booking/Grid.aspx") as r:
            html = await r.text()
        key = re.search(r"hl90njda2b89k\s*=\s*[\x27\x22]([^\x27\x22]+)[\x27\x22]", html).group(1)
        headers = {"Content-Type": "application/json; charset=utf-8"}

        today = datetime.now()
        for offset in [0, 1, 2, 3, 7]:
            d = today + timedelta(days=offset)
            ds = d.strftime("%d/%m/%Y")
            day_name = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"][d.weekday()]

            # ID=6 = Padel Lyon (Craponne)
            async with s.post(
                f"{base}/booking/srvc.aspx/ObtenerCuadro",
                json={"idCuadro": 6, "fecha": ds, "key": key},
                headers=headers,
            ) as r:
                resp = await r.json()
                grid = resp.get("d", {})
                if grid:
                    cols = grid.get("Columnas", [])
                    h_start = grid.get("StrHoraInicio")
                    h_end = grid.get("StrHoraFin")
                    fecha_min = grid.get("StrFechaMin")
                    fecha_max = grid.get("StrFechaMax")
                    print(f"{day_name} {ds}: {len(cols)} pistes, {h_start}-{h_end}, range=[{fecha_min} -> {fecha_max}]")
                    if cols:
                        for col in cols[:3]:
                            cname = col.get("TextoPrincipal", "?")
                            occs = col.get("Ocupaciones", [])
                            print(f"  {cname}: {len(occs)} occupations")
                            for o in occs[:3]:
                                print(f"    {o.get('StrHoraInicio')}-{o.get('StrHoraFin')} | {o.get('Texto1','')} | click={o.get('Clickable')}")
                            # Check 16h et 17h
                            for h in ["16:00", "17:00"]:
                                busy = any(
                                    o.get("StrHoraInicio", "") <= h < o.get("StrHoraFin", "")
                                    for o in occs
                                )
                                print(f"    >> {h}: {'OCCUPE' if busy else 'LIBRE'}")
                else:
                    print(f"{day_name} {ds}: PAS DE GRILLE")

        # Test aussi Saint-Genis
        print("\n=== SAINT-GENIS-LAVAL ===")
        base2 = "https://padelshotsaintgenislaval-fr.matchpoint.com.es"
        async with s.get(f"{base2}/Booking/Grid.aspx") as r:
            html2 = await r.text()
        key2 = re.search(r"hl90njda2b89k\s*=\s*[\x27\x22]([^\x27\x22]+)[\x27\x22]", html2).group(1)

        for offset in [0, 1, 2]:
            d = today + timedelta(days=offset)
            ds = d.strftime("%d/%m/%Y")
            day_name = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"][d.weekday()]

            async with s.post(
                f"{base2}/booking/srvc.aspx/ObtenerCuadro",
                json={"idCuadro": 4, "fecha": ds, "key": key2},
                headers=headers,
            ) as r:
                resp = await r.json()
                grid = resp.get("d", {})
                if grid:
                    cols = grid.get("Columnas", [])
                    print(f"{day_name} {ds}: {len(cols)} pistes")
                    if cols:
                        for col in cols[:2]:
                            cname = col.get("TextoPrincipal", "?")
                            occs = col.get("Ocupaciones", [])
                            print(f"  {cname}: {len(occs)} occ")
                            for h in ["16:00", "17:00"]:
                                busy = any(
                                    o.get("StrHoraInicio", "") <= h < o.get("StrHoraFin", "")
                                    for o in occs
                                )
                                print(f"    >> {h}: {'OCCUPE' if busy else 'LIBRE'}")
                else:
                    print(f"{day_name} {ds}: PAS DE GRILLE")


if __name__ == "__main__":
    asyncio.run(test_dates())
