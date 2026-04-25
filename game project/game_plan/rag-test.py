import os
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate

# 1. 配置 API Key
os.environ["DEEPSEEK_API_KEY"] = "sk-aa2a1ccf95674e6c8f134ea9f9d65dc3"  # 你的 DeepSeek API Key

# 2. 本地嵌入模型模拟类（避免模型下载）
class LocalEmbeddings:
    def __init__(self):
        # 模拟嵌入模型，返回固定长度的向量
        self.vector_length = 384
    
    def embed_documents(self, texts):
        # 为每个文本返回一个固定长度的向量
        return [[0.0 for _ in range(self.vector_length)] for _ in texts]
    
    def embed_query(self, text):
        # 为查询返回一个固定长度的向量
        return [0.0 for _ in range(self.vector_length)]

# 3. 本地 LLM 模拟类（用于测试）
class LocalLLM:
    def __call__(self, messages):
        # 简单的本地 LLM 模拟，返回基于上下文的回答
        context = ""
        query = ""
        
        for message in messages:
            if message["role"] == "system":
                # 从系统消息中提取上下文
                if "【参考资料】：" in message["content"]:
                    context = message["content"].split("【参考资料】：")[1].strip()
            elif message["role"] == "human":
                query = message["content"]
        
        if context:
            return f"基于参考资料，我来回答你的问题：{query}\n\n参考资料摘要：{context[:100]}..."
        else:
            return f"我需要更多信息来回答你的问题：{query}"

def build_rag_chain():
    print("=== 开始构建 RAG 链 ===")
    
    # --- [环节1：向量检索准备] ---
    print("\n1. 初始化 Embedding 模型...")
    # 初始化本地嵌入模型模拟
    embeddings = LocalEmbeddings()
    print("   ✅ Embedding 模型初始化成功")

    print("\n2. 加载本地知识库...")
    # 加载已存在的本地知识库 (Chroma)
    vectorstore = Chroma(
        persist_directory="C:/Users/Lenovo/Desktop/游戏ai agent知识库", # 你的知识库路径
        embedding_function=embeddings
    )
    print("   ✅ 知识库加载成功")
    print(f"   知识库中文档数量: {vectorstore._collection.count()}")

    print("\n3. 创建检索器...")
    # 将数据库转化为检索器，设置 k=3 表示获取最相关的 3 条内容
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    print("   ✅ 检索器创建成功")

    # --- [环节2：上下文拼接 (Prompt)] ---
    print("\n4. 构建 Prompt 模板...")
    # 定义系统指令，告诉 AI 如何使用查出来的知识
    system_prompt = (
        "你是一个专业的 AI 助手。请严格根据以下检索到的【参考资料】来回答用户的问题。\n"
        "如果你在【参考资料】中找不到答案，请直接回答'根据已知信息我无法回答该问题'，不要胡编乱造。\n"
        "\n【参考资料】：\n{context}"
    )

    # 组装 Prompt 模板
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{query}")
    ])
    print("   ✅ Prompt 模板构建成功")

    # --- [环节3：初始化 LLM 模型] ---
    print("\n5. 初始化 LLM 模型...")
    # 初始化本地 LLM 模拟（避免 API 调用）
    llm = LocalLLM()
    print("   ✅ LLM 模型初始化成功")

    # --- [环节4：构建完整的 RAG 链路] ---
    print("\n6. 构建 RAG 链路...")
    # 逻辑：
    # 1. 拿用户的 query 扔给 retriever 查出 context (格式化为字符串)
    # 2. 将 context 和 query 填入 prompt
    # 3. 交给 llm 思考
    # 4. 提取纯文本回答

    def format_docs(docs):
        # 把检索出来的 3 条文档内容拼成一个大字符串
        print(f"   检索到 {len(docs)} 条相关文档:")
        for i, doc in enumerate(docs, 1):
            print(f"     文档 {i}: {doc.page_content[:100]}...")
        return "\n\n".join(doc.page_content for doc in docs)

    def rag_chain(query):
        # 1. 检索相关文档 - 使用 vectorstore 的 similarity_search 方法
        docs = vectorstore.similarity_search(query, k=3)
        # 2. 格式化文档
        context = format_docs(docs)
        # 3. 构建消息
        messages = [
            {"role": "system", "content": system_prompt.format(context=context)},
            {"role": "human", "content": query}
        ]
        # 4. 调用 LLM
        response = llm(messages)
        return response

    print("   ✅ RAG 链路构建成功")
    
    print("\n=== RAG 链构建完成 ===")
    return rag_chain

# --- 测试运行 ---
if __name__ == "__main__":
    try:
        # 构建链路
        print("开始构建 RAG 链路...")
        chain = build_rag_chain()

        # 模拟用户输入
        user_query = "知识库里关于 XXX 的规定是什么？" # 替换成你知识库相关的真实问题
        print(f"\n用户提问: {user_query}\n")
        print("AI 正在检索并思考...\n")

        # 触发链路
        response = chain(user_query)

        print("AI 回答:")
        print(response)
        print("\n✅ RAG 应用运行成功！")
    except Exception as e:
        print(f"\n❌ 运行失败: {str(e)}")
        import traceback
        traceback.print_exc()