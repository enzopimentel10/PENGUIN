import os
import sys
import json
import uuid
import subprocess
from datetime import datetime

class Runtime:
    def __init__(self, workspace_root):
        self.workspace_root = workspace_root
        self.tasks_dir = os.path.join(workspace_root, "workspace", "tasks")
        self._engine_dir = os.path.join(workspace_root, "engine")

    def create_task_file(self, objective):
        os.makedirs(self.tasks_dir, exist_ok=True)

        task_id = f"task-{str(uuid.uuid4())[:8]}"
        task_data = {
            "task_id": task_id,
            "objective": objective,
            "execution_status": "pending",
            "routing_metadata": {
                "assigned_agent": None,
                "competency_tags": [],
                "required_skills": []
            },
            "graph_metadata": {
                "dependencies": [],
                "dependents": []
            },
            "payload": {
                "instruction": objective,
                "input_artifacts": [],
                "output_artifacts": []
            },
            "execution_log": {
                "session_id": str(uuid.uuid4()),
                "started_at": str(datetime.now()),
                "completed_at": None,
                "error_trace": None
            }
        }

        file_path = os.path.join(self.tasks_dir, f"{task_id}.json")
        with open(file_path, "w") as f:
            json.dump(task_data, f, indent=4)

        return task_id, file_path

    def execute_pipeline(self, objective):
        print("[PEN.GUIN] Task received.")

        task_id, task_file = self.create_task_file(objective)
        print(f"[PEN.GUIN] Task file created: {task_file}")

        main_script = os.path.join(self._engine_dir, "main.py")
        if not os.path.isfile(main_script):
            print(f"[PEN.GUIN] ERROR — engine entry point not found: {main_script}")
            sys.exit(1)

        cmd = [sys.executable, main_script, "--task", task_file]
        print(f"[PEN.GUIN] Launching pipeline: {' '.join(cmd)}\n")

        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )

        if process.stdout:
            for line in process.stdout:
                print(line, end="")

        return_code = process.wait()

        if return_code == 0:
            print(f"\n[PEN.GUIN] Task {task_id} completed successfully.")
        else:
            print(f"\n[PEN.GUIN] Task {task_id} failed (exit code {return_code}).")
            sys.exit(return_code)
