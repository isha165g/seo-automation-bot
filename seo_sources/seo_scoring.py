def score_seoanalyzer(report: dict):
    score = 100
    issues = []

    # Title length
    if report["meta"]["title_length"] < 30 or report["meta"]["title_length"] > 65:
        score -= 10
        issues.append("Title length is not optimal")

    # Meta description
    if report["meta"]["meta_description_length"] < 70:
        score -= 10
        issues.append("Meta description is too short or missing")

    # Canonical
    if not report["meta"]["has_canonical"]:
        score -= 10
        issues.append("Missing canonical tag")

    # Robots
    if not report["meta"]["has_robots"]:
        score -= 5
        issues.append("Missing robots meta tag")

    # Viewport
    if not report["meta"]["has_viewport"]:
        score -= 5
        issues.append("Missing viewport meta tag")

    # H1
    if report["headings"]["h1_count"] == 0:
        score -= 15
        issues.append("Missing H1 heading")
    elif report["headings"]["h1_count"] > 1:
        score -= 10
        issues.append("Multiple H1 headings detected")

    # Images
    missing_alt = report["images"]["missing_alt"]
    if missing_alt > 0:
        penalty = min(20, missing_alt * 3)
        score -= penalty
        issues.append(f"{missing_alt} images missing alt text")

    score = max(score, 0)

    return {
        "on_page_score": score,
        "issues": issues
    }
