# CLI Output System

The PEN.GUIN CLI output system is designed to provide clear, actionable, and visually engaging feedback during the AI development lifecycle. It adheres to a "Big & Bold" and "Premium" aesthetic, ensuring that developers are always informed of the system's state.

## Output Components

### 1. Task Progress Visualization
Progress for multi-task workflows (e.g., `penguin build feature`) is displayed using a hierarchical tree-view or a compact progress dashboard:
- **Task Tree**: Shows the dependency graph in real-time. Completed tasks are marked with a distinct checkmark, while active tasks are highlighted with a pulse effect or a specialized spinner.
- **Progress Bars**: For long-running operations (like building or scanning), a high-resolution progress bar shows the percentage of completion.
- **Milestone Updates**: Significant transitions in the graph (e.g., "Architecture phase complete") are announced with bold, distinct headers.

### 2. Agent Activity Monitoring
When an agent is active, the CLI provides granular insights into its "thinking" and "doing":
- **Activity Streams**: Real-time snippets of the agent's current focus (e.g., "Frontend Agent is generating UI components...").
- **Tool Call Indicators**: When an agent invokes a tool (like `read_file` or `write_file`), a small HUD-style indicator appears, showing the tool name and the target file/resource.
- **Thought Bubbles**: For more complex tasks, the CLI can display a summary of the agent's recent reasoning steps to provide transparency into its logic.

### 3. Execution Status
The overall status of a session is always visible at the bottom of the terminal window or as a persistent status bar:
- **States**: `pending`, `ready`, `running`, `completed`, `failed`, `blocked`.
- **Color Coding**: Statuses are color-coded (e.g., green for `completed`, red for `failed`, yellow for `blocked`) to provide instant visual cues.
- **Resource Usage**: Displays real-time metrics like active agents, elapsed time, and token consumption (if applicable).

### 4. Result Presentation
Upon completion, the CLI delivers a synthesized summary of the outcomes:
- **Final Report**: A high-level overview of the work performed, highlighting the primary artifacts created.
- **Artifact Manifest**: A clear list of file paths for all generated code, docs, and analysis reports, with links to open them directly.
- **Next Steps**: Actionable suggestions for the developer to verify or continue the workflow.

### 5. Error Reporting and Recovery
Errors are treated as first-class citizens in the PEN.GUIN CLI:
- **Bold Error Headers**: Failures are announced with a clear "FAILURE" or "ERROR" block.
- **Actionable Diagnostics**: Instead of raw stack traces, the CLI provides a human-readable explanation of the root cause.
- **Context Snapshots**: Shows the exact task and agent that failed, along with the inputs that led to the error.
- **Recovery Options**: When possible, the CLI offers immediate recovery paths, such as `penguin retry` or `penguin rollback`.

## Visual Style Guide

The CLI output uses stylized typography and symbols to create a premium feel:
- **Symbols**: Custom Unicode symbols are used for status markers and progress indicators.
- **Borders**: HUD-style borders and frames (using box-drawing characters) separate different sections of the output.
- **Dark Mode Optimization**: Colors are chosen for maximum contrast and visibility in dark mode terminal environments.

```text
┌────────────────────────────────────────────────────────────────────────────┐
│ PENGUIN | build feature "user-auth"                              [ RUNNING ] │
├────────────────────────────────────────────────────────────────────────────┤
│ ├─ Architecture Phase ........................................... [  DONE  ] │
│ ├─ Backend implementation (API Routes) .......................... [ ACTIVE ] │
│ │  └─ Agent: backend-agent | Action: write_file -> /api/auth.ts            │
│ └─ Frontend scaffolding ......................................... [ PENDING ]│
└────────────────────────────────────────────────────────────────────────────┘
```
