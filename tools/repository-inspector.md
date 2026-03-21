# Repository Inspector

The Repository Inspector is a powerful, read-only analysis tool designed to help agents quickly map, search, and understand large codebases without needing to read every file individually.

## Purpose
To provide high-signal, low-noise context to agents. It encompasses capabilities like fast regex searching (ripgrep-style), glob pattern matching, and AST-based symbol extraction (finding where functions are defined or called).

## When Agents Should Use It
Agents should use this tool extensively during the "Research" and "Architecture Design" phases, or anytime they are introduced to an unfamiliar part of the codebase. It is crucial for:
- Finding all references to a deprecated API before a refactor.
- Locating existing UI components to ensure styles remain consistent.
- Mapping dependencies to understand the blast radius of a planned change.

## Interaction with the AI Kernel
The Repository Inspector feeds massive amounts of data into the `Context Engine`. To prevent token-window exhaustion, the Kernel automatically filters and truncates the Inspector's output, summarizing findings or providing only the most relevant code snippets to the agent's active memory.

## Interaction with the Routing System
The `Task Classifier` often invokes the Repository Inspector proactively before even assigning an agent. By inspecting the repository to see which files are involved in a user's request, the router can more accurately tag the domain (Frontend vs. Backend) and make a better routing decision.
