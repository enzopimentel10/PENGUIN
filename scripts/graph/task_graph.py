import json
import os
from enum import Enum
from typing import List, Dict, Any, Optional

class NodeStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"

class TaskNode:
    def __init__(self, node_id: str, agent: str, instruction: str):
        self.node_id = node_id
        self.agent = agent
        self.instruction = instruction
        self.status = NodeStatus.PENDING
        self.dependencies: List[str] = []
        self.results: Any = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_id": self.node_id,
            "agent": self.agent,
            "instruction": self.instruction,
            "status": self.status.value,
            "dependencies": self.dependencies,
            "results": self.results
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TaskNode':
        node = cls(data["node_id"], data["agent"], data["instruction"])
        node.status = NodeStatus(data["status"])
        node.dependencies = data.get("dependencies", [])
        node.results = data.get("results")
        return node

class TaskGraph:
    def __init__(self, task_id: str):
        self.task_id = task_id
        self.nodes: Dict[str, TaskNode] = {}

    def add_node(self, node: TaskNode):
        self.nodes[node.node_id] = node

    def add_dependency(self, node_id: str, depends_on: str):
        if node_id in self.nodes and depends_on in self.nodes:
            if depends_on not in self.nodes[node_id].dependencies:
                self.nodes[node_id].dependencies.append(depends_on)

    def get_executable_nodes(self) -> List[TaskNode]:
        """Returns nodes that have all dependencies completed and are still pending."""
        executable = []
        for node in self.nodes.values():
            if node.status == NodeStatus.PENDING:
                all_deps_completed = True
                for dep_id in node.dependencies:
                    if self.nodes[dep_id].status != NodeStatus.COMPLETED:
                        all_deps_completed = False
                        break
                if all_deps_completed:
                    executable.append(node)
        return executable

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "nodes": {node_id: node.to_dict() for node_id, node in self.nodes.items()}
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TaskGraph':
        graph = cls(data["task_id"])
        for node_id, node_data in data["nodes"].items():
            graph.add_node(TaskNode.from_dict(node_data))
        return graph

    def save(self, directory: str):
        os.makedirs(directory, exist_ok=True)
        filepath = os.path.join(directory, f"{self.task_id}_graph.json")
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2)
        print(f"Task graph saved to: {filepath}")
