"""Hop 2 — glue generate_sql → execute."""

from app.sql_flow.execute import run_generated_sql
from app.sql_flow.generate import generate_sql


def compose_db_answer(question: str) -> str:
    sql = generate_sql(question)
    rows = run_generated_sql(sql)
    return f"Executed SQL:\n{sql}\n\nResults:\n{rows}"
