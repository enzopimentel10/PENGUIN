# Register Skill Workflow (`register-skill.sh`)

This script manages the addition of new capabilities to the ecosystem, ensuring they are safely available for agent use.

## Workflow Overview
When `register-skill --name <skill-name>` is executed, the following sequence occurs:

1. **Dependency Resolution:** The script first checks if the skill has any system-level dependencies (e.g., requires `npm install`, requires a specific CLI tool like `ripgrep`). It attempts to resolve these automatically.
2. **Manifest Validation:** It validates the skill's definition, checking for required metadata such as input parameters, expected output format, and authorization requirements.
3. **Security Sandboxing:** The script sets up the execution boundaries for the skill. If the skill involves executing raw code, the script ensures it is wrapped in the `Task Executor` sandbox.
4. **Kernel Registration:** The validated skill profile is sent to the AI Kernel.
5. **Skill Registry Update:** The Kernel updates the `Skill Registry`. The `Skill Router` is notified, making the new capability available for dynamic provisioning during the `Task Analysis` phase of the automation pipeline.
