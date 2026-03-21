# Task Classifier

The Task Classifier is the initial entry point for all directives within the PEN.GUIN routing system. Its primary role is to interpret high-level objectives and break them down into specialized, actionable sub-tasks that can be routed to individual agents.

## How Tasks Are Classified

When an objective is received, the Task Classifier employs the following decision logic to categorize the work:

1. **Intent Extraction:** The classifier analyzes the prompt to determine the core intent (e.g., *Feature Implementation*, *Bug Fix*, *Refactoring*, *Security Audit*, *Documentation Update*).
2. **Domain Mapping:** Based on the intent, the classifier maps the request to specific software domains:
   - **Client-Side:** Mentions of UI, styles, DOM manipulation, or browser behavior.
   - **Server-Side:** Mentions of databases, API routes, authentication, or server logic.
   - **Infrastructure:** Mentions of deployment, CI/CD, or architectural changes.
3. **Dependency Analysis:** The classifier identifies implicit dependencies within the request. For example, a request to "Add user login" implies both frontend (login form) and backend (authentication endpoint) domains.
4. **Sub-Task Generation:** The objective is decomposed into an ordered list of atomic sub-tasks. Each sub-task is tagged with its domain, required context, and expected output format.

## Workflow Orchestration
By tagging tasks accurately, the Task Classifier ensures that broad, ambiguous requests are translated into a structured workflow pipeline, preventing agents from operating outside their domain of expertise and setting the stage for the Agent Router.
