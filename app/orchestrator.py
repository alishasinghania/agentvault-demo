import asyncio
from typing import Dict, Any, List, Optional

from app.agents.primary_agent import PrimaryAgent
from app.agents.code_agent import CodeAgent
from app.agents.research_crew import run_research
from app.agents.memory_agent import MemoryAgent
from app.rag.retrieval_chain import RetrievalChain
from app.tools.utils import quick_classify
from app.tools.database_tool import execute_query


class AgentOrchestrator:
    def __init__(self):
        self.primary_agent = PrimaryAgent()
        self.code_agent = CodeAgent()
        self.memory_agent = MemoryAgent()
        self.retrieval_chain = RetrievalChain()

    async def run(self, user_message: str, session_id: str = "default") -> str:
        intent = quick_classify(user_message)

        history = self.memory_agent.get_langchain_history(session_id)

        if intent == "code_execution":
            response = await asyncio.to_thread(self.code_agent.run, user_message)

        elif intent == "research":
            response = await asyncio.to_thread(
                run_research,
                user_message,
                self.primary_agent.run,
            )

        elif intent == "rag_query":
            rag_response = await asyncio.to_thread(
                self.retrieval_chain.query_with_sources,
                user_message,
            )
            messages = history + [{"role": "user", "content": user_message}]
            response = await asyncio.to_thread(
                self.primary_agent.run,
                messages,
                rag_response.get("answer", ""),
            )

        elif intent == "database_query":
            db_result = await asyncio.to_thread(execute_query, user_message)
            messages = history + [{"role": "user", "content": user_message}]
            response = await asyncio.to_thread(
                self.primary_agent.run,
                messages,
                f"Database tool result:\n{db_result}",
            )

        elif intent == "email":
            # Demo path: ask the model to draft fields, then attempt send
            messages = history + [{"role": "user", "content": user_message}]
            draft = await asyncio.to_thread(
                self.primary_agent.run,
                messages,
                (
                    "The user wants an email sent. Reply with a short confirmation of what "
                    "you would send (to, subject, body). If details are missing, ask for them."
                ),
            )
            response = draft

        else:
            rag_context = await asyncio.to_thread(
                self.retrieval_chain.query,
                user_message,
            )
            messages = history + [{"role": "user", "content": user_message}]
            response = await asyncio.to_thread(
                self.primary_agent.run,
                messages,
                rag_context,
            )

        self.memory_agent.add_exchange(session_id, user_message, response)
        return response

    def get_history(self, session_id: str) -> List[Dict]:
        return self.memory_agent.get_history(session_id)

    def clear_session(self, session_id: str):
        self.memory_agent.clear(session_id)
