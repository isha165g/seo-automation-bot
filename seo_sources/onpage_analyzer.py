import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def run_onpage_analyzer(url: str):
    response = requests.get(url, timeout=20)
    html = response.text

    soup = BeautifulSoup(html, "lxml")

    # ---- Meta ----
    title_tag = soup.title.string.strip() if soup.title and soup.title.string else ""
    meta_desc = soup.find("meta", attrs={"name": "description"})
    canonical = soup.find("link", rel="canonical")
    robots = soup.find("meta", attrs={"name": "robots"})
    viewport = soup.find("meta", attrs={"name": "viewport"})

    # ---- Headings ----
    h1_tags = soup.find_all("h1")
    h2_tags = soup.find_all("h2")
    h3_tags = soup.find_all("h3")

    # ---- Images ----
    images = soup.find_all("img")
    images_missing_alt = [img for img in images if not img.get("alt")]

    # ---- Links ----
    parsed_url = urlparse(url)
    domain = parsed_url.netloc

    internal_links = 0
    external_links = 0

    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("http"):
            if domain in href:
                internal_links += 1
            else:
                external_links += 1

    return {
        "meta": {
            "title_length": len(title_tag),
            "meta_description_length": len(meta_desc["content"]) if meta_desc and meta_desc.get("content") else 0,
            "has_canonical": bool(canonical),
            "has_robots": bool(robots),
            "has_viewport": bool(viewport),
        },
        "headings": {
            "h1_count": len(h1_tags),
            "h2_count": len(h2_tags),
            "h3_count": len(h3_tags),
        },
        "images": {
            "total": len(images),
            "missing_alt": len(images_missing_alt),
        },
        "links": {
            "internal": internal_links,
            "external": external_links,
        }
    }
