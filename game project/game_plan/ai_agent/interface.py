# ai_agent/interface.py
from .agent import GameAIAgent

def run_chat_interface():
    """运行聊天界面"""
    agent = GameAIAgent()
    print("=== 游戏AI Agent ===")
    print("我是一个专业的游戏AI顾问，可以回答你关于游戏AI设计和实现的问题。")
    print("输入'清除历史'清空对话记录，输入'退出'结束对话\n")
    
    while True:
        user_input = input("你: ")
        
        if user_input == "退出":
            print("再见！")
            break
        elif user_input == "清除历史":
            response = agent.clear_history()
            print(f"Agent: {response}\n")
            continue
        
        print("Agent: 正在思考...")
        response = agent.run(user_input)
        print(f"Agent: {response}\n")