# Multinomial‑Naive‑Bayes Programming Language Classifier

A project that builds a **programming language classifier** using the Multinomial Naive Bayes algorithm.
<br><b>ACCURACY: 0.95</b><br>
It downloads source code for various languages from GitHub, normalizes and tokenizes it, trains a model and allows you to test arbitrary code snippets to see which language they likely belong to.<br>
<b>LANGUAGES : Python, JavaScript, Java, C++, C, SQL, Shell, Rust, C#, x86 Assembly, Html, CSS, Haskell, TypeScript</b>

## Dataset Collection

### `get_data.py`

This script downloads source code from public GitHub repositories and builds a structured dataset for training the model.

### Output Structure

- creates a main directory **`dataset/`**
- inside it, one folder per programming language
- each folder contains `FILES_PER_LANGUAGE = 300` files
- file naming format **`dataset/{Language}/{Language}_{index}.{ext}`**
- sizes between `0.5 KB` and `50 KB`
  
### Download strategy:
- **`25%`** deterministic: top files from random GitHub search pages  
- **`75%`** randomized: files containing keywords from `RANDOM_KEYWORDS` to increase diversity

### Example Directory Tree
```
dataset/
├── Python/
│ ├── Python_0.py
│ ├── Python_1.py
│ └── ...
├── JavaScript/
│ ├── JavaScript_0.js
│ ├── JavaScript_1.js
│ └── ...
└── ... (other languages)
```

## Dataset Normalization  

### `normalize_data.py`, `create_dataset_pkl.py`  
First script processes the raw dataset and prepares it for training by performing several cleanup and preprocessing steps.<br>
Second script saves the normalized dataset in a `.pkl` file.

- loads all collected source code files from the `dataset/` directory
- removes noise such as:
  - excess whitespace  
  - comments  
  - non-ASCII characters  
- converts all text to lowercase for consistent processing
- saves the normalized files into the **`dataset_normalized/`** directory  
- stores the cleaned **`(code, language)`** pairs from the contents of `dataset_normalized/` into a single list
- creates the final pickle object **`dataset.pkl`** 

## Training the model

### `train_model.py`
This script loads the normalized dataset and trains a **Multinomial Naive Bayes (MNB)** classifier to predict the programming language of a given code snippet.

### What the script does
- loads the preprocessed dataset from `dataset.pkl`
- splits the data into:
  - **training set** **`80%`**
  - **test set** **`20%`**
- tokenizes the source code by splitting it into meaningful units (tokens) such as words, symbols and identifiers
- vectorizes the tokens using `TfidfVectorizer`, which converts each file into a numerical feature vector based on:
  - how often each token appears in that file (term frequency)
  - how unique that token is across the entire dataset (inverse document frequency)  
- trains a **Multinomial Naive Bayes** classifier using the implementation from **`scikit-learn`** (**`sklearn.naive_bayes.MultinomialNB`**)  
  - the model learns patterns in token frequencies from the TF-IDF vectors  
  - each programming language becomes a class, and the classifier learns which tokens and sequences are most representative of each  
  - uses **2‑grams** (pairs of consecutive tokens) in addition to single tokens, allowing the model to capture token sequences and simple syntactic patterns  
  - during training, the model computes probability distributions over tokens and token pairs to determine how likely a piece of code belongs to each language
- evaluates the model using:  
  - **accuracy score** — the overall percentage of correctly predicted files  
  - **classification report** — precision, recall, and F1-score for each programming language, showing how well the model performs per class  
  - **confusion matrix** — a table showing which languages were correctly classified and which were confused with others, helping identify patterns of misclassification
- saves the trained components:
  - **`model.pkl`** — the trained MNB model  
  - **`vectorizer.pkl`** — the TF-IDF vectorizer  

## How to use

There are two main ways to use this project.

### I Prebuilt dataset and trained model
The repository already has the normalized dataset `dataset.pkl`, you can skip directly to:    
**Dependencies:** `joblib` and `scikit-learn`.
```
pip install joblib scikit-learn
```
**Training** (the model is not in the repository because it has over `100MB`)
```
python train_model.py
```
**Testing** (`test.txt` will contain code in any of the 14 coding languages)
```
python tester.py test.txt
```


###  II Full pipeline (download and prepare your own dataset)
If you want to **collect new code files or modify the dataset**:
1. Install dependencies
   ```
   pip install -r requirements.txt
   ```
2. Download code files from GitHub
   ```
   python get_data.py
   ```
3. Normalize the dataset
   ```
   python normalize_data.py
   python create_dataset_pkl.py
   ```
4. Train the Multinomial Naive Bayes model
   ```
   python train_model.py
   ```
After this, you can test your own code snippets using `tester.py`.

## Results
<p align="center">
  <img height="300px" alt="class_accuracy_plot" src="https://github.com/user-attachments/assets/b14dd69c-b6a6-45dc-9d05-b5b0a2ee8870" />
  <img height="300px" alt="confusion_matrix_heatmap" src="https://github.com/user-attachments/assets/f20c0fb4-f1d3-4beb-8e62-38a1f6376bb8" />
</p>




