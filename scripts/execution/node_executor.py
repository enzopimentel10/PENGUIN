import os
import json
from datetime import datetime
from typing import Any, Dict, List

from scripts.agents.agent_registry import AgentRegistry
from scripts.agents.agent_loader import AgentLoader
from scripts.agents.agent_runner import AgentRunner
from scripts.cognition.cognitive_loop import CognitiveLoop
from scripts.cognition.context_engine import ContextEngine

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.abspath(os.path.join(_SCRIPT_DIR, "..", ".."))

class NodeExecutor:
    def __init__(self, log_dir: str = None):
        if log_dir is None:
            self.log_dir = os.path.join(_PROJECT_ROOT, "workspace", "logs")
        else:
            self.log_dir = log_dir
            
        os.makedirs(self.log_dir, exist_ok=True)
        
        # Load registry and agents
        self.registry = AgentRegistry()
        agents_dir = os.path.join(_PROJECT_ROOT, "agents")
        loader = AgentLoader(agents_dir, self.registry)
        loader.load_agents()
        
        # Initialize components
        self.runner = AgentRunner(self.registry)
        self.cognitive_loop = CognitiveLoop()
        self.context_engine = ContextEngine() # Shared blackboard
        
        self.max_retries = 3
        self.max_steps = 10
        
        self.iter_log_file = os.path.join(self.log_dir, "iteration.log")

    def _log(self, task_id: str, node_id: str, message: str):
        """Logs everything to workspace/logs/ (or provided log_dir)"""
        log_file = os.path.join(self.log_dir, f"{task_id}_execution.log")
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] [Node: {node_id}] {message}\n"
        
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)
        print(log_entry.strip())

    def _log_iteration(self, task_id: str, node_id: str, step: int, message: str):
        """Logs each step iteration to iteration.log"""
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] [Task: {task_id}] [Node: {node_id}] [Step: {step}] {message}\n"
        
        with open(self.iter_log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)

    def execute(self, task_id: str, node: Any) -> Dict[str, Any]:
        """
        Executes an individual node with iterative support and shared context.
        """
        node_id = node.node_id
        agent_name = node.agent
        original_instruction = node.instruction

        self._log(task_id, node_id, f"Starting iterative execution with agent: {agent_name}")
        
        execution_memory = [] # Store actions and results for context
        step_counter = 0
        retries = 0
        
        # Inject context from other nodes (Blackboard)
        blackboard_context = self.context_engine.get_formatted_context(exclude_node_id=node_id)
        current_instruction = f"{blackboard_context}\n\n### CURRENT TASK INSTRUCTION:\n{original_instruction}"

        while step_counter < self.max_steps:
            step_counter += 1
            
            # Use Agent Registry to resolve the agent
            agent = self.registry.get_agent_by_name(agent_name)
            if not agent:
                err_msg = f"Agent '{agent_name}' not found."
                self._log(task_id, node_id, err_msg)
                return {"status": "failed", "error": err_msg}

            # Prepare input data including memory for next iteration
            input_data = {
                "instruction": current_instruction,
                "task_id": task_id,
                "node_id": node_id,
                "step": step_counter,
                "history": execution_memory[-3:] # Pass only last 3 steps of current node execution
            }

            self._log_iteration(task_id, node_id, step_counter, f"Executing instruction: {current_instruction}")
            
            # Execute agent via runner
            result = self.runner.run_agent(agent_name, input_data)
            
            # Store in memory
            execution_memory.append({
                "step": step_counter,
                "instruction": current_instruction,
                "result": result
            })
            
            # Attach result temporarily for Cognitive Loop
            node.results = result
            
            # Send result to cognitive loop
            decision = self.cognitive_loop.process_node_result(None, node)
            self._log_iteration(task_id, node_id, step_counter, f"Decision: {decision}")

            if decision in ["complete", "accept"]:
                self._log(task_id, node_id, f"Execution completed at step {step_counter}")
                # Record the final result for future nodes to see
                self.context_engine.record_result(node_id, result)
                return result
                
            elif decision == "continue":
                self._log(task_id, node_id, f"Continuing to step {step_counter + 1}...")
                current_instruction = f"Continue the task based on the previous result: {json.dumps(result.get('output'))}"
                continue
                
            elif decision == "retry":
                retries += 1
                if retries <= self.max_retries:
                    self._log(task_id, node_id, f"Retrying step {step_counter} (Retry {retries}/{self.max_retries})")
                    step_counter -= 1
                    continue
                else:
                    err_msg = f"Node {node_id} failed after {self.max_retries} retries at step {step_counter}."
                    self._log(task_id, node_id, err_msg)
                    return {"status": "failed", "error": err_msg}
            
            elif decision == "refine":
                self._log(task_id, node_id, "Plan refinement required. Stopping iteration.")
                return result
            
            else:
                self._log(task_id, node_id, f"Unknown decision '{decision}'. Finishing.")
                return result

        err_msg = f"Node {node_id} reached max steps limit ({self.max_steps})."
        self._log(task_id, node_id, err_msg)
        return {"status": "failed", "error": err_msg, "memory": execution_memory}
