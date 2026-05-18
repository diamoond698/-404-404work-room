from fastapi import FastAPI, APIRouter, HTTPException, Query, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, String, Text, Integer, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
from passlib.context import CryptContext
from concurrent.futures import ThreadPoolExecutor, as_completed
import uvicorn
import os
import requests
import uuid
from typing import List

try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./game_ai.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    api_credits = Column(Integer, default=1000)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"))
    title = Column(String(200), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Message(Base):
    __tablename__ = "messages"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = Column(String(36), ForeignKey("conversations.id"))
    role = Column(String(20), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class LLMService:
    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_API_KEY", "")
        self.base_url = "https://api.deepseek.com/v1"
    
    def chat(self, messages, system_prompt=None, temperature=0.7):
        full_messages = []
        if system_prompt:
            full_messages.append({"role": "system", "content": system_prompt})
        full_messages.extend(messages)
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                json={"model": "deepseek-chat", "messages": full_messages, "temperature": temperature},
                timeout=60
            )
            result = response.json()
            if "choices" in result and len(result["choices"]) > 0:
                return {"content": result["choices"][0]["message"]["content"], "tokens_used": 0}
        except Exception as e:
            print(f"LLM Error: {e}")
        return {"content": "抱歉，我遇到了一些问题...", "tokens_used": 0}

AGENTS = {
    "designer": {"name": "游戏设计师", "avatar": "👩‍🎨", "system_prompt": "你是资深游戏设计师，专注于AI系统设计。"},
    "coder": {"name": "代码专家", "avatar": "🧑‍💻", "system_prompt": "你是Unity/Unreal专家，精通游戏AI编程。"},
    "perf": {"name": "性能专家", "avatar": "🚀", "system_prompt": "你是游戏性能优化专家。"},
    "tester": {"name": "测试专家", "avatar": "🔬", "system_prompt": "你是QA测试专家，擅长发现AI系统问题。"}
}

task_status = {}

app = FastAPI(title="Game AI Agent API", version="1.0.0")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/")
async def root():
    return {"message": "Game AI Agent API", "version": "1.0.0", "docs": "/docs"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/api/v1/user/register")
async def register(username: str = Query(...), email: str = Query(...), password: str = Query(...)):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = pwd_context.hash(password)
    db = SessionLocal()
    user = User(id=str(uuid.uuid4()), username=username, email=email, password_hash=hashed_password)
    db.add(user)
    db.commit()
    return {"user_id": user.id, "username": username}

@app.post("/api/v1/chat/conversations")
async def create_conversation(title: str = Query(...), user_id: str = Query(...)):
    db = SessionLocal()
    conv = Conversation(id=str(uuid.uuid4()), user_id=user_id, title=title)
    db.add(conv)
    db.commit()
    return {"conversation_id": conv.id, "title": title}

@app.post("/api/v1/chat/conversations/{conv_id}/messages")
async def send_message(conv_id: str, content: str = Query(...)):
    llm = LLMService()
    db = SessionLocal()
    
    user_msg = Message(conversation_id=conv_id, role="user", content=content)
    db.add(user_msg)
    
    messages = db.query(Message).filter(Message.conversation_id == conv_id).order_by(Message.created_at).all()
    history = [{"role": m.role, "content": m.content} for m in messages]
    
    response = llm.chat(history, system_prompt="你是专业的游戏AI顾问。")
    
    ai_msg = Message(conversation_id=conv_id, role="assistant", content=response["content"])
    db.add(ai_msg)
    db.commit()
    
    return {"message_id": ai_msg.id, "role": "assistant", "content": response["content"]}

@app.get("/api/v1/collaboration/agents/list")
async def get_agents_list():
    return {"agents": [{"key": k, "name": v["name"], "avatar": v["avatar"]} for k, v in AGENTS.items()]}

def run_single_agent(agent_key, prompt, quick_mode):
    agent = AGENTS[agent_key]
    llm = LLMService()
    agent_prompt = f"用户需求：{prompt}\n请从您的专业角度给出建议。"
    if quick_mode:
        agent_prompt += "\n请简洁回答（100-200字）。"
    response = llm.chat([{"role": "user", "content": agent_prompt}], system_prompt=agent["system_prompt"])
    return {"agent": agent_key, "content": response["content"]}

@app.post("/api/v1/collaboration/start")
async def start_collaboration(prompt: str = Query(...), agents: List[str] = Query(...), speed_mode: str = Query("fast"), background_tasks: BackgroundTasks = None):
    task_id = str(uuid.uuid4())
    task_status[task_id] = {"status": "processing", "progress": 0, "results": []}
    
    def run_collab():
        quick_mode = speed_mode == "fast"
        results = []
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {executor.submit(run_single_agent, agent, prompt, quick_mode): agent for agent in agents}
            completed = 0
            for future in as_completed(futures):
                result = future.result()
                results.append(result)
                completed += 1
                task_status[task_id]["progress"] = int((completed / len(agents)) * 100)
                task_status[task_id]["results"] = results.copy()
        
        ordered_results = []
        for agent in agents:
            for result in results:
                if result["agent"] == agent:
                    ordered_results.append(result)
                    break
        task_status[task_id] = {"status": "completed", "progress": 100, "results": ordered_results}
    
    if background_tasks:
        background_tasks.add_task(run_collab)
    
    return {"task_id": task_id, "status": "processing"}

@app.get("/api/v1/collaboration/{task_id}/status")
async def get_collaboration_status(task_id: str):
    return task_status.get(task_id, {"status": "not_found"})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
