import sys
sys.path.append(".")

from parser.parser import load_html, extract_seo_tags
from seo_rules.rules import run_seo_checks
from suggestions.suggestions import generate_fix_suggestions
from modifier.modifier import modify_html
from diff_engine.diff_generator import generate_diff
from ai_engine.ai_writer import generate_text
from ai_engine.tasks import generate_meta_description
from ai_engine.tasks import generate_alt_text
from ai_engine.tasks import rewrite_title

ORIGINAL_HTML = "data/pages/home.html"
MODIFIED_HTML = "data/pages/home_modified.html"

def main():
    print("\n=== SEO AUTOMATION PIPELINE STARTED ===\n")

    # 1. Load HTML
    html = load_html(ORIGINAL_HTML)
    if not html:
        print("Failed to load HTML")
        return

    # 2. Parse SEO data
    seo_data = extract_seo_tags(html)
    print("Parsed SEO data ✓")

    # 3. Run SEO rules
    seo_report = run_seo_checks(seo_data)
    print("SEO rules executed ✓")

    # 4. Generate fix suggestions
    fixes = generate_fix_suggestions(seo_report)
    print("Fix suggestions generated ✓")

    # 5a. AI for meta description (only if missing)
    ai_text = None

    if "Missing meta description" in seo_report.get("meta_description", []):
        print("\nUsing AI to generate meta description...")
        ai_text = generate_meta_description(seo_data)
        print("AI suggestion:", ai_text)
    else:
        print("Meta description already present — no AI action needed.")    
    
    # 5b. AI for image alt (only if missing)
    alt_texts = {}

    image_issues = seo_report.get("images", [])
    images = seo_data.get("images", [])

    if image_issues:
        print("\nUsing AI to generate alt text for images...")

        for issue in image_issues:
            idx = issue["index"]
            if idx >= len(images):
                continue
            image = images[idx]


            ai_alt = generate_alt_text(image)
            if ai_alt:
                alt_texts[idx] = ai_alt

            print(f"AI alt text for image {idx}:", ai_alt)
    else:
        print("\nAlt text for image exists — no AI action needed.")
        
    # 5c. AI for title (only if missing)
    new_title = None

    title_issues = seo_report.get("title", [])

    if title_issues:
        print("\nUsing AI to rewrite page title...")
        new_title = rewrite_title(seo_data)
        print("AI title suggestion:", new_title)
    else:
        print("\nTitle is SEO-friendly — no AI action needed.")

    # 6. Apply fixes to HTML
    modified_html = modify_html(
        html,
        meta_description_text=ai_text,
        alt_texts=alt_texts,
        new_title=new_title
    )

    with open(MODIFIED_HTML, "w", encoding="utf-8") as f:
        f.write(modified_html)

    print("\nHTML modifications prepared ✓")

    # 7. Generate diff
    diffs = generate_diff(html, modified_html)

    print("\n=== PROPOSED CHANGES ===")
    for op, text in diffs:
        if op == 1:
            print("[ADDED]", text.strip())
        elif op == -1:
            print("[REMOVED]", text.strip())

    # 8. Human approval
    approve = input("\nApprove these changes? (y/n): ").lower()

    if approve == "y":
        print("\nChanges approved ✅")
        print("You can now commit these changes.")
    else:
        print("\nChanges rejected ❌")
        print("Original HTML remains untouched.")

    print("\n=== PIPELINE COMPLETE ===")

if __name__ == "__main__":
    main()
