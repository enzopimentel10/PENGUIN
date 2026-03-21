# PEN.GUIN Agent Registry

## Overview
The Agent Registry is the directory of all available autonomous agents within the PEN.GUIN ecosystem. It manages the definitions, capabilities, and lifecycles of these specialized AI actors.

## How Agents Interact With the Kernel
Agents are not monolithic entities; they are specialized actors that interact with the Kernel in a highly structured manner.

- **Registration and Discovery:** When an agent is created or instantiated, it registers itself with the Kernel, detailing its core competencies, required skills, and operational constraints. The Kernel uses this registry to discover suitable agents for incoming tasks.
- **Task Assignment:** Agents do not spontaneously decide to work. They receive explicit task assignments from the Kernel. The Kernel provides the necessary context, objectives, and access rights.
- **Execution and Reporting:** During execution, agents report their progress, status updates, and any encountered errors back to the Kernel. This allows the Kernel to monitor the workflow and intervene if an agent becomes stuck or deviates from the objective.
- **Resource Requests:** If an agent requires additional resources (e.g., access to a new skill, more memory, or permission to execute a specific tool), it must request these from the Kernel. The Kernel evaluates the request based on the agent's role and security policies.
- **Handoff and Completion:** Upon completing a task, the agent notifies the Kernel and provides a summary of its actions. The Kernel then orchestrates the handoff of any artifacts or context to the next agent in the workflow.
- **Feedback Loop:** Agents receive feedback from the Kernel based on task outcomes and user interactions. This feedback is used to refine their internal models and improve future performance.
