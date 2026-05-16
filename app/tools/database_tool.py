import sqlite3
import anthropic
from typing import Any, Dict, List

from app.config import DATABASE_PATH, ANTHROPIC_API_KEY, DB_PASSWORD


query_database_tool = {
    "name": "query_database",
    "description": (
        "Query the Meridian Corp employee and project database using natural language. "
        "Translates your question into SQL and returns the results. "
        "Use this to look up employee records, project information, or any company data."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Natural language description of what data you want to retrieve",
            }
        },
        "required": ["query"],
    },
}


def _nl_to_sql(natural_language_query: str) -> str:
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=256,
        system=(
            "You are a SQL expert for Meridian Corp's SQLite database. "
            "Tables: employees(id, name, email, department, salary, hire_date), "
            "projects(id, name, budget, lead_id, status), "
            "assignments(employee_id, project_id, role). "
            "Convert the user's natural language query to a single SQL statement. "
            "Return ONLY the SQL, no explanation."
        ),
        messages=[{"role": "user", "content": natural_language_query}],
    )
    return response.content[0].text.strip()


def execute_query(natural_language_query: str) -> Dict[str, Any]:
    sql = _nl_to_sql(natural_language_query)

    try:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.close()

        results = [dict(row) for row in rows]
        return {
            "status": "success",
            "query": sql,
            "row_count": len(results),
            "results": results,
        }
    except sqlite3.Error as e:
        return {
            "status": "error",
            "query": sql,
            "error": str(e),
        }
