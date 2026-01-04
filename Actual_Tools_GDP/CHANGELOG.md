# Changelog

All notable changes to Actual_Tools are documented in this file.

## [1.3.0] - 2026-01-02

### Added
- **EffectManager** - Full CRUD for Effects:
  - `create()`, `clone()`, `get()`, `delete()` returning `EffectHandle`
  - `EffectHandle` with command management
  - `EffectCommandHandle` for individual effect commands
  - Factory method `workspace.effect_manager()`

- **TechHandle** - High-level wrapper for Technologies:
  - Attribute access (research_time, effect_id, icon_id, etc.)
  - TechManager now returns `TechHandle` from `create()`, `copy()`, `get()`
  - Added `copy()` and `delete()` methods

- **SoundHandle** - High-level wrapper for Sounds:
  - `SoundItemHandle` for individual sound items
  - Item management: `add_item()`, `get_item()`, `remove_item()`
  - SoundManager now returns `SoundHandle` from `create()`, `copy()`, `get()`
  - Added `copy()` and `delete()` methods

- **CivHandle** - High-level wrapper for Civilizations:
  - Attribute access (name, icon_set, tech_tree_id, etc.)
  - Unit access methods: `get_unit()`, `unit_exists()`
  - CivilizationsManager now returns `CivHandle` from `get()`

### Changed
- All managers now have consistent API: `create()`, `copy()`, `get()`, `delete()`
- All `get()` methods return Handle objects (use `get_raw()` for raw objects)
- All managers have `count_active()` method for non-None count

### Enhanced Registry
- **UUID tracking** for persistent object identity (survives ID changes)
- **Effect registration** via `register_effect()`
- **Dependency tracking** with `link_tech_to_effect()`, `link_unit_to_graphic()`, etc.
- Query methods: `get_dependencies_for()`, `get_dependents_of()`
- UUID lookup: `get_id_by_uuid()`, `update_id()`

### Enhanced Validation
- Tech → Effect reference checks in `validate()`
- Effect command target validation (unit references)
- Referential integrity warnings for deleted effects

## [1.2.0] - 2026-01-01

### Added
- **Colored console logging** - All managers now output colored status messages:
  - `[Workspace] Loading empires2_x2_p1.dat...`
  - `[UnitManager] ✓ Created 'Hero1' at ID 2900`
  - `[GraphicManager] ✓ Created 'hero.slp' at ID 17068`
- **JSON registry** for communication with AoE2ScenarioParser:
  - `workspace.save_registry("genie_edits.json")` exports created items
  - Format: `{"units": [{"name": "Hero1", "id": 2900}], ...}`
  - Use `registry.get_unit_id("Hero1")` to look up IDs
- **Elapsed time tracking** with `workspace.print_summary()`
- **Global logger** accessible via `from Actual_Tools import logger`
- **Global registry** accessible via `from Actual_Tools import registry`

### Control Options
- `logger.disable()` / `logger.enable()` - Toggle console output
- `registry.disable()` / `registry.enable()` - Toggle auto-registration
- `registry.clear()` - Clear registered items

## [1.1.0] - 2026-01-01

### Added
- **`__all__` exports** in all modules to hide internal functions from IDE autocomplete
- **Type hints** everywhere with proper `TYPE_CHECKING` guards
- **Comprehensive docstrings** (Google style) for all public classes and methods
- **Consistent manager API**: all managers now have `get()`, `exists()`, `count()` methods
- **CivilizationsManager.names()** and **CivilizationsManager.all()** helper methods
- **Round-trip test_main.py** that verifies changes persist after save/reload

### Changed
- **UnitHandle** now proxies ALL Unit attributes via `__getattr__`/`__setattr__`
- **UnitHandle** auto-filters invalid civ_ids (no more silent failures)
- **graphics.attack setter** now accepts both `Graphic` objects and `int` IDs
- **GraphicManager.add_graphic()** now has optional `graphic_id` parameter
- **SoundManager.add_sound()** now has optional `sound_id` parameter  
- **TechManager.add_tech()** now has optional `tech_id` parameter
- Renamed `get_civ()` to `get()` in CivilizationsManager for consistency
- Renamed `get_civ_by_name()` to `get_by_name()` in CivilizationsManager
- Renamed `get_all_civs()` to `all()` in CivilizationsManager
- Renamed `get_sound()` to `get()` in SoundManager
- Renamed `get_tech()` to `get()` in TechManager

### Fixed
- **Empty unit bug**: units created with invalid `enable_for_civs` now work correctly
- **Name not persisting**: UnitHandle property assignments now properly update all civs
- **Graphic assignment**: `handle.graphics.attack = graphic_obj` now works

### Documentation
- Updated README.md with comprehensive quickstart and API reference
- Added exception hierarchy documentation
- Added invariant documentation (gap rules, ID semantics)

## [1.0.0] - 2026-01-01

### Initial Release
- GenieWorkspace as root entry point
- UnitHandle with tab-style property access
- GenieUnitManager with create(), clone_into(), move()
- GraphicManager, SoundManager, TechManager, CivilizationsManager
- Centralized exceptions
- Placeholder-based "no gaps" policy for unit tables
