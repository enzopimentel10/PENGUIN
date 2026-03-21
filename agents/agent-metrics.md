# Agent Metrics

The PEN.GUIN AI Kernel constantly monitors the behavior and output of its AI agents to ensure the ecosystem operates at peak efficiency. Evaluating an agent involves tracking a specific set of quantitative and qualitative metrics over time.

## Core Evaluation Metrics

The `Learning Engine` extracts the following data points from the `/workspace/sessions/` logs and the `/workspace/artifacts/` repository to build a comprehensive profile for each agent:

### 1. Tasks Completed (Throughput)
- **Definition:** The raw volume of tasks successfully moved from `Assigned` to `Completed` status by the agent.
- **Measurement:** Counted over specific time windows (e.g., daily, weekly) and categorized by task complexity or domain.
- **Importance:** Indicates the agent's baseline reliability and capacity. A sudden drop in throughput might indicate an issue with the agent's prompt or a systemic bottleneck.

### 2. Execution Time (Efficiency)
- **Definition:** The total time an agent spends in the `Active` state for a given task, from initial context retrieval to final artifact generation.
- **Measurement:** Usually measured in cognitive loop cycles or total wall-clock time. The engine calculates averages for specific task types (e.g., average time to generate a React component).
- **Importance:** Faster execution saves compute resources (API tokens) and accelerates the development pipeline. Consistently slow execution times may suggest the agent is struggling with ambiguous prompts or over-using tools.

### 3. Error Rate (Autonomy)
- **Definition:** The frequency at which an agent encounters errors that force it into a recovery loop, or worse, cause the task to fail completely.
- **Measurement:** The ratio of tool execution failures (e.g., syntax errors, failed test runs) against successful tool calls during a session.
- **Importance:** A low error rate indicates high autonomy and a strong grasp of the provided context and skills. High error rates flag a need for the `Learning Engine` to step in and adjust the agent's persona or provide better context.

### 4. Review Scores (Quality)
- **Definition:** A qualitative assessment of the agent's final artifacts, generated during the `Review & Validation` phase.
- **Measurement:** Derived from the outputs of the `Review Agent` and `Security Agent`. This includes factors like cyclomatic complexity of generated code, adherence to styling guidelines, and the number of iterations required to pass a pull request.
- **Importance:** An agent might be incredibly fast (high throughput, low execution time), but if its code is consistently rejected by the Review Agent for being non-idiomatic or buggy, its overall performance rating will correctly reflect that poor quality.
