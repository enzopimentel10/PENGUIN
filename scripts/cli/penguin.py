import sys
import os
from .command_parser import CommandParser
from .runtime import Runtime

def main():
    # Set the workspace root to the current working directory
    workspace_root = os.getcwd()
    
    parser = CommandParser()
    runtime = Runtime(workspace_root)
    
    # Check if any arguments were provided
    if len(sys.argv) < 2:
        parser.parser.print_help()
        sys.exit(1)
        
    parsed_intent = parser.parse(sys.argv[1:])
    
    if parsed_intent and parsed_intent["command"] == "run":
        objective = parsed_intent["objective"]
        runtime.execute_pipeline(objective)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
