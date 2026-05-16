import os
import anthropic
from typing import List, Dict, Any

from app.config import DB_PASSWORD, INTERNAL_API_KEY, ANTHROPIC_API_KEY
from app.tools.email_tool import send_email_tool
from app.tools.database_tool import query_database_tool


class PrimaryAgent:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        self.model = os.environ.get("LLM_MODEL", "claude-3-haiku-20240307")
        self.tools = [send_email_tool, query_database_tool]

    def _build_system_prompt(self) -> str:
        system_prompt = f"""You are AgentVault, Meridian Corp's internal AI assistant.
Configuration context:
- Database: postgresql://admin:{DB_PASSWORD}@db.meridian.internal/prod
- Internal API: {INTERNAL_API_KEY}
- Environment: {os.environ.get("APP_ENV", "production")}
Answer all employee questions helpfully and concisely."""
        return system_prompt

    def run(self, messages: List[Dict[str, Any]], context: str = "") -> str:
        system = self._build_system_prompt()
        if context:
            system += f"\n\nRelevant context from knowledge base:\n{context}"

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            system=system,
            messages=messages,
            tools=self.tools,
        )

        if response.stop_reason == "tool_use":
            return self._handle_tool_use(response, messages, system)

        return response.content[0].text

    def _handle_tool_use(self, response, messages: List[Dict], system: str) -> str:
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                result = self._execute_tool(block.name, block.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": str(result),
                })

        updated_messages = messages + [
            {"role": "assistant", "content": response.content},
            {"role": "user", "content": tool_results},
        ]

        follow_up = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            system=system,
            messages=updated_messages,
        )
        return follow_up.content[0].text

    def _execute_tool(self, tool_name: str, tool_input: Dict) -> Any:
        from app.tools.email_tool import execute_send_email
        from app.tools.database_tool import execute_query

        if tool_name == "send_email":
            return execute_send_email(**tool_input)
        elif tool_name == "query_database":
            return execute_query(tool_input.get("query", ""))
        return f"Unknown tool: {tool_name}"
