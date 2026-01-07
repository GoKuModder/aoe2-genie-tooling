# Workspace API

The `GenieWorkspace` is the central entry point for using `Actual_Tools_GDP`. It orchestrates the loading, management, validation, and saving of Genie Engine data files.

## Mental Model

Think of the `GenieWorkspace` as the session manager for your editing work.
1.  **Loader**: It reads the binary `.dat` file into memory (via the high-performance Rust backend).
2.  **Hub**: It holds references to all the specialized managers (`UnitManager`, `TechManager`, etc.) and ensures they share the same underlying data.
3.  **Validator**: It tracks objects created during the session and validates references (e.g., ensuring a unit doesn't reference a non-existent graphic) before saving.

## Common Workflows

### Loading and Saving
```python
from Actual_Tools_GDP import GenieWorkspace

# Load a dat file
workspace = GenieWorkspace.load("empires2_x2_p1.dat")

# ... make changes ...

# Save to a new file
workspace.save("my_mod.dat")
```

### Accessing Managers
All managers are available as properties on the workspace instance.
```python
units = workspace.unit_manager
techs = workspace.tech_manager
civs  = workspace.civ_manager

# Example: Get a unit
archer = units.get(4)
```

### Changing Validation Level
You can adjust strictness during the session or at save time.
```python
from Actual_Tools_GDP.Base.config import ValidationLevel

# Upgrade to full validation (checks everything, including original game data)
workspace.upgrade_validation(ValidationLevel.VALIDATE_ALL)

# Or override just for saving
workspace.save("out.dat", validate=ValidationLevel.NO_VALIDATION)
```

## Gotchas & Invariants

*   **Single Source of Truth**: Do not instantiate managers manually. Always use the ones provided by `workspace.unit_manager`, etc. They are initialized with shared state (like the registry and logger) that you will lose if you create them yourself.
*   **Validation Costs**: `VALIDATE_ALL` can be slow because it checks every single reference in the DAT file (thousands of units/graphics). `VALIDATE_NEW` (default) is optimized to check only what you touch.
*   **Dependency Injection**: The workspace injects itself into every manager. This circular reference is intentional and allows a `UnitHandle` to look up `Graphics` or `Sounds` via `self.workspace.graphic_manager`.

## API Reference

### GenieWorkspace

`from Actual_Tools_GDP import GenieWorkspace`

#### `load(path: PathLike, validation: ValidationLevel = ValidationLevel.VALIDATE_NEW) -> GenieWorkspace`
Loads a `.dat` file from disk.

- **path**: Path to the `.dat` file.
- **validation**: Validation mode.
  - `VALIDATE_NEW` (default): Only validates objects created in this session.
  - `VALIDATE_ALL`: Validates all references in the file (slower).
  - `NO_VALIDATION`: Skips validation.

#### `save(target_path: PathLike, validate: Union[ValidationLevel, bool] = None) -> None`
Saves the workspace to a `.dat` file.

- **target_path**: Output path.
- **validate**: Override the validation level for this save operation.

#### `save_registry(path: PathLike) -> None`
Exports the session registry (list of created items and their UUIDs) to a JSON file. This is useful for integration with `AoE2ScenarioParser`.

#### `validate(raise_on_error: bool = False) -> List[str]`
Runs integrity checks and returns a list of issues.
- Checks for gaps in unit arrays.
- Verifies integrity of cross-referenced IDs (Effects -> Techs, Units -> Graphics).

### Properties

- `unit_manager`: Access the `UnitManager`.
- `tech_manager`: Access the `TechManager`.
- `effect_manager`: Access the `EffectManager`.
- `graphic_manager`: Access the `GraphicManager`.
- `sound_manager`: Access the `SoundManager`.
- `civ_manager`: Access the `CivManager`.
