# Adaptive Routing System

The Adaptive Routing System is the evolutionary core of the PEN.GUIN ecosystem's orchestrator. Unlike static routing logic that relies entirely on hardcoded domain tags, adaptive routing continuously adjusts its own decision-making matrices based on empirical execution data, resulting in a self-optimizing workflow.

## The Self-Optimizing Mechanism

The system operates on a continuous feedback loop connected to the `Learning Engine` and `Decision Memory`:

1. **Observation:** Every routing decision (which agent gets a task, which skills are provisioned) is recorded alongside its final outcome (success, failure, execution time, review score).
2. **Analysis:** The `Learning Engine` periodically analyzes these records, looking for statistical correlations between specific routing choices and positive or negative outcomes.
3. **Adaptation (Weight Adjustment):** Based on the analysis, the routing algorithms automatically adjust the internal weighting of their decision trees. 

## How Routing Decisions Improve Over Time

- **From General to Specific:** Initially, the system might route all `Frontend` tasks equally among available frontend agents. Over time, it learns that `Agent A` is 30% faster at React tasks while `Agent B` has a lower error rate in Vue tasks. The routing logic adapts to split the workload based on these discovered specializations rather than broad tags.
- **Contextual Awareness:** The system learns that certain tasks are highly context-dependent. If a task requires manipulating legacy code, the router learns to prioritize agents that historically perform well with the `refactor-agent` and specific AST manipulation skills, rather than defaulting to the standard `frontend-agent`.
- **Failure Avoidance:** If a specific combination of agent, skill, and task type results in a failure rate above a certain threshold, the adaptive router effectively "blacklists" that combination, instantly preventing future systemic failures.
