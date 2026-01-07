# Base Workspace & File I/O

The `GenieWorkspace` is the heart of `Actual_Tools_GDP`. It serves as the root entry point for loading, editing, and saving Age of Empires II Definitive Edition DAT files.

## Mental Model

Think of the `GenieWorkspace` as the "God Object" or "Session" for your editing task.

*   **Ownership**: It owns the raw `DatFile` data structure loaded from disk.
*   **Central Hub**: It initializes and holds references to all Managers (`UnitManager`, `TechManager`, etc.). You don't create managers manually; you access them through the workspace.
*   **Safety System**: It manages the `Validator`, `Registry`, and `Logger` to ensure your edits are safe and traceable.

Instead of passing raw lists of units or civs around, you pass the `GenieWorkspace` object. This ensures that every part of your code has access to the full context of the game data.

## Public API

### GenieWorkspace

The main class located in `Actual_Tools_GDP.Base.workspace`.

```python
class GenieWorkspace:
    @classmethod
    def load(cls, path: str | Path, validation: ValidationLevel = ValidationLevel.VALIDATE_NEW) -> GenieWorkspace:
        """Loads a DAT file and initializes the workspace."""

    def save(self, target_path: str | Path, validate: ValidationLevel | bool = None) -> None:
        """Saves the current state to a new DAT file."""

    def save_registry(self, path: str | Path) -> None:
        """Exports a JSON log of all items created in this session."""

    @property
    def unit_manager(self) -> UnitManager: ...
    @property
    def tech_manager(self) -> TechManager: ...
    @property
    def effect_manager(self) -> EffectManager: ...
    @property
    def graphic_manager(self) -> GraphicManager: ...
    @property
    def sound_manager(self) -> SoundManager: ...
    @property
    def civ_manager(self) -> CivManager: ...
```

### ValidationLevel

Enum controlling how much validation is performed during load/save operations.

*   `NO_VALIDATION`: Fastest. Skips all checks. Use only if you know what you are doing.
*   `VALIDATE_NEW`: Default. Checks integrity of objects created or modified in the current session.
*   `VALIDATE_ALL`: Slowest. Checks the entire DAT file for consistency (e.g., verifying every unit refers to valid graphics).

## Workflows

### Loading a Workspace

```python
from Actual_Tools_GDP import GenieWorkspace

# Load the file
workspace = GenieWorkspace.load("empires2_x2_p1.dat")

# Access a manager
unit_manager = workspace.unit_manager
print(f"Loaded {unit_manager.count()} units.")
```

### Saving with Validation

```python
from Actual_Tools_GDP import GenieWorkspace, ValidationLevel

workspace = GenieWorkspace.load("input.dat")

# ... perform edits ...

# Save with default validation (VALIDATE_NEW)
workspace.save("output.dat")

# Save with full validation (checks everything)
workspace.save("output_verified.dat", validate=ValidationLevel.VALIDATE_ALL)
```

### Exporting Registry

The registry is useful for external tools (like scenario parsers) to know what IDs were assigned to your new units.

```python
workspace.save_registry("mod_registry.json")
```

## Gotchas & Invariants

*   **File Existence**: The `load()` method requires the path to exist. It does not create a new empty DAT file from scratch; it always edits an existing one.
*   **Validation Errors**: `save()` will raise a `ValidationError` if consistency checks fail (e.g., you assigned a graphic ID that doesn't exist).
*   **Single Instance**: Typically, you should only have one `GenieWorkspace` active at a time for a given DAT file to avoid confusion, though the library does not strictly enforce singleton behavior.
*   **Memory Usage**: Loading a full DE DAT file consumes significant memory (hundreds of MBs) as it parses the entire binary structure into Python objects.

## Cross-Links

*   [Overview](../overview.md)
*   [Units Manager](units_manager.md)
*   [Effects Manager](effects_manager.md)
