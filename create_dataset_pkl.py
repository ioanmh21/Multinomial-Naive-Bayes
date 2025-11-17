import os
import pickle

def load_normalized_dataset(base_dir="dataset_normalized"):
    dataset = []
    for lang in os.listdir(base_dir):
        lang_dir = os.path.join(base_dir, lang)
        if not os.path.isdir(lang_dir):
            continue
        for filename in os.listdir(lang_dir):
            file_path = os.path.join(lang_dir, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                code = f.read()
            dataset.append((code, lang))
    return dataset

dataset = load_normalized_dataset()

with open("dataset.pkl", "wb") as f:
    pickle.dump(dataset, f)

print(f"Saved {len(dataset)} code snippets to dataset.pkl")
