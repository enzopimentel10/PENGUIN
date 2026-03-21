# Bootstrap System Workflow (`bootstrap-system.sh`)

This script handles the initialization and cold-start of the PEN.GUIN ecosystem.

## Workflow Overview
When `bootstrap-system` is executed, the following operational sequence occurs:

1. **Environment Validation:** The script verifies that the host environment meets all necessary prerequisites (e.g., correct Node.js version, Python version, Docker availability, and necessary OS permissions).
2. **Directory Scaffolding:** It ensures the core structural directories (`/kernel`, `/agents`, `/workspace`, `/docs`, `/tools`, `/scripts`, `/core`, `/routing`, `/automation`, `/skills`) exist and are appropriately permissioned.
3. **Kernel Initialization:** The AI Kernel is instantiated. The script starts the `Context Engine` daemon and initializes an empty or localized instance of the `Memory Model` (e.g., spinning up a local vector store or SQLite DB).
4. **Registry Population:** The script scans the `/agents` and `/skills` directories, automatically triggering the `register-agent` and `register-skill` logic to populate the Kernel's internal routing tables.
5. **System Readiness:** Once all components are loaded and communication channels are verified, the script outputs a "System Ready" signal, putting the Workflow Engine into a listening state for incoming tasks.
