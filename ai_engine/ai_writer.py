import subprocess

def generate_text(prompt):
    process = subprocess.Popen(
        ["ollama", "run", "phi"], #mistral / phi
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="ignore"
    )

    stdout, stderr = process.communicate(prompt)

    def clean_ai_output(text):
        # Take only the first non-empty line
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        if not lines:
            return ""
        return lines[0]

    cleaned = clean_ai_output(stdout)
    cleaned = cleaned.strip('"').strip("'")
    cleaned = cleaned[:155]    # hard SEO limit
    return cleaned


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
