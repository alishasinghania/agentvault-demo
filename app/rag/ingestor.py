import os
from pathlib import Path
from typing import List
from llama_index import SimpleDirectoryReader, Document

from app.rag.vectorstore import add_documents


def ingest_document(file_path: str) -> int:
    path = Path(file_path)
    parent_dir = str(path.parent)

    reader = SimpleDirectoryReader(
        input_dir=parent_dir,
        input_files=[str(path)],
        recursive=False,
    )
    documents: List[Document] = reader.load_data()

    texts = []
    metadatas = []
    for doc in documents:
        chunks = _chunk_text(doc.text, chunk_size=512, overlap=50)
        for chunk in chunks:
            texts.append(chunk)
            metadatas.append({
                "source": path.name,
                "file_path": str(path),
            })

    if texts:
        add_documents(texts, metadatas)

    return len(texts)


def ingest_directory(directory: str) -> int:
    reader = SimpleDirectoryReader(
        input_dir=directory,
        recursive=True,
    )
    documents: List[Document] = reader.load_data()

    texts = []
    metadatas = []
    for doc in documents:
        chunks = _chunk_text(doc.text, chunk_size=512, overlap=50)
        for chunk in chunks:
            texts.append(chunk)
            metadatas.append({
                "source": doc.metadata.get("file_name", "unknown"),
                "file_path": doc.metadata.get("file_path", ""),
            })

    if texts:
        add_documents(texts, metadatas)

    return len(texts)


def _chunk_text(text: str, chunk_size: int = 512, overlap: int = 50) -> List[str]:
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks if chunks else [text]
