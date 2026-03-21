import os
import sys
import json
from typing import Dict, Any, Optional

from .agent_registry import Agent, AgentRegistry
from scripts.llm.llm_adapter import LLMAdapter
from scripts.skills.skill_engine import SkillEngine

class AgentRunner:
    def __init__(self, registry: AgentRegistry):
        self.registry = registry
        self.llm_adapter = LLMAdapter(provider="gemini")
        self.skill_engine = SkillEngine()

    def run_agent(self, agent_name: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes an agent by name with the given input data.
        """
        agent = self.registry.get_agent_by_name(agent_name)
        if not agent:
            return {
                "status": "failed",
                "error": f"Agent '{agent_name}' not found in registry."
            }

        # Build the prompt
        prompt = self._build_prompt(agent, input_data)
        
        print(f"[AgentRunner] Running agent: {agent_name} via LLM Adapter")

        # Execute agent via LLM Adapter
        llm_output = self.llm_adapter.generate_response(agent_name, prompt)
        
        # 1. try to parse response as JSON and execute skills if any
        # 2. if it contains an action, execute skill
        skill_results = self.skill_engine.execute_actions(llm_output)
        
        # Determine final output
        if skill_results:
            # If we have skill results, we return those
            # For multiple skills, we return a list of results
            final_output = {
                "llm_response": llm_output,
                "skill_executions": skill_results
            }
        else:
            # 3. if not, return raw response
            final_output = llm_output
        
        return {
            "status": "success",
            "agent": agent_name,
            "output": final_output,
            "prompt_used": prompt
        }

    def _build_prompt(self, agent: Agent, input_data: Dict[str, Any]) -> str:
        """
        Constructs the prompt using agent instructions and input data.
        """
        prompt = f"### AGENT: {agent.agent_name}\n"
        prompt += f"### DESCRIPTION: {agent.description}\n\n"
        prompt += "### INSTRUCTIONS:\n"
        prompt += f"{agent.instructions}\n\n"
        prompt += "### INPUT:\n"
        prompt += json.dumps(input_data, indent=2)
        prompt += "\n\n### TASK: Execute the instruction based on the input above."
        
        return prompt
