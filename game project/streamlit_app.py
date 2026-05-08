import streamlit as st
import requests

st.set_page_config(
    page_title="游戏AI Agent - Web Inference",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .response-box {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #1f77b4;
    }
    .user-msg {
        background-color: #e3f2fd;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .assistant-msg {
        background-color: #f5f5f5;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

def call_deepseek_api(messages, temperature=0.7, max_tokens=2000):
    api_key = st.secrets.get("DEEPSEEK_API_KEY", "")
    if not api_key:
        return "错误：请在 Settings → Secrets 中配置 DEEPSEEK_API_KEY"
    
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
                "temperature": temperature,
                "max_tokens": max_tokens
            },
            timeout=90
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"API调用失败：{str(e)}"

st.markdown('<h1 class="main-header">🤖 游戏AI Agent - Web Inference</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">专业的游戏AI设计顾问，为您提供AI设计建议和实现方案</p>', unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("对话")
    
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []
    
    for msg in st.session_state.conversation_history:
        if msg["role"] == "user":
            st.markdown(f'<div class="user-msg">👤 {msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="assistant-msg">🤖 {msg["content"]}</div>', unsafe_allow_html=True)
    
    user_input = st.text_area(
        "输入您的问题...",
        height=100,
        placeholder="例如：如何设计游戏AI的行为树？"
    )

with col2:
    st.subheader("设置")
    
    temperature = st.slider(
        "Temperature (创意度)",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1
    )
    
    max_tokens = st.number_input(
        "Max Tokens (最大输出长度)",
        min_value=100,
        max_value=4000,
        value=2000,
        step=100
    )
    
    st.markdown("---")
    
    system_prompt = st.text_area(
        "System Prompt (系统提示)",
        value="你是一个专业的游戏AI顾问，擅长回答关于游戏AI设计和实现的问题，包括行为树、状态机、路径规划、难度平衡等主题。",
        height=100
    )
    
    st.markdown("---")
    
    col_clear, col_new = st.columns(2)
    with col_clear:
        if st.button("🗑️ 清空对话"):
            st.session_state.conversation_history = []
            st.experimental_rerun()
    with col_new:
        if st.button("🔄 新对话"):
            st.session_state.conversation_history = []
            st.experimental_rerun()

st.markdown("---")

if st.button("🚀 发送", type="primary") and user_input:
    with st.spinner("正在推理中..."):
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(st.session_state.conversation_history)
        messages.append({"role": "user", "content": user_input})
        
        response = call_deepseek_api(
            messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        st.session_state.conversation_history.append({"role": "user", "content": user_input})
        st.session_state.conversation_history.append({"role": "assistant", "content": response})
        
        st.experimental_rerun()

with st.expander("📝 使用说明"):
    st.markdown("""
    ### 如何使用：
    1. 在左侧输入您的游戏AI相关问题
    2. 点击"发送"按钮
    3. AI会生成专业回答
    4. 可以继续追问，保持上下文连续
    
    ### 功能特点：
    - 📊 可调节温度控制创意度
    - 📝 可自定义系统提示
    - 📜 保存对话历史
    - 🗑️ 一键清空对话
    
    ### 示例问题：
    - 如何设计游戏AI的行为树？
    - 游戏AI路径规划有哪些常用算法？
    - 如何平衡游戏中的AI难度？
    - 如何实现游戏中的AI决策系统？
    """)