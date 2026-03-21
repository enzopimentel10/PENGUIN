import json
import os
import argparse
from typing import Optional
import sys

from .task_graph import TaskGraph, TaskNode

class GraphBuilder:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir

    def build_graph(self, plan_file: str) -> Optional[str]:
        if not os.path.exists(plan_file):
            print(f"Error: Plan file not found at {plan_file}")
            return None

        try:
            with open(plan_file, 'r', encoding='utf-8') as f:
                plan_data = json.load(f)
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in plan file {plan_file}")
            return None
        except Exception as e:
            print(f"Error reading plan file: {e}")
            return None

        task_id = plan_data.get("task_id")
        if not task_id:
            print("Error: task_id not found in plan file")
            return None

        graph = TaskGraph(task_id)
        # Handle both 'nodes' (new) and 'steps' (old) for maximum compatibility
        nodes_data = plan_data.get("nodes", plan_data.get("steps", []))

        # Step 1: Create all nodes first
        node_id_list = []
        for node_data in nodes_data:
            node_id = node_data.get("node_id", node_data.get("step_id"))
            agent = node_data.get("agent")
            instruction = node_data.get("instruction")
            
            if not all([node_id, agent, instruction]):
                print(f"Warning: Skipping incomplete node: {node_data}")
                continue
                
            node = TaskNode(node_id, agent, instruction)
            graph.add_node(node)
            node_id_list.append(node_id)

        # Step 2: Define dependencies
        for i, node_data in enumerate(nodes_data):
            node_id = node_data.get("node_id", node_data.get("step_id"))
            if node_id not in graph.nodes:
                continue
                
            explicit_deps = node_data.get("dependencies", [])
            
            if explicit_deps:
                # Use LLM-provided dependencies
                for dep_id in explicit_deps:
                    if dep_id in graph.nodes:
                        graph.add_dependency(node_id, dep_id)
                    else:
                        print(f"Warning: Dependency {dep_id} for {node_id} not found in nodes.")
            elif i > 0:
                # Fallback to sequential if no dependencies are specified
                # This ensures the graph is always connected and logical.
                prev_node_id = nodes_data[i-1].get("node_id", nodes_data[i-1].get("step_id"))
                graph.add_dependency(node_id, prev_node_id)

        graph.save(self.output_dir)
        return os.path.join(self.output_dir, f"{task_id}_graph.json")

def main():
    parser = argparse.ArgumentParser(description="PEN.GUIN Graph Builder")
    parser.add_argument("--plan-file", required=True, help="Path to the execution plan file")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
    default_output_dir = os.path.join(project_root, "workspace", "sessions")
    
    parser.add_argument("--output-dir", default=default_output_dir, help="Directory to save the task graph")
    
    args = parser.parse_args()
    
    builder = GraphBuilder(args.output_dir)
    builder.build_graph(args.plan_file)

if __name__ == "__main__":
    main()
