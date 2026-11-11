"""LLM generates SQL from natural language (llm_output source for FLOW-SQL)."""

from app.llm import get_langchain_llm


def generate_sql(question: str) -> str:
    llm = get_langchain_llm()
    prompt = (
        "You are a SQL expert for Meridian Corp's SQLite database. "
        "Tables: employees(id, name, email, department, salary, hire_date), "
        "projects(id, name, budget, lead_id, status), "
        "assignments(employee_id, project_id, role). "
        "Convert the user's natural language query to a single SQL statement. "
        "Return ONLY the SQL, no explanation.\n\n"
        f"Question: {question}"
    )
    text = llm.invoke(prompt).strip()
    if text.startswith("```"):
        lines = text.split("\n")
        text = "\n".join(lines[1:-1] if lines[-1].strip() == "```" else lines[1:])
    return text.strip()
