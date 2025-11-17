import pickle
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import joblib

with open("dataset.pkl", "rb") as f:
    dataset = pickle.load(f)

X = [code for code, lang in dataset]
y = [lang for code, lang in dataset]

print(f"Loaded {len(dataset)} code snippets from dataset.pkl")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Training set: {len(X_train)} samples")
print(f"Test set: {len(X_test)} samples")

def code_tokenizer(code):
    """
    Tokenizes normalized code into identifiers, keywords, operators, and placeholders.
    """
    return re.findall(r'\b\w+\b|==|!=|<=|>=|->|[\+\-\*/=<>{}()\[\];]', code)

vectorizer = CountVectorizer(tokenizer=code_tokenizer, ngram_range=(1,2))
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

print(f"Vocabulary size: {len(vectorizer.vocabulary_)} tokens")

clf = MultinomialNB(alpha=1.0)
clf.fit(X_train_vec, y_train)

print("Model training completed!")

y_pred = clf.predict(X_test_vec)

print("\n Accuracy:", accuracy_score(y_test, y_pred))
print("\n Classification Report:\n", classification_report(y_test, y_pred))
print("\n Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

joblib.dump(clf, "mnb_language_model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("\nModel and vectorizer saved as 'mnb_language_model.pkl' and 'vectorizer.pkl'")
