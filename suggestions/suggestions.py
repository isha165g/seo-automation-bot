import json

def suggest_title_fix(issues):
    suggestions = []
    for issue in issues:
        if "Missing <title>" in issue:
            suggestions.append("Add a descriptive <title> tag (max 60 characters)")
        elif "longer than 60" in issue:
            suggestions.append("Shorten the <title> tag to under 60 characters")
    return suggestions

def suggest_meta_description_fix(issues):
    suggestions = []
    for issue in issues:
        if "Missing meta description" in issue:
            suggestions.append("Add a meta description (max 160 characters)")
        elif "longer than 160" in issue:
            suggestions.append("Shorten the meta description to under 160 characters")
    return suggestions

def suggest_h1_fix(issues):
    suggestions = []
    for issue in issues:
        if "Missing <h1>" in issue:
            suggestions.append("Add exactly one <h1> tag describing the page")
        elif "Multiple <h1>" in issue:
            suggestions.append("Keep only one <h1> tag per page")
    return suggestions

def suggest_image_alt_fix(issues):
    suggestions = []
    for issue in issues:
        suggestions.append(f"Add meaningful alt text for image: {issue}")
    return suggestions

def generate_fix_suggestions(seo_report):
    return {
        "title": suggest_title_fix(seo_report.get("title", [])),
        "meta_description": suggest_meta_description_fix(seo_report.get("meta_description", [])),
        "h1": suggest_h1_fix(seo_report.get("h1", [])),
        "images": suggest_image_alt_fix(seo_report.get("images", []))
    }

if __name__ == "__main__":
    # Sample SEO report (from Module 3)
    sample_seo_report = {
        "title": [],
        "meta_description": ["Missing meta description"],
        "h1": [],
        "images": []
    }

    fixes = generate_fix_suggestions(sample_seo_report)
    print(json.dumps(fixes, indent=4))
