# Task Executor

The Task Executor is the primary action-oriented tool for agents. It provides a secure sandbox for running code, scripts, test suites, and compilation commands within the workspace.

## Purpose
To execute dynamic commands safely. It ensures that commands do not run indefinitely, consume excessive resources, or access restricted directories outside the active workspace. It captures `stdout`, `stderr`, and exit codes perfectly.

## When Agents Should Use It
Agents should use the Task Executor whenever they need to validate their work empirically. Examples include:
- Running `npm test` or `pytest` to verify logic.
- Executing a build script (`tsc`, `cargo build`) to check for compilation errors.
- Running a formatter or linter (`eslint --fix`, `black .`).

## Interaction with the AI Kernel
The Task Executor is tightly bound to the AI Kernel's `Workflow Engine`. When the executor runs a command, the Kernel monitors the process. If a command hangs, the Kernel intervenes and kills the process. If a command fails (non-zero exit code), the Kernel triggers the "Error Recovery" protocol, preventing the workflow from advancing until the error is resolved.

## Interaction with the Routing System
The Routing System uses the results of the Task Executor as validation gates. If the Task Executor reports a successful test run, the `Agent Router` knows the current task is complete and proceeds to route the next sub-task to the appropriate agent. If it fails, the router loops the task back to the current agent for fixing.
