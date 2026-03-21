# Skill Index

The Skill Index is the central, dynamic directory of all capabilities currently loaded into the PEN.GUIN ecosystem. It acts as the bridge between raw discovered skills and the routing logic that provisions them to agents.

## Dynamic Querying by Agents

Agents do not need to memorize the entire index. The `Skill Router` automatically provisions the most relevant skills into an agent's context based on the task description. However, agents with sufficient permissions can dynamically query the Skill Index during execution:
- An agent can output a specific tool call (e.g., `query_skill_index(category="frontend")`) to discover available capabilities if it encounters an unforeseen roadblock.
- The index returns a structured list of available skills, including instructions on how to invoke them via the `Skill Loader`.

## Supported Features

The Skill Index is designed to support a robust, enterprise-grade capability ecosystem:

### Skill Categorization
The index organizes skills into strictly defined domains (e.g., Architecture, Frontend, Security, Documentation). This taxonomy ensures that the `Skill Router` only provisions backend tools to a `Backend Agent`, maintaining architectural guardrails.

### Skill Versioning
When importing from libraries like `antigravity-awesome-skills`, the index tracks the version of each skill. If a skill is updated, the index maintains backward compatibility by keeping the older version available for legacy tasks while defaulting new tasks to the latest version.

### Agent Permissions
Not all skills are available to all agents. The index enforces an Access Control List (ACL). A `Frontend Agent` does not have permission to invoke the `schema-designer` skill. The index verifies an agent's role and security clearance before allowing the `Skill Loader` to execute a requested skill.

### Skill Chaining
The index maps "Input/Output" schemas for every skill. This allows the `Agent Orchestrator` to automatically determine if two skills can be chained together (i.e., if the output format of Skill A matches the required input format of Skill B).
