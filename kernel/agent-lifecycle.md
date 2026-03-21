# Agent Lifecycle

This document defines the continuous lifecycle states an AI agent moves through within the PEN.GUIN ecosystem, from the moment it is instantiated to the successful completion of an objective.

## 1. Idle (Standby State)
When an agent is initialized by the Kernel, it enters the `Idle` state. It consumes minimal resources, actively polling the `Agent Router` and watching the `/workspace/tasks` queue for assigned work that matches its specific competency matrix.

## 2. Task Received
An event triggers a state change. The `Agent Router` assigns a discrete sub-task (e.g., `frontend-task-004.json`) to the agent. The agent transitions to an active state and a new session file is generated in `/workspace/sessions` to track its progress.

## 3. Task Analysis
The agent reads the task payload. It parses the overarching objective, the specific requirements of its sub-task, and the defined success criteria. If the task is ambiguous, the agent may query the Kernel for clarification, but primarily relies on the structured prompt provided.

## 4. Context Retrieval
Before acting, the agent must understand the environment. The `Context Engine` automatically injects the most relevant workspace state (e.g., existing API contracts, related file contents, user preferences from the `Memory Model`) into the agent's context window. If the provided context is insufficient, the agent uses read-only tools like the `Repository Inspector` to gather more information.

## 5. Skill Selection & Provisioning
Based on the task analysis, the `Skill Router` dynamically provisions the agent with necessary tools from the `Skill Registry`. The agent's prompt is updated to include instructions on how to invoke these specific skills (e.g., receiving instructions on how to use `component-generator` via the `Skill Loader`).

## 6. Execution (The Action Phase)
This is the core operational phase. The agent formulates a plan and executes it step-by-step.
- It uses the provisioned skills or standard tools (`Task Executor`, file writers) to mutate the workspace state.
- Every action and its output (stdout, errors) is logged to the active session.
- The agent iteratively adjusts its approach based on tool feedback (e.g., fixing a syntax error reported by a linter).

## 7. Review & Validation
An agent does not declare a task complete simply by finishing its code generation. It must empirically validate its work.
- It invokes test suites or validation gates (e.g., `a11y-validator`, `unit-test-generator`).
- If validation fails, the agent automatically loops back to the **Execution** phase with the error trace as new context.
- Once internal validation passes, the output may be routed to a specialized `Review Agent` for external code-quality checks.

## 8. Completion & Handoff
Once all validations pass, the task is marked complete.
- The agent writes its final, verified output to the `/workspace/artifacts/` directory.
- It generates a "Handoff Summary" detailing what was achieved, which the Kernel synthesizes for the next agent in the pipeline.
- The active session is closed, archived into the `Memory Model`, and the agent returns to the **Idle** state, awaiting its next assignment.
