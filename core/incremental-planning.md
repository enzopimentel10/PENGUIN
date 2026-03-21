# Incremental Planning Strategy

The PEN.GUIN ecosystem avoids the "Waterfall" trap of generating massive, rigid, and fragile execution plans upfront. Instead, it utilizes an Incremental Planning Strategy. The `Planner Agent` acts continuously alongside the execution phase, generating plans in small, adaptable steps and refining them based on real-world feedback.

## 1. The Initial Plan (The Skeleton)

When a complex objective is received, the Planner Agent does not attempt to map out every single function and file change. It creates a "Skeleton Plan."

- **High-Level Milestones:** The initial plan defines the major architectural phases (e.g., "1. Setup Database," "2. Build Auth API," "3. Build Frontend UI").
- **First-Step Detailing:** It only generates granular, actionable `subtasks` for the *very first milestone*.
- **Unknowns Acknowledged:** Downstream milestones are left intentionally vague, represented as placeholders in the Execution Plan, acknowledging that their specifics depend heavily on the outcome of the first phase.

## 2. Execution Feedback (The Reality Check)

Once the first set of subtasks is generated, the Kernel routes them to the implementation agents (e.g., `Backend Agent`). As these agents work, they generate critical feedback:

- **Artifact Realities:** The Backend Agent might realize that the requested database schema needs a join table that wasn't anticipated, and it outputs this modified schema as an artifact.
- **Error Traces:** An agent might encounter an unexpected dependency conflict that forces a change in the tech stack (e.g., switching from `npm` to `yarn`).
- **Contextual Discoveries:** Read-only tools might uncover undocumented legacy code that changes the scope of the integration.

## 3. Plan Refinement (The Pivot)

The Planner Agent is not idle during execution; it operates in a continuous "Observe and Orient" loop.

- **Ingesting Feedback:** The Kernel feeds the generated artifacts and execution session logs back to the Planner Agent.
- **Re-evaluating the Skeleton:** The Planner compares the new reality (the actual database schema produced) against its original assumptions.
- **Just-In-Time Detailing:** The Planner now generates the granular `subtasks` for the *next* milestone (e.g., "Build Auth API"), but it bases these new tasks entirely on the concrete, validated output of the first milestone, not on its initial theoretical guesses.

## 4. Dynamic Task Creation (Self-Healing)

Incremental planning allows the system to react dynamically to unforeseen roadblocks without crashing the entire workflow.

- **Spawning Remediation Tasks:** If the `Review Agent` consistently fails a piece of code because of a complex architectural flaw, the standard "Retry Loop" might not be enough. The Planner Agent will intervene, dynamically creating a new, previously unplanned subtask (e.g., "Refactor legacy routing module to support new Auth flow") and inserting it into the `Task Queue` as a blocking dependency.
- **Adapting to Skill Failures:** If a planned skill (e.g., `auto-migrator`) is quarantined due to high error rates during the first milestone, the Planner dynamically re-writes the upcoming subtasks to use manual database querying instead, preventing a total system stall.

By planning incrementally, the PEN.GUIN ecosystem ensures that its execution strategy is always grounded in the current, validated state of the workspace, rather than a fragile assumption made at the start of the project.
