import pickle
from .similarity_engine import fetch_context
from .mark_analyzer import detect_marks
from .ollama_engine import generate_answer
from .translator import handle_language, translate_back

import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "../models")

try:
    with open(os.path.join(MODELS_DIR, "vectorizer.pkl"), "rb") as f:
        vectorizer = pickle.load(f)

    with open(os.path.join(MODELS_DIR, "matrix.pkl"), "rb") as f:
        tfidf_matrix = pickle.load(f)

    with open(os.path.join(MODELS_DIR, "sentences.pkl"), "rb") as f:
        sentences = pickle.load(f)
except FileNotFoundError as e:
    print(f"Error loading models: {e}")
    print("Please run `src/tfidf_trainer.py` first to generate models.")
    sys.exit(1)

def chatbot(question):
    q_en, lang = handle_language(question)
    marks = detect_marks(q_en)

    q_vec = vectorizer.transform([q_en])
    context = fetch_context(q_vec, tfidf_matrix, sentences)

    answer_en = generate_answer(context, q_en, marks)
    return translate_back(answer_en, lang)
