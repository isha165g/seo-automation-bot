import requests
from bs4 import BeautifulSoup
import os

def fetch_page(url):
    try:
        print(f"Fetching URL: {url}", flush=True)

        headers = {
            "User-Agent": "Mozilla/5.0 (SEO-Automation-Bot)"
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=10   # 🔑 IMPORTANT
        )

        response.raise_for_status()
        return response.text

    except requests.exceptions.Timeout:
        print("❌ Request timed out", flush=True)
        return None

    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching page: {e}", flush=True)
        return None

def save_page(html_content, filename):
    os.makedirs("data/pages", exist_ok=True)

    file_path = f"data/pages/{filename}.html"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"HTML saved to {file_path}")

if __name__ == "__main__":
    url = "https://example.com"
    html = fetch_page(url)

    if html:
        save_page(html, "home")
