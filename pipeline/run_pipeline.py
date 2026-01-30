import sys
sys.path.append(".")
import os
import io

UI_MODE = False

CONFIG_FILE = "ui_backend/config.txt"

from crawler.static_crawler import fetch_page
from crawler.dynamic_crawler import fetch_dynamic_page
from parser.parser import load_html, extract_seo_tags
from seo_rules.rules import run_seo_checks
from suggestions.suggestions import generate_fix_suggestions
from modifier.modifier import modify_html
from diff_engine.diff_generator import generate_diff
from ai_engine.ai_writer import generate_text
from ai_engine.tasks import generate_meta_description
from ai_engine.tasks import generate_alt_text
from ai_engine.tasks import rewrite_title

if len(sys.argv) >= 3:
    TARGET_URL = sys.argv[1]
    USE_DYNAMIC_RENDERING = sys.argv[2].lower() == "true"
    UI_MODE = True
else:
    TARGET_URL = "https://www.wileyindia.com/resources_engineering/"
    USE_DYNAMIC_RENDERING = False

if UI_MODE:
    sys.stdout = io.StringIO()
 
def log(message):
    if not UI_MODE:
        print(message, flush=True) 
    
ORIGINAL_HTML = "data/pages/home.html"
MODIFIED_HTML = "data/pages/home_modified.html"


def main():
    pipeline_result = {
        "url": TARGET_URL,
        "crawler": "dynamic" if USE_DYNAMIC_RENDERING or UI_MODE else "static",
        "summary": {
            "meta_description": "unknown",
            "title": "unknown",
            "images_missing_alt": 0
        },
        "ai_actions": {},
        "diffs": []
    }
    
    print("\n=== SEO AUTOMATION PIPELINE STARTED ===\n", flush=True)

    # 1. Load HTML
    if UI_MODE:
        log("Using dynamic crawler (forced for UI)...")
        html = fetch_dynamic_page(TARGET_URL)
    else:
        if USE_DYNAMIC_RENDERING:
            print("Using dynamic crawler (Playwright)...", flush=True)
            html = fetch_dynamic_page(TARGET_URL)
        else:
            print("Using static crawler...", flush=True)
            html = fetch_page(TARGET_URL)

    if not html:
        print("Failed to load HTML")
        return
    
    with open(ORIGINAL_HTML, "w", encoding="utf-8") as f:
        f.write(html)
        
    # 2. Parse SEO data
    seo_data = extract_seo_tags(html)
    log("Pipeline progressing after dynamic fetch...")
    log("Parsed SEO data ✓")

    # 3. Run SEO rules
    seo_report = run_seo_checks(seo_data)
    log("SEO rules executed ✓")

    # 4. Generate fix suggestions
    fixes = generate_fix_suggestions(seo_report)
    log("Fix suggestions generated ✓")

    pipeline_result["summary"] = {
        "meta_description": (
            "missing"
            if "Missing meta description" in seo_report.get("meta_description", [])
            else "present"
        ),
        "title": (
            "issues"
            if seo_report.get("title")
            else "ok"
        ),
        "images_missing_alt": len(seo_report.get("images", []))
    }


    # 5a. AI for meta description (only if missing)
    ai_text = None

    if "Missing meta description" in seo_report.get("meta_description", []):
        print("\nUsing AI to generate meta description...")
        ai_text = generate_meta_description(seo_data)
        print("AI suggestion:", ai_text)
    else:
        print("Meta description already present — no AI action needed.")    
    pipeline_result["ai_actions"]["meta_description"] = ai_text
    
    # 5b. AI for image alt (only if missing)
    alt_texts = {}

    image_issues = seo_report.get("images", [])
    images = seo_data.get("images", [])

    if image_issues:
        print("\nUsing AI to generate alt text for images...")
        MAX_ALT_IMAGES = 5  # safety limit
        for issue in image_issues[:MAX_ALT_IMAGES]:
            idx = issue["index"]
            if idx >= len(images):
                continue
            image = images[idx]


            ai_alt = generate_alt_text(image)

            if not ai_alt:
                print(f"⚠️ Skipped alt text for image {idx} (invalid or timeout)")
                continue

            alt_texts[idx] = ai_alt
            print(f"AI alt text for image {idx}:", ai_alt)

        if len(image_issues) > MAX_ALT_IMAGES:
            print(f"⚠️ Skipping alt text for {len(image_issues) - MAX_ALT_IMAGES} images (limit reached)")

    else:
        print("\nAlt text for image exists — no AI action needed.")
    pipeline_result["ai_actions"]["alt_texts"] = alt_texts
        
    # 5c. AI for title (only if missing)
    new_title = None

    title_issues = seo_report.get("title", [])

    if title_issues:
        print("\nUsing AI to rewrite page title...")
        new_title = rewrite_title(seo_data)
        print("AI title suggestion:", new_title)
    else:
        print("\nTitle is SEO-friendly — no AI action needed.")
    pipeline_result["ai_actions"]["title"] = new_title
    
    # 6. Apply fixes to HTML
    modified_html = modify_html(
        html,
        meta_description_text=ai_text,
        alt_texts=alt_texts,
        new_title=new_title
    )

    with open(MODIFIED_HTML, "w", encoding="utf-8") as f:
        f.write(modified_html)

    log("HTML modifications prepared ✓")

    # 7. Generate diff
    diffs = generate_diff(html, modified_html)

    log("=== PROPOSED CHANGES ===")
    for op, text in diffs:
        if op == 1:
            pipeline_result["diffs"].append({
                "type": "added",
                "content": text.strip()
            })
        elif op == -1:
            pipeline_result["diffs"].append({
                "type": "removed",
                "content": text.strip()
            })

    # --- SAFETY: ensure summary always exists ---
    if not pipeline_result.get("summary"):
        pipeline_result["summary"] = {
            "meta_description": "unknown",
            "title": "unknown",
            "images_missing_alt": 0
        }

    # 8. Human approval
    if UI_MODE:
        import json
        sys.__stdout__.write(json.dumps(pipeline_result))
        return
    else:
        approve = input("\nApprove these changes? (y/n): ").lower()

        if approve == "y":
            print("\nChanges approved ✅", flush=True)
        else:
            print("\nChanges rejected ❌", flush=True)

        print("\n=== PIPELINE COMPLETE ===", flush=True)

if __name__ == "__main__":
    main()
