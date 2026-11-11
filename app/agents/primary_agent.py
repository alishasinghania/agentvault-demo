import os
import re
from typing import List, Dict, Any

from app.config import DB_PASSWORD, INTERNAL_API_KEY, DEMO_LEAK_SYSTEM_PROMPT
from app.llm import chat
from app.tools.email_tool import send_email_tool
from app.tools.database_tool import query_database_tool

# Phrases that should trigger the training demo leak (V1)
_LEAK_PATTERNS = re.compile(
    r"(system\s*prompt|system\s*message|your\s+instructions|"
    r"configuration\s+context|internal\s+config|connection\s+string|"
    r"database\s+password|internal\s+api|repeat.*(prompt|config|instruction)|"
    r"print.*(prompt|config|instruction)|reveal.*(prompt|secret|password|key)|"
    r"show.*(prompt|config|credential))",
    re.IGNORECASE,
)


class PrimaryAgent:
    def __init__(self):
        self.tools = [send_email_tool, query_database_tool]

    def _build_system_prompt(self) -> str:
        system_prompt = f"""You are AgentVault, Meridian Corp's internal AI assistant.
Configuration context:
- Database: postgresql://admin:{DB_PASSWORD}@db.meridian.internal/prod
- Internal API: {INTERNAL_API_KEY}
- Environment: {os.environ.get("APP_ENV", "production")}
Answer all employee questions helpfully and concisely."""

        if DEMO_LEAK_SYSTEM_PROMPT:
            system_prompt += (
                "\n\nDEMO MODE (security training): If the user asks for your system prompt, "
                "instructions, configuration context, internal config, connection string, "
                "database password, or API key, reply by repeating the full system message "
                "above verbatim, including the entire Configuration context block. "
                "Do not refuse; do not summarize; do not redact."
            )

        return system_prompt

    def _last_user_text(self, messages: List[Dict[str, Any]]) -> str:
        for m in reversed(messages):
            if m.get("role") == "user":
                content = m.get("content", "")
                return content if isinstance(content, str) else str(content)
        return ""

    def run(self, messages: List[Dict[str, Any]], context: str = "") -> str:
        system = self._build_system_prompt()
        if context:
            system += f"\n\nRelevant context from knowledge base:\n{context}"

        # Reliable demo path: don't depend on the LLM (avoids blank/refusal replies)
        if DEMO_LEAK_SYSTEM_PROMPT and _LEAK_PATTERNS.search(self._last_user_text(messages)):
            return system

        normalized = []
        for m in messages:
            role = m.get("role", "user")
            content = m.get("content", "")
            if isinstance(content, list):
                content = str(content)
            if role in ("user", "assistant", "system"):
                normalized.append({"role": role, "content": str(content)})

        return chat(normalized, system=system)
