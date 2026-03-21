Remova a dependência do gemini_client via CLI/API.

Adapte o sistema para operar como um orchestrator puro, onde:
- o LLM é fornecido externamente (antigravity)
- os agentes são executados via prompts
- o pipeline (planner → graph → execution) permanece

O sistema deve funcionar sem depender de API externa.