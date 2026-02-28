"""Quick test - login + screenshot for visual debug."""
import asyncio, os, sys, io
from dotenv import load_dotenv
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
load_dotenv()

async def main():
    from playwright.async_api import async_playwright
    email = os.getenv("PADELSHOT_EMAIL")
    pwd = os.getenv("PADELSHOT_PASSWORD")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # 1. Login Craponne
        await page.goto("https://padelshot-fr.matchpoint.com.es/Login.aspx", wait_until="networkidle")
        # Kill cookie banner
        await page.evaluate("document.querySelectorAll('.banner-block-screen,.banner-cookies,[class*=cookie]').forEach(e=>e.remove())")
        await page.fill("#ctl00_ContentPlaceHolderContenido_Login1_UserName", email)
        await page.fill("#ctl00_ContentPlaceHolderContenido_Login1_Password", pwd)
        await page.screenshot(path="padel_before_login.png")
        await page.click("#ctl00_ContentPlaceHolderContenido_Login1_LoginButton", force=True)
        try:
            await page.wait_for_url("**/Booking/**", timeout=10000)
            print("LOGIN OK - redirige vers Booking")
        except:
            await page.wait_for_load_state("networkidle")
            print(f"URL apres login: {page.url}")
            await page.screenshot(path="padel_after_login.png")
            # Check visible text for errors
            body = await page.inner_text("body")
            if "incorrect" in body.lower() or "invalide" in body.lower() or "error" in body.lower():
                print(f"ERREUR VISIBLE: login/mdp incorrect")
            else:
                print("Pas d'erreur visible mais toujours sur Login.aspx")
                print("Le compte existe peut-etre pas sur ce portail")

        # 2. Try Saint-Genis-Laval
        page2 = await browser.new_page()
        await page2.goto("https://padelshotsaintgenislaval-fr.matchpoint.com.es/Login.aspx", wait_until="networkidle")
        await page2.evaluate("document.querySelectorAll('.banner-block-screen,.banner-cookies,[class*=cookie]').forEach(e=>e.remove())")
        # Check if same form structure
        has_form = await page2.locator("#ctl00_ContentPlaceHolderContenido_Login1_UserName").count()
        if has_form:
            await page2.fill("#ctl00_ContentPlaceHolderContenido_Login1_UserName", email)
            await page2.fill("#ctl00_ContentPlaceHolderContenido_Login1_Password", pwd)
            await page2.click("#ctl00_ContentPlaceHolderContenido_Login1_LoginButton", force=True)
            try:
                await page2.wait_for_url("**/Booking/**", timeout=10000)
                print("\nSAINT-GENIS LOGIN OK!")
            except:
                await page2.wait_for_load_state("networkidle")
                print(f"\nSaint-Genis URL: {page2.url}")
        else:
            # Different form structure
            inputs = await page2.locator("input[type=text], input[type=email]").all()
            print(f"\nSaint-Genis: {len(inputs)} text inputs found")
            for inp in inputs:
                name = await inp.get_attribute("name")
                id_ = await inp.get_attribute("id")
                print(f"  name={name} id={id_}")

        await browser.close()

asyncio.run(main())
