from langchain.chains import RetrievalQA
from langchain_community.llms import Anthropic
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

from app.config import ANTHROPIC_API_KEY, CHROMA_PERSIST_DIR, EMBEDDING_MODEL
from app.rag.vectorstore import similarity_search


class RetrievalChain:
    def __init__(self):
        self.llm = Anthropic(
            anthropic_api_key=ANTHROPIC_API_KEY,
            model="claude-3-haiku-20240307",
            max_tokens_to_sample=1024,
        )

    def query(self, user_query: str) -> str:
        docs = similarity_search(user_query)

        context = "\n".join([d["page_content"] for d in docs])

        prompt = f"Context:\n{context}\n\nQuestion: {user_query}\n\nAnswer:"

        response = self.llm(prompt)
        return response

    def query_with_sources(self, user_query: str) -> dict:
        docs = similarity_search(user_query)

        context = "\n".join([d["page_content"] for d in docs])
        prompt = f"Context:\n{context}\n\nQuestion: {user_query}\n\nAnswer:"
        response = self.llm(prompt)

        sources = list({d["metadata"].get("source", "unknown") for d in docs})

        return {
            "answer": response,
            "sources": sources,
        }
