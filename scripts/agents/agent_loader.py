import os
import json
from typing import List
from .agent_registry import Agent, AgentRegistry

class AgentLoader:
    def __init__(self, agents_dir: str, registry: AgentRegistry):
        self.agents_dir = agents_dir
        self.registry = registry

    def load_agents(self):
        if not os.path.exists(self.agents_dir):
            print(f"[AgentLoader] Directory not found: {self.agents_dir}")
            return

        for filename in os.listdir(self.agents_dir):
            if filename.endswith(".json"):
                file_path = os.path.join(self.agents_dir, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    agent_name = data.get("agent_name")
                    if not agent_name:
                        print(f"[AgentLoader] Skipping {filename}: Missing agent_name")
                        continue

                    # Try to load Markdown instructions
                    instructions = ""
                    md_path = os.path.join(self.agents_dir, f"{agent_name}.md")
                    if os.path.exists(md_path):
                        with open(md_path, 'r', encoding='utf-8') as md_f:
                            instructions = md_f.read()
                    
                    data["instructions"] = instructions
                    agent = Agent.from_dict(data)
                    self.registry.register_agent(agent)
                except Exception as e:
                    print(f"[AgentLoader] Error loading {filename}: {e}")

if __name__ == "__main__":
    # For standalone testing
    from .agent_registry import AgentRegistry
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
    agents_dir = os.path.join(project_root, "agents")
    
    registry = AgentRegistry()
    loader = AgentLoader(agents_dir, registry)
    loader.load_agents()
    
    print(f"Total agents registered: {len(registry.list_all_agents())}")
