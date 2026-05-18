from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import uuid

from database import get_db
from models import User

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register")
async def register(
    username: str = Query(..., description="用户名"),
    email: str = Query(..., description="邮箱"),
    password: str = Query(..., description="密码"),
    db: Session = Depends(get_db)
):
    existing = db.query(User).filter(
        (User.username == username) | (User.email == email)
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="用户已存在")
    
    hashed_password = pwd_context.hash(password)
    
    user = User(
        id=str(uuid.uuid4()),
        username=username,
        email=email,
        password_hash=hashed_password
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return {
        "user_id": str(user.id),
        "username": username,
        "email": email
    }

@router.post("/login")
async def login(
    username: str = Query(..., description="用户名"),
    password: str = Query(..., description="密码"),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == username).first()
    
    if not user or not pwd_context.verify(password, user.password_hash):
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    
    if not user.is_active:
        raise HTTPException(status_code=403, detail="用户已被禁用")
    
    return {
        "user_id": str(user.id),
        "username": user.username,
        "email": user.email,
        "api_credits": user.api_credits,
        "subscription_tier": user.subscription_tier
    }

@router.get("/profile/{user_id}")
async def get_profile(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    return {
        "user_id": str(user.id),
        "username": user.username,
        "email": user.email,
        "avatar_url": user.avatar_url,
        "api_credits": user.api_credits,
        "subscription_tier": user.subscription_tier,
        "created_at": user.created_at.isoformat() if user.created_at else None
    }
