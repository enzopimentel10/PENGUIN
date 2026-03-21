import argparse

class CommandParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="PEN.GUIN CLI - Command Parser")
        self.subparsers = self.parser.add_subparsers(dest="command", help="The command to execute")
        
        # Subcommand 'run'
        run_parser = self.subparsers.add_parser("run", help="Trigger the execution of a task")
        run_parser.add_argument("objective", type=str, help="The task or feature to build")

    def parse(self, args):
        parsed_args = self.parser.parse_args(args)
        if parsed_args.command == "run":
            return {
                "command": "run",
                "objective": parsed_args.objective
            }
        else:
            self.parser.print_help()
            return None
