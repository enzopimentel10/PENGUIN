# Register Agent Workflow (`register-agent.sh`)

This script integrates a new or updated AI agent into the PEN.GUIN ecosystem, making it available to the Agent Router.

## Workflow Overview
When `register-agent --path path/to/agent.md` is executed, the following sequence occurs:

1. **Manifest Parsing:** The script parses the agent's definition file (e.g., `agents/frontend-agent.md`). It extracts the agent's identifier, core responsibilities, specific task capabilities, and interaction rules.
2. **Competency Mapping:** The extracted data is translated into a standardized schema (JSON/YAML) representing the agent's competencies (e.g., domains: `Client-Side`, `UI`).
3. **Kernel Handshake:** The script sends a registration payload to the running AI Kernel.
4. **Registry Update:** The Kernel updates its `Agent Registry` in memory, adding the new agent to the pool of available resources.
5. **Router Synchronization:** The `Agent Router` recalculates its routing tables. If a newly registered agent possesses a higher specialization for certain sub-tasks than existing agents, future task assignments will dynamically route to the new agent.
