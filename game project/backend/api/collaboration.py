from fastapi import APIRouter, Depends, BackgroundTasks, Query
from sqlalchemy.orm import Session
from typing import List
import uuid

from database import get_db
from services.agent_service import AgentCollaborationService
from prompts.agent_prompts import AGENTS

router = APIRouter()
agent_service = AgentCollaborationService()

task_status = {}

@router.post("/start")
async def start_collaboration(
    prompt: str = Query(..., description="用户需求"),
    agents: List[str] = Query(..., description="选择的Agent列表"),
    speed_mode: str = Query("fast", description="速度模式: fast/balanced"),
    background_tasks: BackgroundTasks = None
):
    task_id = str(uuid.uuid4())
    
    valid_agents = list(AGENTS.keys())
    for agent in agents:
        if agent not in valid_agents:
            return {"error": f"无效的Agent: {agent}"}
    
    task_status[task_id] = {
        "status": "processing",
        "progress": 0,
        "results": []
    }
    
    if background_tasks:
        background_tasks.add_task(
            agent_service.run_collaboration,
            task_id,
            prompt,
            agents,
            speed_mode,
            task_status
        )
    
    return {
        "task_id": task_id,
        "status": "processing",
        "estimated_time": 15 if speed_mode == "fast" else 30
    }

@router.get("/{task_id}/status")
async def get_collaboration_status(task_id: str):
    if task_id not in task_status:
        return {"status": "not_found"}
    
    return task_status[task_id]

@router.get("/agents/list")
async def get_agents_list():
    return {
        "agents": [
            {
                "key": key,
                "name": agent["name"],
                "avatar": agent["avatar"]
            }
            for key, agent in AGENTS.items()
        ]
    }
