import pytest
import sys
import os

def test_imports():
    # These should work without sys.path hacks if running from project root
    import scripts.graph.task_graph
    import scripts.cognition.result_evaluator
    import scripts.cognition.cognitive_loop
    import scripts.autonomy.autonomy_guard
    import scripts.autonomy.risk_evaluator
    import scripts.planner.plan_generator
    import scripts.agents.agent_registry
    import scripts.agents.agent_loader
    import scripts.agents.agent_runner
    print("All core modules imported successfully.")
