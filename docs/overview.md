# Actual_Tools_GDP Overview

The `Actual_Tools_GDP` library provides a high-level, production-quality interface for editing Age of Empires 2 Genie Engine data files (`.dat`). It acts as a wrapper around the high-performance Rust-based `GenieDatParser`.

## Architecture

The library follows a strict top-down architecture:

```mermaid
graph TD
    WS[GenieWorkspace] --> UM[UnitManager]
    WS --> TM[TechManager]
    WS --> EM[EffectManager]
    WS --> GM[GraphicManager]
    WS --> SM[SoundManager]
    WS --> CM[CivManager]

    UM --> UH[UnitHandle]
    TM --> TH[TechHandle]
    EM --> EH[EffectHandle]
    GM --> GH[GraphicHandle]
    SM --> SH[SoundHandle]
    CM --> CH[CivHandle]

    WS --> DAT[DatFile (Rust Backend)]
```

### 1. GenieWorkspace
The `GenieWorkspace` is the root object. It holds the `DatFile` data structure, manages file I/O, and instantiates all specific managers. It is the single source of truth for the editing session.

### 2. Managers
Each subsystem (Units, Techs, Effects, etc.) has a dedicated Manager. Managers are responsible for:
- Creating new objects (handling ID allocation).
- Cloning existing objects.
- Retrieving handles to objects.
- Maintaining integrity (e.g., ensuring unit lists match across all civilizations).

### 3. Handles
Handles are lightweight wrappers around the raw data objects. They provide:
- **Attribute Flattening**: Access nested properties directly (e.g., `unit.hit_points` instead of `unit.type_50.hit_points`).
- **Multi-Civ Propagation**: When you modify a unit attribute via a `UnitHandle`, the change is automatically applied to that unit across all enabled civilizations.
- **Fluent APIs**: Helper builders for complex structures like Tasks and Effect Commands.

### 4. Registry
The `Registry` tracks every item created during a session. It assigns UUIDs to created objects, allowing for persistent identification even if IDs change (e.g., due to reordering). This is particularly useful when integrating with external tools like `AoE2ScenarioParser`.

## Data Model

- **Data Source**: The library wraps `GenieDatParser` structures.
- **IDs**: Objects are referenced by their integer index (ID).
- **Civilizations**: Units are stored per-civilization. `Actual_Tools_GDP` abstracts this by treating units as a single logical entity that exists across multiple civs.
- **Validation**: The library supports different validation levels (`NO_VALIDATION`, `VALIDATE_NEW`, `VALIDATE_ALL`) to ensure data integrity, checking for invalid references (e.g., a unit referencing a non-existent graphic).

## Key Concepts

### Attribute Flattening
The underlying data structure for a Unit is complex and nested. `Actual_Tools_GDP` flattens this.
*   **Raw**: `unit.type_50.hit_points`
*   **Handle**: `unit.hit_points`

### Multi-Civ Propagation
In the `.dat` file, every civilization has its own copy of every unit.
*   **Raw**: You must loop through `dat.civilizations` and update `civ.units[id].hit_points`.
*   **Handle**: `unit_handle.hit_points = 100` updates all relevant civs automatically.
