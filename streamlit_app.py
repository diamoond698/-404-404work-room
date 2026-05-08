import streamlit as st
import requests
import json
from typing import List, Dict
from datetime import datetime

st.set_page_config(page_title="🎮 游戏AI Agent", layout="wide")

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        min-height: 100vh;
    }
    
    .stSidebar {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        border-radius: 8px;
        color: white;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .user-message {
        display: flex;
        justify-content: flex-end;
        margin-bottom: 16px;
    }
    
    .user-content {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px 16px 4px 16px;
        padding: 16px 20px;
        max-width: 70%;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .assistant-message {
        display: flex;
        justify-content: flex-start;
        margin-bottom: 16px;
    }
    
    .assistant-content {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 16px 16px 16px 4px;
        padding: 16px 20px;
        max-width: 70%;
        backdrop-filter: blur(10px);
    }
    
    .thinking-content {
        background: rgba(255, 255, 255, 0.05);
        border: 1px dashed rgba(102, 126, 234, 0.5);
        border-radius: 16px 16px 16px 4px;
        padding: 16px 20px;
        max-width: 70%;
        backdrop-filter: blur(10px);
    }
    
    .avatar {
        width: 48px;
        height: 48px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        margin: 0 12px;
        flex-shrink: 0;
    }
    
    .user-avatar {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    }
    
    .assistant-avatar {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .message-text {
        color: white;
        font-size: 15px;
        line-height: 1.6;
    }
    
    .chat-input-area {
        position: fixed;
        bottom: 0;
        left: 240px;
        right: 0;
        background: rgba(26, 26, 46, 0.95);
        backdrop-filter: blur(20px);
        padding: 16px 24px;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        z-index: 100;
    }
    
    .stTextInput>div>div>input {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 24px;
        color: white;
        padding: 12px 20px;
        font-size: 15px;
    }
    
    .stCodeBlock {
        background: rgba(0, 0, 0, 0.4) !important;
        border-radius: 8px;
        border: 1px solid rgba(102, 126, 234, 0.3);
        margin-top: 12px;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #fff;
        text-shadow: 0 0 20px rgba(102, 126, 234, 0.5);
    }
    
    p, li, label {
        color: rgba(255, 255, 255, 0.8);
    }
    
    .stSlider>div>div>div>div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    }
    
    .stSelectbox>div>div {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 8px;
        color: white;
    }
    
    .sidebar-title {
        font-size: 18px !important;
        font-weight: bold !important;
        color: #ffffff !important;
        margin-bottom: 12px !important;
    }
</style>
""", unsafe_allow_html=True)

if "conversations" not in st.session_state:
    st.session_state.conversations = [{"id": "conv_001", "name": "新对话", "messages": [], "created": datetime.now().isoformat()}]
if "current_conv_id" not in st.session_state:
    st.session_state.current_conv_id = "conv_001"
if "knowledge_base" not in st.session_state:
    st.session_state.knowledge_base = []
if "kb_loaded" not in st.session_state:
    st.session_state.kb_loaded = False
if "is_thinking" not in st.session_state:
    st.session_state.is_thinking = False
if "code_generated" not in st.session_state:
    st.session_state.code_generated = ""
if "performance_result" not in st.session_state:
    st.session_state.performance_result = ""

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
        st.error(f"加载知识库失败: {str(e)}")
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
        return f"❌ 响应异常: {result}"
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
    st.markdown("""
    <div style="text-align: center; margin-bottom: 16px;">
        <img src="https://neeko-copilot.bytedance.net/api/text_to_image?prompt=anime%20girl%20portrait%20cyberpunk%20style%20blue%20hair%20neon%20lights%20purple%20pink%20background%20digital%20art&image_size=square" 
             style="width: 120px; height: 120px; border-radius: 50%; border: 3px solid #667eea; box-shadow: 0 0 20px rgba(102, 126, 234, 0.5);">
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-title">📝 对话列表</div>', unsafe_allow_html=True)
    
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
        active = "✅ " if conv["id"] == st.session_state.current_conv_id else ""
        if st.button(f"{active}{conv['name']}", use_container_width=True):
            st.session_state.current_conv_id = conv["id"]
    
    st.markdown("---")
    st.markdown('<div class="sidebar-title">📚 知识库</div>', unsafe_allow_html=True)
    
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
    st.markdown('<div class="sidebar-title">⚙️ 设置</div>', unsafe_allow_html=True)
    temperature = st.slider("创意度", 0.0, 1.0, 0.7, 0.1)
    use_knowledge = st.checkbox("使用知识库", value=True)

st.markdown("""
<div style="text-align: center; padding: 20px; margin-bottom: 20px;">
    <h1 style="font-size: 2.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
        🎮 游戏AI Agent
    </h1>
    <p style="color: rgba(255,255,255,0.7); font-size: 1.1rem;">专业的游戏AI设计顾问 - 赛博朋克版</p>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["💬 聊天", "🔧 代码生成", "⚡ 性能预估"])

with tab1:
    current_conv = get_current_conversation()
    if current_conv:
        st.markdown(f"<h3 style='color: #fff; margin-bottom: 20px;'>{current_conv['name']}</h3>", unsafe_allow_html=True)
        
        for idx, msg in enumerate(current_conv["messages"]):
            if msg["role"] == "user":
                st.markdown(f"""
                <div class="user-message">
                    <div class="user-content">
                        <p class="message-text">{msg['content']}</p>
                    </div>
                    <div class="avatar user-avatar">👤</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="assistant-message">
                    <div class="avatar assistant-avatar">🤖</div>
                    <div class="assistant-content">
                        <p class="message-text">{msg['content']}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                col_copy = st.columns([10, 1])
                with col_copy[1]:
                    if st.button("📋", key=f"copy_{idx}"):
                        st.success("✅ 已复制到剪贴板！")
        
        if st.session_state.is_thinking:
            st.markdown(f"""
            <div class="assistant-message">
                <div class="avatar assistant-avatar">🤖</div>
                <div class="thinking-content">
                    <p class="message-text">🤔 思考中...</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="chat-input-area">
            <div style="max-width: 800px; margin: 0 auto;">
        """, unsafe_allow_html=True)
        
        prompt = st.chat_input("输入您的游戏AI问题...")
        
        st.markdown("""
            </div>
        </div>
        <div style="height: 80px;"></div>
        """, unsafe_allow_html=True)
        
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
            
            answer = call_api(history, temperature)
            current_conv["messages"].append({"role": "assistant", "content": answer})

with tab2:
    st.markdown("<h3 style='color: #fff;'>🔧 AI代码生成器</h3>", unsafe_allow_html=True)
    st.write("根据您的需求，自动生成游戏AI代码！")
    
    code_prompt = st.text_area("描述您的AI需求", height=200, placeholder="例如：创建一个Unity中的敌人巡逻AI，包含追逐玩家和攻击行为...", key="code_prompt")
    
    language = st.selectbox("选择语言", ["C# (Unity)", "Python", "Lua", "C++ (Unreal)"], key="lang_select")
    lang_map = {"C# (Unity)": "csharp", "Python": "python", "Lua": "lua", "C++ (Unreal)": "cpp"}
    
    if st.button("🚀 生成代码", key="gen_code_btn"):
        if code_prompt.strip():
            with st.spinner("正在生成代码..."):
                code = generate_code(code_prompt, lang_map[language])
                st.session_state.code_generated = code
                st.markdown("<h4 style='color: #fff;'>生成的代码</h4>", unsafe_allow_html=True)
                st.code(code, language=lang_map[language])
        else:
            st.error("请输入AI需求描述")
    elif st.session_state.code_generated:
        st.markdown("<h4 style='color: #fff;'>生成的代码</h4>", unsafe_allow_html=True)
        st.code(st.session_state.code_generated, language=lang_map[language])

with tab3:
    st.markdown("<h3 style='color: #fff;'>⚡ AI性能预估</h3>", unsafe_allow_html=True)
    st.write("分析AI系统的性能消耗，提供优化建议")
    
    ai_type = st.selectbox("AI类型", ["behavior_tree", "state_machine", "pathfinding", "neural_network"], 
                          format_func=lambda x: {
                              "behavior_tree": "行为树",
                              "state_machine": "状态机",
                              "pathfinding": "寻路系统",
                              "neural_network": "神经网络"
                          }[x], key="ai_type_select")
    
    complexity = st.slider("复杂度等级", 1, 5, 3, help="1=简单，5=复杂", key="complexity_slider")
    entity_count = st.slider("实体数量", 10, 1000, 100, step=10, key="entity_slider")
    
    if st.button("📊 分析性能", key="analyze_btn"):
        with st.spinner("正在分析..."):
            result = analyze_performance(ai_type, complexity, entity_count)
            st.session_state.performance_result = result
            st.markdown("<h4 style='color: #fff;'>性能分析报告</h4>", unsafe_allow_html=True)
            st.write(result)
    elif st.session_state.performance_result:
        st.markdown("<h4 style='color: #fff;'>性能分析报告</h4>", unsafe_allow_html=True)
        st.write(st.session_state.performance_result)
