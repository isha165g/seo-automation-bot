from bs4 import BeautifulSoup

def extract_meta_description(html):
    soup = BeautifulSoup(html, "html.parser")
    tag = soup.find("meta", attrs={"name": "description"})
    return str(tag) if tag else ""

def generate_diff(original_html, modified_html):
    original_meta = extract_meta_description(original_html)
    modified_meta = extract_meta_description(modified_html)

    diffs = []

    if original_meta != modified_meta:
        if original_meta:
            diffs.append((-1, original_meta))
        if modified_meta:
            diffs.append((1, modified_meta))

    return diffs
