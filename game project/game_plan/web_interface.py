# game_plan/web_interface.py
import streamlit as st
from ai_agent.agent import GameAIAgent
import pyperclip
import re

def extract_components(response):
    """从回答中提取推理过程、最终回答和流程图"""
    reasoning = ""
    answer = response
    flowchart = ""
    
    if "【推理过程】" in response and "【最终回答】" in response:
        parts = response.split("【推理过程】")
        rest = parts[1]
        
        if "【最终回答】" in rest:
            reasoning_parts = rest.split("【最终回答】")
            reasoning = reasoning_parts[0].strip()
            answer_part = reasoning_parts[1].strip()
            
            if "【流程图】" in answer_part:
                answer_parts = answer_part.split("【流程图】")
                answer = answer_parts[0].strip()
                flowchart = answer_parts[1].strip() if len(answer_parts) > 1 else ""
            else:
                answer = answer_part
    
    elif "【流程图】" in response:
        parts = response.split("【流程图】")
        answer = parts[0].strip()
        flowchart = parts[1].strip() if len(parts) > 1 else ""
    
    return reasoning, answer, flowchart

def render_flowchart(flowchart_code):
    """渲染流程图"""
    if flowchart_code:
        st.subheader("📊 流程图")
        st.code(flowchart_code, language="markdown")
        st.info("💡 您可以复制上面的Mermaid代码到 [Mermaid Live](https://mermaid.live) 查看可视化图表")

def render_reasoning(reasoning):
    """渲染推理过程"""
    if reasoning:
        with st.expander("🧠 查看推理过程", expanded=False):
            st.markdown(reasoning)

def main():
    st.set_page_config(
        page_title="游戏AI Agent",
        page_icon="🎮",
        layout="wide"
    )
    
    st.title("🎮 游戏AI Agent")
    st.write("我是一个专业的游戏AI顾问，可以回答你关于游戏AI设计和实现的问题。")
    st.write("---")
    
    if "agent" not in st.session_state:
        st.session_state.agent = GameAIAgent()
        st.success("游戏AI Agent 初始化成功！")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "last_response" not in st.session_state:
        st.session_state.last_response = ""
    
    with st.sidebar:
        st.header("功能")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ 清除历史"):
                st.session_state.agent.clear_history()
                st.session_state.messages = []
                st.session_state.last_response = ""
                st.success("对话历史已清除！")
        
        st.header("使用说明")
        st.write("1. 在聊天框中输入游戏AI相关问题")
        st.write("2. AI会从知识库检索相关信息")
        st.write("3. 自动生成专业回答和流程图")
        st.write("4. 支持复制回答和重新生成")
        
        st.header("示例问题")
        examples = [
            "如何设计游戏AI的行为树？",
            "游戏AI路径规划有哪些常用算法？",
            "如何平衡游戏中的AI难度？",
            "如何实现游戏中的AI决策系统？"
        ]
        for example in examples:
            if st.button(f"❓ {example}"):
                st.session_state.messages.append({"role": "user", "content": example})
                with st.spinner("AI 正在思考..."):
                    response = st.session_state.agent.run(example)
                    st.session_state.last_response = response
                    st.session_state.messages.append({"role": "assistant", "content": response})
                st.experimental_rerun()
    
    for i, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            if message["role"] == "assistant":
                reasoning, answer, flowchart = extract_components(message["content"])
                st.markdown(answer)
                
                render_reasoning(reasoning)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📋 复制回答", key=f"copy_{i}"):
                        pyperclip.copy(answer)
                        st.success("✅ 已复制到剪贴板！")
                with col2:
                    if st.button("🔄 重新生成", key=f"regenerate_{i}"):
                        if i > 0 and st.session_state.messages[i-1]["role"] == "user":
                            user_query = st.session_state.messages[i-1]["content"]
                            with st.spinner("AI 正在重新生成..."):
                                new_response = st.session_state.agent.regenerate_response()
                                st.session_state.messages[i] = {"role": "assistant", "content": new_response}
                                st.session_state.last_response = new_response
                            st.experimental_rerun()
                
                if flowchart:
                    render_flowchart(flowchart)
            else:
                st.markdown(message["content"])
    
    if prompt := st.chat_input("输入你的游戏AI问题..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("AI 正在思考..."):
                response = st.session_state.agent.run(prompt)
                st.session_state.last_response = response
                reasoning, answer, flowchart = extract_components(response)
                st.markdown(answer)
                
                render_reasoning(reasoning)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📋 复制回答", key="copy_last"):
                        pyperclip.copy(answer)
                        st.success("✅ 已复制到剪贴板！")
                with col2:
                    if st.button("🔄 重新生成", key="regenerate_last"):
                        with st.spinner("AI 正在重新生成..."):
                            new_response = st.session_state.agent.regenerate_response()
                            st.session_state.messages[-1] = {"role": "assistant", "content": new_response}
                            st.session_state.last_response = new_response
                        st.experimental_rerun()
                
                if flowchart:
                    render_flowchart(flowchart)
        
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()