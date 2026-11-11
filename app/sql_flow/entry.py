"""Hop 1 — database question entry."""

from app.sql_flow.compose import compose_db_answer


def handle_db_question(message: str) -> str:
    return compose_db_answer(message)
