# Agent Execution Model

This document details the operational mechanics of a Gemini-powered agent once it has been instantiated by the PEN.GUIN Kernel to execute a specific task.

## How Agents Receive Tasks

Tasks are not handed to Gemini agents as vague conversational requests. They are provided as highly structured data contracts.
1. **The Task Payload:** The Gemini CLI reads the initial prompt, which contains a strict breakdown of the `Task Context` (what to do), `Acceptance Criteria` (how to know it's done), and `Environment State` (what files exist).
2. **The Observation Phase:** The agent's first internal step is to parse this payload. If the payload indicates missing context, the agent utilizes its read-only tools to map the current state of the `/workspace/` before attempting any modifications.

## How Agents Interact With Skills

Gemini agents do not execute raw terminal commands to use external capabilities (like those from `antigravity-awesome-skills`). They use the `Skill Adapter Layer`.

1. **Skill Awareness:** If the `Skill Router` provisioned a skill for the task, the agent's prompt includes the schema required to invoke it.
2. **Invocation via Tool Calling:** The Gemini agent utilizes its native tool-calling capabilities to format a request. For example, it might output a tool call for `invoke_skill(name="component-generator", parameters={...})`.
3. **Execution & Return:** The Kernel intercepts this tool call, passes it to the `Skill Loader`, executes the skill safely in the sandbox, and returns the generated output (e.g., a string of React code) back into the Gemini CLI's context window.

## How Agents Store Results in the Workspace

A Gemini agent's execution is not complete until its output is safely committed to the workspace.

1. **Iterative Modification:** During execution, the agent uses provided tools (like file writers or regex replacers) to mutate files directly in the active `/workspace/` directory.
2. **Validation:** The agent invokes testing tools. If tests fail, the error is fed back into the Gemini CLI, and the agent iterates.
3. **Artifact Promotion:** Once the agent determines the objective is met and validated, it emits a `Task_Complete` signal to the Kernel, including pointers to the specific files it modified.
4. **Kernel Archival:** The Kernel validates the signal, moves the final, approved files into `/workspace/artifacts/`, and safely terminates the Gemini CLI process, returning the agent to an `Idle` state.
