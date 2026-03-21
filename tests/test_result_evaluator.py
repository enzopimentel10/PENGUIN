import pytest
from scripts.cognition.result_evaluator import ResultEvaluator, EvaluationResult

def test_empty_results():
    evaluator = ResultEvaluator()
    res = evaluator.evaluate("node_1", {})
    assert res.action == "retry"

def test_failed_status():
    evaluator = ResultEvaluator()
    res = evaluator.evaluate("node_1", {"status": "failed"})
    assert res.action == "retry"

def test_empty_output():
    evaluator = ResultEvaluator()
    res = evaluator.evaluate("node_1", {"status": "success", "output": ""})
    assert res.action == "retry"

def test_task_complete_keyword():
    evaluator = ResultEvaluator()
    res = evaluator.evaluate("node_1", {"status": "success", "output": "TASK_COMPLETE: all done"})
    assert res.action == "complete"

def test_status_complete_dict():
    evaluator = ResultEvaluator()
    res = evaluator.evaluate("node_1", {"status": "success", "output": {"status": "complete"}})
    assert res.action == "complete"

def test_skill_executions_continue():
    evaluator = ResultEvaluator()
    res = evaluator.evaluate("node_1", {"status": "success", "output": {"skill_executions": ["some_skill"]}})
    assert res.action == "continue"

def test_default_success_complete():
    evaluator = ResultEvaluator()
    res = evaluator.evaluate("node_1", {"status": "success", "output": "Regular response"})
    assert res.action == "complete"

def test_ambiguous_refine():
    evaluator = ResultEvaluator()
    res = evaluator.evaluate("node_1", {"status": "unknown", "output": "something"})
    assert res.action == "refine"
