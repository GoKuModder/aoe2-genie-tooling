# Validation, Registry, and Safety

`Actual_Tools_GDP` includes robust systems to prevent data corruption and ensure the integrity of your modifications.

## Mental Model

1.  **Registry**: A tracking system that records every object you create (Units, Effects, Graphics, Sounds). It assigns a unique UUID to each creation, allowing you to trace your objects even if their internal IDs change.
2.  **Validator**: A quality assurance engine that runs checks on your data. It can spot issues like references to non-existent graphics, gaps in unit lists, or invalid tech effects.
3.  **Typed IDs**: A system of semantic types (e.g., `UnitId`, `GraphicId`) that helps IDEs and developers distinguish between different kinds of integers, preventing errors where you might accidentally pass a sound ID to a graphic function.

## Public API

### Registry (`Actual_Tools_GDP.Base.core.registry`)

The registry is accessed via `workspace.registry` or the global `registry` object.

*   `register_unit(name, id, uuid=None)`: Tracks a new unit.
*   `export_json(path)`: Saves the session's creation history to a JSON file.
*   `get_uuid(id, type_name)`: Retrieves the UUID for a given ID.

### Validator (`Actual_Tools_GDP.Base.core.validator`)

The validator is used internally by the workspace during `save()` operations, but can be invoked manually.

*   `validate_all_references(workspace, validate_existing=False)`: Scans the entire dataset for broken links.

### Exceptions (`Actual_Tools_GDP.Base.core.exceptions`)

*   `GenieToolsError`: Base class for all library exceptions.
*   `InvalidIdError`: Raised when accessing an ID that is out of range.
*   `UnitIdConflictError`: Raised when creating a unit at an occupied ID with `on_conflict="error"`.
*   `GapNotAllowedError`: Raised when an operation would create illegal `None` gaps in data lists.
*   `ValidationError`: Raised when data integrity checks fail.

## Workflows

### Handling Validation Errors

Validation errors often occur when you delete an asset that is still being used, or typos in IDs.

```python
from Actual_Tools_GDP import GenieWorkspace, ValidationError

workspace = GenieWorkspace.load("data.dat")

try:
    workspace.save("output.dat")
except ValidationError as e:
    print("Save failed due to validation errors:")
    print(e)
    # The error message will often suggest which ID or Unit is causing the problem.
```

### Using the Registry for External Tools

If you are building a mod pipeline where Python scripts generate data and another tool (like a Scenario Parser) places units on a map, the Registry JSON is the bridge.

```python
# In your generation script:
unit = workspace.unit_manager.create("My Custom Hero")
workspace.save_registry("mod_manifest.json")
```

The JSON file will contain entries mapping "My Custom Hero" -> ID 1500 -> UUID "a1b2...".

### Typed IDs

While the API accepts standard integers, using Typed IDs can make your code self-documenting and safer.

```python
from Actual_Tools_GDP.Base.core.typed_ids import UnitId, GraphicId

def assign_graphic(unit_id: UnitId, graphic_id: GraphicId):
    # ... implementation ...
    pass
```

## Gotchas & Invariants

*   **Validation Timing**: Most validation happens at **save time**, not assignment time. You can assign `unit.standing_graphic = 99999` (an invalid ID) without immediate error. The `save()` method will catch this if validation is enabled.
*   **Allow-Lists**: Wrapper classes (like `unit.combat`) often use allow-lists for attribute flattening. If you try to access a property that exists in the raw backend but isn't in the allow-list, you might get an `AttributeError` or `ValidationError`.
*   **Rich Errors**: `InvalidIdError` provides detailed context, often printing a snippet of your code and a list of valid items nearby to help you debug typos.

## Cross-Links

*   [Base Workspace](base_workspace.md)
*   [Datasets](datasets.md)
