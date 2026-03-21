import pytest
from scripts.cognition.context_engine import ContextEngine

def test_record_and_get():
    ce = ContextEngine()
    results = {"status": "success", "output": "Discovery 1"}
    ce.record_result("node_1", results)
    
    all_res = ce.get_all_results()
    assert "node_1" in all_res
    assert all_res["node_1"] == results

def test_formatted_context():
    ce = ContextEngine()
    ce.record_result("node_1", {"output": "Findings from node 1"})
    ce.record_result("node_2", {"output": {"skill_executions": [{"action": "read_file", "status": "success", "result": "Content of file"}]}})
    
    ctx = ce.get_formatted_context()
    assert "Results from Node: node_1" in ctx
    assert "Findings from node 1" in ctx
    assert "Executed read_file (success): Content of file" in ctx

def test_formatted_context_exclude():
    ce = ContextEngine()
    ce.record_result("node_1", {"output": "A"})
    ce.record_result("node_2", {"output": "B"})
    
    ctx = ce.get_formatted_context(exclude_node_id="node_2")
    assert "node_1" in ctx
    assert "node_2" not in ctx

def test_clear():
    ce = ContextEngine()
    ce.record_result("node_1", {"output": "A"})
    ce.clear()
    assert ce.get_all_results() == {}
