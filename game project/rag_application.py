#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAG 应用实现脚本
使用 LangChain 框架，支持多种向量数据库、嵌入模型和 LLM 模型
"""

import os
from typing import List, Dict, Any
from langchain.vectorstores import Chroma, FAISS
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceEmbeddings
from langchain.llms import OpenAI, HuggingFaceHub
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate


class RAGApplication:
    """RAG 应用类"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        初始化 RAG 应用
        
        Args:
            config: 配置字典，包含以下键：
                - vector_db_type: 向量数据库类型，可选 'chroma' 或 'faiss'
                - vector_db_path: 向量数据库路径
                - embedding_model: 嵌入模型类型，可选 'openai' 或 'huggingface'
                - embedding_model_name: 嵌入模型名称
                - llm_model: LLM 模型类型，可选 'openai' 或 'huggingface'
                - llm_model_name: LLM 模型名称
                - openai_api_key: OpenAI API 密钥（如果使用 OpenAI 模型）
                - huggingface_api_key: Hugging Face API 密钥（如果使用 Hugging Face 模型）
        """
        self.config = config
        self.vector_store = self._init_vector_store()
        self.llm = self._init_llm()
        self.qa_chain = self._init_qa_chain()
    
    def _init_vector_store(self):
        """初始化向量数据库"""
        # 初始化嵌入模型
        if self.config['embedding_model'] == 'openai':
            # 使用 OpenAI 嵌入模型
            embeddings = OpenAIEmbeddings(
                openai_api_key=self.config.get('openai_api_key')
            )
        else:
            # 使用 Hugging Face 开源嵌入模型
            embeddings = HuggingFaceEmbeddings(
                model_name=self.config.get('embedding_model_name', 'sentence-transformers/all-MiniLM-L6-v2')
            )
        
        # 初始化向量数据库
        vector_db_path = self.config.get('vector_db_path', './my_vector_db')
        if self.config['vector_db_type'] == 'chroma':
            # 使用 Chroma 向量数据库
            vector_store = Chroma(
                persist_directory=vector_db_path,
                embedding_function=embeddings
            )
        else:
            # 使用 FAISS 向量数据库
            # 注意：FAISS 需要先加载索引文件
            vector_store = FAISS.load_local(
                folder_path=vector_db_path,
                embeddings=embeddings
            )
        
        return vector_store
    
    def _init_llm(self):
        """初始化 LLM 模型"""
        if self.config['llm_model'] == 'openai':
            # 使用 OpenAI 模型
            llm = OpenAI(
                openai_api_key=self.config.get('openai_api_key'),
                model_name=self.config.get('llm_model_name', 'gpt-3.5-turbo-instruct')
            )
        else:
            # 使用 Hugging Face 模型（如 DeepSeek 等）
            llm = HuggingFaceHub(
                repo_id=self.config.get('llm_model_name', 'deepseek-ai/deepseek-llm-7b-base'),
                huggingfacehub_api_token=self.config.get('huggingface_api_key'),
                model_kwargs={"temperature": 0.7, "max_new_tokens": 512}
            )
        
        return llm
    
    def _init_qa_chain(self):
        """初始化问答链"""
        # 定义系统提示模板
        prompt_template = """
        你是一个基于知识库的问答助手。请根据以下提供的上下文信息，回答用户的问题。
        如果你无法从上下文中找到答案，请直接说明无法回答，不要编造信息。
        
        上下文信息：
        {context}
        
        用户问题：
        {question}
        
        回答：
        """
        
        PROMPT = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        
        # 创建检索问答链
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",  # 使用 stuff 类型，将所有上下文拼接在一起
            retriever=self.vector_store.as_retriever(
                search_kwargs={"k": 3}  # 检索 Top-3 相关文本
            ),
            chain_type_kwargs={"prompt": PROMPT}
        )
        
        return qa_chain
    
    def run_query(self, query: str) -> str:
        """
        运行查询并返回回答
        
        Args:
            query: 用户查询
            
        Returns:
            回答文本
        """
        result = self.qa_chain.run(query)
        return result
    
    def get_relevant_documents(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """
        获取与查询相关的文档
        
        Args:
            query: 用户查询
            k: 返回的文档数量
            
        Returns:
            相关文档列表
        """
        docs = self.vector_store.similarity_search(query, k=k)
        return docs


def main():
    """主函数"""
    # 配置信息
    config = {
        # 向量数据库配置
        "vector_db_type": "chroma",  # 可选: 'chroma', 'faiss'
        "vector_db_path": "./my_vector_db",
        
        # 嵌入模型配置
        "embedding_model": "huggingface",  # 可选: 'openai', 'huggingface'
        "embedding_model_name": "sentence-transformers/all-MiniLM-L6-v2",
        
        # LLM 模型配置
        "llm_model": "huggingface",  # 可选: 'openai', 'huggingface'
        "llm_model_name": "deepseek-ai/deepseek-llm-7b-base",  # DeepSeek 模型
        
        # API 密钥（如果使用需要 API 密钥的模型）
        # "openai_api_key": "your-openai-api-key",
        # "huggingface_api_key": "your-huggingface-api-key",
    }
    
    # 创建 RAG 应用实例
    rag_app = RAGApplication(config)
    
    # 测试查询
    test_query = "请介绍一下 RAG 技术的原理"
    print(f"测试查询: {test_query}")
    
    # 获取相关文档
    relevant_docs = rag_app.get_relevant_documents(test_query)
    print("\n检索到的相关文档:")
    for i, doc in enumerate(relevant_docs, 1):
        print(f"\n文档 {i}:")
        print(f"内容: {doc.page_content[:200]}...")  # 只显示前 200 个字符
        if doc.metadata:
            print(f"元数据: {doc.metadata}")
    
    # 运行查询并获取回答
    answer = rag_app.run_query(test_query)
    print("\n模型回答:")
    print(answer)


if __name__ == "__main__":
    main()
