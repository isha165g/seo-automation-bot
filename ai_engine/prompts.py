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
    "Generate alt text for an image.\n\n"

    "FORMAT (must follow exactly):\n"
    "<subject> <action> <object>\n\n"

    "STRICT RULES:\n"
    "- Use 5 to 9 words only\n"
    "- Use ONLY nouns and verbs\n"
    "- Do NOT use prepositions (no to, on, at, in, with, during)\n"
    "- Do NOT use punctuation\n"
    "- Do NOT use years or numbers\n"
    "- End with a concrete object noun\n"
    "- Do NOT write a sentence\n"
    "- Output ONLY the alt text\n\n"

    "Image context:\n"
    "{context}\n\n"

    "Examples (follow style exactly):\n"
    "Professional speakers presenting conference stage\n"
    "Andrew delivering keynote presentation\n"
    "Lauren presenting slides team meeting\n"
    "Musician singing microphone stage\n"
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
