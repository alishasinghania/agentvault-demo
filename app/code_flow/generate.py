"""LLM generates Python from the user question (llm_output / user-influenced)."""

from app.llm import get_langchain_llm


def generate_code(question: str) -> str:
    llm = get_langchain_llm()
    prompt = (
        "You are a Python coding assistant for Meridian Corp. "
        "Write a short Python snippet that solves the task. "
        "Put the final value in a variable named result. "
        "Return ONLY executable Python code, no markdown.\n\n"
        f"Task: {question}"
    )
    text = llm.invoke(prompt).strip()
    if text.startswith("```"):
        lines = text.split("\n")
        text = "\n".join(lines[1:-1] if lines[-1].strip() == "```" else lines[1:])
    return text.strip()
