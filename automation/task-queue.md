# Task Queue Management

The Task Queue is the central nervous system for workload distribution within the PEN.GUIN ecosystem. It ensures that multiple agents can operate concurrently without stepping on each other's toes, and that dependencies between tasks are strictly respected.

## Queue Structure and State

The queue is primarily managed through the `/workspace/tasks` directory, where each task file maintains a specific state:
- **Pending:** The task has been classified and is waiting for an available, capable agent.
- **Assigned:** An agent has been selected by the `Agent Router`, but execution has not yet begun.
- **Active (Locked):** An agent is currently executing the task. A mutex lock is applied to prevent other agents from claiming it.
- **Blocked:** The task cannot proceed because it depends on the output of another task that is not yet complete.
- **Completed:** The task has been successfully executed and validated.
- **Failed:** The task failed execution beyond the retry limit and requires escalation.

## Dependency Graph and Distribution

Tasks are rarely entirely independent. The Task Queue operates as a Directed Acyclic Graph (DAG):
1. **Dependency Parsing:** When the `Task Classifier` generates sub-tasks, it defines their dependencies (e.g., "Build Frontend Login" depends on "Build Auth API Endpoint").
2. **Topological Sorting:** The queue management system sorts tasks topologically. Only tasks with zero unresolved dependencies are marked as `Pending` and made available for the `Agent Router` to distribute.
3. **Event-Driven Unblocking:** When the Backend Agent completes the "Auth API Endpoint" task, it generates an artifact. The `Workflow Engine` detects this completion, updates the queue graph, and transitions the "Build Frontend Login" task from `Blocked` to `Pending`.

## Distribution Logic (Agent Router)

The Task Queue does not "push" work to agents; rather, the `Agent Router` acts as a matchmaker:
- **Availability Polling:** Agents in the `Idle` state signal their availability to the Router.
- **Competency Matching:** The Router scans all `Pending` tasks. It evaluates the required tags (e.g., `Python`, `Database`) against the idle agents' competencies.
- **Priority Scoring:** If multiple tasks are pending, the queue prioritizes them based on dependency weight (tasks that block many downstream tasks are prioritized) and user-defined urgency.
- **Assignment and Lock:** The Router pairs the highest-priority matching task with the idle agent, updates the task state to `Assigned`, and triggers the agent's transition to the `Task Received` lifecycle phase.
