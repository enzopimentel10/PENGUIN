# Skill-Aware Planning Mechanism

The PEN.GUIN ecosystem relies on a "Skill-Aware" planning approach. The `Planner Agent` does not generate abstract execution plans in a vacuum; it dynamically adapts its strategies based on the specific capabilities currently loaded into the system, particularly those sourced from external libraries like `antigravity-awesome-skills`.

## How the Planner Queries the Skill Registry

The Planner Agent begins its planning cycle by understanding its available toolset.

1. **Initial Index Query:** Before decomposing a user objective, the Planner Agent emits a `query_skill_index` request to the AI Kernel.
2. **State Ingestion:** The Kernel responds with a serialized overview of the `Skill Index`. This includes all active skills, their domain categories, required input schemas, guaranteed output formats, and their current "Trust Scores" derived from the `Decision Memory`.
3. **Contextual Awareness:** This allows the Planner to know exactly what the ecosystem *can* do natively versus what will require an agent to write manual, raw code.

## How it Selects Skills for Subtasks

As the Planner breaks down an objective, it actively pairs requirements with available skills.

1. **Intent-to-Capability Mapping:** If a subtask involves database interactions, the Planner searches its cached Skill Index for tags like `Backend` or `Database`. It discovers the `schema-designer` skill.
2. **Explicit Assignment:** The Planner explicitly adds `schema-designer` to the `required_skills` array of the generated subtask within the `execution-plan.md`. This guarantees that when the `Agent Router` eventually assigns the task, the `Skill Router` will provision that specific tool.
3. **Permission Validation:** The Planner ensures it only assigns skills that align with the target agent's permissions. It will not assign a `frontend-agent` to a subtask that requires `sast-analyzer` if the security ACL forbids it.

## How Skills Influence Task Decomposition

The most critical aspect of Skill-Aware Planning is that the *availability* of skills fundamentally alters the *structure* of the Execution Plan.

- **Granularity Adjustment (Skill-Driven):** 
  - *Scenario A (Rich Skillset):* If the ecosystem has a powerful `full-auth-scaffolder` skill, the Planner creates a single, high-level subtask: "Implement User Authentication."
  - *Scenario B (Basic Skillset):* If that skill is quarantined or missing, the Planner adapts and decomposes the same objective into five granular subtasks: "Design User Schema", "Implement Password Hashing", "Build JWT Middleware", "Create Login Route", "Create Registration Route".
- **Chaining Awareness:** The Planner uses the Input/Output schemas from the Skill Index to design seamless pipelines. It knows that the `api-scaffolder` skill requires a JSON schema as input. Therefore, it explicitly commands the preceding `schema-designer` subtask to output its artifact as structured JSON, rather than plain text, ensuring the output of task 1 cleanly feeds the input of task 2.
- **Risk Mitigation:** If the Planner must use a skill with a historically high Error Rate (based on the provided Trust Scores), it automatically generates subsequent "Review" or "Testing" subtasks immediately following it, padding the Execution Plan with extra validation gates to ensure system stability.
