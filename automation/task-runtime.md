# Task Execution Runtime

The Task Execution Runtime is the end-to-end conveyor belt that powers the PEN.GUIN automation pipeline. It describes the lifecycle of a single unit of work (a task) as it flows from inception to finalized artifact.

## The Task Lifecycle

1. **Ingestion to `/workspace/tasks`**
   - The runtime begins when a high-level objective is received (e.g., via the `run-task` script or an external trigger like a GitHub Issue).
   - This raw objective is ingested and temporarily stored for processing.

2. **Task Classification**
   - The `Task Classifier` picks up the objective and breaks it down. 
   - It performs semantic analysis to deduce intent and splits the broad objective into an ordered list of atomic sub-tasks.
   - Each sub-task is written as a structured file (e.g., JSON) into the `/workspace/tasks` directory, waiting to be claimed.

3. **Agent Routing**
   - The `Agent Router` continuously evaluates the queue of sub-tasks in `/workspace/tasks`.
   - It matches the classified domain tags of a task (e.g., `Frontend`, `UI`) against the competency matrices of registered agents in the `Agent Registry`.
   - Once a match is found, the Router assigns the task to the specific agent and moves the task state from "Pending" to "Assigned".

4. **Skill Routing & Context Provisioning**
   - Before the agent begins execution, the `Skill Router` analyzes the specific requirements of the sub-task.
   - It dynamically provisions necessary tools from the `Skill Registry` (e.g., `component-generator`) and injects their usage instructions into the agent's prompt.
   - Concurrently, the `Context Engine` provides the required workspace context (relevant files, previous task outputs) to the agent.

5. **Execution (The Sandbox)**
   - The assigned agent enters its cognitive loop within the runtime sandbox.
   - It reads the task, formulates a plan, and uses its provisioned skills (via the `Skill Loader`) or native tools (via `Task Executor`) to manipulate code or state.
   - Every action is logged in real-time to a dedicated session file in `/workspace/sessions`. 
   - The agent iteratively validates its own work against test suites and linters.

6. **Artifact Generation & Validation**
   - Once the agent verifies the task is complete, it outputs the final code, diagrams, or text.
   - The runtime intercepts this output and pushes it to `/workspace/artifacts/`.
   - A final validation gate (often triggering the `Review Agent` or `Security Agent`) ensures the artifact meets system standards.
   - If successful, the artifact is merged into the main project state, the session is archived to the `Memory Model`, and the original task in `/workspace/tasks` is marked "Complete".
