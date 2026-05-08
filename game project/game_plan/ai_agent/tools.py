# ai_agent/tools.py
def create_knowledge_tool():
    """创建知识库检索工具"""
    class KnowledgeTool:
        func = staticmethod(lambda query: "")
    
    return KnowledgeTool()

def create_game_rules_tool():
    """创建游戏规则查询工具"""
    class GameRulesTool:
        func = staticmethod(lambda topic: "")
    
    return GameRulesTool()