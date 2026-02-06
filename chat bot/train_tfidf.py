import os
import pickle
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from src.pdf_processor import extract_sentences

# Download required NLTK data
nltk.download("stopwords", quiet=True)
nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)

# Robust path handling
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODELS_DIR = os.path.join(BASE_DIR, "models")

if not os.path.exists(MODELS_DIR):
    os.makedirs(MODELS_DIR)

# Iterate over all PDFs in the data directory
sentences = []
if os.path.exists(DATA_DIR) and os.path.isdir(DATA_DIR):
    for file in os.listdir(DATA_DIR):
        if file.endswith(".pdf"):
            full_path = os.path.join(DATA_DIR, file)
            print(f"Processing: {file}")
            sentences.extend(extract_sentences(full_path))
else:
    print(f"Error: Directory not found at {DATA_DIR}")

# TF-IDF Training
if sentences:
    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        max_features=15000
    )

    tfidf_matrix = vectorizer.fit_transform(sentences)

    # Save models
    with open(os.path.join(MODELS_DIR, "vectorizer.pkl"), "wb") as f:
        pickle.dump(vectorizer, f)

    with open(os.path.join(MODELS_DIR, "matrix.pkl"), "wb") as f: # Note: chatbot.py expects matrix.pkl not tfidf_matrix.pkl
        pickle.dump(tfidf_matrix, f)

    with open(os.path.join(MODELS_DIR, "sentences.pkl"), "wb") as f:
        pickle.dump(sentences, f)

    print("✅ TF-IDF training completed")
    print(f"📁 Saved models to: {MODELS_DIR}")
else:
    print("⚠️ No sentences extracted. Check your PDF files.")
