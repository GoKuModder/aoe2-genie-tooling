# Project Context for Gemini CLI

## Project Overview
This is the AOE2 Genie Tooling project - a Python toolkit for editing Age of Empires II .dat files. It currently serves as a high-level wrapper that can interface with multiple backends (`genieutils-py` and `GenieDatParser`).

## External Libraries
- **genieutils-py** (Legacy Backend): [https://github.com/SiegeEngineers/genieutils-py](https://github.com/SiegeEngineers/genieutils-py)
- **GenieDatParser** (New Backend): [https://github.com/Divy1211/GenieDatParser](https://github.com/Divy1211/GenieDatParser)

**Key Capabilities:**
- **Object-Oriented API**: Provides properly typed wrappers for Units, Graphics, Sounds, etc.
- **Multi-backend Support**: Can switch between `GenieDatParser` (Rust-backed, high performance) and `genieutils-py` (pure Python, legacy).
- **Attribute Flattening**: Simplifies access to deeply nested properties.
- **Data Safety**: Uses Enums and typed constants to prevent errors.

## Project Structure
- **Actual_Tools/** - Main Python API and user-facing tools. Contains the core logic, managers, and backend adapters.
- **Actual_Tools_GDP/** - Directory dedicated to the migration effort towards `GenieDatParser`.
- **Datasets/** - Contains Python modules defining constants, enums, and data derived from the game (e.g., `resources.py`, `tasks.py`).
- **docs/** - Project documentation source files (likely for MkDocs).

## Jules Session Registry
| Alias | Session ID | Purpose | Status |
| :--- | :--- | :--- | :--- |
| `agents-doc` | 3484528132322107041 | Create AGENTS.md in Actual_Tools | Active |

## Architecture Overview
**Backend Integration:**
The project uses a backend abstraction layer located in `Actual_Tools/backend.py`. It attempts to import `GenieDatParser` (Option 1, high performance via Rust) and falls back to `genieutils-py` (Option 2, legacy pure Python).
- **GenieDatParser**: A high-performance backend (Python frontend with Rust internals).
- **genieutils-py**: The legacy pure Python backend (slower link, kept for API stability).

**Data Flow:**
1.  **Loading**: `GenieWorkspace.load("file.dat")` uses the selected backend to parse the binary file into memory.
2.  **Manipulation**: User scripts uses Managers (e.g., `GenieUnitManager`) to access and modify data. These managers wrap the raw backend objects into user-friendly Python objects (`UnitWrapper`).
3.  **Saving**: `workspace.save("out.dat")` serializes the modified data structures back to binary format.

**Key Classes:**
- `GenieWorkspace`: The central entry point for loading files and accessing managers.
- `GenieUnitManager`, `GraphicManager`, `SoundManager`: specialized managers for different data types.
- `DatFileWrapper`, `UnitWrapper` (in `backend.py`): Shim classes that normalize the API differences between backends.

## Orchestration Instructions
- When I refer to a session by its **Alias**, look up the **Session ID** in the Registry above
- You are authorized to run `jules remote status --session <ID>` and check session progress
- Before approving any Jules changes, verify they align with project structure above
- All documentation should be in Markdown format

## Coding Standards
**Python Style:**
- **PEP 8**: Followed generally.
- **Type Hinting**: Extensively used, especially in newer files like `backend.py` and `Actual_Tools` modules. `typing.Protocol` is used for structural typing.
- **Imports**: Absolute imports preferred (e.g., `from Actual_Tools import ...`).

**Testing:**
- **Framework**: `pytest`.
- **Location**: `Actual_Tools/tests`.
- **Coverage**: `pyproject.toml` has coverage configuration, omitting tests and caches.

**Documentation:**
- **Format**: Markdown (`.md`).
- **Docstrings**: Present in classes and methods, explaining arguments and behaviors.

## Development Workflow
**Environment Setup:**
1.  Install Python 3.11+.
2.  Install dependencies: `pip install -e .[dev]` (installs `genieutils-py`, `pytest`, `ruff`).

**Running Tests:**
- Run `pytest` from the root or `Actual_Tools` directory.
- `pytest.ini_options` in `pyproject.toml` points to `Actual_Tools/tests`.

**Build Process:**
- Uses `hatchling` as the build backend.
- `pip build` or similar tools can generate wheels.

## Git Configuration
- This project uses the modding account: **GoKuModder**
- Repository: **GoKuModder/aoe2-genie-tooling**
- **Never expose real identity in commits**

**Ignored Files (.gitignore):**
- Virtual environments (`.venv/`, `env/`)
- IDE settings (`.idea/`, `.vscode/`)
- Compiled Python files (`__pycache__/`, `*.pyc`)
- Rust build artifacts (`Genie-Rust/target/`)
- Game Data Files: `*.dat` (except specific test files if whitelisted)
- Text notes: `*.txt`
- Secrets (`.env`, `*.pem`, `*.key`)

## Important Files
- **pyproject.toml**: Main project configuration, define dependencies, build system, and tool configs (Ruff, Pytest).
- **Actual_Tools/backend.py**: The abstraction bridging the Python tools to the underlying parser (GenieDatParser or genieutils-py).
- **MIGRATION_PLAN_GenieDatParser.md**: Detailed roadmap for switching the default backend to `GenieDatParser`.
- **README.md**: User-facing documentation and quick start guide.

## Known Issues & TODOs
- **Migration in Progress**: The project is actively migrating from `genieutils-py` to `GenieDatParser`. `backend.py` currently handles both but `Actual_Tools_GDP` suggests ongoing work.
- **Rust Backend Discrepancy**: Documentation mentions a Rust backend (`Genie-Rust`), but the directory is not present in the root (though ignored in `.gitignore`). The current code primarily relies on Python implementations.
- **TODOs**: (None found in `Actual_Tools` scan, but check code comments in `Actual_Tools_GDP` for migration specifics).



## Gemini CLI Commands Reference

### Session Management
- **List all sessions**: `jules remote list --session`
- **Start new session**: `jules remote new "<task>" --repo <owner/repo>`
  - *Example*: `jules remote new "Fix bugs" --repo GoKuModder/aoe2-genie-tooling`
- **Pull session results**: `jules remote pull --session <session_id> --apply`
- **Check session details**: `jules remote list --session | findstr "<session_id>"`

### Working with Session Registry
When I reference a session by alias (e.g., "check agents-doc status"):
1. Look up the Session ID in the Jules Session Registry table above
2. Execute: `/jules status <session_id>`
3. Report the findings

### File Operations
- **Read project files**: Automatically available in context
- **Create/modify files**: Request through `/jules` commands with explicit file paths
- **Never use git patches**: Always request direct file creation/modification

### MCP and Tools
- **Available MCP servers**: (list any MCP servers you have configured)
- **Web search**: Available for looking up documentation or APIs
- **File system access**: Full access to project directory

## Gemini Behavior Instructions

### When I ask you to work with Jules sessions:
1. **Always check the Session Registry first** for the correct ID
2. **Verify the session status** before taking action
3. **Report back** what you find before suggesting next steps
4. **Never invent session IDs** - only use IDs from the registry or from `/jules status` output

### When creating documentation:
1. Use **Markdown format** exclusively
2. Structure with clear headers and sections
3. Include code examples where relevant
4. Keep explanations concise but complete

### When analyzing code:
1. **Respect the backend abstraction** - understand which backend is being used
2. **Check type hints** for expected interfaces
3. **Look for tests** to understand intended behavior
4. **Note TODOs and FIXMEs** in your analysis

### Privacy Protection:
- **NEVER** suggest commits with real name/email
- **ALWAYS** verify git config shows "GoKuModder" identity
- **WARN** if any operation might expose real identity

## Common Workflows

### Creating a new Jules task:
```
/jules "create AGENTS.md in [directory] explaining purpose and key files"
```
Then add the session to the registry above with a meaningful alias.

### Checking multiple sessions:
```
> /jules status
```
Review all active sessions and update the Status column in the registry.

### Before approving Jules changes:
1. Review the proposed changes in Jules console
2. Verify changes align with project structure
3. Check that no sensitive info is exposed
4. Approve via console or `/jules approve <id>`

## Emergency Commands
- **Stop Gemini CLI**: `Ctrl+C` or type `exit`
- **Cancel Jules session**: Visit Jules console and manually cancel
- **Reset context**: Exit and restart `gemini` command