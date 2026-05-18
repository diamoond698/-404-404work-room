from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
import uuid

from database import get_db
from models import KnowledgeBase

router = APIRouter()

@router.post("/")
async def add_knowledge(
    title: str = Query(..., description="知识标题"),
    content: str = Query(..., description="知识内容"),
    category: str = Query(None, description="分类"),
    user_id: str = Query(..., description="用户ID"),
    is_public: bool = Query(False, description="是否公开"),
    db: Session = Depends(get_db)
):
    kb = KnowledgeBase(
        id=str(uuid.uuid4()),
        user_id=user_id,
        title=title,
        content=content,
        category=category,
        is_public=is_public
    )
    db.add(kb)
    db.commit()
    db.refresh(kb)
    return {"kb_id": str(kb.id), "title": title}

@router.get("/")
async def get_knowledge_list(
    user_id: str = Query(..., description="用户ID"),
    category: str = Query(None, description="分类过滤"),
    db: Session = Depends(get_db)
):
    query = db.query(KnowledgeBase).filter(
        (KnowledgeBase.user_id == user_id) | (KnowledgeBase.is_public == True)
    )
    
    if category:
        query = query.filter(KnowledgeBase.category == category)
    
    knowledge_list = query.order_by(KnowledgeBase.created_at.desc()).all()
    
    return {
        "knowledge_list": [
            {
                "id": str(kb.id),
                "title": kb.title,
                "content": kb.content[:200] + "..." if len(kb.content) > 200 else kb.content,
                "category": kb.category,
                "created_at": kb.created_at.isoformat() if kb.created_at else None
            }
            for kb in knowledge_list
        ]
    }

@router.post("/search")
async def search_knowledge(
    query: str = Query(..., description="搜索关键词"),
    top_k: int = Query(5, description="返回数量"),
    db: Session = Depends(get_db)
):
    all_knowledge = db.query(KnowledgeBase).all()
    
    results = []
    for kb in all_knowledge:
        if query.lower() in kb.content.lower() or query.lower() in kb.title.lower():
            results.append({
                "id": str(kb.id),
                "title": kb.title,
                "content": kb.content,
                "similarity": 0.8
            })
    
    return {"results": results[:top_k]}

@router.delete("/{kb_id}")
async def delete_knowledge(kb_id: str, db: Session = Depends(get_db)):
    kb = db.query(KnowledgeBase).filter(KnowledgeBase.id == kb_id).first()
    if kb:
        db.delete(kb)
        db.commit()
    return {"message": "删除成功"}
