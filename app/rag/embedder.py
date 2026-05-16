from sentence_transformers import SentenceTransformer
from typing import List


model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def embed_texts(texts: List[str]) -> List[List[float]]:
    embeddings = model.encode(texts, convert_to_numpy=True)
    return embeddings.tolist()


def embed_query(query: str) -> List[float]:
    embedding = model.encode([query], convert_to_numpy=True)
    return embedding[0].tolist()
