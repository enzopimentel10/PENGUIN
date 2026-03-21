import os
import sys
import json
import argparse
import time
from typing import Optional

from scripts.graph.task_graph import TaskGraph, NodeStatus
from scripts.execution.node_executor import NodeExecutor
from scripts.cognition.cognitive_loop import CognitiveLoop

class ExecutionEngine:
    def __init__(self, log_dir: str, sessions_dir: str):
        self.executor = NodeExecutor(log_dir)
        self.sessions_dir = sessions_dir
        self.cognition = CognitiveLoop()
        self.retry_limit = 3
        self.retry_counts = {} # node_id -> count

    def load_graph(self, graph_path: str) -> Optional[TaskGraph]:
        if not os.path.exists(graph_path):
            print(f"Error: Graph file not found at {graph_path}")
            return None
        
        try:
            with open(graph_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return TaskGraph.from_dict(data)
        except Exception as e:
            print(f"Error loading graph: {e}")
            return None

    def run(self, graph: TaskGraph):
        print(f"[*] Starting execution engine for Task ID: {graph.task_id}")
        
        while True:
            executable_nodes = graph.get_executable_nodes()
            
            if not executable_nodes:
                # Check if all nodes are completed
                all_completed = all(node.status == NodeStatus.COMPLETED for node in graph.nodes.values())
                if all_completed:
                    print(f"[+] Task {graph.task_id} completed successfully.")
                    break
                
                # Support resuming from RUNNING status if it was interrupted (e.g. by handoff)
                running_nodes = [n for n in graph.nodes.values() if n.status == NodeStatus.RUNNING]
                if running_nodes:
                    executable_nodes = running_nodes
                else:
                    print("[-] Execution engine: No more executable nodes. Graph might be completed or stalled.")
                    break

            for node in executable_nodes:
                if node.status != NodeStatus.RUNNING:
                    node.status = NodeStatus.RUNNING
                    graph.save(self.sessions_dir) # Persist status change

                try:
                    results = self.executor.execute(graph.task_id, node)
                    node.results = results
                    
                    # Evaluate result via Cognitive Loop
                    action = self.cognition.process_node_result(graph, node)
                    
                    if action == "retry":
                        node_id = node.node_id
                        self.retry_counts[node_id] = self.retry_counts.get(node_id, 0) + 1
                        if self.retry_counts[node_id] >= self.retry_limit:
                            print(f"[!] Node {node_id} reached retry limit. Failing task.")
                            node.status = NodeStatus.FAILED
                        else:
                            print(f"[*] Node {node_id} will retry ({self.retry_counts[node_id]}/{self.retry_limit})")
                    
                    # status change (COMPLETED/FAILED/etc) is persisted here
                    graph.save(self.sessions_dir)
                    
                except Exception as e:
                    print(f"[!] Error executing node {node.node_id}: {e}")
                    node.status = NodeStatus.FAILED
                    graph.save(self.sessions_dir)
                
            time.sleep(0.5)

def main():
    parser = argparse.ArgumentParser(description="PEN.GUIN Execution Engine")
    parser.add_argument("--graph-file", required=True, help="Path to the task graph file")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
    
    default_log_dir = os.path.join(project_root, "workspace", "logs")
    default_sessions_dir = os.path.join(project_root, "workspace", "sessions")
    
    parser.add_argument("--log-dir", default=default_log_dir, help="Directory to save execution logs")
    parser.add_argument("--sessions-dir", default=default_sessions_dir, help="Directory to persist graph updates")
    
    args = parser.parse_args()
    
    engine = ExecutionEngine(args.log_dir, args.sessions_dir)
    graph = engine.load_graph(args.graph_file)
    
    if graph:
        engine.run(graph)

if __name__ == "__main__":
    main()
