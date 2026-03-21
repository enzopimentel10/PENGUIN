# CLI Command Interface

The PEN.GUIN CLI is the primary gateway for developers to interact with the AI ecosystem. This document defines the core command set and describes how each command interacts with the underlying automation and kernel layers.

## Core Commands

### 1. `penguin init`
**Description**: Initializes a new PEN.GUIN workspace in the current directory.
- **Action**: Creates the necessary directory structure (`.penguin/`, `core/`, `automation/`, `workspace/`, etc.) and populates baseline configuration files (`AGENT_OPERATING_MODEL.md`, `ARCHITECTURE_GUARDRAILS.md`).
- **Interaction**: Sets the local context for the `Context Engine` and prepares the environment for agent execution.

### 2. `penguin run <objective>`
**Description**: Triggers the execution of a specific objective or task.
- **Action**: Can accept a single task or a high-level feature description (e.g., `penguin run "build login page"`).
- **Interaction**:
    - For high-level objectives: Triggers the `Planner Agent` via the `Automation Layer` to generate a task graph.
    - For direct tasks: Submits a single `Task Node` to the `Execution Engine`.
    - Leverages the `Graph Scheduler` to assign tasks to available agents.

### 3. `penguin review [files]`
**Description**: Initiates an audit of the current workspace or specific files.
- **Action**: Analyzes code for quality, security, and adherence to engineering rules.
- **Interaction**: Dispatches tasks to the `Review Agent` and `Security Agent`. It retrieves analysis results from the `Artifact Manager` and synthesizes a report.

### 4. `penguin analyze`
**Description**: Performs a structural and architectural analysis of the project.
- **Action**: Maps dependencies, calculates complexity metrics, and assesses technical debt.
- **Interaction**: Triggers the `Architecture Agent` and `Repository Inspector`. It generates an architectural overview stored as a system artifact.

### 5. `penguin docs`
**Description**: Synchronizes documentation with the latest code changes.
- **Action**: Scans the codebase for API changes and updates relevant markdown documentation.
- **Interaction**: Triggers the `Documentation Agent` to ensure that docs in `docs/` and `workspace/` are up-to-date with the `Artifact System`.

### 6. `penguin status`
**Description**: Displays the current state of the active task graph and agent activity.
- **Action**: Provides a real-time view of `pending`, `running`, `completed`, and `failed` tasks.
- **Interaction**: Queries the `Execution Engine` and `Graph Scheduler` for the current status of the task registry.

### 7. `penguin logs [task_id]`
**Description**: Retrieves execution logs for the entire session or a specific task.
- **Action**: Outputs logs from agent runs, skill execution, and system errors.
- **Interaction**: Accesses the `Execution Logs` maintained in the `workspace/` directory, providing transparency into agent reasoning and tool calls.

## Summary Table

| Command | Layer Interaction | Primary Agent/Tool |
| :--- | :--- | :--- |
| `init` | Workspace Setup | CLI Internal |
| `run` | Automation/Kernel | Planner, Specialist Agents |
| `review` | Quality/Security | Review & Security Agents |
| `analyze` | Architecture | Architecture Agent, Inspector |
| `docs` | Documentation | Documentation Agent |
| `status` | State Monitoring | Execution Engine |
| `logs` | Observability | Execution Logs |
