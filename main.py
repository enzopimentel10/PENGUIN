import argparse
import os
import json
import sys

from scripts.planner.plan_generator import PlanGenerator
from scripts.graph.graph_builder import GraphBuilder
from scripts.execution.execution_engine import ExecutionEngine

def main():
    parser = argparse.ArgumentParser(description="PENGUIN Native Orchestrator")
    parser.add_argument("--task", required=True, help="Path to the task JSON file")
    args = parser.parse_args()

    task_file = args.task
    if not os.path.exists(task_file):
        print(f"Error: Task file not found: {task_file}")
        return

    # 0. Setup Workspace
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(script_dir)
    
    plan_dir = os.path.join(project_root, "workspace", "plan")
    session_dir = os.path.join(project_root, "workspace", "sessions")
    log_dir = os.path.join(project_root, "workspace", "logs")
    
    os.makedirs(plan_dir, exist_ok=True)
    os.makedirs(session_dir, exist_ok=True)
    os.makedirs(log_dir, exist_ok=True)

    # 1. Planner
    print(f"\n[*] PHASE 1: PLANNING...")
    planner = PlanGenerator(plan_dir)
    plan_file = planner.generate_plan(task_file)
    
    if not plan_file:
        print("[!] Planning failed. Aborting.")
        sys.exit(1)

    # 2. Graph Builder
    print(f"\n[*] PHASE 2: BUILDING TASK GRAPH...")
    builder = GraphBuilder(session_dir)
    graph_file = builder.build_graph(plan_file)
    
    if not graph_file:
        print("[!] Graph building failed. Aborting.")
        sys.exit(1)

    # 3. Execution Engine
    print(f"\n[*] PHASE 3: EXECUTING...")
    engine = ExecutionEngine(log_dir, session_dir)
    graph = engine.load_graph(graph_file)
    
    if not graph:
        print("[!] Failed to load graph for execution. Aborting.")
        sys.exit(1)
        
    try:
        engine.run(graph)
        print(f"\n[+] Task {graph.task_id} orchestration complete.")
    except Exception as e:
        print(f"\n[!] Critical error during execution: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
