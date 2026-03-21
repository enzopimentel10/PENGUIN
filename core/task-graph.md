# Task Graph System

The PEN.GUIN ecosystem relies on a mathematical model to guarantee that complex, multi-step workflows are executed in the correct order without breaking dependencies. This model is the **Task Graph**.

## What is a Task Graph?

A Task Graph is a Directed Acyclic Graph (DAG). It is an in-memory data structure maintained by the `Workflow Engine` that visualizes an `Execution Plan` not as a simple list of chores, but as a web of interconnected prerequisites. 

- **Directed:** The relationships have a strict direction (Task A *must precede* Task B).
- **Acyclic:** There are no loops. (Task A cannot depend on Task B if Task B also depends on Task A. The `Planner Agent` runs a validation check to ensure no cycles are created, which would cause an infinite deadlock).

## Tasks as Nodes

When the `Workflow Engine` ingests an Execution Plan, the first step is node generation.
- Every `subtask` defined in the JSON plan is instantiated as a "Node" in the graph.
- A Node contains the task's state (`Pending`, `Active`, `Completed`, `Failed`), its required `competency_tags`, and the actual payload that will be sent to the agent.
- Independent tasks (e.g., "Setup Linter" and "Initialize Database Schema") become standalone nodes with no initial constraints.

## Dependencies as Edges

The true structure of the graph is formed by its edges (the lines connecting the nodes).
- The `Workflow Engine` reads the `dependencies` array within each subtask.
- If Subtask-2 (Build Login UI) lists Subtask-1 (Build Auth API) in its dependencies array, the Engine draws a directed edge from Subtask-1 to Subtask-2.
- This edge acts as a strict state lock. It mathematically guarantees that the Node for Subtask-2 cannot transition from a `Blocked` state to a `Pending` state until the Node for Subtask-1 achieves a `Completed` state.

## Executing the Graph

The system executes tasks by "walking" the graph topographically.

1. **Identifying the Frontier:** The `Agent Router` continuously polls the graph to find the "Frontier"—the set of all nodes that currently have zero incoming edges (meaning they have no unresolved dependencies). 
2. **Parallel Execution:** Because nodes on the frontier are independent of each other, the Router can assign them to different agents simultaneously. The Backend Agent can work on the Database Schema while the Automation Agent configures the CI/CD pipeline.
3. **Edge Resolution:** When an agent finishes a task (e.g., Subtask-1 is completed), the `Workflow Engine` updates that node's state. It then follows the outgoing edges from that node and "resolves" the dependency lock on the downstream nodes (e.g., Subtask-2).
4. **Dynamic Frontier Expansion:** As upstream nodes complete, new downstream nodes have their final dependencies resolved. These newly freed nodes enter the `Pending` state and become the new Frontier, ready to be picked up by idle agents.
5. **Handling Failures:** If a node (task) fails, the graph prevents cascading corruption. The `Workflow Engine` freezes the failed node. Because the node never reaches the `Completed` state, its outgoing edges never resolve. Therefore, all downstream tasks remain safely `Blocked`, preventing agents from attempting to build a UI on top of a failed API.
