import json
import re
from typing import Dict, Any, List, Optional

class EvaluationResult:
    def __init__(self, action: str, feedback: str):
        self.action = action  # 'complete', 'continue', 'retry', 'refine'
        self.feedback = feedback

class ResultEvaluator:
    """
    Strict evaluator: a node is only marked complete when the LLM returns
    an explicit JSON block containing {"status": "completed"} (or "complete").
    Loose keyword detection is intentionally removed.
    """

    _COMPLETED_VALUES = {"completed", "complete"}

    # -------------------------------------------------------------------
    # helpers
    # -------------------------------------------------------------------
    @staticmethod
    def _extract_json_blocks(text: str) -> List[dict]:
        """Return all valid JSON objects found inside a raw string."""
        blocks: List[dict] = []
        for match in re.finditer(r"\{[^{}]*\}", text):
            try:
                blocks.append(json.loads(match.group()))
            except (json.JSONDecodeError, ValueError):
                continue
        return blocks

    def _has_explicit_completion(self, output: Any) -> bool:
        """
        Returns True ONLY if:
          • output is a dict with output["status"] in {"completed", "complete"}, OR
          • output is a string containing a JSON block like {"status": "completed"}
        """
        # --- dict output (already parsed) ---
        if isinstance(output, dict):
            return str(output.get("status", "")).lower() in self._COMPLETED_VALUES

        # --- string output — look for embedded JSON ---
        if isinstance(output, str):
            for block in self._extract_json_blocks(output):
                if str(block.get("status", "")).lower() in self._COMPLETED_VALUES:
                    return True

        return False

    # -------------------------------------------------------------------
    # public API
    # -------------------------------------------------------------------
    def evaluate(self, node_id: str, results: Dict[str, Any]) -> EvaluationResult:
        """
        Analyzes the execution result of a node.
        Completion requires an explicit JSON status — never keyword guessing.
        """
        if not results:
            return EvaluationResult("retry", f"Node {node_id} produced no results.")

        status = results.get("status")
        output = results.get("output", "")

        if status == "failed":
            return EvaluationResult("retry", f"Execution failed for node {node_id}.")

        if not output:
            return EvaluationResult("retry", f"Node {node_id} produced an empty output.")

        # ── Strict completion gate ──────────────────────────────────
        if self._has_explicit_completion(output):
            return EvaluationResult(
                "complete",
                f"Node {node_id} completed — explicit JSON status found.",
            )

        # ── The node produced output but no completion signal ───────
        if isinstance(output, dict) and "skill_executions" in output:
            return EvaluationResult(
                "continue",
                f"Node {node_id} executed skills. Continuing for next steps.",
            )

        # Default: the node is NOT complete — keep iterating.
        return EvaluationResult(
            "continue",
            f"Node {node_id} produced output but no explicit completion signal.",
        )
