from concurrent.futures import ThreadPoolExecutor, as_completed
from services.llm_service import LLMService
from prompts.agent_prompts import AGENTS

class AgentCollaborationService:
    def __init__(self):
        self.llm = LLMService()
    
    def run_single_agent(self, agent_key: str, prompt: str, quick_mode: bool):
        agent = AGENTS[agent_key]
        
        agent_prompt = f"""用户需求：{prompt}
        
请从您的专业角度给出建议。"""
        
        if quick_mode:
            agent_prompt += "\n请简洁回答（100-200字）。"
        
        response = self.llm.chat(
            messages=[{"role": "user", "content": agent_prompt}],
            system_prompt=agent["system_prompt"],
            temperature=0.5 if quick_mode else 0.7
        )
        
        return {
            "agent": agent_key,
            "content": response["content"]
        }
    
    def run_collaboration(self, task_id: str, prompt: str, 
                         agents: list, speed_mode: str, task_status: dict):
        quick_mode = speed_mode == "fast"
        results = []
        
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {
                executor.submit(self.run_single_agent, agent, prompt, quick_mode): agent
                for agent in agents
            }
            
            completed = 0
            for future in as_completed(futures):
                result = future.result()
                results.append(result)
                completed += 1
                
                task_status[task_id] = {
                    "status": "processing",
                    "progress": int((completed / len(agents)) * 100),
                    "current_agent": result["agent"],
                    "results": results.copy()
                }
        
        ordered_results = []
        for agent in agents:
            for result in results:
                if result["agent"] == agent:
                    ordered_results.append(result)
                    break
        
        task_status[task_id] = {
            "status": "completed",
            "progress": 100,
            "results": ordered_results
        }
