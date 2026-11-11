"""Multi-hop DB path — user/LLM text → generate_sql → cursor.execute (FLOW-SQL)."""

from app.sql_flow.entry import handle_db_question

__all__ = ["handle_db_question"]
