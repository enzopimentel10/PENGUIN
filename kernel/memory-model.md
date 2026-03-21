# PEN.GUIN Memory Model

## Overview
The Memory Model is the system through which the AI Kernel records, structures, and retrieves historical data about past tasks, architectural decisions, user preferences, and successfully executed code blocks.

## How Memory of Past Tasks is Stored
The memory model ensures that the environment learns over time, becoming more efficient and aligned with the user's intent.

- **Episodic Memory:** The system logs discrete events and tasks as "episodes." This includes the initial prompt, the steps taken by the agents, the tools used, the resulting code changes, and any user feedback. These episodes are structured and indexed for future retrieval.
- **Semantic Memory:** The kernel extracts general concepts and patterns from episodic memory. For example, if an agent successfully implements a specific authentication flow, the semantic memory stores the underlying principles, required libraries, and common pitfalls associated with that flow, abstracting away the project-specific details.
- **Vector Embeddings:** To enable efficient retrieval, the system converts code snippets, documentation, and task summaries into vector embeddings. When a new task arrives, the kernel queries the vector database to find semantically similar past tasks, providing agents with relevant historical context.
- **User Preference Profiles:** The memory model maintains persistent profiles of user preferences regarding coding style, formatting, preferred tools, and architectural choices. This ensures that agents consistently adhere to the user's conventions across different projects and sessions.
- **Knowledge Graphs:** For complex projects, the memory model constructs a knowledge graph representing the dependencies between different components, modules, and concepts. This allows agents to navigate the codebase more effectively and understand the broader impact of their changes.
