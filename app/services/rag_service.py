from typing import List
import chromadb
from chromadb.utils import embedding_functions
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

# -----------------------------
# ChromaDB setup
# -----------------------------
client = chromadb.Client()

collection_name = "user_skills"
try:
    collection = client.get_collection(collection_name)
except:
    collection = client.create_collection(
        name=collection_name,
        embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
    )

# -----------------------------
# Sparse TF-IDF storage
# -----------------------------
sparse_index = {}  # {user_id: {"skills": [...], "vectorizer": TFIDF, "tfidf_matrix": matrix}}

# -----------------------------
# Functions
# -----------------------------
def add_user_skills(user_id: str, skills: List[str]):
    ids = [f"{user_id}_{i}" for i in range(len(skills))]
    metadatas = [{"user_id": user_id} for _ in skills]

    # Dense
    collection.add(
        ids=ids,
        documents=skills,
        metadatas=metadatas
    )

    # Sparse
    sparse_index[user_id] = {}
    sparse_index[user_id]["skills"] = skills
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(skills)
    sparse_index[user_id]["vectorizer"] = vectorizer
    sparse_index[user_id]["tfidf_matrix"] = tfidf_matrix

def retrieve_user_skills(user_id: str, job_description: str, top_k: int = 10) -> List[str]:
    if user_id not in sparse_index:
        return []

    # Sparse retrieval
    vectorizer = sparse_index[user_id]["vectorizer"]
    tfidf_matrix = sparse_index[user_id]["tfidf_matrix"]
    skills = sparse_index[user_id]["skills"]

    job_vec = vectorizer.transform([job_description])
    cosine_sim = (tfidf_matrix @ job_vec.T).toarray().flatten()
    sparse_scores = cosine_sim / (cosine_sim.max() + 1e-8)

    # Dense retrieval
    results = collection.query(
        query_texts=[job_description],
        n_results=top_k,
        where={"user_id": user_id}
    )
    dense_skills = results.get("documents", [[]])[0]
    dense_scores = np.linspace(1.0, 0.5, num=len(dense_skills))
    dense_dict = dict(zip(dense_skills, dense_scores))

    # Hybrid scoring
    hybrid_scores = {}
    alpha, beta = 0.5, 0.5
    for idx, skill in enumerate(skills):
        sparse_score = sparse_scores[idx] if idx < len(sparse_scores) else 0
        dense_score = dense_dict.get(skill, 0)
        hybrid_scores[skill] = alpha * dense_score + beta * sparse_score

    ranked_skills = sorted(hybrid_scores.items(), key=lambda x: x[1], reverse=True)
    top_skills = [s for s, score in ranked_skills[:top_k]]
    return top_skills
