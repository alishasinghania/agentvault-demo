from langchain.memory import ConversationBufferMemory
from typing import List, Dict


class MemoryAgent:
    def __init__(self):
        self.sessions: Dict[str, ConversationBufferMemory] = {}

    def get_memory(self, session_id: str) -> ConversationBufferMemory:
        if session_id not in self.sessions:
            self.sessions[session_id] = ConversationBufferMemory(
                return_messages=True,
                memory_key="history",
            )
        return self.sessions[session_id]

    def add_exchange(self, session_id: str, human_message: str, ai_message: str):
        memory = self.get_memory(session_id)
        memory.chat_memory.add_user_message(human_message)
        memory.chat_memory.add_ai_message(ai_message)

    def get_history(self, session_id: str) -> List[Dict]:
        memory = self.get_memory(session_id)
        messages = memory.chat_memory.messages
        history = []
        for msg in messages:
            role = "user" if msg.type == "human" else "assistant"
            history.append({"role": role, "content": msg.content})
        return history

    def get_langchain_history(self, session_id: str) -> List[Dict]:
        history = self.get_history(session_id)
        formatted = []
        for msg in history:
            formatted.append({"role": msg["role"], "content": msg["content"]})
        return formatted

    def clear(self, session_id: str):
        if session_id in self.sessions:
            self.sessions[session_id].clear()

    def clear_all(self):
        self.sessions.clear()
