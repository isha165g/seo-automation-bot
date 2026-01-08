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

    if stderr:
        print("Ollama errors (ignored):", stderr)

    return stdout.strip()

if __name__ == "__main__":
    prompt = (
        "Write a clear SEO meta description under 155 characters "
        "for an ERP and AI services company. "
        "No marketing fluff. Simple and factual."
    )

    text = generate_text(prompt)

    print("AI Generated Text:\n")
    print(text if text else "[No output received]")
