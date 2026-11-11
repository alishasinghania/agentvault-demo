"""Hop 1 — coding / calculate question entry."""

from app.code_flow.compose import compose_code_answer


def handle_code_question(message: str) -> str:
    return compose_code_answer(message)
