# Agent Performance and Routing

The metrics collected in the Agent Evaluation System are not static dashboards; they are dynamic inputs that feed directly into the `Decision Memory`. This creates a powerful feedback loop where past performance directly shapes future workload distribution.

## Shaping Agent Routing Decisions

The `Agent Router` leverages historical performance data to optimize task assignment, ensuring the right agent is paired with the right job based on proven empirical success.

### 1. Competency Weighting
When multiple agents share overlapping domain tags (e.g., two agents are capable of `Frontend` work), the router uses the **Review Scores** and **Error Rates** to break ties. If "Agent A" historically produces React components with fewer linting errors and a higher first-pass approval rate than "Agent B", the router will dynamically weight Agent A higher for critical UI tasks.

### 2. Dynamic Specialization
Performance data reveals true specializations that may not be explicitly defined in an agent's initial manifest.
- **Discovery:** The `Learning Engine` might notice that a general `Backend Agent` has exceptionally low **Execution Times** and high **Success Rates** specifically when handling PostgreSQL optimization tasks, compared to other backend tasks.
- **Routing Adjustment:** The router updates the agent's profile in the `Decision Memory` to heavily favor routing database performance tasks to this specific agent, organically evolving a new, highly specialized expert within the ecosystem.

### 3. Task Complexity Matching
The router matches the historical **Execution Time** and **Error Rate** profiles against the classified complexity of a new task.
- Simple, repetitive tasks (e.g., boilerplate generation) are routed to agents optimized for high **Throughput**.
- Complex, architecturally sensitive tasks (e.g., refactoring core authentication logic) are routed exclusively to agents with the highest **Review Scores**, prioritizing quality over speed.

### 4. Workload Rebalancing and Quarantine
If an agent's metrics suddenly degrade (e.g., a spike in **Error Rate** due to a misaligned update to its system prompt), the router will detect this anomaly. It can automatically pause routing complex tasks to the degraded agent, temporarily assigning it low-risk work or quarantining it entirely until the `Learning Engine` or a human operator can resolve the degradation.
