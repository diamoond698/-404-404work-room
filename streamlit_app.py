import streamlit as st
import requests
import json
from typing import List, Dict
from datetime import datetime

st.set_page_config(page_title="🎮 游戏AI Agent", layout="wide")

st.title("🎮 游戏AI Agent")
st.subheader("专业的游戏AI设计顾问")

if "conversations" not in st.session_state:
    st.session_state.conversations = [{"id": "conv_001", "name": "新对话", "messages": [], "created": datetime.now().isoformat()}]
if "current_conv_id" not in st.session_state:
    st.session_state.current_conv_id = "conv_001"
if "knowledge_base" not in st.session_state:
    st.session_state.knowledge_base = []
if "kb_loaded" not in st.session_state:
    st.session_state.kb_loaded = False

def get_current_conversation():
    for conv in st.session_state.conversations:
        if conv["id"] == st.session_state.current_conv_id:
            return conv
    return None

def load_knowledge_base():
    try:
        knowledge_url = "https://raw.githubusercontent.com/diamoon698/404-404-work-room/main/knowledge_base.json"
        response = requests.get(knowledge_url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            st.session_state.knowledge_base = data
            st.session_state.kb_loaded = True
            return len(data)
        return 0
    except Exception as e:
        return 0

def search_knowledge(query: str, top_k: int = 3) -> List[Dict]:
    if not st.session_state.knowledge_base:
        return []
    
    query_keywords = set(query.lower().split())
    scored_docs = []
    
    for doc in st.session_state.knowledge_base:
        content = doc.get("content", "").lower()
        score = sum(1 for keyword in query_keywords if keyword in content)
        
        if score > 0:
            scored_docs.append({
                "content": doc["content"],
                "score": score,
                "id": doc.get("id", "")
            })
    
    scored_docs.sort(key=lambda x: x["score"], reverse=True)
    return scored_docs[:top_k]

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
        return f"❌ 响应异常"
    except Exception as e:
        return f"❌ 调用失败: {str(e)}"

def generate_code(prompt, language="csharp"):
    code_prompt = f"""根据以下需求生成{language}游戏AI代码：

需求描述：
{prompt}

要求：
- 符合游戏引擎规范（Unity优先）
- 代码结构清晰，有必要的注释
- 返回完整可运行的代码片段
- 包含必要的命名空间和类定义

语言：{language}"""
    
    return call_api([{"role": "user", "content": code_prompt}], temperature=0.3)

def analyze_performance(ai_type, complexity, entity_count):
    prompts = {
        "behavior_tree": f"分析行为树AI性能：复杂度等级{complexity}，实体数量{entity_count}。请预估CPU占用率、内存使用、推荐优化方案。",
        "state_machine": f"分析状态机AI性能：复杂度等级{complexity}，实体数量{entity_count}。请预估CPU占用率、内存使用、推荐优化方案。",
        "pathfinding": f"分析寻路AI性能：复杂度等级{complexity}，实体数量{entity_count}。请预估CPU占用率、内存使用、推荐优化方案。",
        "neural_network": f"分析神经网络AI性能：复杂度等级{complexity}，实体数量{entity_count}。请预估CPU占用率、内存使用、推荐优化方案。"
    }
    
    if ai_type in prompts:
        return call_api([{"role": "user", "content": prompts[ai_type]}], temperature=0.5)
    return "❌ 不支持的AI类型"

with st.sidebar:
    st.subheader("📝 对话列表")
    
    if st.button("➕ 新对话"):
        new_id = f"conv_{len(st.session_state.conversations) + 1:03d}"
        st.session_state.conversations.append({
            "id": new_id,
            "name": "新对话",
            "messages": [],
            "created": datetime.now().isoformat()
        })
        st.session_state.current_conv_id = new_id
    
    st.markdown("---")
    
    for conv in st.session_state.conversations:
        if st.button(conv["name"], key=conv["id"], use_container_width=True):
            st.session_state.current_conv_id = conv["id"]
    
    st.markdown("---")
    st.subheader("📚 知识库")
    
    if not st.session_state.kb_loaded:
        if st.button("📥 加载知识库"):
            count = load_knowledge_base()
            if count > 0:
                st.success(f"✅ 已加载 {count} 个文档")
            else:
                st.error("❌ 加载失败")
    else:
        st.success(f"✅ 已加载 {len(st.session_state.knowledge_base)} 个文档")
    
    st.markdown("---")
    st.subheader("⚙️ 设置")
    temperature = st.slider("创意度", 0.0, 1.0, 0.7, 0.1)
    use_knowledge = st.checkbox("使用知识库", value=True)
    show_reasoning = st.checkbox("显示思考过程", value=True)
    show_flowchart = st.checkbox("显示流程图", value=True)

tab1, tab2, tab3 = st.tabs(["💬 聊天", "🔧 代码生成", "⚡ 性能预估"])

with tab1:
    current_conv = get_current_conversation()
    if current_conv:
        st.subheader(f"{current_conv['name']}")
        
        for msg in current_conv["messages"]:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
                if msg["role"] == "assistant":
                    st.code(msg["content"], language="markdown")
        
        prompt = st.chat_input("输入您的游戏AI问题...")
        
        if prompt:
            current_conv["messages"].append({"role": "user", "content": prompt})
            
            context = ""
            if use_knowledge and st.session_state.kb_loaded and st.session_state.knowledge_base:
                relevant_docs = search_knowledge(prompt, top_k=3)
                if relevant_docs:
                    context = "\n\n".join([doc["content"] for doc in relevant_docs])
            
            system_msg = "你是专业游戏AI顾问，擅长游戏AI设计和实现。"
            if context:
                system_msg += f"\n\n参考以下知识库内容：\n{context}"
            
            history = [{"role": "system", "content": system_msg}]
            for m in current_conv["messages"]:
                history.append({"role": m["role"], "content": m["content"]})
            
            with st.chat_message("assistant"):
                with st.spinner("思考中..."):
                    answer = call_api(history, temperature)
                    st.write(answer)
                    
                    if show_reasoning:
                        with st.expander("🧠 思考过程"):
                            reason_prompt = f"分析问题: {prompt}，请分4点回答: 1.问题分析 2.信息检索 3.推理步骤 4.结论形成"
                            reasoning = call_api([{"role": "user", "content": reason_prompt}], 0.5)
                            st.write(reasoning)
                    
                    if show_flowchart:
                        with st.expander("📊 流程图"):
                            flowchart_prompt = f"生成Mermaid流程图代码，只输出代码。问题: {prompt} 回答: {answer}"
                            flowchart = call_api([{"role": "user", "content": flowchart_prompt}], 0.3)
                            st.code(flowchart, language="markdown")
                    
                    current_conv["messages"].append({"role": "assistant", "content": answer})

with tab2:
    st.subheader("🔧 AI代码生成器")
    st.write("根据您的需求，自动生成游戏AI代码！")
    
    code_prompt = st.text_area("描述您的AI需求", height=200, placeholder="例如：创建一个Unity中的敌人巡逻AI，包含追逐玩家和攻击行为...")
    
    language = st.selectbox("选择语言", ["C# (Unity)", "Python", "Lua", "C++ (Unreal)"])
    lang_map = {"C# (Unity)": "csharp", "Python": "python", "Lua": "lua", "C++ (Unreal)": "cpp"}
    
    if st.button("🚀 生成代码"):
        if code_prompt.strip():
            with st.spinner("正在生成代码..."):
                code = generate_code(code_prompt, lang_map[language])
                st.subheader("生成的代码")
                st.code(code, language=lang_map[language])
        else:
            st.error("请输入AI需求描述")

with tab3:
    st.subheader("⚡ AI性能预估")
    st.write("分析AI系统的性能消耗，提供优化建议")
    
    ai_type = st.selectbox("AI类型", ["behavior_tree", "state_machine", "pathfinding", "neural_network"], format_func=lambda x: {
        "behavior_tree": "行为树",
        "state_machine": "状态机",
        "pathfinding": "寻路系统",
        "neural_network": "神经网络"
    }[x])
    
    complexity = st.slider("复杂度等级", 1, 5, 3, help="1=简单，5=复杂")
    entity_count = st.slider("实体数量", 10, 1000, 100, step=10)
    
    if st.button("📊 分析性能"):
        with st.spinner("正在分析..."):
            result = analyze_performance(ai_type, complexity, entity_count)
            st.subheader("性能分析报告")
            st.write(result)
