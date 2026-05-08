import streamlit as st
from game_plan.ai_agent.agent import GameAIAgent
import re

st.set_page_config(
    page_title="游戏AI Agent",
    page_icon="🎮",
    layout="wide"
)

if 'agent' not in st.session_state:
    st.session_state.agent = GameAIAgent()

if 'history' not in st.session_state:
    st.session_state.history = []

def extract_components(response):
    reasoning = ""
    final_answer = ""
    flowchart = ""
    
    reasoning_match = re.search(r'【推理过程】(.*?)【最终回答】', response, re.DOTALL)
    if reasoning_match:
        reasoning = reasoning_match.group(1).strip()
    
    flowchart_match = re.search(r'【流程图】(.*)', response, re.DOTALL)
    if flowchart_match:
        flowchart = flowchart_match.group(1).strip()
    
    if reasoning:
        final_answer_start = response.find("【最终回答】") + 5
        if flowchart_match:
            final_answer_end = response.find("【流程图】")
            final_answer = response[final_answer_start:final_answer_end].strip()
        else:
            final_answer = response[final_answer_start:].strip()
    else:
        if flowchart_match:
            final_answer = response[:response.find("【流程图】")].strip()
        else:
            final_answer = response
    
    return reasoning, final_answer, flowchart

st.sidebar.title("🎮 游戏AI Agent")
st.sidebar.markdown("---")

st.sidebar.subheader("使用说明")
st.sidebar.markdown("1. 在聊天框中输入您的游戏AI相关问题")
st.sidebar.markdown("2. AI Agent会从知识库中检索相关信息")
st.sidebar.markdown("3. 基于检索到的信息生成专业回答")
st.sidebar.markdown("4. 可以继续追问，AI会记住上下文")
st.sidebar.markdown("---")

st.sidebar.subheader("示例问题")
example_questions = [
    "如何设计游戏AI的行为树？",
    "游戏AI路径规划有哪些常用算法？",
    "如何平衡游戏中的AI难度？",
    "如何实现游戏中的AI决策系统？"
]

for q in example_questions:
    if st.sidebar.button(q):
        st.session_state.user_input = q

if st.sidebar.button("🔄 清除对话历史"):
    st.session_state.agent.clear_history()
    st.session_state.history = []
    st.experimental_rerun()

st.title("🎮 游戏AI Agent")
st.markdown("我是一个专业的游戏AI顾问，可以回答您关于游戏AI设计和实现的问题。")
st.markdown("---")

for msg in st.session_state.history:
    if msg['role'] == 'user':
        st.chat_message("user").markdown(msg['content'])
    else:
        with st.chat_message("assistant"):
            reasoning, final_answer, flowchart = extract_components(msg['content'])
            
            if reasoning:
                with st.expander("🧠 查看推理过程"):
                    st.markdown(reasoning)
            
            st.markdown(final_answer)
            
            if flowchart:
                st.markdown("### 📊 流程图")
                st.code(flowchart, language="markdown")
                st.markdown("提示：您可以将上面的Mermaid代码复制到 [Mermaid Live](https://mermaid.live) 中查看可视化图表")

user_input = st.chat_input("输入您的游戏AI问题...")

if user_input:
    st.session_state.history.append({"role": "user", "content": user_input})
    
    with st.chat_message("user"):
        st.markdown(user_input)
    
    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            response = st.session_state.agent.run(user_input)
        
        reasoning, final_answer, flowchart = extract_components(response)
        
        if reasoning:
            with st.expander("🧠 查看推理过程"):
                st.markdown(reasoning)
        
        st.markdown(final_answer)
        
        if flowchart:
            st.markdown("### 📊 流程图")
            st.code(flowchart, language="markdown")
            st.markdown("提示：您可以将上面的Mermaid代码复制到 [Mermaid Live](https://mermaid.live) 中查看可视化图表")
    
    st.session_state.history.append({"role": "assistant", "content": response})