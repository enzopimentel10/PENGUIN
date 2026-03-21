# Agent Operating Model

This document outlines the collaborative framework for AI agents operating within the PEN.GUIN ecosystem, ensuring seamless cooperation and system stability.

## Agent Collaboration
- **Explicit Handoffs:** Agents must communicate state changes and required context when passing tasks to other agents. The Context Engine synthesizes this handoff, but the departing agent must leave a clear, structured summary of what was achieved and what remains.
- **Specialized Roles:** Agents must stay strictly within their defined domain of expertise. A frontend agent should not attempt to modify database schemas but should instead signal the kernel to assign a backend agent.
- **Conflict Resolution:** If two agents require access to the same resource or file concurrently, the kernel mediates access. Agents must be designed to handle resource locks gracefully and await their turn.

## Protecting System Architecture
- **Non-Destructive Operations:** Unless a task explicitly requires refactoring, agents must append or surgically modify existing structures rather than rewriting entire modules.
- **Validation Before Commitment:** Agents must utilize read-only operations (like parallel searching) to map dependencies before making architectural changes.
- **Fail-Safe Execution:** If an agent encounters an unrecoverable error or an ambiguous architectural boundary, it must halt execution, roll back its current isolated changes, and report the ambiguity to the Kernel or User rather than guessing.
- **Continuous Alignment:** Agents must frequently cross-reference the `ARCHITECTURE_GUARDRAILS.md` and `AI_ENGINEERING_RULES.md` to ensure their actions are aligned with global system constraints.
