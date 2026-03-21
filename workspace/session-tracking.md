# Session Tracking System

The Session Tracking System acts as the "flight data recorder" for the PEN.GUIN ecosystem. While the `/workspace/tasks/` directory acts as a queue and `/workspace/artifacts/` acts as the final ledger of results, the `/workspace/sessions/` directory captures the real-time, chronological narrative of *how* a task was executed.

## Purpose of Sessions

A session represents a continuous, stateful execution thread dedicated to a specific task. By tracking execution chronologically, the system ensures:
- **Observability:** Human operators can audit exactly what an agent did and why it made specific decisions.
- **Resiliency:** If a process crashes or is interrupted, the `Workflow Engine` can parse the session file to resume execution from the last known good state.
- **Context Handoff:** Sequential agents can read a session to understand the immediate history of the workspace before picking up a task.

## Session Record Structure

Each session systematically records comprehensive data about the execution lifecycle. A session file (typically a structured JSON or YAML file appended to continuously) contains the following schemas:

### 1. Task Information
Every session begins by anchoring itself to the objective.
- `session_id`: Unique identifier for the execution thread.
- `task_id`: Link back to the specific task in `/workspace/tasks/`.
- `objective_summary`: A brief description of the goal.
- `status`: Current state (`Initializing`, `Running`, `Blocked`, `Completed`, `Failed`).

### 2. Agents Involved
A session tracks the actors operating within its scope.
- `primary_agent`: The core agent assigned to the task (e.g., `frontend-agent`).
- `consulting_agents`: Any agents invoked dynamically for review or assistance (e.g., a `review-agent` called in to check a specific function).

### 3. Skills Used
To monitor capability utilization, the session logs every skill provisioned and invoked.
- `provisioned_skills`: List of skills from the `Skill Registry` made available to the agent for this task.
- `skill_invocations`: An array tracking which skills were actually used, including the exact parameters passed to the `Skill Loader` and the timestamp of invocation.

### 4. Artifacts Generated
As the agent produces outputs, the session links to them.
- `intermediate_artifacts`: Pointers to temporary files or drafts created during the execution loop.
- `final_artifacts`: Pointers (UUIDs) to the verified outputs saved in `/workspace/artifacts/` upon task completion.

### 5. Execution Logs (The Cognitive Trail)
This is the core of the session—the step-by-step audit trail of the execution loop.
- `observations`: The context or tool output the agent ingested.
- `reasoning`: The agent's internal thought process (e.g., "The test failed with a syntax error, I need to add a missing comma.").
- `actions`: The specific tool calls executed (e.g., `replace`, `run_shell_command`).
- `tool_outputs`: The raw `stdout`, `stderr`, and exit codes resulting from the agent's actions.

## Storage in `/workspace/sessions/`

The `/workspace/sessions/` folder is designed for high-throughput I/O and easy retrieval.

1. **File Convention:** When a task begins, a new file is created, formatted as `session-<task_id>.jsonl` (JSON Lines). This append-only format ensures that even if the system crashes abruptly, the logs written up to the point of failure remain uncorrupted.
2. **Directory Partitioning:** In a highly active environment, sessions are partitioned into subdirectories by date (e.g., `/workspace/sessions/2026-03-15/`) to prevent folder bloat.
3. **Archival:** Active sessions are kept in the root of the sessions folder. Once a session transitions to `Completed` or `Failed` (and the escalation is resolved), the `Workflow Engine` compresses the session data and archives it into the `Memory Model` for long-term historical analysis, freeing up active workspace storage.
