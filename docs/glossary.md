# Glossary

## Workspace
The **GenieWorkspace** is the root entry point. It loads the DAT file, initializes all managers, and coordinates saving. It is the owner of the data.

## Manager
A **Manager** (e.g., `UnitManager`, `EffectManager`) is responsible for the lifecycle of data objects. It handles:
*   **Creation**: allocating new IDs and memory.
*   **Deletion**: removing objects.
*   **Lookup**: finding objects by ID or name.
*   **Cloning**: creating deep copies of objects.

## Handle
A **Handle** (e.g., `UnitHandle`, `TechHandle`) is a temporary wrapper around a specific data object ID and the Workspace. It provides a convenient API to read and write data for that specific ID. Handles are lightweight and do not store data themselves; they proxy access to the backend.

## Wrapper
A **Wrapper** (e.g., `CombatWrapper`, `BuildingWrapper`) is a component attached to a Handle that groups related attributes. It maps to the "tabs" you might see in tools like AGE (Advanced Genie Editor). For example, `unit.combat` provides access to attack, armor, and range statistics.

## Builder
A **Builder** (e.g., `TaskBuilder`, `EffectCommandBuilder`) is a fluent interface helper. It is used to construct complex objects or append items to lists using a readable, method-chaining style.

## Registry
The **Registry** is a system that tracks created objects (Units, Effects, etc.) by assigning them unique UUIDs. This allows external tools or future scripts to reliably find objects even if their internal IDs change (e.g., due to reordering).

## Validator
The **Validator** runs consistency checks on the data, ensuring that references (like a unit referring to a non-existent graphic ID) are valid and that there are no logical errors in the dataset.
