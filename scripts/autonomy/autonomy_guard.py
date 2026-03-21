import os
import shutil
import json
from datetime import datetime
from typing import Dict, Any, Tuple, Optional
from .risk_evaluator import RiskEvaluator, RiskLevel

# Define project root
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
ARTIFACTS_DIR = os.path.join(project_root, "workspace", "artifacts")

class AutonomyGuard:
    def __init__(self):
        self.risk_evaluator = RiskEvaluator()
        self.log_file = os.path.join(project_root, "workspace", "logs", "autonomy.log")
        self.max_execution_steps = 10
        self.step_counter = {} # session_id -> count

    def _log_decision(self, action: str, params: Dict[str, Any], risk_level: str, decision: str, reasoning: str):
        timestamp = datetime.now().isoformat()
        log_entry = (
            f"[{timestamp}] [Action: {action}] [Risk: {risk_level}] [Decision: {decision}]\n"
            f"Params: {json.dumps(params)}\n"
            f"Reasoning: {reasoning}\n"
            f"{'-'*60}\n"
        )
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(log_entry)
        print(f"[AutonomyGuard] Decision: {decision} for {action} ({risk_level})")

    def _get_safe_path(self, path: str) -> str:
        """Ensures the path is inside the artifacts directory."""
        full_path = os.path.abspath(os.path.join(ARTIFACTS_DIR, path))
        if not full_path.startswith(ARTIFACTS_DIR):
            return ""
        return full_path

    def authorize_action(self, action: str, params: Dict[str, Any], session_id: str = "default") -> Tuple[str, Dict[str, Any]]:
        """
        Intercepts skill execution requests, evaluates risk, and enforces rules.
        Returns (decision, modified_params).
        """
        # --- Safety Rule: Execution Loop Prevention ---
        current_steps = self.step_counter.get(session_id, 0)
        if current_steps >= self.max_execution_steps:
            self._log_decision(action, params, RiskLevel.HIGH, "block", f"Infinite execution loop detected (steps={current_steps}).")
            return "block", {}
        self.step_counter[session_id] = current_steps + 1

        # --- Safety Rule: Boundary Check ---
        filename = params.get("filename")
        if filename:
             safe_path = self._get_safe_path(filename)
             if not safe_path:
                 self._log_decision(action, params, RiskLevel.HIGH, "block", f"Access denied: '{filename}' is outside artifacts directory.")
                 return "block", {}

        # --- Evaluate Risk ---
        risk_level, reasoning = self.risk_evaluator.evaluate(action, params)

        # --- Enforce Decisions ---
        if risk_level == RiskLevel.LOW:
            self._log_decision(action, params, risk_level, "allow", reasoning)
            return "allow", params

        if risk_level == RiskLevel.MEDIUM:
            self._log_decision(action, params, risk_level, "allow", reasoning + " (Logged for medium risk)")
            return "allow", params

        if risk_level == RiskLevel.HIGH:
            # Overwrite protection: Backup before allowing
            if action in ["write_file", "create_file"] and filename:
                path = os.path.abspath(os.path.join(ARTIFACTS_DIR, filename))
                if os.path.exists(path):
                    backup_path = f"{path}.bak"
                    shutil.copy2(path, backup_path)
                    self._log_decision(action, params, risk_level, "modify", f"Backup created as '{filename}.bak' before modification.")
                    return "modify", params

            self._log_decision(action, params, risk_level, "block", reasoning)
            return "block", {}

        return "block", {}
