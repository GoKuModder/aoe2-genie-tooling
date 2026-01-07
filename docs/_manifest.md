# Manifest for Actual_Tools_GDP documentation

## Public API Inventory

### Core (Base)
- **File:** `Actual_Tools_GDP/Base/workspace.py`
  - `GenieWorkspace`: Main entry point. Loads/saves .dat files.
    - `load(path, validation)`
    - `save(path, validate)`
    - `save_registry(path)`
    - `upgrade_validation(level)`
    - `validate(raise_on_error)`
    - Properties: `unit_manager`, `tech_manager`, `effect_manager`, `graphic_manager`, `sound_manager`, `civ_manager`, `terrain_manager` (TODO: check if fully implemented)
- **File:** `Actual_Tools_GDP/Base/config.py`
  - `ValidationLevel` (Enum): `NO_VALIDATION`, `VALIDATE_NEW`, `VALIDATE_ALL`
  - `Config` (Internal mostly, but exposes defaults)

### Managers & Handles

#### Units
- **Manager:** `Actual_Tools_GDP/Units/unit_manager.py` -> `UnitManager`
  - `get(id)` -> `UnitHandle`
  - `create(name, base_unit_id, ...)` -> `UnitHandle`
  - `clone_into(dest_unit_id, base_unit_id, ...)` -> `UnitHandle`
  - `move(src_unit_id, dst_unit_id, ...)` -> `None`
- **Handle:** `Actual_Tools_GDP/Units/unit_handle.py` -> `UnitHandle`
  - Wraps `genie_rust.Unit` (or `genieutils.Unit`)
  - Attributes: `name`, `hit_points`, `line_of_sight`, etc.
  - `add_task(...)` -> `TaskBuilder` (fluent API)
- **Builder:** `Actual_Tools_GDP/Units/task_builder.py` -> `TaskBuilder`

#### Techs
- **Manager:** `Actual_Tools_GDP/Techs/tech_manager.py` -> `TechManager`
  - `get(id)` -> `TechHandle`
  - `add(name, ...)` -> `TechHandle`
- **Handle:** `Actual_Tools_GDP/Techs/tech_handle.py` -> `TechHandle`

#### Effects
- **Manager:** `Actual_Tools_GDP/Effects/effect_manager.py` -> `EffectManager`
  - `get(id)` -> `EffectHandle`
  - `add(name)` -> `EffectHandle`
- **Handle:** `Actual_Tools_GDP/Effects/effect_handle.py` -> `EffectHandle`
  - `add_command` -> `EffectCommandBuilder`
- **Builder:** `Actual_Tools_GDP/Effects/effect_command_builder.py` -> `EffectCommandBuilder`
  - Fluent methods: `attribute_modifier`, `modify_tech`, etc.

#### Graphics
- **Manager:** `Actual_Tools_GDP/Graphics/graphic_manager.py` -> `GraphicManager`
  - `get(id)` -> `GraphicHandle`
  - `add_copy(source_id, name)` -> `GraphicHandle`
- **Handle:** `Actual_Tools_GDP/Graphics/graphic_handle.py` -> `GraphicHandle`
  - `add_delta(...)`

#### Sounds
- **Manager:** `Actual_Tools_GDP/Sounds/sound_manager.py` -> `SoundManager`
  - `get(id)` -> `SoundHandle`
  - `add_copy(source_id, name)` -> `SoundHandle`
- **Handle:** `Actual_Tools_GDP/Sounds/sound_handle.py` -> `SoundHandle`

#### Civilizations
- **Manager:** `Actual_Tools_GDP/Civilizations/civ_manager.py` -> `CivManager`
  - `get(id)` -> `CivHandle`
- **Handle:** `Actual_Tools_GDP/Civilizations/civ_handle.py` -> `CivHandle`

### Utilities
- **File:** `Actual_Tools_GDP/Base/core/logger.py` -> `logger`
- **File:** `Actual_Tools_GDP/Base/core/registry.py` -> `registry`
  - `export_json(path)`

### Datasets (Enums)
- **Module:** `Actual_Tools_GDP/Datasets/__init__.py`
  - Exports: `Attribute`, `UnitClass`, `UnitType`, `Resource`, `Effect`, `TechModifier`, `Task`, etc.

## Documentation Plan

1.  **Overview (`docs/overview.md`)**
    - High-level architecture: Workspace -> Managers -> Handles
    - Data flow: Local edits -> Save -> Output DAT
    - Concept of "Registry" and tracking new items.

2.  **API Reference (`docs/api/`)**
    - `workspace.md`: `GenieWorkspace`, `ValidationLevel`
    - `units.md`: `UnitManager`, `UnitHandle`, `TaskBuilder`
    - `techs.md`: `TechManager`, `TechHandle`
    - `effects.md`: `EffectManager`, `EffectHandle`, `EffectCommandBuilder`
    - `graphics.md`: `GraphicManager`, `GraphicHandle`
    - `sounds.md`: `SoundManager`, `SoundHandle`
    - `civs.md`: `CivManager`, `CivHandle`
    - `datasets.md`: Validation, constants, enums (if any exposed)

3.  **Examples (`docs/examples/`)**
    - `load_and_save.py`
    - `create_unit.py`
    - `modify_effect.py`

## TODOs & Uncertainties
- [ ] Check if `TerrainManager` is actually implemented and exposed. `GenieWorkspace` has a commented-out line `self._terrain_manager = TerrainManager(self)` but also a property `terrain_manager`. Need to verify if `TerrainManager` class exists and is usable.
- [ ] Verify `registry` usage. Is it just for internal tracking or useful for end-users? `save_registry` suggests it's for external tools (ASP).
- [ ] Check exact signature of `UnitManager.create` vs `copy`.
