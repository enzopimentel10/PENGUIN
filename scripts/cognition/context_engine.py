import os
import json
from typing import Dict, Any, List, Optional

class ContextEngine:
    """
    Manages the shared state (Blackboard) between agents in a task graph.
    Allows agents to 'see' what previous agents have discovered.
    """
    def __init__(self):
        self.results_manifest: Dict[str, Any] = {} # node_id -> results

    def record_result(self, node_id: str, results: Dict[str, Any]):
        """Saves the result of a node execution to the blackboard."""
        self.results_manifest[node_id] = results

    def get_all_results(self) -> Dict[str, Any]:
        """Returns the entire results manifest."""
        return self.results_manifest

    def get_formatted_context(self, exclude_node_id: Optional[str] = None) -> str:
        """
        Returns a string representation of previous results for prompt injection.
        """
        if not self.results_manifest:
            return "No previous findings."

        context_parts = ["### PREVIOUS FINDINGS (Blackboard):"]
        
        for node_id, results in self.results_manifest.items():
            if node_id == exclude_node_id:
                continue
                
            # Extract the actual output content
            output = results.get("output", "No output.")
            
            # If output is complex (e.g. from skill executions), summarize it
            if isinstance(output, dict):
                skill_summary = []
                if "skill_executions" in output:
                    for sexec in output["skill_executions"]:
                        action = sexec.get("action")
                        status = sexec.get("status")
                        res = sexec.get("result", sexec.get("error", ""))
                        skill_summary.append(f"- Executed {action} ({status}): {res}")
                
                output_text = "\n".join(skill_summary) if skill_summary else json.dumps(output)
            else:
                output_text = str(output)

            context_parts.append(f"#### Results from Node: {node_id}\n{output_text}")

        return "\n\n".join(context_parts)

    def clear(self):
        """Resets the context engine for a new task."""
        self.results_manifest = {}
