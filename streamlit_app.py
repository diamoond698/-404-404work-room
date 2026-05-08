import streamlit as st
import requests
import json

st.set_page_config(page_title="🎮 游戏AI Agent", layout="wide")
st.title("🎮 游戏AI Agent")
st.subheader("专业的游戏AI设计顾问")

if "messages" not in st.session_state:
    st.session_state.messages = []

def call_api(messages, temperature=0.7):
    api_key = st.secrets.get("DEEPSEEK_API_KEY", "")
    if not api_key:
        return "⚠️ 请在 Settings → Secrets 中配置 DEEPSEEK_API_KEY"
    
    try:
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={"model": "deepseek-chat", "messages": messages, "temperature": temperature},
            timeout=90
        )
        result = response.json()
        if "choices" in result:
            return result["choices"][0]["message"]["content"]
        elif "error" in result:
            return f"❌ API错误: {result['error'].get('message', '未知错误')}"
        return f"❌ 响应异常: {json.dumps(result, ensure_ascii=False)}"
    except Exception as e:
        return f"❌ 调用失败: {str(e)}"

col1, col2 = st.columns([3, 1])

with col2:
    st.subheader("设置")
    temperature = st.slider("创意度", 0.0, 1.0, 0.7, 0.1)
    show_reasoning = st.checkbox("显示思考过程", value=True)
    show_flowchart = st.checkbox("显示流程图", value=True)
    st.markdown("---")
    if st.button("🗑️ 清空对话"):
        st.session_state.messages = []
        st.experimental_rerun()
    if st.button("🔄 重新生成"):
        if st.session_state.messages:
            st.session_state.messages.pop()
            st.experimental_rerun()

with col1:
    st.subheader("对话")
    
    for i, msg in enumerate(st.session_state.messages):
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            
            if msg["role"] == "assistant":
                if st.button("📋 复制", key=f"copy_{i}"):
                    st.code(msg["content"])

    prompt = st.chat_input("输入您的游戏AI问题...")
    
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("🤔 思考中..."):
                history = [{"role": "system", "content": "你是专业游戏AI顾问，擅长游戏AI设计和实现"}]
                history += st.session_state.messages[:-1]
                history.append({"role": "user", "content": prompt})
                
                final_answer = call_api(history, temperature)
                st.write(final_answer)
                
                full_response = final_answer
                
                if show_reasoning:
                    with st.expander("🧠 查看思考过程"):
                        reason_prompt = f"请模拟游戏AI顾问的思考过程，分析这个问题: {prompt}。请分4点回答: 1.问题分析 2.信息检索 3.推理步骤 4.结论形成"
                        reasoning = call_api([{"role": "user", "content": reason_prompt}], 0.5)
                        st.write(reasoning)
                        full_response = f"【推理过程】\n{reasoning}\n\n【最终回答】\n{final_answer}"
                
                if show_flowchart:
                    st.markdown("### 📊 流程图")
                    flowchart_prompt = f"请为以下问答生成Mermaid格式流程图，只输出代码。问题: {prompt} 回答: {final_answer}"
                    flowchart = call_api([{"role": "user", "content": flowchart_prompt}], 0.3)
                    st.code(flowchart, language="markdown")
                    st.info("提示: 将Mermaid代码复制到 https://mermaid.live 可查看图表")
                    if show_reasoning:
                        full_response = f"{full_response}\n\n【流程图】\n{flowchart}"
                    else:
                        full_response = f"【最终回答】\n{final_answer}\n\n【流程图】\n{flowchart}"
                
                st.session_state.messages.append({"role": "assistant", "content": full_response})