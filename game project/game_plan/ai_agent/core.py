# ai_agent/core.py
import os
from langchain_community.vectorstores import Chroma

class LocalEmbeddings:
    """本地嵌入模型模拟类"""
    def __init__(self):
        self.vector_length = 384
    
    def embed_documents(self, texts):
        return [[0.0 for _ in range(self.vector_length)] for _ in texts]
    
    def embed_query(self, text):
        return [0.0 for _ in range(self.vector_length)]

class LocalLLM:
    """本地LLM模拟类"""
    def __call__(self, messages):
        context = ""
        query = ""
        
        for message in messages:
            if message["role"] == "system" and "【参考资料】：" in message["content"]:
                context = message["content"].split("【参考资料】：")[1].strip()
            elif message["role"] == "human":
                query = message["content"]
        
        if context:
            return f"基于参考资料，我来回答你的问题：{query}\n\n参考资料摘要：{context[:100]}..."
        else:
            return f"我需要更多信息来回答你的问题：{query}"

def get_vectorstore():
    """获取知识库连接"""
    embeddings = LocalEmbeddings()
    vectorstore = Chroma(
        persist_directory="C:/Users/Lenovo/Desktop/游戏ai agent知识库",
        embedding_function=embeddings
    )
    return vectorstore

def get_llm():
    """获取LLM模型"""
    return LocalLLM()