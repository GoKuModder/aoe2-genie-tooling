---
description: SOP for Parallel Development (Antigravity + Jules)
---
# Parallel Development Strategy

To work efficiently with multiple agents:

1.  **Divide and Conquer**:
    *   **Antigravity (Me)**: Use for interactive debugging, complex logic requiring deep context, and immediate fixes.
    *   **Jules**: Use for large-scale implementation patterns, repetitive boilerplate, or self-contained modules.

2.  **Avoid Conflicts**:
    *   Do **NOT** edit the same file as Jules at the same time.
    *   Work on separate modules (e.g., I handle `Units/`, Jules handles `Techs/`).

3.  **Workflow**:
    *   Create a task for Jules: `run workflow delegate_to_jules`.
    *   While Jules works, asking me to work on a *different* part of the codebase.
