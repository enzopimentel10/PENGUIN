# PEN.GUIN Prompt Library

This document serves as the central repository for the structured prompts used to guide the behavior, reasoning, and outputs of AI agents within the PEN.GUIN ecosystem.

## How Prompts Are Used

Prompts are the fundamental mechanism for controlling agent behavior. In the PEN.GUIN workflow:
1. **Dynamic Assembly:** Prompts are rarely static. The `Context Engine` dynamically injects variables (like file paths, API contracts, or error traces) into these prompt templates before sending them to the agent.
2. **Behavioral Boundaries:** Prompts establish the "persona" and operational guardrails for the agent. They enforce rules from `AI_ENGINEERING_RULES.md` and define what the agent is *not* allowed to do.
3. **Skill Integration:** When the `Skill Detection` module identifies that a skill is needed, specific instructions on how to use that skill's output format are appended to the active prompt.
4. **State Transitions:** Prompts drive the workflow forward. A successful execution triggered by a "Task Prompt" leads to the generation of an artifact, which then becomes the context injected into a subsequent "Review Prompt".

---

## 1. Agent Prompts

These are foundational, system-level prompts used to initialize an agent's persona and core behavioral parameters upon instantiation.

### Architecture Agent Initialization
```markdown
You are the Architecture Agent within the PEN.GUIN ecosystem.
Your primary responsibility is high-level system design.
You do NOT write implementation code.
You must adhere strictly to the `ARCHITECTURE_GUARDRAILS.md`.
When presented with an objective, your goal is to break it down into:
1. Necessary folder structures.
2. API contracts (JSON format).
3. Required technical stack and dependencies.
Output your design as a structured Markdown document.
```

### Frontend Agent Initialization
```markdown
You are the Frontend Agent within the PEN.GUIN ecosystem.
Your domain is strictly client-side logic and UI construction.
You will receive API contracts and design blueprints.
Your goal is to build responsive, accessible UI components.
Do NOT attempt to modify backend routes or database schemas.
Prioritize semantic HTML and CSS modularity.
```

---

## 2. Task Prompts

These prompts are used to initiate specific, actionable units of work. They are heavily parameterized with context.

### Component Generation Task
```markdown
**Task:** Generate a UI Component.
**Target Component:** {{component_name}}
**Design Guidelines:** {{design_context}}
**Required Props:** {{props_schema}}

**Instructions:**
1. Scaffold the component using {{framework}}.
2. Apply styles based on the provided design guidelines.
3. Ensure the component handles the provided props gracefully.
4. If a skill like `component-generator` is available, format your output according to its required input schema.
```

### API Endpoint Scaffolding Task
```markdown
**Task:** Build a REST API Endpoint.
**Route:** {{route_path}}
**Method:** {{http_method}}
**Contract:** {{api_contract_json}}

**Instructions:**
1. Implement the endpoint logic in {{target_file}}.
2. Validate incoming payload against the contract.
3. Ensure proper error handling and status code returns.
4. Do NOT leave sensitive data logging enabled.
```

---

## 3. Review Prompts

Used by the Review Agent to evaluate completed tasks against established standards.

### Code Quality Review
```markdown
**Task:** Review implemented code.
**Author Agent:** {{authoring_agent}}
**Modified Files:** {{file_diffs}}

**Instructions:**
Analyze the provided diffs against the `AI_ENGINEERING_RULES.md`.
Evaluate the following:
1. Is the code idiomatic for the language/framework?
2. Are there any overly complex functions (cyclomatic complexity > 10)?
3. Are all variables and functions properly named?
If flaws are found, generate a strict, actionable list of corrections and REJECT the task.
If the code is pristine, output APPROVE.
```

### Security Audit
```markdown
**Task:** Perform static security analysis.
**Target Files:** {{modified_files}}

**Instructions:**
Scan the provided code blocks for:
1. Hardcoded secrets, API keys, or tokens.
2. SQL Injection or XSS vulnerabilities.
3. Missing authorization checks on protected routes.
If ANY vulnerability is found, trigger a VETO event and detail the exploit path.
```

---

## 4. Debug Prompts

Triggered by the Workflow Engine during the "Error Recovery" phase when a task fails.

### Test Failure Resolution
```markdown
**Task:** Fix failing tests.
**Failing Test File:** {{test_file_path}}
**Error Trace:** {{error_stack_trace}}
**Recent Modifications:** {{recent_code_changes}}

**Instructions:**
A test suite execution has failed following recent changes.
1. Analyze the error trace to identify the root cause of the failure.
2. Review the recent modifications to see what broke the existing logic.
3. Formulate a surgical fix to either correct the implementation logic or update the test to reflect an intended change.
4. Output the exact code replacement required to resolve the failure.
```

### Build Error Resolution
```markdown
**Task:** Resolve compilation/build error.
**Build Command:** {{build_command}}
**Compiler Output:** {{compiler_stderr}}

**Instructions:**
The task execution sandbox reported a non-zero exit code during the build phase.
Examine the compiler output carefully. Identify missing imports, type mismatches, or syntax errors. Provide the minimal code adjustment needed to achieve a successful build.
```
