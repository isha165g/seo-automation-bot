from bs4 import BeautifulSoup

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

def modify_html(html, meta_description_text=None, alt_texts=None):
    soup = BeautifulSoup(html, "html.parser")

    # Apply AI-generated alt text safely
    if alt_texts:
        images = soup.find_all("img")

        for idx, alt in alt_texts.items():
            if idx >= len(images):
                continue

            img = images[idx]
            existing_alt = img.get("alt", "").strip().lower()

            if not existing_alt or existing_alt in ["image", "photo", "picture", "logo"]:
                img["alt"] = alt

    # Apply AI-generated meta description safely
    if meta_description_text:
        add_meta_description(soup, meta_description_text)

    return str(soup)
