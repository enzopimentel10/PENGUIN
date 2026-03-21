from typing import Dict, Any, Optional

from scripts.graph.task_graph import TaskNode, NodeStatus
from .result_evaluator import ResultEvaluator, EvaluationResult

class CognitiveLoop:
    def __init__(self):
        self.evaluator = ResultEvaluator()

    def process_node_result(self, graph: Optional[Any], node: TaskNode) -> str:
        """
        Evaluates a node result and updates its status or initiates a retry/refinement/iteration.
        Returns the action taken ('complete', 'continue', 'retry', 'refine').
        """
        print(f"[CognitiveLoop] Evaluating results for node: {node.node_id}")
        
        if node.results is None or node.results.get("output") is None:
            print(f"[CognitiveLoop] No results or output found for node {node.node_id}. Retrying.")
            return "retry"
            
        evaluation = self.evaluator.evaluate(node.node_id, node.results)
        print(f"[CognitiveLoop] Action: {evaluation.action} - Feedback: {evaluation.feedback}")

        # In iterative execution, we don't always change status here, NodeExecutor handles it.
        # But for legacy/simple execution:
        if evaluation.action == "complete" or evaluation.action == "accept":
            node.status = NodeStatus.COMPLETED
        elif evaluation.action == "retry":
            print(f"[CognitiveLoop] Retrying node {node.node_id}...")
            # node.status = NodeStatus.PENDING # NodeExecutor will handle status if retrying
        elif evaluation.action == "refine":
            print(f"[CognitiveLoop] Node {node.node_id} requires plan refinement.")
            node.status = NodeStatus.BLOCKED 
        
        return evaluation.action
