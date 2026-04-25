# game_plan/web_interface.py
import streamlit as st
from ai_agent.agent import GameAIAgent

def main():
    # 设置页面标题和图标
    st.set_page_config(
        page_title="游戏AI Agent",
        page_icon="🎮",
        layout="wide"
    )
    
    # 页面标题和介绍
    st.title("🎮 游戏AI Agent")
    st.write("我是一个专业的游戏AI顾问，可以回答你关于游戏AI设计和实现的问题。")
    st.write("---")
    
    # 初始化Agent
    if "agent" not in st.session_state:
        st.session_state.agent = GameAIAgent()
        st.success("游戏AI Agent 初始化成功！")
    
    # 聊天历史
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # 侧边栏
    with st.sidebar:
        st.header("功能")
        if st.button("🗑️ 清除对话历史"):
            st.session_state.agent.clear_history()
            st.session_state.messages = []
            st.success("对话历史已清除！")
        
        st.header("使用说明")
        st.write("1. 在聊天框中输入你的游戏AI相关问题")
        st.write("2. AI Agent 会从知识库中检索相关信息")
        st.write("3. 基于检索到的信息生成专业回答")
        st.write("4. 可以继续追问，AI 会记住上下文")
        
        st.header("示例问题")
        st.write("- 如何设计游戏AI的行为树？")
        st.write("- 游戏AI路径规划有哪些常用算法？")
        st.write("- 如何平衡游戏中的AI难度？")
        st.write("- 如何实现游戏中的AI决策系统？")
    
    # 显示聊天历史
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # 用户输入
    if prompt := st.chat_input("输入你的游戏AI问题..."):
        # 添加用户消息
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # 生成Agent回复
        with st.chat_message("assistant"):
            with st.spinner("AI 正在思考..."):
                response = st.session_state.agent.run(prompt)
                st.markdown(response)
        
        # 添加Agent消息
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()