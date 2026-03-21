# Gemini Runtime

The PEN.GUIN ecosystem relies on the **Gemini CLI** as its primary execution engine for AI agents. The Gemini Runtime acts as the vital bridge connecting the orchestration logic of the AI Kernel to the actual computational capabilities of the Gemini models.

## How the Kernel Starts a Gemini Agent

Agents in the PEN.GUIN ecosystem are not constantly running processes; they are instantiated on-demand by the Kernel via the Gemini CLI.

1. **Task Assignment:** When the `Agent Router` assigns a task to an agent (e.g., `frontend-agent`), the Kernel retrieves that agent's specific manifest (persona, guardrails).
2. **Context Compilation:** The `Context Engine` compiles the necessary workspace state, the task description, and any provisioned skill instructions into a single, cohesive prompt payload.
3. **CLI Invocation:** The Kernel spawns a child process to execute the Gemini CLI. It passes the compiled prompt as the initial input, effectively "waking up" the agent with a hyper-specific objective.
   *Example:* `gemini-cli run --prompt-file /workspace/sessions/temp-prompt.md --agent frontend-agent`
4. **Session Binding:** The CLI's output streams (stdout, stderr) are piped directly into the active session file within `/workspace/sessions/`, ensuring every cognitive step and tool call is captured by the Kernel.

## Interaction Between Gemini and the Kernel

The Gemini CLI runs in an interactive mode, but it does not converse with a human; it converses with the AI Kernel's event loop.
- **Structured Outputs:** The agent is instructed (via its persona prompt) to output specific JSON blocks when it needs the Kernel to perform an action (e.g., locking a file, escalating an error, or marking a task as complete).
- **Context Polling:** If the Gemini agent encounters an ambiguity, it can output a specific query formatted for the `Repository Inspector`. The Kernel intercepts this, executes the search, and feeds the result back into the Gemini CLI's standard input.
