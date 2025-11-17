import os
import re

DATASET_DIR = "dataset"
OUTPUT_DIR = "dataset_normalized"
SAVE_NORMALIZED_FILES = True

def normalize_code(code, lang=None):
    code = re.sub(r"#.*", "", code)      # Python, Shell
    code = re.sub(r"//.*", "", code)     # C-like: C, C++, C#, Java, JS, TS, Rust
    code = re.sub(r"--.*", "", code)     # SQL, Haskell
    code = re.sub(r";.*", "", code)      # x86 Assembly

    code = re.sub(r"/\*.*?\*/", "", code, flags=re.DOTALL)      # C-like, CSS, SQL
    code = re.sub(r'"""(.*?)"""', "", code, flags=re.DOTALL)    # Python multi-line
    code = re.sub(r"'''(.*?)'''", "", code, flags=re.DOTALL)    # Python multi-line
    code = re.sub(r"{-.*?-}", "", code, flags=re.DOTALL)        # Haskell multi-line
    code = re.sub(r"<!--.*?-->", "", code, flags=re.DOTALL)    # HTML

    code = re.sub(r'".*?"', "STRING", code)     # double-quoted strings
    code = re.sub(r"'.*?'", "STRING", code)     # single-quoted strings
    code = re.sub(r"\b\d+\b", "NUMBER", code)   # numeric literals
    
    code = re.sub(r"\s+", " ", code)

    return code.strip()

def process_language(lang_dir, output_base):
    lang_name = os.path.basename(lang_dir)
    output_dir = os.path.join(output_base, lang_name)
    os.makedirs(output_dir, exist_ok=True)

    files = os.listdir(lang_dir)
    normalized_texts = []

    for idx, file in enumerate(files):
        file_path = os.path.join(lang_dir, file)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                code = f.read()
        except Exception as e:
            print(f"Skipping {file}: {e}")
            continue

        norm_code = normalize_code(code, lang=lang_name)
        normalized_texts.append((norm_code, lang_name))

        if SAVE_NORMALIZED_FILES:
            out_file = os.path.join(output_dir, f"{lang_name}_{idx}.txt")
            with open(out_file, "w", encoding="utf-8") as f:
                f.write(norm_code)

    print(f"✔ Processed {len(normalized_texts)} files for {lang_name}")
    return normalized_texts

def main():
    all_data = []

    for lang_name in os.listdir(DATASET_DIR):
        lang_dir = os.path.join(DATASET_DIR, lang_name)
        if not os.path.isdir(lang_dir):
            continue

        normalized = process_language(lang_dir, OUTPUT_DIR)
        all_data.extend(normalized)

    print(f"\nNormalization complete! Total files processed: {len(all_data)}")

    return all_data

if __name__ == "__main__":
    dataset = main()
