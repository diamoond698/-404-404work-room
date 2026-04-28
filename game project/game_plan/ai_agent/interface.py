# ai_agent/interface.py
from .agent import GameAIAgent
import pyperclip

def print_response(response):
    """格式化打印回答，分离文本和流程图"""
    if "【流程图】" in response:
        parts = response.split("【流程图】")
        text_part = parts[0].strip()
        flowchart_part = parts[1].strip() if len(parts) > 1 else ""
        
        print("Agent:")
        print(text_part)
        
        if flowchart_part:
            print("\n" + "="*60)
            print("流程图（Mermaid格式）:")
            print("="*60)
            print(flowchart_part)
            print("="*60)
            print("\n提示：您可以将上面的Mermaid代码复制到Mermaid在线编辑器中查看可视化图表")
            print("推荐工具：https://mermaid.live")
    else:
        print(f"Agent: {response}")

def run_chat_interface():
    """运行聊天界面"""
    agent = GameAIAgent()
    print("=== 游戏AI Agent ===")
    print("我是一个专业的游戏AI顾问，可以回答你关于游戏AI设计和实现的问题。")
    print("输入'清除历史'清空对话记录，输入'复制'复制上一个回答，输入'重新生成'重新生成上一个回答，输入'退出'结束对话")
    print("每次回答都会自动生成流程图，您可以复制Mermaid代码到可视化工具中查看\n")
    
    last_response = ""
    
    while True:
        user_input = input("你: ")
        
        if user_input == "退出":
            print("再见！")
            break
        elif user_input == "清除历史":
            response = agent.clear_history()
            last_response = ""
            print(f"Agent: {response}\n")
            continue
        elif user_input == "复制":
            if last_response:
                pyperclip.copy(last_response)
                print("Agent: 上一个回答已复制到剪贴板\n")
            else:
                print("Agent: 没有可复制的回答\n")
            continue
        elif user_input == "重新生成":
            print("Agent: 正在重新生成回答...")
            response = agent.regenerate_response()
            last_response = response
            print_response(response)
            print("\n")
            continue
        
        print("Agent: 正在思考...")
        response = agent.run(user_input)
        last_response = response
        print_response(response)
        print("\n")