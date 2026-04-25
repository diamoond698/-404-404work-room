import os
from langchain_openai import ChatOpenAI

# 配置 DeepSeek API Key
os.environ["DEEPSEEK_API_KEY"] = "sk-aa2a1ccf95674e6c8f134ea9f9d65dc3"  # 你的 DeepSeek API Key

def test_deepseek_api():
    print("开始测试 DeepSeek API...")
    
    try:
        # 初始化 DeepSeek LLM 模型
        llm = ChatOpenAI(
            model="deepseek-chat",
            api_key=os.environ["DEEPSEEK_API_KEY"],
            base_url="https://api.deepseek.com/v1"
        )
        
        # 测试简单的提示
        response = llm.invoke("你好，DeepSeek！")
        print("✅ DeepSeek API 调用成功！")
        print(f"响应内容: {response}")
        
        return True
    except Exception as e:
        print(f"❌ DeepSeek API 调用失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_deepseek_api()