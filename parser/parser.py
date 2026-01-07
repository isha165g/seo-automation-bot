from bs4 import BeautifulSoup
import os
import json

HTML_PATH = "data/pages/home.html"

def load_html(path):
    if not os.path.exists(path):
        print("HTML file not found")
        return None

    with open(path, "r", encoding="utf-8") as file:
        return file.read()

def extract_seo_tags(html):
    soup = BeautifulSoup(html, "html.parser")

    title = soup.title.string if soup.title else None

    meta_desc_tag = soup.find("meta", attrs={"name": "description"})
    meta_description = meta_desc_tag["content"] if meta_desc_tag else None

    h1_tags = [h1.get_text(strip=True) for h1 in soup.find_all("h1")]

    images = []
    for img in soup.find_all("img"):
        images.append({
            "src": img.get("src"),
            "alt": img.get("alt")
        })

    return {
        "title": title,
        "meta_description": meta_description,
        "h1_tags": h1_tags,
        "images": images
    }

if __name__ == "__main__":
    html = load_html(HTML_PATH)

    if html:
        seo_data = extract_seo_tags(html)
        print(json.dumps(seo_data, indent=4))
