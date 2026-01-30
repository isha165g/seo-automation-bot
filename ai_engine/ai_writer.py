import os
from google import genai

# Create Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def clean_ai_output(text):
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return ""
    return lines[0]


def clean_alt_text(text):
    if not text:
        return None

    words = text.split()
    if not (5 <= len(words) <= 9):
        return None

    # hard reject if any preposition sneaks in
    forbidden = {"to", "on", "at", "in", "with", "during"}
    if any(w.lower() in forbidden for w in words):
        return None

    return text.strip()


def generate_text(prompt):
    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt,
            config={
                "temperature": 0.4,
                "max_output_tokens": 200
            }
        )
    except Exception as e:
        print("Gemini error:", e)
        return None

    if not response or not response.text:
        return None

    cleaned = clean_ai_output(response.text)

    MAX_LEN = 155
    if len(cleaned) > MAX_LEN:
        truncated = cleaned[:MAX_LEN]
        if "." in truncated:
            truncated = truncated.rsplit(".", 1)[0] + "."
        cleaned = truncated

    return clean_alt_text(cleaned)


if __name__ == "__main__":
    prompt = (
        "Write ONE single-sentence SEO meta description.\n"
        "- Maximum 155 characters\n"
        "- Do NOT write explanations\n"
        "- Do NOT use quotes\n"
        "- Output ONLY the meta description text\n"
        "Context: ERP and AI services company."
    )

    text = generate_text(prompt)

    print("AI Generated Text:\n")
    print(text if text else "[No output received]")
