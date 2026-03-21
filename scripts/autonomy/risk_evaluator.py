import os
from typing import Dict, Any, Tuple

# Define project root
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
ARTIFACTS_DIR = os.path.join(project_root, "workspace", "artifacts")

class RiskLevel:
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class RiskEvaluator:
    def evaluate(self, action: str, params: Dict[str, Any]) -> Tuple[str, str]:
        """
        Analyzes requested actions and classifies risk level.
        Returns (risk_level, reasoning).
        """
        if not action:
            return RiskLevel.LOW, "No action specified — treated as low risk (missing_action)."

        filename = params.get("filename")
        path = ""
        if filename:
            path = os.path.abspath(os.path.join(ARTIFACTS_DIR, filename))

        if action == "list_directory":
            return RiskLevel.LOW, "List directory is a read-only operation with no side effects."
            
        if action == "read_file":
            return RiskLevel.LOW, f"Read file '{filename}' is a safe operation."

        if action == "create_file":
            if filename and os.path.exists(path):
                 return RiskLevel.HIGH, f"Attempting to create file '{filename}', but it already exists."
            return RiskLevel.LOW, f"Creating empty file '{filename}'."

        if action == "write_file":
            if filename and os.path.exists(path):
                 # Overwriting an existing file
                 return RiskLevel.HIGH, f"Overwriting existing file '{filename}' is a high-risk operation."
            return RiskLevel.MEDIUM, f"Writing content to a new file '{filename}'."

        return RiskLevel.MEDIUM, f"Unknown action '{action}' evaluated as medium risk."
