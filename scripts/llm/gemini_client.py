import os
import json
import sys
import hashlib
from datetime import datetime
from typing import Optional

class GeminiClient:
    """
    Handoff-based LLM Client (Pure Orchestrator).
    Emits prompts to files and expects responses from files.
    Decoupled from any external API.
    """
    def __init__(self, log_dir: Optional[str] = None):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
        
        self.handoff_dir = os.path.join(project_root, "workspace", "handoff")
        self.prompts_dir = os.path.join(self.handoff_dir, "prompts")
        self.responses_dir = os.path.join(self.handoff_dir, "responses")
        
        if log_dir is None:
            self.log_dir = os.path.join(project_root, "workspace", "logs")
        else:
            self.log_dir = log_dir
        
        os.makedirs(self.prompts_dir, exist_ok=True)
        os.makedirs(self.responses_dir, exist_ok=True)
        os.makedirs(self.log_dir, exist_ok=True)

    def _log_interaction(self, prompt: str, response: str, error: Optional[str] = None):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        log_file = os.path.join(self.log_dir, f"llm_handoff_{timestamp}.log")
        
        try:
            with open(log_file, "w", encoding="utf-8") as f:
                f.write("=== PROMPT ===\n")
                f.write(prompt + "\n\n")
                f.write("=== RESPONSE ===\n")
                f.write(response + "\n\n")
                if error:
                    f.write("=== ERROR ===\n")
                    f.write(error + "\n\n")
        except Exception as e:
            print(f"[GeminiClient] Failed to write log: {e}")

    def execute(self, prompt: str) -> str:
        """
        Emits the prompt and halts, or reads the response if already provided.
        Uses a stable MD5 hash for the prompt to identify handoff files.
        """
        prompt_hash = hashlib.md5(prompt.encode("utf-8")).hexdigest()
        prompt_file = os.path.join(self.prompts_dir, f"prompt_{prompt_hash}.txt")
        response_file = os.path.join(self.responses_dir, f"response_{prompt_hash}.txt")
        
        # 1. Check if response already exists
        if os.path.exists(response_file):
            with open(response_file, "r", encoding="utf-8") as f:
                response = f.read().strip()
            self._log_interaction(prompt, response)
            return response
            
        # 2. If not, write the prompt and halt
        with open(prompt_file, "w", encoding="utf-8") as f:
            f.write(prompt)
            
        print(f"\n[ORCHESTRATOR] Handoff required.")
        print(f"[ORCHESTRATOR] Prompt written to: {prompt_file}")
        print(f"[ORCHESTRATOR] Please provide response in: {response_file}")
        
        sys.exit(100)
