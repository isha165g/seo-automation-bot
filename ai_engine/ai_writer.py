import subprocess

def generate_text(prompt):
    process = subprocess.Popen(
        ["ollama", "run", "mistral"], #mistral / phi
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="ignore"
    )

    try:
        stdout, stderr = process.communicate(prompt, timeout=20)
    except Exception:
        process.kill()
        return None


    def clean_ai_output(text):
        # Take only the first non-empty line
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        if not lines:
            return ""
        return lines[0]

    def clean_alt_text(text):
        if len(text) > 80:
            return None
        
        text = text.strip().strip('"').strip("'")

        # Remove obvious AI chatter
        banned_phrases = [
        "alt text", "this is", "would be", "i am", "i'm",
        "assistant", "the output", "the image shows", "description"
    ]

        lowered = text.lower()
        for phrase in banned_phrases:
            if phrase in lowered:
                return None  # reject bad output

        # Keep only first sentence
        if "." in text:
            text = text.split(".")[0]

        # Enforce max words
        words = text.split()
        if len(words) > 10:
            text = " ".join(words[:10])

        return text

    cleaned = clean_ai_output(stdout)
    cleaned = cleaned.strip('"').strip("'")

    MAX_LEN = 155
    if len(cleaned) > MAX_LEN:
        truncated = cleaned[:MAX_LEN]
        # Try to cut at last full stop
        if "." in truncated:
            truncated = truncated.rsplit(".", 1)[0] + "."
        cleaned = truncated

    cleaned_alt = clean_alt_text(cleaned)
    return cleaned_alt


if __name__ == "__main__":
    prompt = (
    "Write ONE single-sentence SEO meta description.\n"
    "- Maximum 155 characters\n"
    "- Do NOT write explanations, stories, or examples\n"
    "- Do NOT use quotes\n"
    "- Do NOT add headings or new lines\n"
    "- Output ONLY the meta description text\n"
    "Context: ERP and AI services company."
)

    text = generate_text(prompt)

    print("AI Generated Text:\n")
    print(text if text else "[No output received]")
