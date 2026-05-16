import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any

from app.config import CHROMA_PERSIST_DIR
from app.rag.embedder import embed_texts, embed_query

COLLECTION_NAME = "meridian_knowledge_base"

_client = None
_collection = None


def _get_client():
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(
            path=CHROMA_PERSIST_DIR,
            settings=Settings(anonymized_telemetry=False),
        )
    return _client


def get_collection():
    global _collection
    if _collection is None:
        client = _get_client()
        _collection = client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )
    return _collection


def add_documents(texts: List[str], metadatas: List[Dict] = None, ids: List[str] = None):
    collection = get_collection()
    embeddings = embed_texts(texts)

    if ids is None:
        import uuid
        ids = [str(uuid.uuid4()) for _ in texts]

    if metadatas is None:
        metadatas = [{}] * len(texts)

    collection.add(
        embeddings=embeddings,
        documents=texts,
        metadatas=metadatas,
        ids=ids,
    )
    return len(texts)


def similarity_search(query: str, n_results: int = 4) -> List[Dict[str, Any]]:
    collection = get_collection()
    query_embedding = embed_query(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=["documents", "metadatas", "distances"],
    )

    docs = []
    for i, doc in enumerate(results["documents"][0]):
        docs.append({
            "page_content": doc,
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i],
        })
    return docs


def get_collection_count() -> int:
    return get_collection().count()
