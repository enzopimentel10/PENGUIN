# Skill Discovery

The PEN.GUIN ecosystem automatically discovers and integrates capabilities from external libraries like `antigravity-awesome-skills` without requiring manual definition for every tool.

## The Discovery Process

The discovery process is initiated during the system bootstrap phase or when a manual `register-skill --scan` command is executed.

1. **Index Scanning:** The discovery module prioritizes reading the `skills_index.json` file located at the root of `skills/antigravity-awesome-skills/`. This file acts as the primary manifest for the entire third-party library.
2. **Directory Traversal:** If the index is missing or out of date, the discovery module falls back to traversing the `skills/` and `tools/` subdirectories within the external library, parsing individual markdown and JSON files to identify capabilities.
3. **Metadata Extraction:** The scanner extracts critical metadata for each discovered skill, including its name, description, required tool parameters, system prompts, version number, and categorization tags.
4. **Validation:** The scanner validates the extracted metadata against the PEN.GUIN internal schema to ensure all required fields are present before attempting registration.

## Dynamic Registration

Once a skill is successfully discovered and validated, it is passed to the AI Kernel for dynamic registration. 

- The Kernel does not modify the external files. Instead, it generates a virtual "Skill Profile" in the active Memory Model.
- This profile maps the external skill's attributes to the internal fields required by the `Skill Router` and `Agent Router`.
- The skill is then appended to the active `Skill Index`, making it instantly available for provisioning to agents based on their assigned tasks and permissions.
