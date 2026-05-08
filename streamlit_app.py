import streamlit as st
import requests
import json
from typing import List, Dict

st.set_page_config(
    page_title="🎮 游戏AI Agent",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🎮 游戏AI Agent")
st.subheader("专业的游戏AI设计顾问 - 增强版（带知识库训练）")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "knowledge_base" not in st.session_state:
    st.session_state.knowledge_base = []
if "kb_loaded" not in st.session_state:
    st.session_state.kb_loaded = False

def load_knowledge_base():
    """从GitHub加载知识库"""
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
        st.sidebar.error(f"知识库加载失败: {str(e)}")
        return 0

def search_knowledge(query: str, top_k: int = 3) -> List[Dict]:
    """简单的关键词检索"""
    if not st.session_state.knowledge_base:
        return []
    
    query_keywords = set(query.lower().split())
    scored_docs = []
    
    for doc in st.session_state.knowledge_base:
        content = doc.get("content", "").lower()
        metadata = doc.get("metadata", {})
        
        score = sum(1 for keyword in query_keywords if keyword in content)
        
        if score > 0:
            scored_docs.append({
                "content": doc["content"],
                "metadata": metadata,
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
        return f"❌ 响应异常: {json.dumps(result, ensure_ascii=False)}"
    except Exception as e:
        return f"❌ 调用失败: {str(e)}"

with st.sidebar:
    st.subheader("📚 知识库管理")
    
    if not st.session_state.kb_loaded:
        if st.button("📥 加载知识库"):
            with st.spinner("正在加载..."):
                count = load_knowledge_base()
                if count > 0:
                    st.success(f"✅ 已加载 {count} 个文档")
                    st.rerun()
                else:
                    st.error("❌ 加载失败")
    else:
        st.success(f"✅ 知识库已就绪 ({len(st.session_state.knowledge_base)} 个文档)")
        
        st.markdown("---")
        st.subheader("➕ 添加知识")
        
        new_id = st.text_input("知识ID", value=f"doc_{len(st.session_state.knowledge_base) + 1:03d}")
        new_content = st.text_area("知识内容", height=150, placeholder="请输入新知识内容...")
        new_category = st.text_input("分类标签", value="未分类")
        new_source = st.text_input("来源", value="用户添加")
        
        if st.button("💾 添加到知识库"):
            if new_content.strip():
                new_doc = {
                    "id": new_id,
                    "content": new_content.strip(),
                    "metadata": {
                        "source": new_source,
                        "category": new_category
                    }
                }
                st.session_state.knowledge_base.append(new_doc)
                
                # 生成新的JSON文件供下载
                updated_kb = st.session_state.knowledge_base
                st.download_button(
                    label="📥 下载更新后的知识库",
                    data=json.dumps(updated_kb, ensure_ascii=False, indent=2),
                    file_name="knowledge_base.json",
                    mime="application/json"
                )
                st.success(f"✅ 已添加！请下载并上传到GitHub更新！")
            else:
                st.error("❌ 请输入知识内容")
        
        st.markdown("---")
        if st.button("🔄 重新加载知识库"):
            st.session_state.kb_loaded = False
            st.session_state.knowledge_base = []
            st.rerun()
    
    st.markdown("---")
    st.subheader("⚙️ 设置")
    temperature = st.slider("创意度", 0.0, 1.0, 0.7, 0.1)
    use_knowledge = st.checkbox("使用知识库", value=True)
    show_reasoning = st.checkbox("显示思考过程", value=True)
    show_flowchart = st.checkbox("显示流程图", value=True)
    show_sources = st.checkbox("显示知识来源", value=True)
    
    st.markdown("---")
    if st.button("🗑️ 清空对话"):
        st.session_state.messages = []
        st.rerun()
    if st.button("🔄 重新生成"):
        if st.session_state.messages:
            st.session_state.messages.pop()
            st.rerun()

st.markdown("---")

chat_container = st.container()
with chat_container:
    st.subheader("💬 对话")
    
    for i, msg in enumerate(st.session_state.messages):
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            
            if msg["role"] == "assistant":
                if st.button("📋 复制", key=f"copy_{i}"):
                    st.code(msg["content"])

st.markdown("---")

prompt = st.chat_input("输入您的游戏AI问题...", key="fixed_input")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("🤔 思考中..."):
            context = ""
            sources = []
            
            if use_knowledge and st.session_state.knowledge_base:
                relevant_docs = search_knowledge(prompt, top_k=3)
                if relevant_docs:
                    context = "\n\n".join([doc["content"] for doc in relevant_docs])
                    sources = relevant_docs
                    if show_sources:
                        st.info(f"📚 从知识库检索到 {len(relevant_docs)} 个相关文档")
            
            system_msg = "你是专业游戏AI顾问，擅长游戏AI设计和实现。"
            if context:
                system_msg += f"\n\n参考以下知识库内容回答问题：\n{context}"
            
            history = [{"role": "system", "content": system_msg}]
            history += st.session_state.messages[:-1]
            history.append({"role": "user", "content": prompt})
            
            final_answer = call_api(history, temperature)
            st.write(final_answer)
            
            if show_sources and sources:
                with st.expander("📖 知识来源"):
                    for idx, doc in enumerate(sources, 1):
                        st.markdown(f"**来源 {idx}** (相关度: {doc['score']}, ID: {doc['id']})")
                        st.text(doc["content"][:200] + "...")
                        st.markdown("---")
            
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
                full_response = f"{full_response}\n\n【流程图】\n{flowchart}"
            
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            st.rerun()
