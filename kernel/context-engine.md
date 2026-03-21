# PEN.GUIN Context Engine

## Overview
The Context Engine is a crucial component of the AI Kernel, designed to manage the instantaneous state of the workspace and provide agents with the necessary information to perform their tasks effectively.

## How Context is Shared Between Agents
The context engine ensures that agents have access to a unified, coherent state of the project, preventing information silos and redundant work.

- **Centralized State:** The Context Engine maintains a real-time, centralized representation of the workspace. This includes file contents, active processes, open issues, and the current task breakdown.
- **Dynamic Scoping:** Rather than providing every agent with the entire project context (which is token-inefficient and cognitively overwhelming), the engine dynamically scopes context based on the agent's current task. An agent tasked with editing a UI component receives context about that component, its dependencies, and design guidelines, but not the backend database schema.
- **Inter-Agent Handoffs:** When an agent completes a task and passes the baton to another (e.g., a frontend agent passing to a testing agent), the Context Engine synthesizes a "handoff context." This includes a summary of the changes made, the current state of the files, and specific instructions or points of interest for the next agent.
- **Live Updates:** As an agent mutates the workspace (e.g., writing a file), the Context Engine captures these events and broadcasts relevant updates to other active agents, ensuring all agents operate on the most current truth.
