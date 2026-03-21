# AI Kernel and Skill System Integration

This document outlines how the PEN.GUIN AI Kernel integrates with external skill packages, specifically focusing on the integration of `antigravity-awesome-skills`.

## 1. Skill Discovery

The AI Kernel does not hardcode skills. It discovers them dynamically during the system bootstrap phase.
- **Manifest Scanning:** The `bootstrap-system` script scans the `skills/antigravity-awesome-skills/` directory for `manifest.json` files. These manifests conform to a strict schema, defining the skill's name, description, required inputs, guaranteed outputs, and category (e.g., `frontend`, `security`).
- **Dynamic Registration:** For each valid manifest found, the discovery script triggers the `register-skill` workflow, sending the parsed metadata to the Kernel via the API.

## 2. Skill Loading

Loading a skill makes it available for execution within the workspace sandbox.
- **Dependency Resolution:** When a skill is registered, the Kernel checks the manifest for required CLI tools, NPM packages, or Python libraries. It uses the `Task Executor` to silently install these dependencies into an isolated virtual environment or node_modules cache specific to the skills layer.
- **Mounting:** The Kernel mounts the skill's executable logic into the `Skill Loader`. The Skill Loader acts as an abstraction layer; it knows *how* to run the skill (e.g., executing a node script or a python module) so the agent doesn't have to figure out the command line syntax.

## 3. Skill Router Selection

The Skill Router determines *when* a skill should be provided to an agent.
- **Task Intent Matching:** When the `Task Classifier` analyzes an objective (e.g., "Check for exposed API keys"), it tags the task with intents (`Security`, `Secret Scanning`).
- **Provisioning:** The Skill Router queries the loaded skill manifests. If the `secret-scanner` skill from `antigravity-awesome-skills` matches the task tags, the Router provisions this capability to the active agent.
- **Context Injection:** Provisioning means the Router instructs the `Context Engine` to append the skill's usage instructions (from its manifest) to the agent's active prompt. The agent is now "aware" it possesses this specific capability.

## 4. Agent Invocation

Agents invoke skills using a standardized tool interface, rather than raw shell commands.
- **Structured Tool Call:** The agent outputs a structured command (e.g., JSON format) directed at the `Skill Loader`, passing the required parameters defined in the skill's manifest.
- **Execution via Loader:** The Skill Loader intercepts this command, formats the raw system command, executes the `antigravity-awesome-skills` script within the sandbox, and captures the stdout/stderr.
- **Feedback Loop:** The output is sanitized and injected back into the agent's context window. If the skill failed (e.g., bad parameters), the error is provided to the agent so it can correct its tool call.
