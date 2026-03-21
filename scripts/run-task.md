# Run Task Workflow (`run-task.sh`)

This script is the primary entry point for users or external triggers to feed objectives into the PEN.GUIN ecosystem.

## Workflow Overview
When `run-task "User Objective"` is executed, the script initiates the full automated development pipeline.

1. **Prompt Ingestion:** The script captures the raw objective string and any attached context files.
2. **Task Classification Initiation:** The payload is immediately passed to the `Task Classifier` within the routing system. The classifier breaks the objective into atomic sub-tasks.
3. **Workflow Engine Hand-off:** The script hands control over to the `Workflow Engine`. The engine creates a new "Episode" in the `Memory Model` to track the lifecycle of this specific request.
4. **Agent Orchestration Loop:** The `Agent Orchestrator` takes over, routing the first sub-task to the appropriate agent (e.g., the Architecture Agent for planning).
5. **Continuous Execution:** The script process remains active, streaming logs and status updates (from the Context Engine) to the terminal as agents perform chained skills, handoffs, validations, and testing.
6. **Task Finalization:** Once the final phase (Testing/Documentation) completes without errors, the script receives a success signal from the Workflow Engine, outputs a summary of changes, and safely terminates the process.
