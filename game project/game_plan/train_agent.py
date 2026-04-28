# train_agent.py - AI Agent自动化训练脚本
import os
import json
import sys

try:
    from langchain_chroma import Chroma
except ImportError:
    from langchain_community.vectorstores import Chroma

from langchain_core.documents import Document as LangChainDocument

# DeepSeek API配置
os.environ["DEEPSEEK_API_KEY"] = "sk-aa2a1ccf95674e6c8f134ea9f9d65dc3"

class DeepSeekLLM:
    """DeepSeek LLM 调用类"""
    def __init__(self):
        self.api_key = os.environ.get("DEEPSEEK_API_KEY")
        self.api_url = "https://api.deepseek.com/chat/completions"
    
    def generate(self, messages, temperature=0.7):
        import requests
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        data = {
            "model": "deepseek-chat",
            "messages": messages,
            "temperature": temperature
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=data, timeout=60)
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"API调用失败: {str(e)}")
            return None

class LocalEmbeddings:
    """本地嵌入模型（用于Chroma）"""
    def __init__(self):
        self.vector_length = 384
    
    def embed_documents(self, texts):
        return [[0.0 for _ in range(self.vector_length)] for _ in texts]
    
    def embed_query(self, text):
        return [0.0 for _ in range(self.vector_length)]

class AITrainer:
    """AI Agent训练器"""
    def __init__(self, knowledge_base_path):
        self.llm = DeepSeekLLM()
        self.knowledge_base_path = knowledge_base_path
        self.embeddings = LocalEmbeddings()
        self.vectorstore = None
    
    def initialize_knowledge_base(self):
        """初始化知识库"""
        try:
            self.vectorstore = Chroma(
                persist_directory=self.knowledge_base_path,
                embedding_function=self.embeddings
            )
            print(f"知识库已加载，现有文档数: {self.vectorstore._collection.count()}")
            return True
        except Exception as e:
            print(f"初始化知识库失败: {str(e)}")
            return False
    
    def generate_qa_pairs(self, topic, num_pairs=10):
        """使用AI生成问答对"""
        print(f"\n正在为主题「{topic}」生成 {num_pairs} 个问答对...")
        
        prompt = f"""你是一个专业的游戏AI训练师。请为以下主题生成 {num_pairs} 个高质量的问答对。

主题：{topic}

要求：
1. 每个问答对应该包含一个问题和答案
2. 问题和答案都应该详细、准确、有价值
3. 涵盖该主题的不同方面
4. 答案应该基于游戏AI设计的最佳实践

请以JSON格式输出，格式如下：
[
    {{"question": "问题1", "answer": "答案1"}},
    {{"question": "问题2", "answer": "答案2"}}
]

只输出JSON，不要有其他内容："""
        
        messages = [{"role": "user", "content": prompt}]
        response = self.llm.generate(messages)
        
        if response:
            try:
                qa_pairs = json.loads(response)
                print(f"成功生成 {len(qa_pairs)} 个问答对")
                return qa_pairs
            except json.JSONDecodeError:
                print("解析JSON失败，尝试清理响应...")
                return self.clean_json_response(response)
        return []
    
    def clean_json_response(self, response):
        """清理JSON响应"""
        try:
            start_idx = response.find('[')
            end_idx = response.rfind(']') + 1
            if start_idx != -1 and end_idx != 0:
                json_str = response[start_idx:end_idx]
                return json.loads(json_str)
        except Exception as e:
            print(f"清理JSON失败: {str(e)}")
        return []
    
    def generate_document(self, topic, content_type="guide"):
        """使用AI生成文档内容"""
        print(f"\n正在为主题「{topic}」生成文档内容...")
        
        if content_type == "guide":
            prompt = f"""请为游戏AI设计主题「{topic}」撰写一篇详细的指南文档。

要求：
1. 内容全面、深入，涵盖理论和实践
2. 包含具体示例和最佳实践
3. 解释关键概念和技术实现方法
4. 提供可操作的建议

请用中文撰写，字数不少于800字："""
        else:
            prompt = f"""请为游戏AI设计主题「{topic}」撰写技术文档。

要求：
1. 内容专业、准确
2. 包含实现细节和代码示例
3. 涵盖常见问题和解决方案
4. 提供最佳实践建议

请用中文撰写，字数不少于600字："""
        
        messages = [{"role": "user", "content": prompt}]
        response = self.llm.generate(messages, temperature=0.6)
        
        if response:
            print(f"成功生成文档内容，字数: {len(response)}")
            return response
        return ""
    
    def add_qa_pairs_to_knowledge_base(self, qa_pairs):
        """将问答对添加到知识库"""
        if not qa_pairs:
            print("没有问答对可添加")
            return 0
        
        if not self.vectorstore:
            print("知识库未初始化，尝试重新初始化...")
            if not self.initialize_knowledge_base():
                print("知识库初始化失败")
                return 0
        
        documents = []
        for qa in qa_pairs:
            content = f"问题：{qa['question']}\n\n答案：{qa['answer']}"
            doc = LangChainDocument(
                page_content=content,
                metadata={"source": "AI生成-问答对", "type": "qa_pair"}
            )
            documents.append(doc)
        
        try:
            self.vectorstore.add_documents(documents)
            print(f"成功添加 {len(documents)} 个问答对到知识库")
            return len(documents)
        except Exception as e:
            print(f"添加问答对失败: {str(e)}")
            return 0
    
    def add_document_to_knowledge_base(self, content, topic, doc_type="guide"):
        """将文档添加到知识库"""
        if not content:
            print("没有文档内容可添加")
            return 0
        
        if not self.vectorstore:
            print("知识库未初始化，尝试重新初始化...")
            if not self.initialize_knowledge_base():
                print("知识库初始化失败")
                return 0
        
        chunks = [content[i:i+800] for i in range(0, len(content), 800)]
        documents = []
        
        for i, chunk in enumerate(chunks):
            doc = LangChainDocument(
                page_content=chunk,
                metadata={"source": f"AI生成-{doc_type}", "topic": topic, "chunk": i+1}
            )
            documents.append(doc)
        
        try:
            self.vectorstore.add_documents(documents)
            print(f"成功添加 {len(documents)} 个文档块到知识库")
            return len(documents)
        except Exception as e:
            print(f"添加文档失败: {str(e)}")
            return 0
    
    def train_on_topic(self, topic, qa_count=10, generate_doc=True):
        """训练指定主题"""
        print(f"\n{'='*50}")
        print(f"开始训练主题：{topic}")
        print(f"{'='*50}")
        
        total_added = 0
        
        qa_pairs = self.generate_qa_pairs(topic, qa_count)
        if qa_pairs:
            total_added += self.add_qa_pairs_to_knowledge_base(qa_pairs)
        
        if generate_doc:
            doc_content = self.generate_document(topic)
            if doc_content:
                total_added += self.add_document_to_knowledge_base(doc_content, topic)
        
        print(f"\n主题「{topic}」训练完成，新增 {total_added} 个文档")
        return total_added
    
    def batch_train(self, topics):
        """批量训练多个主题"""
        print(f"\n{'#'*60}")
        print(f"开始批量训练，共 {len(topics)} 个主题")
        print(f"{'#'*60}")
        
        total_added = 0
        for i, topic in enumerate(topics, 1):
            print(f"\n[{i}/{len(topics)}]")
            added = self.train_on_topic(topic)
            total_added += added
        
        print(f"\n{'#'*60}")
        print(f"批量训练完成！共新增 {total_added} 个文档")
        print(f"知识库现有文档总数: {self.vectorstore._collection.count()}")
        print(f"{'#'*60}")
        
        return total_added

