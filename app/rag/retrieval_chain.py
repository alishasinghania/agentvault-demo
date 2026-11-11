from app.llm import get_langchain_llm
from app.rag.vectorstore import similarity_search


class RetrievalChain:
    def __init__(self):
        self.llm = get_langchain_llm()

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
