from ai_engine.ai_writer import generate_text

def generate_ai_insights(seo_report: dict):
    issues = []

    if "Missing meta description" in seo_report.get("meta_description", []):
        issues.append("missing meta description")

    if seo_report.get("images"):
        issues.append(f"{len(seo_report['images'])} images missing alt text")

    if seo_report.get("title"):
        issues.append("page title not optimized for SEO")

    # No issues case
    if not issues:
        return (
            "The page demonstrates strong adherence to SEO best practices. "
            "Metadata, accessibility attributes, and structural elements are "
            "properly implemented, resulting in good search visibility and usability."
        )

    issues_text = ", ".join(issues)

    prompt = (
        "You are an experienced SEO consultant writing an audit summary.\n"
        "Write ONE complete paragraph (3 to 4 sentences).\n"
        "The paragraph must be fully formed and end cleanly.\n"
        "Explain the impact of the detected SEO issues.\n"
        "Do NOT give instructions or solutions.\n"
        "Do NOT mention AI, tools, or models.\n"
        "Use a professional, report-style tone.\n\n"
        f"Detected SEO issues: {issues_text}"
    )

    insight = generate_text(prompt)

    # 🛡️ Hard quality gate
    if not insight or len(insight.split()) < 20 or insight.endswith(("for", "of", "to", "with")):
        return (
            "The analysis reveals notable SEO and accessibility gaps that may "
            "limit search visibility and user experience. Several images lack "
            "descriptive alternative text, affecting accessibility compliance and "
            "image search performance. Addressing these gaps would strengthen "
            "overall content clarity and discoverability."
        )

    return insight
