from bs4 import BeautifulSoup
import os

INPUT_HTML = "data/pages/home.html"
OUTPUT_HTML = "data/pages/home_modified.html"

def load_html(path):
    if not os.path.exists(path):
        print("Input HTML file not found")
        return None

    with open(path, "r", encoding="utf-8") as file:
        return file.read()

def save_html(html, path):
    with open(path, "w", encoding="utf-8") as file:
        file.write(html)

    print(f"Modified HTML saved to {path}")

def add_meta_description(soup, description_text):
    head = soup.find("head")
    if not head:
        return

    meta = soup.find("meta", attrs={"name": "description"})
    if not meta:
        new_meta = soup.new_tag("meta")
        new_meta.attrs["name"] = "description"
        new_meta.attrs["content"] = description_text
        head.append(new_meta)

def add_missing_alt_tags(soup):
    for img in soup.find_all("img"):
        if not img.get("alt"):
            img["alt"] = "Image description"

def modify_html(html):
    soup = BeautifulSoup(html, "html.parser")

    # SAFE DEFAULT TEXT (temporary, AI comes later)
    add_meta_description(soup, "This is a sample meta description.")
    add_missing_alt_tags(soup)

    return soup.prettify()

if __name__ == "__main__":
    html = load_html(INPUT_HTML)

    if html:
        modified_html = modify_html(html)
        save_html(modified_html, OUTPUT_HTML)
