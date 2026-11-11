"""Hop 2 — glue generate_code → exec."""

from app.code_flow.execute import run_generated_code
from app.code_flow.generate import generate_code


def compose_code_answer(question: str) -> str:
    code = generate_code(question)
    output = run_generated_code(code)
    return f"Generated code:\n{code}\n\nOutput:\n{output}"
