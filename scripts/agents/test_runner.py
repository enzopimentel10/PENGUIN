import os
import json

from scripts.agents.agent_registry import AgentRegistry
from scripts.agents.agent_loader import AgentLoader
from scripts.agents.agent_runner import AgentRunner

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.abspath(os.path.join(_SCRIPT_DIR, "..", ".."))

def test_runner():
    agents_dir = os.path.join(_PROJECT_ROOT, "agents")
    
    registry = AgentRegistry()
    loader = AgentLoader(agents_dir, registry)
    loader.load_agents()
    
    runner = AgentRunner(registry)
    
    test_input = {
        "instruction": "analyze the code structure"
    }
    
    result = runner.run_agent("analysis-agent", test_input)
    print(f"Result: {json.dumps(result, indent=2)}")

if __name__ == "__main__":
    test_runner()
