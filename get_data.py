import os
import requests
import random
import time
import re

LANGUAGES = {
    "Python": "py",
    "JavaScript": "js",
    "Java": "java",
    "C++": "cpp",
    "C": "c",
    "SQL": "sql",
    "Shell": "sh",
    "Rust": "rs",
    "C#": "cs",
    "x86 Assembly": "asm",
    "Html": "html",
    "CSS": "css",
    "Haskell": "hs",
    "TypeScript": "ts",
}

FILES_PER_LANGUAGE = 300
DETERMINISTIC_RATE = 0.25

OUTPUT_DIR = "dataset"
MIN_SIZE = 500
MAX_SIZE = 50_000

RANDOM_KEYWORDS = {
    "Python": ["def", "class", "import", "lambda"],
    "JavaScript": ["function", "const", "let", "class"],
    "Java": ["public", "class", "import", "void"],
    "C++": ["int", "class", "namespace", "template"],
    "C": ["int", "include", "return", "main"],
    "SQL": ["SELECT", "INSERT", "UPDATE", "WHERE"],
    "Shell": ["echo", "#!/bin/bash", "ls", "grep"],
    "Rust": ["fn", "let", "struct", "mod"],
    "C#": ["using", "class", "namespace", "void"],
    "x86 Assembly": ["mov", "push", "call", "ret"],
    "Html": ["<div>", "<p>", "<a>", "<span>"],
    "CSS": ["color:", "font-", "background", "margin"],
    "Haskell": ["data", "import", "where", "module"],
    "TypeScript": ["function", "class", "import", "let"],
}

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise ValueError("ERROR: Set GITHUB_TOKEN environment variable before running.")

HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

def search_github_files(ext, keyword=None, page=1):
    q = f"extension:{ext}"
    if keyword:
        q += f" {keyword}"
    url = "https://api.github.com/search/code"
    params = {"q": q, "per_page": 100, "page": page}
    resp = requests.get(url, headers=HEADERS, params=params)

    if resp.status_code == 403:
        print("Rate limited — sleeping 10 seconds...")
        time.sleep(10)
        return []

    if resp.status_code != 200:
        return []

    return resp.json().get("items", [])


def is_minified(text):
    return any(len(line) > 500 for line in text.split("\n"))


def download_file(item):
    raw_url = item["html_url"].replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
    resp = requests.get(raw_url, headers=HEADERS)

    if resp.status_code != 200:
        return None

    content = resp.content

    if not (MIN_SIZE <= len(content) <= MAX_SIZE):
        return None

    text = content.decode("utf-8", errors="ignore")

    if is_minified(text) or re.search(r"{.{800,}}", text):
        return None

    return text

def collect_files(language, ext):
    target_total = FILES_PER_LANGUAGE
    target_det = int(target_total * DETERMINISTIC_RATE)
    target_rand = target_total - target_det

    lang_dir = os.path.join(OUTPUT_DIR, language.replace(" ", "_"))
    os.makedirs(lang_dir, exist_ok=True)

    collected = []
    existing_files = os.listdir(lang_dir)
    existing_count = len(existing_files)
    if existing_count >= target_total:
        print(f"\n✔ {language} already complete ({existing_count} files). Skipping.")
        return

    print(f"\n=== Collecting {language} ({ext}) ===")
    print(f"Target: {target_total} files → Deterministic: {target_det}, Random: {target_rand}")

    keywords = RANDOM_KEYWORDS.get(language, [None])

    det_pages = random.sample(range(1, 51), k=10)
    det_files_needed = target_det
    for page in det_pages:
        if det_files_needed <= 0:
            break
        keyword = random.choice(keywords)
        results = search_github_files(ext, keyword=keyword, page=page)
        for item in results:
            if det_files_needed <= 0:
                break
            code = download_file(item)
            if code:
                collected.append(code)
                det_files_needed -= 1
        time.sleep(0.3)
        
    rand_attempts = 0
    max_rand_attempts = 500
    while len(collected) < target_total and rand_attempts < max_rand_attempts:
        rand_attempts += 1
        rand_page = random.randint(1, 50)
        keyword = random.choice(keywords)
        results = search_github_files(ext, keyword=keyword, page=rand_page)
        random.shuffle(results)
        for item in results:
            if len(collected) >= target_total:
                break
            code = download_file(item)
            if code:
                collected.append(code)
        time.sleep(0.3)

    random.shuffle(collected)

    print(f"Saving {len(collected)} files for {language}...")
    for i, code in enumerate(collected):
        filename = os.path.join(lang_dir, f"{language}_{i}.{ext}")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(code)

    print(f"✔ {language} complete.")


def main():
    for lang, ext in LANGUAGES.items():
        collect_files(lang, ext)
    print("\nDataset collection complete!")


if __name__ == "__main__":
    main()
