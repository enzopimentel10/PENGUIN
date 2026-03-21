from typing import Dict, Any, Optional

class EvaluationResult:
    def __init__(self, action: str, feedback: str):
        self.action = action  # 'complete', 'continue', 'retry', 'refine'
        self.feedback = feedback

class ResultEvaluator:
    def evaluate(self, node_id: str, results: Dict[str, Any]) -> EvaluationResult:
        """
        Analyzes the execution result of a node and returns an action and feedback.
        """
        if not results:
            return EvaluationResult("retry", f"Node {node_id} produced no results.")

        status = results.get("status")
        output = results.get("output", "")

        if status == "failed":
            return EvaluationResult("retry", f"Execution failed for node {node_id}.")
        
        if not output:
            return EvaluationResult("retry", f"Node {node_id} produced an empty output.")

        # Logic to decide between 'continue' and 'complete'
        output_str = str(output)
        
        # Check for JSON "status": "complete"
        if isinstance(output, dict) and output.get("status") == "complete":
             return EvaluationResult("complete", f"Node {node_id} marked as complete via status field.")
             
        # Legacy checks or fallback
        if "TASK_COMPLETE" in output_str or "FINAL_ANSWER" in output_str:
            return EvaluationResult("complete", f"Node {node_id} marked as complete via keyword.")
        
        # If it's a success but doesn't have the completion flag, and we want autonomous iteration,
        # we can return 'continue' if it performed a skill.
        if isinstance(output, dict) and "skill_executions" in output:
             return EvaluationResult("continue", f"Node {node_id} executed skills. Continuing for next steps.")

        if status == "success":
             # If it's a raw string and we haven't found a completion flag, 
             # we might want to continue to ask for the next step, 
             # but to avoid infinite loops with raw text, we'll mark it complete unless it looks like an action.
             return EvaluationResult("complete", f"Node {node_id} execution successful (default to complete).")

        return EvaluationResult("refine", f"Node {node_id} result is ambiguous. Status: {status}")
