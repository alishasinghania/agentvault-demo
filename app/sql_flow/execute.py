"""Hop 3 — SQL sink: generated SQL executed without parameterization."""

import sqlite3
from typing import Any, List

from app.config import DATABASE_PATH


def run_generated_sql(sql: str) -> List[Any]:
    """Intentionally unsafe: LLM/user-derived SQL string → cursor.execute."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows
