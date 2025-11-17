import re
import joblib
import sys

def code_tokenizer(code):
    return re.findall(r'\b\w+\b|==|!=|<=|>=|->|[\+\-\*/=<>{}()\[\];]', code)

clf = joblib.load("mnb_language_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

def remove_comments(code):
    code = re.sub(r'//.*', '', code)
    code = re.sub(r'#.*', '', code)
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    return code

def replace_strings_numbers(code):
    code = re.sub(r'"[^"\n]*"|\'[^\'\n]*\'', 'STRING', code)
    code = re.sub(r'\b\d+(\.\d+)?\b', 'NUMBER', code)
    return code

def normalize(code):
    code = remove_comments(code)
    code = replace_strings_numbers(code)
    return code

def predict_language_from_text(text):
    text_norm = normalize(text)
    vec = vectorizer.transform([text_norm])
    return clf.predict(vec)[0]

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python tester.py <file.txt>")
        sys.exit(1)

    file_path = sys.argv[1]

    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()

    print("Predicted language:", predict_language_from_text(code))
