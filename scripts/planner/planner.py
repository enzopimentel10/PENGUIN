import os
import argparse
from scripts.planner.plan_generator import PlanGenerator

def main():
    parser = argparse.ArgumentParser(description="PEN.GUIN Planner Agent")
    parser.add_argument("--task-file", required=True, help="Path to the task file")
    
    # Determine absolute path to the workspace directory
    # scripts/planner/planner.py -> ../../workspace
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
    default_output_dir = os.path.join(project_root, "workspace", "plan")
    
    parser.add_argument("--output-dir", default=default_output_dir, help="Directory to save the execution plan")
    
    args = parser.parse_args()
    
    generator = PlanGenerator(args.output_dir)
    generator.generate_plan(args.task_file)

if __name__ == "__main__":
    main()