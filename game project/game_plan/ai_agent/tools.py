# ai_agent/tools.py
from langchain_core.tools import Tool
from .core import get_vectorstore

def create_knowledge_tool():
    """创建知识库检索工具"""
    vectorstore = get_vectorstore()
    
    def retrieve_knowledge(query):
        """从知识库中检索相关信息"""
        docs = vectorstore.similarity_search(query, k=3)
        result = "\n\n".join([f"文档 {i+1}：{doc.page_content[:200]}..." for i, doc in enumerate(docs)])
        return result
    
    return Tool(
        name="KnowledgeRetriever",
        func=retrieve_knowledge,
        description="从游戏AI知识库中检索相关信息，用于回答游戏AI相关问题"
    )

def create_game_rules_tool():
    """创建游戏规则查询工具"""
    def get_game_rules(topic):
        """获取游戏规则相关信息"""
        rules = {
            "AI决策": "游戏AI决策通常基于状态评估、行为树或强化学习等方法。",
            "路径规划": "游戏AI路径规划常用A*算法、导航网格等技术。",
            "行为树": "行为树是一种模块化的AI决策结构，由序列、选择、装饰器等节点组成。"
        }
        return rules.get(topic, f"未找到关于{topic}的规则信息")
    
    return Tool(
        name="GameRules",
        func=get_game_rules,
        description="获取游戏规则和AI设计相关的基本信息"
    )