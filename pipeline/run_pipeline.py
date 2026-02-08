from crawler.static_crawler import fetch_page
from crawler.dynamic_crawler import fetch_dynamic_page
from parser.parser import extract_seo_tags
from seo_rules.rules import run_seo_checks
from modifier.modifier import modify_html
from ai_engine.tasks import (
    generate_meta_description,
    generate_alt_text,
    rewrite_title,
)
from ai_engine.insights import generate_ai_insights

def run_pipeline(url: str, use_dynamic: bool):
    # 1. Fetch HTML
    html = (
        fetch_dynamic_page(url)
        if use_dynamic
        else fetch_page(url)
    )

    if not html:
        return {"error": "Failed to fetch HTML"}

    # 2. Parse SEO
    seo_data = extract_seo_tags(html)

    # 3. Run rules
    seo_report = run_seo_checks(seo_data)
    ai_insights = generate_ai_insights(seo_report)

    # 4. AI actions
    ai_meta = None
    ai_title = None
    alt_texts = {}

    if "Missing meta description" in seo_report.get("meta_description", []):
        ai_meta = generate_meta_description(seo_data)

    if seo_report.get("title"):
        ai_title = rewrite_title(seo_data)

    images = seo_data.get("images", [])
    image_issues = seo_report.get("images", [])

    for issue in image_issues[:5]:
        idx = issue["index"]
        if idx < len(images):
            alt = generate_alt_text(images[idx])
            if alt:
                alt_texts[str(idx)] = alt

    # 5. Apply HTML modifications
    modified_html = modify_html(
        html,
        meta_description_text=ai_meta,
        alt_texts=alt_texts,
        new_title=ai_title
    )

    # 6. Return data for UI
    return {
        "summary": {
            "meta_description": "missing"
            if "Missing meta description" in seo_report.get("meta_description", [])
            else "present",
            "title": "issues" if seo_report.get("title") else "ok",
            "images_missing_alt": len(image_issues),
        },
        "ai_actions": {
            "meta_description": ai_meta,
            "title": ai_title,
            "alt_texts": alt_texts,
        },
        "ai_insights": ai_insights,
        "original_html": html,
        "modified_html": modified_html
    }
