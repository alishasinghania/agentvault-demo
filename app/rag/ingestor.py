from pathlib import Path
from typing import List

from app.rag.vectorstore import add_documents

_TEXT_EXTENSIONS = {".txt", ".md", ".markdown", ".csv", ".log", ".json", ".yml", ".yaml"}


def ingest_document(file_path: str) -> int:
    path = Path(file_path)
    if not path.is_file():
        return 0

    text = path.read_text(encoding="utf-8", errors="ignore")
    texts = []
    metadatas = []
    for chunk in _chunk_text(text, chunk_size=512, overlap=50):
        texts.append(chunk)
        metadatas.append({
            "source": path.name,
            "file_path": str(path),
        })

    if texts:
        add_documents(texts, metadatas)

    return len(texts)


def ingest_directory(directory: str) -> int:
    root = Path(directory)
    if not root.is_dir():
        return 0

    texts: List[str] = []
    metadatas: List[dict] = []

    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.name.startswith("."):
            continue
        if path.suffix.lower() not in _TEXT_EXTENSIONS and path.suffix.lower() not in {".txt", ".md"}:
            # Still allow extensionless / .txt knowledge-base files
            if path.suffix and path.suffix.lower() not in _TEXT_EXTENSIONS:
                continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for chunk in _chunk_text(text, chunk_size=512, overlap=50):
            texts.append(chunk)
            metadatas.append({
                "source": path.name,
                "file_path": str(path),
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
