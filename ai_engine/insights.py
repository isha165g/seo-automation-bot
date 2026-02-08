from ai_engine.ai_writer import generate_text


def generate_ai_insights(seo_report: dict, onpage_score: dict):
    issues = []

    # ---- Rule-based issues ----
    if "Missing meta description" in seo_report.get("meta_description", []):
        issues.append("missing meta description")

    if seo_report.get("title"):
        issues.append("page title not optimized for SEO")

    if seo_report.get("images"):
        issues.append(f"{len(seo_report['images'])} images missing alt text")

    # ---- On-page analyzer issues ----
    onpage_issues = onpage_score.get("issues", [])
    score_value = onpage_score.get("on_page_score", 100)

    issues.extend(onpage_issues)

    # Remove duplicates
    issues = list(dict.fromkeys(issues))

    # ---- No issues case ----
    if not issues:
        return (
            "The page demonstrates strong adherence to SEO best practices. "
            "Metadata, accessibility attributes, and content structure are "
            "well optimized, supporting strong search visibility and usability."
        )

    issues_text = ", ".join(issues)

    # ---- Gemini prompt ----
    prompt = (
        "You are an experienced SEO consultant writing an audit summary.\n"
        "Write ONE professional paragraph of 3 to 4 complete sentences.\n"
        "Explain the impact of the detected issues on SEO performance.\n"
        "Do NOT provide fixes or step-by-step instructions.\n"
        "Do NOT mention AI, tools, or models.\n"
        "Use a formal audit-report tone.\n\n"
        f"On-page SEO score: {score_value} out of 100.\n"
        f"Detected SEO issues: {issues_text}"
    )

    insight = generate_text(prompt)

    # ---- Hard fallback (never return weak text) ----
    if not insight or len(insight.split()) < 25:
        return (
            "The audit indicates multiple on-page SEO and accessibility gaps "
            "that may reduce search visibility and user engagement. A low on-page "
            "SEO score reflects weaknesses in metadata, heading structure, and "
            "image accessibility. Addressing these areas would significantly "
            "improve overall discoverability and content clarity."
        )

    return insight
