import streamlit as st
import requests

st.title("🎮 游戏AI Agent")
st.write("专业的游戏AI设计顾问")

if "messages" not in st.session_state:
    st.session_state.messages = []

def call_api(query):
    api_key = st.secrets.get("DEEPSEEK_API_KEY", "")
    if not api_key:
        return "⚠️ 请在 Settings → Secrets 中配置 DEEPSEEK_API_KEY"
    
    messages = [{"role": "system", "content": "你是专业的游戏AI顾问，擅长游戏AI设计和实现"}]
    for m in st.session_state.messages:
        messages.append({"role": m["role"], "content": m["content"]})
    messages.append({"role": "user", "content": query})
    
    try:
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={"model": "deepseek-chat", "messages": messages, "temperature": 0.7},
            timeout=60
        )
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ 调用失败: {str(e)}"

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

prompt = st.chat_input("输入您的游戏AI问题...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            response = call_api(prompt)
            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

if st.sidebar.button("清空对话"):
    st.session_state.messages = []
    st.experimental_rerun()