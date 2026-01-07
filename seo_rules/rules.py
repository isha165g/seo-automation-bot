import json

def check_title(title):
    issues = []

    if not title:
        issues.append("Missing <title> tag")
    elif len(title) > 60:
        issues.append("Title tag is longer than 60 characters")

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

def check_image_alts(images):
    issues = []

    for img in images:
        if not img.get("alt"):
            issues.append(f"Image missing alt text: {img.get('src')}")

    return issues

def run_seo_checks(seo_data):
    report = {
        "title": check_title(seo_data.get("title")),
        "meta_description": check_meta_description(seo_data.get("meta_description")),
        "h1": check_h1(seo_data.get("h1_tags")),
        "images": check_image_alts(seo_data.get("images"))
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
