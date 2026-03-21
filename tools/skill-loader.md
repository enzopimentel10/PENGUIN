# Skill Loader

The Skill Loader is a specialized tool responsible for dynamically mounting and executing discrete "skills" (such as those from `antigravity-awesome-skills`) into the agent's current runtime.

## Purpose
Its purpose is to provide a standardized mechanism to execute complex, multi-step algorithms (skills) without requiring the agent to understand the underlying implementation of the skill itself. It acts as the bridge between declarative skill definitions and executable code.

## When Agents Should Use It
Agents invoke the Skill Loader when they need to utilize a specific, high-level capability that extends beyond basic file manipulation. For example, when an agent needs to "generate a React component," it doesn't write the React code line-by-line from scratch; it uses the Skill Loader to invoke the `component-generator` skill, passing in the required parameters.

## Interaction with the AI Kernel
The Skill Loader requests permission from the AI Kernel before mounting any skill. The Kernel verifies against the `Skill Registry` that the skill exists, is secure, and that the requesting agent is authorized to use it. Once executed, the Skill Loader pipes the output back to the Kernel's Context Engine.

## Interaction with the Routing System
The Skill Loader is heavily directed by the `Skill Router` and `Agent Orchestrator`. The Orchestrator often pre-formats the inputs required for the Skill Loader, chaining the output of one skill directly into the loader for the next, creating a seamless automated pipeline.
