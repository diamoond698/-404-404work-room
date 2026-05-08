import streamlit as st
import requests
import os
import re
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="游戏AI Agent",
    page_icon="🎮",
    layout="wide"
)

def call_deepseek(messages):
    api_key = os.getenv("DEEPSEEK_API_KEY") or st.secrets.get("DEEPSEEK_API_KEY")
    if not api_key:
        return "错误：请设置 DEEPSEEK_API_KEY"
    
    try:
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "deepseek-chat",
                "messages": messages,
                "temperature": 0.7
            },
            timeout=60
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"LLM调用失败：{str(e)}"

def generate_response(query, conversation_history, include_flowchart=True, include_reasoning=True):
    messages = [
        {"role": "system", "content": "你是一个专业的游戏AI顾问，擅长回答关于游戏AI设计和实现的问题。"}
    ]
    
    messages.extend(conversation_history)
    messages.append({"role": "user", "content": query})
    
    reasoning = ""
    if include_reasoning:
        reasoning_prompt = f"""请模拟一个游戏AI顾问的思考过程，详细描述你是如何分析问题并得出答案的。

问题：{query}

请按照以下结构输出推理过程：
1. 问题分析：分析用户的问题意图和核心需求
2. 信息检索：从知识库中检索到的相关信息
3. 推理步骤：一步步推导答案的过程
4. 结论形成：最终答案的形成逻辑

请用中文详细描述，语言要自然，像真实的思考过程："""
        
        reasoning = call_deepseek([{"role": "user", "content": reasoning_prompt}])
    
    response = call_deepseek(messages)
    
    flowchart = ""
    if include_flowchart:
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
        
        flowchart = call_deepseek([{"role": "user", "content": flowchart_prompt}])
    
    full_response = response
    if reasoning:
        full_response = f"【推理过程】\n{reasoning}\n\n【最终回答】\n{response}"
    if flowchart and ("mermaid" in flowchart or "flowchart" in flowchart):
        full_response = f"{full_response}\n\n【流程图】\n{flowchart}"
    
    return full_response

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

if 'history' not in st.session_state:
    st.session_state.history = []

st.sidebar.title("🎮 游戏AI Agent")
st.sidebar.markdown("---")

st.sidebar.subheader("使用说明")
st.sidebar.markdown("1. 在聊天框中输入您的游戏AI相关问题")
st.sidebar.markdown("2. AI会生成专业回答")
st.sidebar.markdown("3. 可以继续追问，AI会记住上下文")
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
            conversation_history = [
                {"role": m['role'], "content": m['content']} 
                for m in st.session_state.history[:-1]
            ]
            response = generate_response(user_input, conversation_history)
        
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