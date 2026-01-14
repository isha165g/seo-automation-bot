from bs4 import BeautifulSoup

def extract_meta_description(html):
    soup = BeautifulSoup(html, "html.parser")
    tag = soup.find("meta", attrs={"name": "description"})
    return str(tag) if tag else ""

def extract_img_tags(html):
    soup = BeautifulSoup(html, "html.parser")
    return [str(img) for img in soup.find_all("img")]

def extract_title(html):
    soup = BeautifulSoup(html, "html.parser")
    tag = soup.find("title")
    return str(tag) if tag else ""

def generate_diff(original_html, modified_html):
    diffs = []

    # Meta description diff 
    original_meta = extract_meta_description(original_html)
    modified_meta = extract_meta_description(modified_html)

    if original_meta != modified_meta:
        if original_meta:
            diffs.append((-1, original_meta))
        if modified_meta:
            diffs.append((1, modified_meta))

    # Image alt diffs
    orig_imgs = extract_img_tags(original_html)
    mod_imgs = extract_img_tags(modified_html)

    for o, m in zip(orig_imgs, mod_imgs):
        if o != m:
            diffs.append((-1, o))
            diffs.append((1, m))

    # Title diff
    original_title = extract_title(original_html)
    modified_title = extract_title(modified_html)

    if original_title != modified_title:
        if original_title:
            diffs.append((-1, original_title))
        if modified_title:
            diffs.append((1, modified_title))

    return diffs

