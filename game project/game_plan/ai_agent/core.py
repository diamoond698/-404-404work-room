# ai_agent/core.py
import os
from langchain_community.vectorstores import Chroma

# 本地嵌入模型模拟类
class LocalEmbeddings:
    def __init__(self):
        self.vector_length = 384
    
    def embed_documents(self, texts):
        return [[0.0 for _ in range(self.vector_length)] for _ in texts]
    
    def embed_query(self, text):
        return [0.0 for _ in range(self.vector_length)]

# DeepSeek LLM 类
class DeepSeekLLM:
    def __init__(self):
        self.api_key = os.environ.get("DEEPSEEK_API_KEY", "sk-aa2a1ccf95674e6c8f134ea9f9d65dc3")
        self.api_url = "https://api.deepseek.com/chat/completions"
    
    def __call__(self, messages):
        import requests
        import json
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        data = {
            "model": "deepseek-chat",
            "messages": messages,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except Exception as e:
            return f"抱歉，我遇到了一些问题：{str(e)}"

def get_vectorstore():
    """获取知识库连接"""
    embeddings = LocalEmbeddings()
    vectorstore = Chroma(
        persist_directory="knowledge_base",  # 修改为相对路径
        embedding_function=embeddings
    )
    return vectorstore

def get_llm():
    """获取LLM模型"""
    return DeepSeekLLM()