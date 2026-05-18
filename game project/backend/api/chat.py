from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
import uuid

from database import get_db
from models import Conversation, Message
from services.llm_service import LLMService
from prompts.agent_prompts import MAIN_CHAT_PROMPT

router = APIRouter()
llm_service = LLMService()

@router.post("/conversations")
async def create_conversation(
    title: str = Query(..., description="对话标题"),
    user_id: str = Query(..., description="用户ID"),
    mode: str = Query("single", description="对话模式"),
    db: Session = Depends(get_db)
):
    conv = Conversation(
        id=str(uuid.uuid4()),
        user_id=user_id,
        title=title,
        mode=mode
    )
    db.add(conv)
    db.commit()
    db.refresh(conv)
    return {"conversation_id": str(conv.id), "title": title, "mode": mode}

@router.get("/conversations/{user_id}")
async def get_conversations(user_id: str, db: Session = Depends(get_db)):
    conversations = db.query(Conversation).filter(
        Conversation.user_id == user_id,
        Conversation.is_archived == False
    ).order_by(Conversation.updated_at.desc()).all()
    
    return {
        "conversations": [
            {
                "id": str(conv.id),
                "title": conv.title,
                "mode": conv.mode,
                "updated_at": conv.updated_at.isoformat() if conv.updated_at else None
            }
            for conv in conversations
        ]
    }

@router.post("/conversations/{conv_id}/messages")
async def send_message(
    conv_id: str,
    content: str = Query(..., description="消息内容"),
    use_kb: bool = Query(True, description="是否使用知识库"),
    db: Session = Depends(get_db)
):
    user_msg = Message(
        conversation_id=conv_id,
        role="user",
        content=content
    )
    db.add(user_msg)
    
    messages = db.query(Message).filter(
        Message.conversation_id == conv_id
    ).order_by(Message.created_at).all()
    
    history = [{"role": m.role, "content": m.content} for m in messages]
    
    response = llm_service.chat(
        messages=history,
        system_prompt=MAIN_CHAT_PROMPT,
        temperature=0.7
    )
    
    ai_msg = Message(
        conversation_id=conv_id,
        role="assistant",
        content=response["content"],
        tokens_used=response.get("tokens_used", 0)
    )
    db.add(ai_msg)
    db.commit()
    
    return {
        "message_id": str(ai_msg.id),
        "role": "assistant",
        "content": response["content"],
        "tokens_used": ai_msg.tokens_used
    }

@router.get("/conversations/{conv_id}/messages")
async def get_messages(conv_id: str, db: Session = Depends(get_db)):
    messages = db.query(Message).filter(
        Message.conversation_id == conv_id
    ).order_by(Message.created_at).all()
    
    return {
        "messages": [
            {
                "id": str(msg.id),
                "role": msg.role,
                "agent_role": msg.agent_role,
                "content": msg.content,
                "created_at": msg.created_at.isoformat() if msg.created_at else None
            }
            for msg in messages
        ]
    }

@router.delete("/conversations/{conv_id}")
async def delete_conversation(conv_id: str, db: Session = Depends(get_db)):
    conv = db.query(Conversation).filter(Conversation.id == conv_id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="对话不存在")
    conv.is_archived = True
    db.commit()
    return {"message": "对话已删除"}
