# Skill Scoring and Routing

The metrics gathered during skill execution are not just for reporting; they are actively fed back into the `Learning Engine` to calculate a dynamic "Trust Score" for every skill. This score directly influences how the `Skill Router` behaves.

## The Dynamic Trust Score

A skill's Trust Score is a weighted composite of its Success Rate, Execution Time, Error Rate, and Review Score.
- **Initial State:** When a new skill is registered, it receives a baseline Trust Score.
- **Continuous Adjustment:** After every execution, the `Learning Engine` recalculates the score. Positive outcomes (fast, bug-free, high-quality code) increase the score. Negative outcomes decrease it.

## Influence on Skill Routing Decisions

The `Skill Router` uses the Trust Score to make intelligent provisioning decisions, ensuring agents are equipped with the most reliable tools available.

### 1. Preferential Provisioning
If two skills exist with overlapping capabilities (e.g., `fast-linter` vs. `deep-linter`), the `Skill Router` will evaluate the context of the task and the current Trust Scores. If rapid iteration is needed and `fast-linter` has a significantly higher success rate and lower execution time, the Router will preferentially provision it over the alternative.

### 2. Automated Deprecation (Quarantine)
If a skill's Error Rate spikes or its overall Trust Score drops below a critical threshold, the `Skill Router` places the skill in Quarantine.
- A quarantined skill is immediately hidden from agent prompts.
- The system prevents agents from invoking it, effectively isolating the unstable component to prevent it from corrupting ongoing workflows.
- The `Learning Engine` flags the quarantined skill for human review or triggers a specialized Meta-Agent to attempt a patch.

### 3. Contextual Routing Adjustments
Scores are often contextual. A skill might have a high success rate when used by the `Frontend Agent` but a high error rate when used by the `Refactor Agent`. 
- The `Decision Memory` tracks these relational metrics. 
- The `Skill Router` learns this pattern and will continue to provision the skill to the Frontend Agent, but will dynamically withhold it when assigning tasks to the Refactor Agent, suggesting safer native tools instead.
