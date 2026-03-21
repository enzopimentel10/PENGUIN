# Execution Loop Architecture

The Execution Loop is the underlying mechanical engine that drives an agent through its lifecycle stages. It ensures that agents operate autonomously, handle errors gracefully, and continuously process tasks from the workspace without stalling.

## The Cognitive Loop

While in the **Execution** phase, the agent operates on a continuous "ReAct" (Reasoning + Acting) cognitive loop, heavily monitored by the Kernel:

1. **Observe (State Ingestion):** The agent reads the current state of its environment from the Context Engine and the results of its previous tool call.
2. **Orient (Analysis):** The agent processes the observation against its assigned task and systemic guardrails. Did the previous action succeed? What is the next logical step?
3. **Decide (Planning):** The agent formulates its next intent. E.g., "The file was created successfully, now I need to run the test suite."
4. **Act (Tool Execution):** The agent outputs a structured command to invoke a tool (e.g., `Task Executor`, `Skill Loader`). 

The loop immediately restarts at **Observe**, reading the output of the action.

## Processing the Workspace Queue

The Execution Loop is designed for continuous, asynchronous throughput:

- **Polling Mechanism:** When an agent is `Idle`, its execution loop is in a lightweight polling state, checking the `/workspace/tasks` queue. 
- **Mutex Task Claiming:** When a matching task is found, the agent applies a mutex lock to the task file, preventing other agents from claiming it.
- **Session Instantiation:** The loop transitions into the active Cognitive Loop, logging every cycle to `/workspace/sessions`.

## Interrupts and Safety Nets

The Execution Loop is not infinite; it has strict safety mechanisms enforced by the AI Kernel to prevent runaway agents:

- **Max Loop Count:** To prevent an agent from getting stuck in an infinite loop of failing, retrying, and failing again (e.g., due to an impossible constraint), the execution loop has a hard limit on iterations per task (e.g., 15 turns). If this limit is reached, the loop is terminated, and the task is escalated to a human or a specialized debugger agent.
- **Context Window Management:** As the loop cycles, the context window grows. The Kernel monitors token usage. If the limit is approached, the loop pauses while the Kernel uses the `Memory Model` to summarize older logs, freeing up space while retaining critical intent.
- **Fatal Error Halts:** If an action results in a critical violation of the `ARCHITECTURE_GUARDRAILS.md` or a security veto, the Kernel immediately interrupts the execution loop and triggers a state rollback.
