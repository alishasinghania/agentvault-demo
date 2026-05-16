#!/usr/bin/env python3
"""Populates ChromaDB with the Meridian Corp knowledge base documents."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.config import KNOWLEDGE_BASE_DIR, CHROMA_PERSIST_DIR
from app.rag.ingestor import ingest_directory
from app.rag.vectorstore import get_collection_count


def main():
    print("AgentVault — Knowledge Base Seeder")
    print("=" * 40)

    kb_dir = os.path.abspath(KNOWLEDGE_BASE_DIR)
    if not os.path.isdir(kb_dir):
        print(f"Error: Knowledge base directory not found: {kb_dir}")
        sys.exit(1)

    files = [f for f in os.listdir(kb_dir) if not f.startswith(".")]
    print(f"Found {len(files)} files in {kb_dir}:")
    for f in files:
        print(f"  - {f}")

    print(f"\nChroma persistence directory: {CHROMA_PERSIST_DIR}")
    print("Starting ingestion...")

    chunk_count = ingest_directory(kb_dir)

    total = get_collection_count()
    print(f"\nIngestion complete.")
    print(f"  Chunks added this run : {chunk_count}")
    print(f"  Total vectors in store: {total}")
    print("\nKnowledge base is ready. Start the server with:")
    print("  uvicorn app.main:app --reload")


if __name__ == "__main__":
    main()
