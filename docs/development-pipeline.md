# AI-Assisted Development Pipeline

This document outlines the full end-to-end AI-assisted development lifecycle within the PEN.GUIN ecosystem. It details how specialized AI agents participate in each phase and how the central AI Kernel orchestrates the entire process.

## 1. Planning Phase
**Goal:** Translate user intent into a structured, actionable roadmap.

* **Agent Participation:** The **Architecture Agent** takes the lead. It parses the initial user prompt, identifies core objectives, and queries the user for necessary clarifications.
* **Kernel Orchestration:** The AI Kernel utilizes the **Task Classifier** to extract intent. It provisions the Architecture Agent with the `codebase-mapper` skill to evaluate the current workspace state. The Kernel then saves the resulting project roadmap into the Context Engine.

## 2. Architecture Design Phase
**Goal:** Define system boundaries, technology stacks, and API contracts.

* **Agent Participation:** The **Architecture Agent** continues its work by drafting the system blueprint. It defines data models, folder structures, and interaction protocols between the frontend and backend.
* **Kernel Orchestration:** The Kernel engages the **Security Agent** in a consultative role to vet the proposed technology stack for known vulnerabilities (using `dependency-auditor`). Once the design is finalized, the Kernel updates the `ARCHITECTURE_GUARDRAILS.md` in memory and signals the start of implementation.

## 3. UI Design & Frontend Development Phase
**Goal:** Build responsive, accessible, and interactive user interfaces.

* **Agent Participation:** The **Frontend Agent** receives the architectural blueprints. It uses skills like `component-generator` and `css-utility-mapper` to scaffold UI elements. It relies on mock APIs to build out state management and routing logic.
* **Kernel Orchestration:** The Kernel provisions the specific UI libraries requested in the architecture phase. As the Frontend Agent completes components, the Kernel automatically runs an `a11y-validator` gate to ensure accessibility standards are met before proceeding.

## 4. Backend Development Phase
**Goal:** Implement server logic, database interactions, and robust API endpoints.

* **Agent Participation:** Operating in parallel with the Frontend Agent, the **Backend Agent** executes the data modeling. It uses the `schema-designer` and `api-scaffolder` skills to build out the server infrastructure, strictly adhering to the API contracts defined in Phase 2.
* **Kernel Orchestration:** The Kernel manages concurrency. If the Backend Agent updates an API contract, the Context Engine dynamically updates the Frontend Agent's context window. The Kernel uses mutex locks on shared files (like `package.json` or `.env.example`) to prevent merge conflicts.

## 5. Testing Phase
**Goal:** Ensure behavioral correctness and prevent regressions.

* **Agent Participation:** The **Test Agent** takes over as implementation units finish. It uses the `unit-test-generator` to scaffold tests for the new components and endpoints. It then executes the full test suite and generates a `coverage-reporter` analysis.
* **Kernel Orchestration:** This is a critical validation gate. If a test fails, the Workflow Engine intercepts the error trace, halts forward progress, and immediately routes the failure context back to the authoring agent (Frontend or Backend) for correction. The pipeline does not advance until all tests pass.

## 6. Security Review Phase
**Goal:** Identify and mitigate vulnerabilities before deployment.

* **Agent Participation:** The **Security Agent** scans the newly written code. It employs `sast-analyzer` to look for injection flaws and `secret-scanner` to ensure no API keys were accidentally hardcoded during development.
* **Kernel Orchestration:** The Kernel runs this phase asynchronously in the background during the testing phase, or synchronously right after. If a critical vulnerability is found, the Kernel exercises veto power, blocking any further merging or deployment until the vulnerability is patched.

## 7. Refactoring & Code Review Phase
**Goal:** Reduce technical debt, improve readability, and ensure stylistic consistency.

* **Agent Participation:** The **Review Agent** and **Refactor Agent** collaborate. The Review Agent runs the `linter-executor` and `complexity-scorer`. If a function is flagged as overly complex or non-idiomatic, the Refactor Agent is deployed to simplify the logic using AST manipulation, without altering the external behavior.
* **Kernel Orchestration:** The Kernel enforces the `AI_ENGINEERING_RULES.md`. It ensures that any code touched by the Refactor Agent is immediately passed back through the Testing Phase to guarantee no regressions were introduced.

## 8. Deployment & Documentation Phase
**Goal:** Finalize the release, document changes, and prepare for production.

* **Agent Participation:** The **Documentation Agent** synthesizes the changes made during the cycle. It updates the `README.md`, generates new API docs using `docstring-generator`, and writes the changelog.
* **Kernel Orchestration:** The Kernel consolidates the entire episode into the Memory Model, saving successful code patterns and user preferences for future tasks. Finally, the Kernel can execute custom deployment scripts (via the `/scripts` directory) to push the verified, secure, and fully tested code to a staging or production environment.
