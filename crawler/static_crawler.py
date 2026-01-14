import requests
from bs4 import BeautifulSoup
import os

def fetch_page(url):
    print(f"Fetching URL: {url}")

    try:
        response = requests.get(url, timeout=10)
    except requests.exceptions.RequestException as e:
        print("Error fetching page:", e)
        return None

    if response.status_code != 200:
        print("Non-200 status code:", response.status_code)
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    return soup.prettify()

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
