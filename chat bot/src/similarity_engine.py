import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def fetch_context(q_vec, tfidf_matrix, sentences, top_k=6):
    scores = cosine_similarity(q_vec, tfidf_matrix)[0]
    top_ids = np.argsort(scores)[-top_k:][::-1]
    return " ".join([sentences[i] for i in top_ids])
