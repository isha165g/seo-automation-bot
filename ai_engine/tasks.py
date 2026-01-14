from ai_engine.ai_writer import generate_text
from ai_engine.prompts import (
    META_DESCRIPTION_PROMPT,
    ALT_TEXT_PROMPT,
    TITLE_REWRITE_PROMPT
)

def generate_meta_description(seo_data):
    prompt = META_DESCRIPTION_PROMPT.format(
        title=seo_data.get("title", ""),
        content=seo_data.get("page_text", "")
    )
    return generate_text(prompt)

def generate_alt_text(image):
    context = image.get("alt") or image.get("src", "")
    prompt = ALT_TEXT_PROMPT.format(context=context)
    return generate_text(prompt)

def rewrite_title(seo_data):
    prompt = TITLE_REWRITE_PROMPT.format(
        title=seo_data.get("title", ""),
        content=seo_data.get("page_text", "")
    )
    return generate_text(prompt)
