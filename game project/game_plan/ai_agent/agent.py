# ai_agent/agent.py
from .core import get_llm
from .tools import create_knowledge_tool, create_game_rules_tool

class GameAIAgent:
    """游戏AI Agent类"""
    def __init__(self):
        self.llm = get_llm()
        self.knowledge_tool = create_knowledge_tool()
        self.game_rules_tool = create_game_rules_tool()
        self.conversation_history = []
    
    def run(self, query):
        """运行Agent处理查询"""
        try:
            # 1. 使用知识库工具检索信息
            context = self.knowledge_tool.func(query)
            
            # 2. 构建消息，包含对话历史
            messages = [
                {"role": "system", "content": "你是一个专业的游戏AI顾问。请根据以下参考资料回答问题。如果参考资料中没有相关信息，请基于你的知识回答。\n【参考资料】：\n" + context}
            ]
            
            # 3. 添加对话历史
            messages.extend(self.conversation_history)
            
            # 4. 添加当前问题
            messages.append({"role": "user", "content": query})
            
            # 5. 使用LLM生成回答
            response = self.llm(messages)
            
            # 6. 保存对话历史
            self.conversation_history.append({"role": "user", "content": query})
            self.conversation_history.append({"role": "assistant", "content": response})
            
            # 7. 限制对话历史长度（保留最近10轮）
            if len(self.conversation_history) > 20:
                self.conversation_history = self.conversation_history[-20:]
            
            return response
        except Exception as e:
            return f"抱歉，我遇到了一些问题：{str(e)}"
    
    def clear_history(self):
        """清除对话历史"""
        self.conversation_history = []
        return "对话历史已清除"