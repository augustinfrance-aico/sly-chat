"""Debug login PadelShot - both portals + check error messages."""
import asyncio
import os
import sys
import io
from dotenv import load_dotenv

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
load_dotenv()


async def test_login_portal(base_url, name):
    from playwright.async_api import async_playwright

    email = os.getenv("PADELSHOT_EMAIL")
    pwd = os.getenv("PADELSHOT_PASSWORD")

    print(f"\n{'='*50}")
    print(f"TESTING: {name}")
    print(f"URL: {base_url}")
    print(f"Email: {email}")
    print(f"{'='*50}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto(f"{base_url}/Login.aspx", wait_until="networkidle")

        # Remove cookie banner
        await page.evaluate("""() => {
            document.querySelectorAll('.banner-block-screen, .banner-cookies, [class*=cookie], [class*=banner]').forEach(el => el.remove());
        }""")
        await asyncio.sleep(0.5)

        # Fill credentials
        await page.fill("#ctl00_ContentPlaceHolderContenido_Login1_UserName", email)
        await page.fill("#ctl00_ContentPlaceHolderContenido_Login1_Password", pwd)

        # Click submit with force
        async with page.expect_navigation(wait_until="networkidle", timeout=15000) as _:
            await page.click("#ctl00_ContentPlaceHolderContenido_Login1_LoginButton", force=True)

        final_url = page.url
        print(f"Final URL: {final_url}")

        if "Login.aspx" not in final_url:
            print(">>> LOGIN SUCCESS!")
            # Navigate to grid
            await page.goto(f"{base_url}/Booking/Grid.aspx", wait_until="networkidle")
            await asyncio.sleep(2)

            key = await page.evaluate(
                "() => typeof hl90njda2b89k !== 'undefined' ? hl90njda2b89k : null"
            )
            print(f"API Key: {key[:40] if key else 'NONE'}...")

            if key:
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
                print(f"Courts: {len(courts)}")
                for c in courts:
                    print(f"  ID={c['Id']} {c['Nombre']}")
        else:
            print(">>> LOGIN FAILED - still on Login.aspx")
            # Get the full page text for error clues
            error_text = await page.evaluate("""() => {
                // Check multiple error locations
                const selectors = [
                    '[id*="Failure"]',
                    '[id*="Error"]',
                    '.error',
                    '.alert',
                    '.validation-summary',
                    '[class*="error"]',
                    '[class*="fail"]',
                    'span[style*="color"]',
                ];
                for (const sel of selectors) {
                    const el = document.querySelector(sel);
                    if (el && el.innerText.trim()) {
                        return `${sel}: ${el.innerText.trim()}`;
                    }
                }

                // Check if the login form has any inline validation
                const validators = document.querySelectorAll('[id*="RequiredFieldValidator"], [id*="Validator"]');
                const validatorTexts = [];
                for (const v of validators) {
                    if (v.style.visibility !== 'hidden' && v.innerText.trim()) {
                        validatorTexts.push(v.innerText.trim());
                    }
                }
                if (validatorTexts.length) return 'Validators: ' + validatorTexts.join(', ');

                return 'No error found on page';
            }""")
            print(f"Error details: {error_text}")

            # Also try to find the login title/header for context
            header = await page.evaluate("""() => {
                const h = document.querySelector('h1, h2, .titulo, [class*="title"]');
                return h ? h.innerText.trim() : 'No header';
            }""")
            print(f"Page header: {header}")

        await browser.close()


async def main():
    portals = [
        ("https://padelshot-fr.matchpoint.com.es", "PadelShot Craponne"),
        ("https://padelshotsaintgenislaval-fr.matchpoint.com.es", "PadelShot Saint-Genis-Laval"),
    ]
    for url, name in portals:
        await test_login_portal(url, name)


if __name__ == "__main__":
    asyncio.run(main())
