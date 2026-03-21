# Skill Chaining and Coordination

Skill Chaining is the process of executing multiple discrete skills in a sequence to achieve a complex objective, managed entirely by the PEN.GUIN routing and orchestration layers.

## How Multiple Skills Can Be Chained

Often, a task requires a sequence of operations that map to multiple skills (e.g., scaffolding a UI, styling it, and then checking accessibility).
1. **Pipeline Definition:** The `Agent Orchestrator` or the agent itself defines a sequential pipeline of skills. For example: `component-generator` -> `css-utility-mapper` -> `a11y-validator`.
2. **Sequential Invocation:** The agent invokes the first skill. Instead of stopping, the agent is instructed by its prompt to immediately invoke the next skill in the defined chain upon successful completion of the first.

## Passing Outputs Between Skills

A crucial aspect of chaining is seamless data flow.
1. **Standardized Outputs:** Skills from `antigravity-awesome-skills` are designed to emit standardized outputs (e.g., structured JSON, specific file paths, or Abstract Syntax Trees).
2. **State Management via Context Engine:** When the first skill (e.g., `component-generator`) completes, the `Skill Loader` captures its output and sends it to the `Context Engine`.
3. **Context Injection:** The `Context Engine` automatically formats this output and injects it as the input parameter for the next skill in the chain (e.g., `css-utility-mapper`), often without the agent needing to manually copy and paste the data. The agent simply triggers the next skill, and the system handles the plumbing.

## Skill Router Coordination

The `Skill Router` ensures that chained executions occur safely and logically.
- **Mutex Locks:** If a chained skill modifies a file, the router locks that file. The next skill in the chain cannot execute until the lock is released, preventing race conditions.
- **Validation Gates:** The router can enforce validation between links in the chain. If `css-utility-mapper` fails or throws an error, the router halts the chain and sends the error trace back to the agent for recovery, preventing the `a11y-validator` from running on broken code.
- **Dynamic Re-routing:** Based on the output of one skill, the router might dynamically suggest a different subsequent skill than originally planned, adapting the chain to the actual workspace state.
