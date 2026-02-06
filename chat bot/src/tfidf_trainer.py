import pickle
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from pdf_processor import extract_sentences

nltk.download("stopwords")

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "../data")
MODELS_DIR = os.path.join(BASE_DIR, "../models")

if not os.path.exists(MODELS_DIR):
    os.makedirs(MODELS_DIR)

PDF_PATH = DATA_DIR

sentences = []
if os.path.exists(PDF_PATH) and os.path.isdir(PDF_PATH):
    for file in os.listdir(PDF_PATH):
        if file.endswith(".pdf"):
            full_path = os.path.join(PDF_PATH, file)
            print(f"Processing: {file}")
            sentences.extend(extract_sentences(full_path))
else:
    print(f"Error: Directory not found at {PDF_PATH}")
    sentences = []

vectorizer = TfidfVectorizer(
    stop_words="english",
    ngram_range=(1, 2),
    max_features=15000
)

tfidf_matrix = vectorizer.fit_transform(sentences)

with open(os.path.join(MODELS_DIR, "vectorizer.pkl"), "wb") as f:
    pickle.dump(vectorizer, f)

with open(os.path.join(MODELS_DIR, "matrix.pkl"), "wb") as f:
    pickle.dump(tfidf_matrix, f)

with open(os.path.join(MODELS_DIR, "sentences.pkl"), "wb") as f:
    pickle.dump(sentences, f)

print("✅ TF-IDF training completed")
