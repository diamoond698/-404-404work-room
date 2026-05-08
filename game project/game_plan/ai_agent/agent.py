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
    
    def run(self, query, include_flowchart=True, include_reasoning=True):
        """运行Agent处理查询"""
        try:
            context = self.knowledge_tool.func(query)
            has_context = len(context.strip()) > 0
            
            messages = [
                {"role": "system", "content": "你是一个专业的游戏AI顾问。请根据以下参考资料回答问题。如果参考资料中没有相关信息，请基于你的知识回答。\n【参考资料】：\n" + context}
            ]
            
            messages.extend(self.conversation_history)
            messages.append({"role": "user", "content": query})
            
            reasoning = ""
            if include_reasoning:
                reasoning = self.generate_reasoning(query, context)
            
            response = self.llm(messages)
            
            flowchart = ""
            if include_flowchart:
                flowchart = self.generate_flowchart(query, response)
            
            full_response = response
            if reasoning:
                full_response = f"【推理过程】\n{reasoning}\n\n【最终回答】\n{response}"
            if flowchart:
                full_response = f"{full_response}\n\n【流程图】\n{flowchart}"
            
            self.conversation_history.append({"role": "user", "content": query})
            self.conversation_history.append({"role": "assistant", "content": full_response})
            
            if len(self.conversation_history) > 20:
                self.conversation_history = self.conversation_history[-20:]
            
            return full_response
        except Exception as e:
            return f"抱歉，我遇到了一些问题：{str(e)}"
    
    def generate_reasoning(self, query, context):
        """生成推理过程"""
        try:
            reasoning_prompt = f"""请模拟一个游戏AI顾问的思考过程，详细描述你是如何分析问题并得出答案的。

问题：{query}

参考资料：{context[:500] if context else "无"}

请按照以下结构输出推理过程：
1. 问题分析：分析用户的问题意图和核心需求
2. 信息检索：从知识库中检索到的相关信息
3. 推理步骤：一步步推导答案的过程
4. 结论形成：最终答案的形成逻辑

请用中文详细描述，语言要自然，像真实的思考过程："""
            
            messages = [{"role": "user", "content": reasoning_prompt}]
            reasoning = self.llm(messages)
            
            if reasoning:
                return reasoning
            else:
                return ""
        except Exception as e:
            print(f"生成推理过程失败: {str(e)}")
            return ""
    
    def generate_flowchart(self, query, response):
        """为回答生成流程图（Mermaid格式）"""
        try:
            flowchart_prompt = f"""请为以下问答生成一个Mermaid格式的流程图。

问题：{query}

回答：{response}

要求：
1. 使用Mermaid的flowchart语法
2. 流程图应清晰展示回答中的核心逻辑或步骤
3. 使用简洁的节点标签
4. 只输出Mermaid代码，不要有其他解释文字

示例格式：
```mermaid
flowchart TD
    A[开始] --> B[步骤1]
    B --> C[步骤2]
    C --> D[结束]
```

请输出Mermaid代码："""
            
            messages = [{"role": "user", "content": flowchart_prompt}]
            flowchart = self.llm(messages)
            
            if flowchart and ("mermaid" in flowchart or "flowchart" in flowchart):
                return flowchart
            else:
                return ""
        except Exception as e:
            print(f"生成流程图失败: {str(e)}")
            return ""
    
    def clear_history(self):
        """清除对话历史"""
        self.conversation_history = []
        return "对话历史已清除"
    
    def regenerate_response(self):
        """重新生成上一个回答"""
        try:
            if len(self.conversation_history) < 2:
                return "没有可重新生成的回答"
            
            last_user_message = self.conversation_history[-2]
            query = last_user_message["content"]
            
            context = self.knowledge_tool.func(query)
            
            messages = [
                {"role": "system", "content": "你是一个专业的游戏AI顾问。请根据以下参考资料回答问题。如果参考资料中没有相关信息，请基于你的知识回答。\n【参考资料】：\n" + context}
            ]
            
            messages.extend(self.conversation_history[:-1])
            
            new_response = self.llm(messages)
            
            self.conversation_history[-1] = {"role": "assistant", "content": new_response}
            
            return new_response
        except Exception as e:
            return f"抱歉，重新生成回答时遇到了一些问题：{str(e)}"