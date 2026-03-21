# Agent Orchestration

Agent Orchestration is the process of coordinating multiple specialized AI agents, ensuring they collaborate efficiently within the automation pipeline without stepping on each other's toes.

## Orchestrating Agents

The orchestrator acts as a project manager for the AI workforce.
- **Dynamic Assignment:** As the Workflow Engine generates tasks, the Orchestrator assigns them to agents based on their registered competencies and current workload.
- **Context Handoff:** The most critical function of orchestration is managing the transfer of knowledge between agents. When the Backend Agent finishes building an API, the Orchestrator synthesizes the API contract and injects it into the Frontend Agent's context window, allowing work to continue without context loss.
- **Conflict Resolution:** If multiple agents need to modify shared files (e.g., `package.json`), the Orchestrator implements mutex locks, forcing agents to queue their modifications to prevent merge conflicts or corrupted state.

## Skill Chaining

To accomplish complex objectives, single skills are rarely enough. The Orchestrator manages "Skill Chaining," where the output of one skill automatically becomes the input for the next.
- **Pipeline Definition:** The Orchestrator builds a localized pipeline for the active agent. For instance, generating a robust backend endpoint might require chaining `api-scaffolder` -> `unit-test-generator` -> `sast-analyzer`.
- **Seamless State Passing:** The Orchestrator captures the structured JSON or code block output from the `api-scaffolder` and seamlessly injects it into the prompt of the `unit-test-generator`. The agent does not need to manually copy-paste or manage this transition; the Orchestrator handles the plumbing.
- **Validation Gates:** Between each chained skill, the Orchestrator can insert automated validation gates to ensure the output meets minimum quality thresholds before proceeding to the next skill in the chain.
