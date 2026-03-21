import os
import shutil
from typing import Dict, Any, List, Callable, Optional

# Define project root
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
ARTIFACTS_DIR = os.path.join(project_root, "workspace", "artifacts")



def _get_safe_path(path: str) -> str:
    """Ensures the path is inside the artifacts directory."""
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    # Normalize path and check if it starts with the artifacts directory
    full_path = os.path.abspath(os.path.join(ARTIFACTS_DIR, path))
    if not full_path.startswith(ARTIFACTS_DIR):
        raise PermissionError(f"Access denied: '{path}' is outside the artifacts directory.")
    return full_path

# --- Skill Implementations ---

def create_file(params: Dict[str, Any]) -> str:
    """Creates an empty file at the specified path."""
    filename = params.get("filename")
    if not filename:
        return "Error: 'filename' is required."
    
    path = _get_safe_path(filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    with open(path, 'w', encoding='utf-8') as f:
        pass
    
    return f"File '{filename}' created successfully."

def read_file(params: Dict[str, Any]) -> str:
    """Reads the contents of a file."""
    filename = params.get("filename")
    if not filename:
        return "Error: 'filename' is required."
    
    path = _get_safe_path(filename)
    if not os.path.exists(path):
        return f"Error: File '{filename}' not found."
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    return content

def write_file(params: Dict[str, Any]) -> str:
    """Writes content to a file."""
    filename = params.get("filename")
    content = params.get("content", "")
    
    if not filename:
        return "Error: 'filename' is required."
    
    path = _get_safe_path(filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return f"Content written to '{filename}' successfully."

def list_directory(params: Dict[str, Any]) -> str:
    """Lists files and folders in a directory."""
    dir_path = params.get("path", "")
    
    path = _get_safe_path(dir_path)
    if not os.path.exists(path):
        return f"Error: Directory '{dir_path}' not found."
    
    items = os.listdir(path)
    return "\n".join(items) if items else "(Empty directory)"

# --- Registry ---

class SkillRegistry:
    def __init__(self):
        self._skills: Dict[str, Callable[[Dict[str, Any]], str]] = {}
        self._register_initial_skills()

    def register_skill(self, name: str, func: Callable[[Dict[str, Any]], str]):
        self._skills[name] = func
        print(f"[SkillRegistry] Registered skill: {name}")

    def get_skill(self, name: str) -> Optional[Callable[[Dict[str, Any]], str]]:
        return self._skills.get(name)

    def list_skills(self) -> List[str]:
        return list(self._skills.keys())

    def _register_initial_skills(self):
        self.register_skill("create_file", create_file)
        self.register_skill("read_file", read_file)
        self.register_skill("write_file", write_file)
        self.register_skill("list_directory", list_directory)

# Global instance
registry = SkillRegistry()
