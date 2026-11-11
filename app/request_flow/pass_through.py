"""Hop 2 — route to multi-flow handlers (LLM / SQL / RCE / email)."""

from app.code_flow.entry import handle_code_question
from app.email_flow.entry import handle_email_request
from app.request_flow.llm_sink import answer_with_context
from app.sql_flow.entry import handle_db_question
from app.tools.utils import quick_classify


def forward_user_query(value: str, session_id: str = "default") -> str:
    """Fan out tainted user text into separate multi-hop sinks by intent."""
    intent = quick_classify(value)

    if intent == "code_execution":
        return handle_code_question(value)

    if intent == "database_query":
        return handle_db_question(value)

    if intent == "email":
        return handle_email_request(value)

    # Default / RAG / research-style questions → LLM sink chain
    return answer_with_context(value, session_id)
