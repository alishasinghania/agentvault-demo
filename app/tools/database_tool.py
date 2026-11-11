from typing import Any, Dict

from app.sql_flow.entry import handle_db_question


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


def execute_query(natural_language_query: str) -> Dict[str, Any]:
    """Delegate to multi-hop sql_flow (generate_sql → cursor.execute)."""
    text = handle_db_question(natural_language_query)
    return {
        "status": "success",
        "summary": text,
    }
