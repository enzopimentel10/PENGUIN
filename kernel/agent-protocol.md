# Agent Communication Protocol

The PEN.GUIN ecosystem relies on a structured JSON-based communication protocol for all interactions between active Gemini agents and the AI Kernel. This ensures that intent is unambiguous and state can be managed reliably.

Agents communicate with the Kernel by emitting specific JSON blocks within their standard output. The Kernel intercepts these blocks, acts upon them, and returns responses via standard input.

## 1. Task Request Protocol

When an agent enters the `Idle` state, it uses this protocol to poll the `/workspace/tasks` queue for work.

**Agent Request:**
```json
{
  "type": "kernel_request",
  "action": "poll_tasks",
  "agent_id": "frontend-agent",
  "competencies": ["client-side", "ui", "react"]
}
```

**Kernel Response (Success):**
```json
{
  "type": "kernel_response",
  "status": "assigned",
  "task_id": "task-004",
  "payload": {
    "objective": "Build login form component",
    "context_files": ["/workspace/docs/api-contracts/auth.json"]
  }
}
```

## 2. Skill Request Protocol

While the Kernel proactively provisions skills based on the task, an agent can dynamically request specific capabilities (from `antigravity-awesome-skills` or custom skills) mid-execution using this protocol.

**Agent Request:**
```json
{
  "type": "kernel_request",
  "action": "load_skill",
  "agent_id": "frontend-agent",
  "skill_name": "css-utility-mapper",
  "reason": "Need to convert generic styles to Tailwind classes."
}
```

**Kernel Response (Success):**
```json
{
  "type": "kernel_response",
  "status": "success",
  "skill_name": "css-utility-mapper",
  "invocation_schema": {
     "name": "css-utility-mapper",
     "parameters": { "css_string": "string" }
  }
}
```

## 3. Artifact Storage Protocol

When an agent completes a task and validates its work, it must formally hand over the resulting files to the Kernel for promotion to the `/workspace/artifacts/` directory.

**Agent Request:**
```json
{
  "type": "kernel_request",
  "action": "store_artifact",
  "agent_id": "frontend-agent",
  "task_id": "task-004",
  "artifacts": [
    {
      "file_path": "/workspace/components/LoginForm.jsx",
      "type": "code"
    }
  ],
  "handoff_summary": "Implemented LoginForm.jsx based on auth.json contract. Tests passing."
}
```

**Kernel Response:**
```json
{
  "type": "kernel_response",
  "status": "success",
  "message": "Artifacts promoted. Task task-004 marked as complete. Session archived."
}
```

## 4. Progress & Error Reporting Protocol

Agents must report their progress or escalate errors they cannot recover from (e.g., if a provisioned skill repeatedly fails).

**Agent Error Escalation Request:**
```json
{
  "type": "kernel_request",
  "action": "report_error",
  "agent_id": "frontend-agent",
  "task_id": "task-004",
  "severity": "critical",
  "details": "The component-generator skill is returning a 500 timeout error. Cannot proceed with UI scaffolding."
}
```

**Kernel Response:**
```json
{
  "type": "kernel_response",
  "status": "acknowledged",
  "action_taken": "halt_execution",
  "message": "Task suspended. Routing issue to specialized debugger agent."
}
```
