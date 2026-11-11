"""Hop 3 — RCE sink: model-generated code passed to exec()."""

from typing import Any


def run_generated_code(code: str) -> Any:
    """Intentionally unsafe: LLM-generated code → exec."""
    namespace: dict = {}
    exec(code, namespace)
    if "result" in namespace:
        return namespace["result"]
    return "executed"
