# ai_agent/core.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

class LocalLLM:
    """基于DeepSeek API的LLM类"""
    def __call__(self, messages):
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            return "错误：请设置DEEPSEEK_API_KEY环境变量"
        
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
                }
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            return f"LLM调用失败：{str(e)}"

def get_llm():
    """获取LLM模型"""
    return LocalLLM()