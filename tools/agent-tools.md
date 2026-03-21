# Agent Tools Overview

The Agent Tools layer provides a standardized, safe, and reusable set of interfaces that allow AI agents to interact with the PEN.GUIN workspace and underlying system infrastructure.

## Purpose
Agent Tools abstract away low-level system operations (like reading files, executing shell commands, or parsing ASTs). They ensure that when an agent needs to perform an action, it does so through a controlled, observable, and secure pathway rather than raw, unchecked execution.

## When Agents Should Use It
Agents should rely on these tools for any action that mutates state or requires reading from the environment. This includes searching codebases, manipulating strings in files, executing test runners, or querying APIs. Agents must never attempt to bypass these tools using raw terminal commands unless explicitly granted the highest level of authorization.

## Interaction with the AI Kernel
The AI Kernel monitors every tool invocation. It logs tool usage into the `Memory Model` (creating a history of actions taken to solve a problem) and tracks state changes via the `Context Engine`. If a tool call fails, the Kernel captures the error and feeds it back to the agent for self-correction.

## Interaction with the Routing System
The `Skill Router` provisions specific configurations of these tools based on the task. For example, if a sub-task is tagged as "Read-Only," the router ensures the agent only has access to read-based tools, masking destructive tools to enforce safe execution boundaries.
