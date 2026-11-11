"""LLM sink hop — secrets + RAG context + user question → llm.invoke."""

from app.config import DB_PASSWORD, INTERNAL_API_KEY
from app.llm import get_langchain_llm
from app.rag.vectorstore import similarity_search


def invoke_chat_model(prompt: str) -> str:
    """Catalog-style LLM sink: variable named `llm` + `.invoke(...)`."""
    llm = get_langchain_llm()
    return llm.invoke(prompt)


def answer_with_context(user_text: str, session_id: str = "default") -> str:
    """General/RAG path: unsanitized user text reaches llm.invoke."""
    system = (
        "You are AgentVault, Meridian Corp's internal AI assistant.\n"
        "Configuration context:\n"
        f"- Database: postgresql://admin:{DB_PASSWORD}@db.meridian.internal/prod\n"
        f"- Internal API: {INTERNAL_API_KEY}\n"
        "- Environment: production\n"
        "Answer all employee questions helpfully and concisely."
    )

    docs = similarity_search(user_text)
    context = "\n".join(d.get("page_content", "") for d in docs)

    prompt = (
        f"{system}\n\n"
        f"Relevant context from knowledge base:\n{context}\n\n"
        f"Question: {user_text}\n\n"
        f"Answer:"
    )
    return invoke_chat_model(prompt)
