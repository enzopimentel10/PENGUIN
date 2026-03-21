# Skill Adapter Layer

The Skill Adapter Layer is a crucial structural pattern in the PEN.GUIN ecosystem. It allows the AI Kernel to utilize third-party capabilities, such as those found in `skills/antigravity-awesome-skills`, without ever modifying the source files of the external library.

## The Purpose of the Adapter

External libraries often have their own specific prompt formats, execution runners, and input/output expectations that do not perfectly align with PEN.GUIN's internal `Skill Loader` and `Agent Tools` architecture. The Adapter Layer serves as a real-time translator.

## How Mapping Works

When an agent invokes a skill originating from the external library, the request passes through the Adapter Layer:

1. **Prompt Translation:** The external library may provide a raw markdown prompt intended for a human to copy-paste. The Adapter parses this markdown, extracts the system instructions, and reformats it into the parameterized prompt format required by PEN.GUIN's `Context Engine`.
2. **Tool Invocation Mapping:** If the external skill defines a specific tool schema (e.g., an OpenAPI spec), the Adapter converts this schema into the native tool-calling format understood by the PEN.GUIN agents. 
3. **Execution Sandboxing:** When the skill requires executing a script from the external `tools/` folder, the Adapter wraps the execution in PEN.GUIN's `Task Executor`. It translates the agent's standardized JSON output into the specific command-line arguments required by the external script.
4. **Output Standardization:** The external tool might output raw text or a proprietary JSON structure. The Adapter intercepts this output and sanitizes/standardizes it before passing it back into the agent's context window, ensuring seamless skill chaining.

## Maintaining Immutability

By routing all interactions through the Adapter Layer, the PEN.GUIN ecosystem guarantees that the `antigravity-awesome-skills` directory remains strictly read-only. This allows the user to easily update the external library via Git pull or NPM update without breaking internal PEN.GUIN integrations or losing custom configurations.
