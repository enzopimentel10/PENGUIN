from typing import Optional
from .gemini_client import GeminiClient

class LLMAdapter:
    def __init__(self, provider: str = "gemini"):
        self.provider = provider
        if self.provider == "gemini":
            self.client = GeminiClient()
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")

    def generate_response(self, agent_name: str, prompt: str) -> str:
        """
        Receives agent prompt from agent_runner, formats the final prompt,
        calls the client, and returns the LLM response.
        """
        # Format the final prompt to ensure context is passed clearly
        final_prompt = f"System Context: You are operating as the agent '{agent_name}'.\n\n{prompt}"
        
        try:
            if self.provider == "gemini":
                return self.client.execute(final_prompt)
            return ""
        except Exception as e:
            print(f"[LLMAdapter] Error generating response from {self.provider}: {e}")
            return f"Error: LLM execution failed - {e}"
