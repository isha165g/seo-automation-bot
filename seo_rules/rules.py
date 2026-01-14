import json

def check_title(title):
    issues = []

    if not title:
        issues.append("Missing title")
    elif len(title.strip()) > 60:
        issues.append("Title too long")

    return issues

def check_meta_description(description):
    issues = []

    if not description:
        issues.append("Missing meta description")
    elif len(description) > 160:
        issues.append("Meta description is longer than 160 characters")

    return issues

def check_h1(h1_tags):
    issues = []

    if not h1_tags:
        issues.append("Missing <h1> tag")
    elif len(h1_tags) > 1:
        issues.append("Multiple <h1> tags found")

    return issues

def check_images(images):
    issues = []
    for index, img in enumerate(images):
        alt = (img.get("alt") or "").strip().lower()

        if not alt:
            issues.append({
                "type": "missing_alt",
                "index": index
            })
        elif alt in ["image", "photo", "picture", "logo"]:
            issues.append({
                "type": "generic_alt",
                "index": index
            })

    return issues

def run_seo_checks(seo_data):
    report = {
        "title": check_title(seo_data.get("title")),
        "meta_description": check_meta_description(seo_data.get("meta_description")),
        "h1": check_h1(seo_data.get("h1_tags")),
        "images": check_images(seo_data.get("images"))
    }

    return report

if __name__ == "__main__":
    # Sample test data (temporary)
    sample_data = {
        "title": "Example Domain",
        "meta_description": None,
        "h1_tags": ["Example Domain"],
        "images": []
    }

    result = run_seo_checks(sample_data)
    print(json.dumps(result, indent=4))
