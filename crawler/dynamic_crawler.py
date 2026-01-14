from playwright.sync_api import sync_playwright

def fetch_dynamic_page(url, wait_time=3000):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(url, wait_until="networkidle")
        page.wait_for_timeout(wait_time)

        html = page.content()
        browser.close()

        return html
