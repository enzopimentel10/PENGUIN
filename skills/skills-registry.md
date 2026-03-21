# Skills Registry

This document serves as the high-level overview of the capability ecosystem within PEN.GUIN, integrating external libraries like `antigravity-awesome-skills` alongside `custom-skills`. 

## Kernel Integration & The Skill Index
Skills are dynamically discovered during system bootstrap (via the `Skill Discovery` module) and compiled into the centralized `Skill Index`. The AI Kernel loads these skills, resolves their dependencies, and utilizes the `Skill Router` to provision them to agents based on task intent matching. 

Crucially, agents can now query the `Skill Index` dynamically during their execution loops if they require new capabilities to overcome an obstacle. 

## The Adapter Layer
External skills are never modified. They are routed through the `Skill Adapter Layer`, which translates external prompts and tool schemas into the native formats required by PEN.GUIN's internal tools and context engines. Agents invoke all skills using the standardized `Skill Loader` abstraction, ensuring secure execution.

## Skill Categories

Skills are grouped by domain to ensure that the Kernel provisions the correct capabilities to the appropriately specialized agents. Agents' access is governed by strict permissions tracked in the index.

### 1. Architecture
*Skills used for system design, structural planning, and codebase analysis.*
- **`codebase-mapper`**: Scans the repository and builds a dependency graph and structural overview.
    - *Agents:* Architecture Agent
    - *When to invoke:* During the initial research phase or when onboarding a large, unfamiliar project.
- **`tech-stack-evaluator`**: Analyzes requirements and recommends compatible, secure libraries or frameworks.
    - *Agents:* Architecture Agent, Security Agent
    - *When to invoke:* When planning a new feature that requires external dependencies.

### 2. Frontend
*Skills used for client-side rendering, styling, and UI logic.*
- **`component-generator`**: Scaffolds reusable UI components (React, Vue, HTML/CSS) based on design descriptions.
    - *Agents:* Frontend Agent
    - *When to invoke:* When implementing new visual elements or views.
- **`css-utility-mapper`**: Translates design guidelines into functional CSS or utility classes (e.g., Tailwind).
    - *Agents:* Frontend Agent
    - *When to invoke:* When styling newly generated components.
- **`a11y-validator`**: Checks DOM structures for accessibility compliance (ARIA roles, contrast).
    - *Agents:* Frontend Agent, Review Agent
    - *When to invoke:* Before handing off UI components to the review phase.

### 3. Backend
*Skills used for server logic, database interactions, and API design.*
- **`schema-designer`**: Generates database schema definitions and migration scripts (SQL, Prisma, etc.).
    - *Agents:* Backend Agent
    - *When to invoke:* When persistent data storage is required for a new feature.
- **`api-scaffolder`**: Creates boilerplate REST/GraphQL endpoint handlers and routing logic.
    - *Agents:* Backend Agent
    - *When to invoke:* When exposing new backend functionality to the frontend.
- **`query-optimizer`**: Analyzes database queries and suggests indexes or structural improvements.
    - *Agents:* Backend Agent, Refactor Agent
    - *When to invoke:* When addressing database performance bottlenecks.

### 4. Security
*Skills used for vulnerability scanning, credential protection, and risk assessment.*
- **`secret-scanner`**: Scans file contents and memory for hardcoded credentials or API keys.
    - *Agents:* Security Agent, Review Agent
    - *When to invoke:* Automatically triggered before any commit or file save operation.
- **`dependency-auditor`**: Checks package manifests against known CVE databases.
    - *Agents:* Security Agent, Architecture Agent
    - *When to invoke:* When adding or updating third-party libraries.
- **`sast-analyzer`**: Performs Static Application Security Testing on source code.
    - *Agents:* Security Agent
    - *When to invoke:* During the review phase of backend or frontend logic implementations.

### 5. Performance
*Skills used for optimizing execution speed, memory usage, and load times.*
- **`bundle-analyzer`**: Evaluates frontend asset sizes and suggests code-splitting opportunities.
    - *Agents:* Frontend Agent, Refactor Agent
    - *When to invoke:* Before finalizing frontend deployments or during technical debt reduction.
- **`algorithmic-profiler`**: Analyzes backend logic for time/space complexity inefficiencies.
    - *Agents:* Refactor Agent, Backend Agent
    - *When to invoke:* When specific functions are identified as bottlenecks.

### 6. Documentation
*Skills used for generating, parsing, and formatting human-readable text.*
- **`docstring-generator`**: Automatically generates inline comments and function signatures based on code logic.
    - *Agents:* Documentation Agent, Review Agent
    - *When to invoke:* When a new module or function is finalized but lacks documentation.
- **`readme-updater`**: Parses recent codebase changes and synthesizes updates for the main `README.md`.
    - *Agents:* Documentation Agent
    - *When to invoke:* At the end of a major feature implementation or architectural change.

### 7. Testing
*Skills used for asserting code behavior and preventing regressions.*
- **`unit-test-generator`**: Scaffolds isolated tests for specific functions or components, including mock data.
    - *Agents:* Test Agent
    - *When to invoke:* Immediately after a new function or component is implemented.
- **`coverage-reporter`**: Executes test suites and parses the output to determine missing test coverage.
    - *Agents:* Test Agent, Review Agent
    - *When to invoke:* During the review process to ensure the `AI_ENGINEERING_RULES.md` are met.

### 8. Code Review
*Skills used for enforcing style, checking complexity, and finding anti-patterns.*
- **`linter-executor`**: Runs language-specific linters and formats code according to project conventions.
    - *Agents:* Review Agent, Refactor Agent
    - *When to invoke:* Before any code is considered "complete" or ready for handoff.
- **`complexity-scorer`**: Calculates the cyclomatic complexity of functions.
    - *Agents:* Review Agent
    - *When to invoke:* During code review to flag functions that require refactoring.
