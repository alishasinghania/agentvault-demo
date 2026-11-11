"""Multi-hop code path — user text → generate_code → exec (FLOW-RCE)."""

from app.code_flow.entry import handle_code_question

__all__ = ["handle_code_question"]
