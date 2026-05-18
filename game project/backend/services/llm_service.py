import os
import requests
from dotenv import load_dotenv

load_dotenv()

class LLMService:
    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_API_KEY", "")
        self.base_url = "https://api.deepseek.com/v1"
    
    def chat(self, messages: list, system_prompt: str = None, temperature: float = 0.7):
        full_messages = []
        
        if system_prompt:
            full_messages.append({"role": "system", "content": system_prompt})
        
        full_messages.extend(messages)
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "deepseek-chat",
                    "messages": full_messages,
                    "temperature": temperature
                },
                timeout=60
            )
            
            result = response.json()
            if "choices" in result and len(result["choices"]) > 0:
                return {
                    "content": result["choices"][0]["message"]["content"],
                    "tokens_used": result["usage"]["total_tokens"] if "usage" in result else 0
                }
            else:
                return {
                    "content": "抱歉，我遇到了一些问题...",
                    "tokens_used": 0
                }
        except Exception as e:
            print(f"LLM Error: {e}")
            return {
                "content": "抱歉，我遇到了一些问题...",
                "tokens_used": 0
            }