def main():
    """主训练流程"""
    print("="*60)
    print("AI Agent 自动化训练系统")
    print("="*60)
    
    knowledge_base_path = os.path.join("C:", "Users", "Lenovo", "Desktop", "游戏ai agent知识库")
    
    print(f"知识库路径: {knowledge_base_path}")
    
    if not os.path.exists(knowledge_base_path):
        print(f"创建知识库文件夹: {knowledge_base_path}")
        os.makedirs(knowledge_base_path, exist_ok=True)
    
    trainer = AITrainer(knowledge_base_path)
    
    if not trainer.initialize_knowledge_base():
        print("知识库初始化失败，请检查路径是否正确")
        return
    
    default_topics = [
        "游戏AI行为树设计",
        "Unity中的导航系统",
        "游戏AI状态机实现",
        "敌人AI巡逻和追击逻辑",
        "游戏Boss战AI设计",
        "游戏AI路径规划算法",
        "游戏AI决策树应用",
        "NPC对话系统设计",
        "游戏AI动画和动作系统",
        "游戏AI难度平衡设计"
    ]
    
    print("\n预设训练主题：")
    for i, topic in enumerate(default_topics, 1):
        print(f"  {i}. {topic}")
    
    print("\n请选择训练模式：")
    print("  1. 使用预设主题训练（推荐）")
    print("  2. 自定义主题训练")
    print("  3. 退出")
    
    choice = input("\n请输入选项 (1/2/3): ").strip()
    
    if choice == "1":
        print("\n将使用所有预设主题进行训练...")
        trainer.batch_train(default_topics)
    
    elif choice == "2":
        print("\n请输入自定义主题（多个主题用逗号分隔）：")
        custom_topics = input("主题: ").strip()
        if custom_topics:
            topics = [t.strip() for t in custom_topics.split(",")]
            trainer.batch_train(topics)
    
    elif choice == "3":
        print("已退出训练系统")
    
    else:
        print("无效选项，已退出")

if __name__ == "__main__":
    main()