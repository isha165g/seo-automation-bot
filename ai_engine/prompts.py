"""
Centralized prompt templates for AI SEO tasks.
Only text. No logic.
"""

META_DESCRIPTION_PROMPT = (
    "Write ONE single-sentence SEO meta description.\n"
    "- Maximum 155 characters\n"
    "- Do NOT explain what you are writing\n"
    "- Do NOT mention 'meta description'\n"
    "- Do NOT repeat the page title verbatim\n"
    "- Neutral, factual tone\n"
    "- Output ONLY the description text\n\n"
    "Page title: {title}\n"
    "Page content summary: {content}"
)

ALT_TEXT_PROMPT = (
    "Write short, descriptive alt text for an image.\n"
    "- Maximum 10 words\n"
    "- No filler words\n"
    "- No punctuation\n"
    "- Output ONLY the alt text\n\n"
    "Image context: {context}"
)

TITLE_REWRITE_PROMPT = (
    "Rewrite the page title for SEO.\n"
    "- Maximum 60 characters\n"
    "- Clear and descriptive\n"
    "- Avoid branding repetition\n"
    "- Output ONLY the title\n\n"
    "Current title: {title}\n"
    "Page content summary: {content}"
)
