# Workflow Engine

The Workflow Engine is the core automation layer of the PEN.GUIN ecosystem. It provides the infrastructure required to run a continuous, scalable AI-driven development pipeline without constant human intervention.

## Workflow Automation

The engine transforms discrete tasks into an automated, end-to-end pipeline.
- **Event-Driven Triggers:** The engine listens for events (e.g., a new GitHub issue, a pull request, or a direct user prompt) and automatically initiates a new development cycle.
- **Pipeline Stages:** Workflows are structured in stages: Planning -> Implementation -> Testing -> Review -> Documentation. The engine ensures tasks seamlessly transition through these stages.
- **State Persistence:** The engine continuously snapshots the workspace state. If the system is interrupted, the engine can resume the exact state, ensuring that long-running tasks are robust and resumable.

## Error Recovery

A fully automated system must handle failures gracefully.
- **Self-Healing Execution:** When an agent encounters an error (e.g., a failing test or a syntax error during compilation), the Workflow Engine catches the exception, captures the error trace, and automatically reroutes the task back to the responsible agent (or to a specialized Refactor/Review agent) with the failure context attached.
- **Rollback Capabilities:** If an agent enters a loop of failures or corrupts the workspace, the engine halts the execution and rolls back to the last known healthy state using snapshot data.
- **Escalation Protocol:** If an issue cannot be resolved autonomously after a predefined number of attempts, the engine pauses the workflow and escalates the issue to the human operator, providing a detailed diagnostic report.

## Scalable AI-Driven Pipeline

To support a scalable development pipeline, the Workflow Engine manages concurrency and resource allocation. It can execute multiple independent tasks in parallel (e.g., the Frontend Agent building UI components while the Backend Agent creates database migrations) and synchronize them at integration points, dramatically reducing cycle times.
