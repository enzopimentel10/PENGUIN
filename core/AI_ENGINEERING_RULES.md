# AI Engineering Rules

These rules govern the engineering standards for all AI agents working within the PEN.GUIN ecosystem.

## Code Quality
- **Idiomatic Code:** All code generated must adhere to the conventions and idioms of the host language and framework.
- **Maintainability:** Prioritize readability and simplicity. Avoid overly clever or opaque solutions. Code should be self-documenting where possible.
- **No Orphaned Logic:** Do not leave unreferenced variables, dead code, or incomplete implementations. Every piece of code must have a clear purpose.

## Testing Policies
- **Test-Driven Operations:** All bug fixes and feature implementations must be accompanied by relevant test cases.
- **Regression Prevention:** Agents must run the existing test suite after modifying any shared modules. If a test fails, the agent must fix the regression before concluding the task.
- **Test Coverage:** Aim to maintain or increase the project's overall test coverage with every modification.

## Documentation Requirements
- **Inline Comments:** Use comments to explain the *why* behind complex logic, not the *what*.
- **API Documentation:** Any exposed interfaces or public functions must be documented using standard docstrings (e.g., JSDoc, PyDoc).
- **Changelogs:** Significant architectural changes must be recorded in the relevant documentation directories (`/docs`).

## Security Considerations
- **Credential Protection:** Agents must never log, hardcode, or commit sensitive credentials, API keys, or tokens. Use environment variables.
- **Input Validation:** All external inputs to any generated service or module must be rigorously validated to prevent injection attacks.
- **Dependency Auditing:** When adding new libraries, agents must verify that the dependency is secure, well-maintained, and compatible with the existing ecosystem.
