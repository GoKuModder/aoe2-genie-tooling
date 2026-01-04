# Agents Directory

This directory contains configuration files for the specialized agents working on the AOE2 Genie Tooling project.

## Active Agents

| Agent (Persona) | Role | Status | Active Session |
| :--- | :--- | :--- | :--- |
| **[Alice](roster/Alice.md)** | Documentation | Idle | None |
| **[Marcus](roster/Marcus.md)** | Core Backend | **Active** | `3748755310644147131` |
| **[Leonidas](roster/Leonidas.md)** | Gameplay/Units | **Wait** | `3408563265722343247` |
| **[Maya](roster/Maya.md)** | Assets/Design | Idle | None |
| **[Elena](roster/Elena.md)** | Data/History | **Active** | `783808832176151754` |
| **[Tess](roster/Tess.md)** | QA/Testing | **Active** | `6420709257444961590` |
| **[Sam](roster/Sam.md)** | Maintenance | Idle | None |
| **[Oscar](roster/Oscar.md)** | Cleanup | Idle | None |

## Usage

Each `.md` file represents an agent's context. When starting work:
1.  Identify the type of task.
2.  Open the corresponding agent file.
3.  Check "Active Tasks" and "Notes".
4.  Update the file with new tasks or session IDs as you work.

## Integration with Jules
- **Jules Sessions** define the unit of work.
- **Agent Files** track the ownership and history of those sessions.
- Use `jules remote list sessions` (or similar) to see active sessions and map them here.
