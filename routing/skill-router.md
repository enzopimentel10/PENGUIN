# Skill Routing System

To maintain absolute security and architectural integrity within the PEN.GUIN ecosystem, agents are strictly prohibited from directly executing skills or terminal commands. Instead, all capabilities must be formally requested from and provisioned by the AI Kernel through the **Skill Router**.

## How Agents Request Skills

Agents operate within an isolated context. If an agent realizes it needs a specific capability to accomplish its task (e.g., it needs to validate CSS but doesn't have a linter in its prompt), it must request it dynamically.

1. **The Request Payload:** The agent outputs a structured JSON `kernel_request` with the action `load_skill`. It includes the requested capability (e.g., "Need a CSS linter") and a brief justification.
2. **Interception:** The Gemini CLI execution environment intercepts this structured output and pauses the agent's cognitive loop. It forwards the request to the AI Kernel.
3. **Provisioning Response:** If approved, the Kernel responds by injecting the skill's specific invocation schema (how to format the tool call) back into the agent's active prompt window, effectively "teaching" the agent how to use the skill.

## How the Kernel Selects the Correct Skill

The Kernel does not blindly grant whatever the agent asks for. The `Skill Router` acts as a highly intelligent mediator.

1. **Intent Matching:** When the router receives a request (or when it proactively provisions skills at the start of a task), it analyzes the agent's intent. If the agent asks for "a way to write to the database," the router looks up the `Backend` category in the `Skill Index`.
2. **Permission Validation (ACL):** The router checks the `Agent Registry`. If a `Frontend Agent` requests a database migration skill, the Skill Router outright rejects the request, enforcing architectural guardrails.
3. **Adaptive Selection:** If multiple skills fit the intent (e.g., `fast-linter` vs. `deep-linter`), the router queries the `Decision Memory`. It selects the specific skill that historically has the highest "Trust Score" (lowest error rate, fastest execution) for that particular agent and task type.
4. **Sandboxing:** Once selected, the Kernel mounts the skill into the `Skill Loader`, ensuring that when the agent finally invokes the schema, the underlying code runs in a secure, isolated sandbox rather than directly on the host machine.

## How Skill Chaining Works

Skill chaining is the orchestration of multiple, sequential skill invocations without requiring constant agent-to-kernel back-and-forth for data passing. It is managed by the Kernel to create seamless, automated pipelines.

1. **Pipeline Definition:** When the Kernel analyzes a complex sub-task, the Skill Router might provision a "chain" of skills (e.g., `component-generator` -> `css-utility-mapper`).
2. **Sequential Execution:** The agent invokes the first skill in the chain using the provided schema. The Kernel executes it via the `Skill Loader`.
3. **Automatic State Passing:** The true power of chaining is that the agent does not need to read the output of Skill 1 and manually paste it into Skill 2. The `Context Engine` captures the standardized output from the first skill (e.g., raw React code) and automatically maps it to the required input parameters of the second skill.
4. **Validation Gates:** Between each link in the chain, the Kernel enforces validation. If the first skill throws a critical error, the Skill Router halts the chain immediately. It prevents the second skill from executing on broken data and returns the error trace to the agent for recovery.
