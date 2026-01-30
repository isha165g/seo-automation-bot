import time
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

def fetch_dynamic_page(url, wait_time=3000):
    print(f"Fetching (dynamic): {url}", flush=True)

    start_time = time.time()

    try:
        with sync_playwright() as p:
            print("Launching Chromium...", flush=True)

            browser = p.chromium.launch(
                headless=True,
                args=[
                    "--disable-gpu",
                    "--no-sandbox",
                    "--disable-dev-shm-usage"
                ]
            )

            page = browser.new_page()

            print("Navigating to page...", flush=True)

            page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=15000
            )

            page.wait_for_timeout(wait_time)

            print("Extracting page content...", flush=True)

            html = page.content()

            browser.close()

            print(
                f"Dynamic fetch complete in {round(time.time() - start_time, 2)}s",
                flush=True
            )

            return html

    except PlaywrightTimeoutError:
        print("❌ Playwright navigation timed out", flush=True)
        return None

    except Exception as e:
        print(f"❌ Playwright failed: {e}", flush=True)
        return None
