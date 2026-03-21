# Decision Optimization

Decision Optimization is the practical application of the Adaptive Routing System, detailing exactly how the PEN.GUIN ecosystem uses real-time and historical performance metrics to optimize the distribution of work and capabilities.

## Influence on Agent Selection

When the `Agent Router` evaluates a pending task, it no longer just checks for matching domain tags. It calculates a dynamic "Fit Score" for every available agent.

- **Execution Time (Speed):** For urgent tasks (e.g., hotfixes), the router heavily weights the historical execution speed metric. It selects the agent proven to resolve similar tasks the fastest.
- **Review Scores (Quality):** For architectural changes or security-sensitive modules, speed is de-prioritized. The router selects the agent with the highest historical review scores and lowest error rates in that specific domain, ensuring high-quality, secure code.
- **Workload Balancing:** The router penalizes the "Fit Score" of an agent if its current queue is full, distributing tasks to slightly less optimal but available agents to maintain overall ecosystem throughput.

## Influence on Skill Selection

The `Skill Router` uses a similar optimization model when provisioning capabilities.

- **Error Rate Monitoring:** If the `Learning Engine` reports that a newly introduced skill from `antigravity-awesome-skills` has a high error rate when used by the `Backend Agent` on database tasks, the `Skill Router` immediately stops provisioning that skill for those specific scenarios, falling back to a safer, older skill.
- **Success Rate Synergy:** If metrics show that the `Frontend Agent` produces code with 50% fewer linting errors when provisioned with *both* `component-generator` and `css-utility-mapper` simultaneously, the `Skill Router` optimizes its strategy to always provision them as a pair.

## Influence on Task Prioritization

Performance metrics also govern the order in which tasks are processed from the `/workspace/tasks` queue.

- **Dependency Weighting:** Tasks that historically block many downstream tasks (e.g., database schema changes) are automatically bumped up in priority by the routing engine.
- **Risk Assessment:** Tasks classified as high-risk (e.g., modifying authentication logic) are prioritized differently. The system might hold a high-risk task in the queue longer, waiting specifically for the ecosystem's most highly-rated `Security Agent` and `Backend Agent` to become available, rather than assigning it immediately to a lesser-rated agent.
