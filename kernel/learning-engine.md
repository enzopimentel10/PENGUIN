# Learning Engine

The Learning Engine is the meta-cognitive layer of the PEN.GUIN ecosystem. While agents execute individual tasks, the Learning Engine observes the entire ecosystem across multiple task lifecycles to identify patterns, optimize workflows, and permanently improve the system's efficiency.

## Evaluating Task Results

Learning begins the moment a task concludes. The engine does not simply log a "Success" or "Failure"; it performs a deep evaluation of the execution:

1. **Efficiency Metrics:** It measures the time taken, the number of API tokens consumed, the number of cognitive loop iterations required, and the frequency of tool failures during the session.
2. **Quality Metrics:** It analyzes the output artifacts. Did the `Review Agent` flag many style violations before approval? Was the code merged seamlessly, or did it require subsequent bug-fix tasks?
3. **Error Analysis:** If a task failed, the engine isolates the exact step in the `/workspace/sessions/` log where the failure occurred. It determines if the failure was due to insufficient context, a flawed tool implementation, or incorrect agent reasoning.

## Continuous Workflow Improvement

The Learning Engine uses these evaluations to adjust the system dynamically:

- **Prompt Optimization:** If agents consistently stumble on a specific type of task (e.g., scaffolding GraphQL schemas), the Learning Engine can automatically synthesize "best practices" derived from successful past attempts and instruct the `Context Engine` to append these hints to future task prompts.
- **Context Pruning:** If the engine notices that agents rarely utilize certain injected files, it updates the `Context Engine`'s retrieval heuristics to exclude that noise, saving tokens and improving agent focus.
- **Pipeline Restructuring:** If a specific sequence of skills (e.g., `skill A` -> `skill B`) frequently results in conflicts or errors, the engine alerts the `Agent Orchestrator` to insert a validation gate or modify the default chaining logic.
