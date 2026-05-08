import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="游戏AI Agent", page_icon="🎮")

def call_deepseek(messages):
    api_key = os.getenv("DEEPSEEK_API_KEY") or st.secrets.get("DEEPSEEK_API_KEY", "")
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

st.title("🎮 游戏AI Agent")
st.markdown("我是一个专业的游戏AI顾问，可以回答您关于游戏AI设计和实现的问题。")
st.markdown("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("输入您的游戏AI问题..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            messages = [
                {"role": "system", "content": "你是一个专业的游戏AI顾问，擅长回答关于游戏AI设计和实现的问题。"}
            ] + st.session_state.messages[:-1]
            
            response = call_deepseek(messages)
        
        st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})

if st.sidebar.button("清除对话历史"):
    st.session_state.messages = []
    st.experimental_rerun()