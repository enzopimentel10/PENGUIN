import pytest
import os
from scripts.autonomy.autonomy_guard import AutonomyGuard
from scripts.autonomy.risk_evaluator import RiskLevel

def test_missing_action():
    guard = AutonomyGuard()
    decision, params = guard.authorize_action("", {})
    assert decision == "allow"
    assert params == {}

def test_read_file_safe():
    guard = AutonomyGuard()
    decision, params = guard.authorize_action("read_file", {"filename": "test.txt"})
    assert decision == "allow"
    assert params == {"filename": "test.txt"}

def test_infinite_loop_prevention():
    guard = AutonomyGuard()
    session_id = "test_loop"
    for _ in range(10):
        decision, _ = guard.authorize_action("read_file", {"filename": "test.txt"}, session_id=session_id)
        assert decision == "allow"
    
    # 11th step should be blocked
    decision, _ = guard.authorize_action("read_file", {"filename": "test.txt"}, session_id=session_id)
    assert decision == "block"

def test_boundary_check(tmp_path):
    guard = AutonomyGuard()
    # Attempting to access file outside artifacts directory
    decision, _ = guard.authorize_action("read_file", {"filename": "../../etc/passwd"})
    assert decision == "block"

def test_write_file_high_risk_backup(tmp_path):
    # This test is a bit complex as it needs to check for side effects (backup)
    # We should point to a temporary artifacts directory
    import scripts.autonomy.autonomy_guard
    import scripts.autonomy.risk_evaluator
    original_dir_guard = scripts.autonomy.autonomy_guard.ARTIFACTS_DIR
    original_dir_risk = scripts.autonomy.risk_evaluator.ARTIFACTS_DIR
    
    scripts.autonomy.autonomy_guard.ARTIFACTS_DIR = str(tmp_path)
    scripts.autonomy.risk_evaluator.ARTIFACTS_DIR = str(tmp_path)
    
    # Create the file first so overwrite is triggered
    test_file = tmp_path / "test.txt"
    test_file.write_text("original")
    
    guard = AutonomyGuard()
    decision, params = guard.authorize_action("write_file", {"filename": "test.txt", "content": "new"})
    
    assert decision == "modify"
    assert (tmp_path / "test.txt.bak").exists()
    assert (tmp_path / "test.txt.bak").read_text() == "original"
    
    # Cleanup
    scripts.autonomy.autonomy_guard.ARTIFACTS_DIR = original_dir_guard
    scripts.autonomy.risk_evaluator.ARTIFACTS_DIR = original_dir_risk
