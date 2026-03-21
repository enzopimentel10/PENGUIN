# Architecture Guardrails

These guardrails ensure the structural integrity of the PEN.GUIN repository is maintained as multiple agents operate concurrently.

## Architecture Protection
- **Layer Isolation:** Agents must respect boundaries between the kernel, agents, workspace, tools, and scripts. Direct, undocumented dependencies between decoupled modules are strictly prohibited.
- **Kernel Immutability:** The `/kernel` directory is the core orchestration engine. Agents must not modify kernel files unless explicitly directed by a high-privilege administrative prompt.
- **State Management:** Agents must not bypass the Context Engine or Memory Model for state persistence. All shared state must be routed through official kernel channels.

## Folder Structure
- `/kernel`: Core system orchestrator and context/memory engines.
- `/agents`: Specialized agent definitions and behaviors.
- `/workspace`: The active environment where project work is executed.
- `/docs`: Centralized system and project documentation.
- `/tools`: Reusable custom tools and scripts accessible by agents.
- `/scripts`: Administrative and environmental setup utilities.
- `/core`: Governance, rules, and fundamental operating guardrails.

Agents must not create top-level directories without explicit user authorization. All work must be scoped within existing structural boundaries.
