"""Hop 1 — HTTP/user entry. Receives attacker-controlled chat text."""

from app.request_flow.pass_through import forward_user_query


def accept_user_message(message: str, session_id: str = "default") -> str:
    """Pass the raw user message into the next hop (no sanitization)."""
    return forward_user_query(message, session_id)
