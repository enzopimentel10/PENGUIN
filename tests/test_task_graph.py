import pytest
import os
import json
from scripts.graph.task_graph import TaskNode, TaskGraph, NodeStatus

def test_node_to_dict():
    node = TaskNode("node_1", "agent_1", "instruction_1")
    node.dependencies = ["node_0"]
    d = node.to_dict()
    assert d["node_id"] == "node_1"
    assert d["agent"] == "agent_1"
    assert d["instruction"] == "instruction_1"
    assert d["status"] == "pending"
    assert d["dependencies"] == ["node_0"]

def test_node_from_dict():
    data = {
        "node_id": "node_1",
        "agent": "agent_1",
        "instruction": "instruction_1",
        "status": "completed",
        "dependencies": ["node_0"],
        "results": {"output": "done"}
    }
    node = TaskNode.from_dict(data)
    assert node.node_id == "node_1"
    assert node.status == NodeStatus.COMPLETED
    assert node.results == {"output": "done"}

def test_graph_executable_nodes():
    graph = TaskGraph("task_1")
    n1 = TaskNode("n1", "a1", "i1")
    n2 = TaskNode("n2", "a2", "i2")
    n2.dependencies = ["n1"]
    
    graph.add_node(n1)
    graph.add_node(n2)
    
    executable = graph.get_executable_nodes()
    assert len(executable) == 1
    assert executable[0].node_id == "n1"
    
    n1.status = NodeStatus.COMPLETED
    executable = graph.get_executable_nodes()
    assert len(executable) == 1
    assert executable[0].node_id == "n2"

def test_graph_serialization(tmp_path):
    graph = TaskGraph("test_task")
    n1 = TaskNode("n1", "a1", "i1")
    graph.add_node(n1)
    
    d = graph.to_dict()
    graph2 = TaskGraph.from_dict(d)
    assert graph2.task_id == "test_task"
    assert "n1" in graph2.nodes
    
    graph.save(str(tmp_path))
    graph_file = tmp_path / "test_task_graph.json"
    assert graph_file.exists()
    with open(graph_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        assert data["task_id"] == "test_task"
