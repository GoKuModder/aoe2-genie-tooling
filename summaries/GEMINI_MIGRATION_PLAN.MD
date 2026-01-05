# Migration Plan: `Actual_Tools_GDP` to `GenieDatParser`

This document outlines the three-phase plan to migrate the `Actual_Tools_GDP` library from the legacy `genieutils-py` backend to the high-performance `GenieDatParser` (Rust) backend.

## Phase 1: Solidify the Backend Foundation

The initial phase focuses on establishing a clean and robust interface with the new backend.

1.  **Enhance `dat_adapter.py`**:
    *   **Goal**: Make `Actual_Tools_GDP/Shared/dat_adapter.py` the single source of truth for all backend data structures.
    *   **Action**: Ensure it exports all necessary data classes from `GenieDatParser`'s `sections` module (e.g., `Unit`, `CombatInfo`, `Graphic`). We will create or update compatibility shims and wrappers as needed to smooth over major API differences identified in the `CODEX_ASSESSMENT.md`.

2.  **Global Import Switch**:
    *   **Goal**: Point all modules within `Actual_Tools_GDP` to the new backend adapter, removing all dependencies on the old `genieutils` library.
    *   **Action**: Perform a project-wide replacement of `from genieutils...` imports with `from Actual_Tools_GDP.Shared.dat_adapter...`. This will prepare the codebase for the targeted refactoring in the next phase.

## Phase 2: Domain-by-Domain Migration

To manage complexity, the migration will proceed manager by manager, from simplest to most complex.

1.  **Simple Managers (Graphics, Sounds, Techs, Effects)**:
    *   **Goal**: Update the handles and managers for Graphics, Sounds, Techs, and Effects to work with `GenieDatParser` objects.
    *   **Action**: Refactor each module (e.g., `graphic_handle.py`, `sound_manager.py`) to align with the new object structures and field names.

2.  **Complex Manager (`UnitManager` and `UnitHandle`)**:
    *   **Goal**: Overhaul `UnitHandle` to serve as a robust abstraction layer over `GenieDatParser`'s nested `Unit` structure.
    *   **Action**:
        *   **Refactor `UnitHandle`**: The core of the migration. We will rewrite its `__getattr__` and `__setattr__` methods to delegate calls to the correct sub-structure (e.g., a call to `unit.max_range` will be routed to the unit's `combat_info.max_range`).
        *   **Update Wrappers**: The helper classes in `Actual_Tools_GDP/Units/wrappers/` will be updated to interface with the new `*Info` structs (e.g., `Type50Wrapper` will now wrap `CombatInfo`).
        *   **Adapt `UnitManager`**: Update `create()` and `clone_into()` to correctly instantiate `GenieDatParser`'s `Unit` objects and their nested data structures.

## Phase 3: Testing and Validation

1.  **Adapt and Run Tests**:
    *   **Goal**: Ensure the migrated code is correct and maintains API compatibility.
    *   **Action**: The test suite in `Actual_Tools_GDP/tests/` will be updated to reflect the backend changes. All tests must pass using the new `GenieDatParser` backend.

2.  **Round-Trip Verification**:
    *   **Goal**: Confirm that a full load -> modify -> save -> reload cycle works without data corruption.
    *   **Action**: A final round-trip test script will be run to ensure data integrity from end to end.
