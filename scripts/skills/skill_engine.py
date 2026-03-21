import os
import json
import re
import concurrent.futures
from datetime import datetime
from typing import Dict, Any, List, Optional
from .skill_registry import registry
from scripts.autonomy.autonomy_guard import AutonomyGuard

class SkillEngine:
    def __init__(self, log_dir: Optional[str] = None):
        if log_dir is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
            self.log_dir = os.path.join(project_root, "workspace", "logs")
        else:
            self.log_dir = log_dir
        
        os.makedirs(self.log_dir, exist_ok=True)
        self.guard = AutonomyGuard()
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)

    def _log_action(self, skill_name: str, params: Dict[str, Any], result: str):
        timestamp = datetime.now().isoformat()
        log_file = os.path.join(self.log_dir, "skill_execution.log")
        
        log_entry = (
            f"[{timestamp}] [Skill: {skill_name}]\n"
            f"Params: {json.dumps(params)}\n"
            f"Result: {result}\n"
            f"{'-'*40}\n"
        )
        
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(log_entry)
        print(f"[SkillEngine] Executed {skill_name}: {result}")

    def parse_actions(self, text: str) -> List[Dict[str, Any]]:
        """
        Parses JSON action blocks from LLM text by finding balanced braces.
        """
        actions = []
        start_idx = 0
        while True:
            # Find the next opening brace
            start_pos = text.find('{', start_idx)
            if start_pos == -1:
                break
            
            # Find the corresponding closing brace
            brace_count = 0
            end_pos = -1
            for i in range(start_pos, len(text)):
                if text[i] == '{':
                    brace_count += 1
                elif text[i] == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        end_pos = i
                        break
            
            if end_pos != -1:
                json_str = text[start_pos:end_pos+1]
                try:
                    data = json.loads(json_str)
                    if "action" in data:
                        actions.append(data)
                except json.JSONDecodeError:
                    pass # Not valid JSON, skip
                
                # Move start_idx forward to continue searching after this JSON block
                start_idx = end_pos + 1
            else:
                # No matching closing brace found for this opening brace
                start_idx = start_pos + 1
        
        return actions

    def execute_actions(self, llm_output: str) -> List[Dict[str, Any]]:
        """
        Receives LLM output, parses structured actions, identifies requested skill,
        executes it, and returns execution results.
        """
        actions = self.parse_actions(llm_output)
        results = []
        
        if not actions:
            print("[SkillEngine] No structured actions found in LLM output.")
            return []

        for action_data in actions:
            skill_name = action_data.get("action")
            params = action_data.get("parameters", {})
            
            # 1. Send action to autonomy_guard
            # 2. Receive decision: allow, modify, block
            decision, modified_params = self.guard.authorize_action(skill_name, params)
            
            if decision == "block":
                # block → skip execution
                err_msg = f"Action blocked by Autonomy Guard: {skill_name}"
                print(f"[SkillEngine] {err_msg}")
                results.append({
                    "action": skill_name,
                    "status": "blocked",
                    "error": err_msg
                })
                continue
            
            # allow → execute
            # modify → adjust parameters
            final_params = modified_params if decision == "modify" else params
            skill_func = registry.get_skill(skill_name)
            
            if skill_func:
                try:
                    # Execute skill with a 30-second timeout
                    future = self.executor.submit(skill_func, final_params)
                    result = future.result(timeout=30)
                    
                    self._log_action(skill_name, final_params, result)
                    results.append({
                        "action": skill_name,
                        "status": "success",
                        "result": result
                    })
                except concurrent.futures.TimeoutError:
                    err_msg = "Skill execution timed out (30s limit reached)."
                    self._log_action(skill_name, final_params, f"Error: {err_msg}")
                    results.append({
                        "action": skill_name,
                        "status": "error",
                        "error": err_msg
                    })
                except Exception as e:
                    err_msg = str(e)
                    self._log_action(skill_name, final_params, f"Error: {err_msg}")
                    results.append({
                        "action": skill_name,
                        "status": "error",
                        "error": err_msg
                    })
            else:
                err_msg = f"Unknown skill: {skill_name}"
                print(f"[SkillEngine] {err_msg}")
                results.append({
                    "action": skill_name,
                    "status": "error",
                    "error": err_msg
                })
        
        return results
