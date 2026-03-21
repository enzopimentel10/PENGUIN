import os
import json
import argparse
import re
from typing import Dict, Any, Optional, List
from scripts.llm.gemini_client import GeminiClient
from scripts.agents.agent_registry import AgentRegistry
from scripts.agents.agent_loader import AgentLoader
from scripts.skills.skill_registry import registry as skill_registry

PLANNER_PROMPT_TEMPLATE = """
You are the PENGUIN Task Planner. Your goal is to break down a high-level objective into a sequence of executable nodes (steps).
Each node must be assigned to a specific agent and have a clear instruction.

Objective: {objective}

Available Agents:
{agent_list}

Available Skills (Global):
{skill_list}

Return the plan ONLY as a JSON object with the following structure:
{{
  "task_id": "{task_id}",
  "nodes": [
    {{
      "node_id": "node_1",
      "agent": "agent-name",
      "instruction": "detailed instruction",
      "dependencies": []
    }},
    ...
  ]
}}

Guidelines:
1. Use descriptive node_ids (e.g., "analyze_code", "write_test").
2. Dependencies should be a list of node_ids that MUST be completed before this node can start.
3. Keep instructions concise but complete for the agent.
"""

class PlanGenerator:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        self.client = GeminiClient()
        
        # Initialize registries to inform the planner
        self.agent_registry = AgentRegistry()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
        agents_dir = os.path.join(project_root, "agents")
        loader = AgentLoader(agents_dir, self.agent_registry)
        loader.load_agents()

    def _get_agent_info(self) -> str:
        agents = []
        for name in self.agent_registry.list_all_agents():
            agent = self.agent_registry.get_agent_by_name(name)
            agents.append(f"- {name}: {agent.description} (Competencies: {', '.join(agent.competencies)})")
        return "\n".join(agents)

    def _get_skill_info(self) -> str:
        return "\n".join([f"- {s}" for s in skill_registry.list_skills()])

    def _extract_json(self, text: str) -> Optional[Dict[str, Any]]:
        """Attempts to extract JSON from LLM response, handling markdown blocks."""
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass
            
        match = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                pass
                
        match = re.search(r"(\{.*?\})", text, re.DOTALL)
        if match:
             try:
                return json.loads(match.group(1))
             except json.JSONDecodeError:
                pass
                
        return None

    def validate_plan(self, plan: Dict[str, Any]) -> bool:
        """Validates the structure of the generated plan."""
        if not isinstance(plan, dict):
            return False
        if "task_id" not in plan or "nodes" not in plan:
            return False
        if not isinstance(plan["nodes"], list):
            return False
        for node in plan["nodes"]:
            if not all(k in node for k in ("node_id", "agent", "instruction")):
                return False
        return True

    def generate_plan(self, task_file: str) -> str:
        if not os.path.exists(task_file):
            print(f"Error: Task file not found at {task_file}")
            return ""
            
        try:
            with open(task_file, 'r', encoding='utf-8') as f:
                task_data = json.load(f)
        except Exception as e:
            print(f"Error reading task file: {e}")
            return ""
        
        task_id = task_data.get("task_id", task_data.get("id"))
        objective = task_data.get("objective", task_data.get("payload", {}).get("instruction", ""))
        
        if not task_id:
            filename = os.path.basename(task_file)
            task_id, _ = os.path.splitext(filename)
            
        prompt = PLANNER_PROMPT_TEMPLATE.format(
            objective=objective, 
            task_id=task_id,
            agent_list=self._get_agent_info(),
            skill_list=self._get_skill_info()
        )
        
        print(f"[*] Calling LLM to generate plan for task: {task_id}")
        llm_response = self.client.execute(prompt)
        
        plan = self._extract_json(llm_response)
        
        if not plan or not self.validate_plan(plan):
            print("Error: Failed to generate a valid plan from LLM response.")
            return ""
        
        # Backward compatibility: ensure 'steps' alias exists if any consumer still uses it
        plan["steps"] = plan["nodes"]
        
        os.makedirs(self.output_dir, exist_ok=True)
        plan_filename = f"{task_id}_plan.json"
        plan_file_path = os.path.join(self.output_dir, plan_filename)
        
        try:
            with open(plan_file_path, 'w', encoding='utf-8') as f:
                json.dump(plan, f, indent=2)
            print(f"Execution plan successfully generated and saved to: {plan_file_path}")
            return plan_file_path
        except Exception as e:
            print(f"Error writing plan file: {e}")
            return ""

def main():
    parser = argparse.ArgumentParser(description="PEN.GUIN Plan Generator")
    parser.add_argument("--task-file", required=True, help="Path to the task definition file")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
    default_output_dir = os.path.join(project_root, "workspace", "plan")
    
    parser.add_argument("--output-dir", default=default_output_dir, help="Directory to save the execution plan")
    
    args = parser.parse_args()
    
    generator = PlanGenerator(args.output_dir)
    generator.generate_plan(args.task_file)

if __name__ == "__main__":
    main()
