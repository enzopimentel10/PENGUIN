# Skill Detection

The Skill Detection module operates as the intelligence layer that evaluates context to dynamically inject capabilities. Rather than agents manually requesting tools, the system automatically detects when skills should be invoked based on semantic understanding of the task.

## Intent Detection

Before any action is taken, the system determines the underlying goal.
- **Semantic Parsing:** The system uses natural language processing on the user's prompt or the current task description to extract core actions and targeted domains (e.g., "optimize the query" implies performance enhancement on a database).
- **Contextual Signals:** The module reads environmental signals, such as file extensions being modified (e.g., `.sql` vs. `.tsx`), to infer the type of work being performed.

## Task Analysis

Once intent is understood, the task is deeply analyzed to map it to discrete skills.
- **Requirement Extraction:** The system breaks down the intent into granular requirements. If the intent is "build a login form," the analysis extracts the need for: 1) scaffolding a UI component, 2) styling it, and 3) handling forms.
- **Automated Skill Mapping:** The analysis output is mapped against the `skills-registry.md`. The system automatically identifies that the agent will require the `component-generator` and the `css-utility-mapper` skills.

## Automatic Invocation

The system preemptively provisions the detected skills to the active agent's toolset. When the agent reaches a phase of execution where the skill's specific trigger conditions are met (e.g., when it is about to output CSS), the system prompts the agent to utilize the provisioned skill rather than relying on raw text generation. This ensures high-quality, standardized outputs.
