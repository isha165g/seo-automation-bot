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

def modify_html(html, meta_description_text=None, alt_texts=None, new_title=None):
    soup = BeautifulSoup(html, "html.parser")

    # Apply AI-generated meta description safely
    if meta_description_text:
        add_meta_description(soup, meta_description_text)
    
    # Apply AI-generated alt text safely
    if alt_texts:
        images = soup.find_all("img")

        for idx_str, alt in alt_texts.items():
            try:
                idx = int(idx_str)
            except ValueError:
                continue

            if idx >= len(images):
                continue

            img = images[idx]
            existing_alt = img.get("alt", "").strip().lower()

            if not existing_alt or existing_alt in ["image", "photo", "picture", "logo"]:
                img["alt"] = alt

    # Apply AI-rewritten title safely
    if new_title:
        title_tag = soup.find("title")
        if title_tag:
            title_tag.string = new_title
        else:
            head = soup.find("head")
            if head:
                new_title_tag = soup.new_tag("title")
                new_title_tag.string = new_title
                head.append(new_title_tag)
            
    return str(soup)
