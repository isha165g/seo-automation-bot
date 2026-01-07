from diff_match_patch import diff_match_patch
import os

ORIGINAL_FILE = "data/pages/home.html"
MODIFIED_FILE = "data/pages/home_modified.html"

def load_file(path):
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return None

    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def generate_diff(original, modified):
    dmp = diff_match_patch()
    diffs = dmp.diff_main(original, modified)
    dmp.diff_cleanupSemantic(diffs)
    return diffs

def print_diff(diffs):
    for op, text in diffs:
        if op == 0:
            continue
        elif op == -1:
            print("[- Removed ]")
            print(text)
        elif op == 1:
            print("[+ Added ]")
            print(text)

if __name__ == "__main__":
    original_html = load_file(ORIGINAL_FILE)
    modified_html = load_file(MODIFIED_FILE)

    if original_html and modified_html:
        diffs = generate_diff(original_html, modified_html)
        print_diff(diffs)
