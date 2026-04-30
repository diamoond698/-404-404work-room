# ai_agent/agent.py
from langchain.agents import AgentType, initialize_agent
from langchain.memory import ConversationBufferMemory
from .core import get_llm
from .tools import create_knowledge_tool, create_game_rules_tool

class GameAIAgent:
    """游戏AI Agent类"""
    def __init__(self):
        self.llm = get_llm()
        self.tools = [
            create_knowledge_tool(),
            create_game_rules_tool()
        ]
        self.memory = ConversationBufferMemory(memory_key="chat_history")
        self.agent = self._initialize_agent()
    
    def _initialize_agent(self):
        """初始化Agent"""
        return initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            memory=self.memory,
            verbose=True
        )
    
    def run(self, query):
        """运行Agent处理查询"""
        try:
            response = self.agent.run(query)
            return response
        except Exception as e:
            return f"抱歉，我遇到了一些问题：{str(e)}"