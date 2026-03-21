# PEN.GUIN Task File Format

Tasks in the PEN.GUIN system are stored in the `workspace/tasks` directory, typically as JSON files. This document outlines the schema and fields used in these task files to track and manage work.

## Core Fields

Every task file uses the following fields to ensure proper tracking, execution, and artifact management within the system:

### `id`
*   **Type:** String
*   **Description:** A unique identifier for the task (e.g., `task-38163142`). This ID is used for referencing the task across the workspace, logs, and routing systems.

### `description`
*   **Type:** String
*   **Description:** A clear, comprehensive description of the objective or work to be performed by the assigned agent.

### `status`
*   **Type:** String
*   **Description:** The current state of the task in its lifecycle. Valid states typically include:
    *   `pending`: The task is queued and waiting for execution.
    *   `in_progress`: The task is currently being processed by an agent.
    *   `completed`: The task has been successfully finished and validated.
    *   `failed`: The task execution failed.
    *   `blocked`: The task cannot proceed due to dependencies or external factors.

### `execution_plan`
*   **Type:** Array / Object
*   **Description:** The structured step-by-step strategy formulated to complete the task. This includes sub-tasks, required tools, and the planned approach.

### `artifacts`
*   **Type:** Array of Strings
*   **Description:** A list of file paths or references to any outputs generated as a result of completing the task. These are typically managed by the artifact system and stored in the `workspace/artifacts` directory.
