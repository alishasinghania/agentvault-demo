from langchain.agents import initialize_agent, AgentType
from langchain_experimental.tools import PythonREPLTool
from langchain.memory import ConversationBufferMemory

from app.llm import get_langchain_llm


class CodeAgent:
    def __init__(self):
        self.llm = get_langchain_llm()
        self.tools = [PythonREPLTool()]
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
        )
        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            memory=self.memory,
            verbose=False,
            handle_parsing_errors=True,
        )

    def run(self, user_input: str) -> str:
        result = self.agent.run(
            f"You are a helpful Python coding assistant for Meridian Corp employees. "
            f"Help with the following task, using Python to compute or demonstrate as needed:\n\n{user_input}"
        )
        return result
