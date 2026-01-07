# Documentation Manifest & API Inventory

This document serves as the single source of truth for the `Actual_Tools_GDP` public API and its mapping to documentation pages.

## Public API Inventory

### Core (`Actual_Tools_GDP`)
| Symbol | Type | Source Module | Doc Page | Notes |
| :--- | :--- | :--- | :--- | :--- |
| `GenieWorkspace` | Class | `Base/workspace.py` | `api/base_workspace.md` | Entry point |
| `logger` | Object | `Base/core/logger.py` | `api/base_workspace.md` | |
| `registry` | Object | `Base/core/registry.py` | `api/base_workspace.md` | |

### Units (`Actual_Tools_GDP.Units`)
| Symbol | Type | Source Module | Doc Page | Notes |
| :--- | :--- | :--- | :--- | :--- |
| `UnitManager` | Class | `Units/unit_manager.py` | `api/units_manager.md` | |
| `UnitHandle` | Class | `Units/unit_handle.py` | `api/units_handle.md` | |
| `TaskBuilder` | Class | `Units/task_builder.py` | `api/units_collections.md` | |
| `TaskHandle` | Class | `Units/handles.py` | `api/units_collections.md` | |
| `AttackHandle` | Class | `Units/handles.py` | `api/units_collections.md` | |
| `ArmourHandle` | Class | `Units/handles.py` | `api/units_collections.md` | |
| `DamageGraphicHandle` | Class | `Units/handles.py` | `api/units_collections.md` | |
| `TrainLocationHandle` | Class | `Units/handles.py` | `api/units_collections.md` | |
| `DropSiteHandle` | Class | `Units/handles.py` | `api/units_collections.md` | |
| `CombatWrapper` | Class | `Units/wrappers/combat.py` | `api/units_handle.md` | Alias: `Type50Wrapper` |
| `CreationWrapper` | Class | `Units/wrappers/creation.py` | `api/units_handle.md` | Alias: `CreatableWrapper` |
| `MovementWrapper` | Class | `Units/wrappers/movement.py` | `api/units_handle.md` | Alias: `DeadFishWrapper` |
| `BehaviorWrapper` | Class | `Units/wrappers/behavior.py` | `api/units_handle.md` | Alias: `BirdWrapper` |
| `ProjectileWrapper` | Class | `Units/wrappers/projectile.py` | `api/units_handle.md` | |
| `BuildingWrapper` | Class | `Units/wrappers/building.py` | `api/units_handle.md` | |

### Effects (`Actual_Tools_GDP.Effects`)
| Symbol | Type | Source Module | Doc Page | Notes |
| :--- | :--- | :--- | :--- | :--- |
| `EffectManager` | Class | `Effects/effect_manager.py` | `api/effects_manager.md` | |
| `EffectHandle` | Class | `Effects/effect_handle.py` | `api/effects_handle.md` | |
| `CommandHandle` | Class | `Effects/command_handle.py` | `api/effects_handle.md` | |
| `EffectCommandBuilder` | Class | `Effects/effect_command_builder.py` | `api/effects_builder.md` | |

### Techs (`Actual_Tools_GDP.Techs`)
| Symbol | Type | Source Module | Doc Page | Notes |
| :--- | :--- | :--- | :--- | :--- |
| `TechManager` | Class | `Techs/tech_manager.py` | `api/techs.md` | |
| `TechHandle` | Class | `Techs/tech_handle.py` | `api/techs.md` | |

### Graphics (`Actual_Tools_GDP.Graphics`)
| Symbol | Type | Source Module | Doc Page | Notes |
| :--- | :--- | :--- | :--- | :--- |
| `GraphicManager` | Class | `Graphics/graphic_manager.py` | `api/graphics.md` | |
| `GraphicHandle` | Class | `Graphics/graphic_handle.py` | `api/graphics.md` | |

### Sounds (`Actual_Tools_GDP.Sounds`)
| Symbol | Type | Source Module | Doc Page | Notes |
| :--- | :--- | :--- | :--- | :--- |
| `SoundManager` | Class | `Sounds/sound_manager.py` | `api/sounds.md` | |
| `SoundHandle` | Class | `Sounds/sound_handle.py` | `api/sounds.md` | |

### Civilizations (`Actual_Tools_GDP.Civilizations`)
| Symbol | Type | Source Module | Doc Page | Notes |
| :--- | :--- | :--- | :--- | :--- |
| `CivManager` | Class | `Civilizations/civ_manager.py` | `api/civs.md` | |
| `CivHandle` | Class | `Civilizations/civ_handle.py` | `api/civs.md` | |
| `ResourceAccessor` | Class | `Civilizations/resource_accessor.py` | `api/civs.md` | |

### Datasets (`Actual_Tools_GDP.Datasets`)
| Symbol | Type | Source Module | Doc Page | Notes |
| :--- | :--- | :--- | :--- | :--- |
| `Attribute` | Enum | `Datasets/attributes.py` | `api/datasets.md` | |
| `Effect` | Enum | `Datasets/commands.py` | `api/datasets.md` | |
| `Resource` | Enum | `Datasets/resources.py` | `api/datasets.md` | |
| `Task` | Enum | `Datasets/tasks.py` | `api/datasets.md` | |
| `UnitClass` | Enum | `Datasets/unit_classes.py` | `api/datasets.md` | |
| `UnitType` | Enum | `Datasets/unit_types.py` | `api/datasets.md` | |
| `...` | Enums | `Datasets/...` | `api/datasets.md` | See full list in module |

### Exceptions (`Actual_Tools_GDP.Base.core.exceptions`)
| Symbol | Type | Source Module | Doc Page | Notes |
| :--- | :--- | :--- | :--- | :--- |
| `GenieToolsError` | Exception | `Base/core/exceptions.py` | `api/base_workspace.md` | |
| `GapNotAllowedError` | Exception | `Base/core/exceptions.py` | `api/base_workspace.md` | |
| `InvalidIdError` | Exception | `Base/core/exceptions.py` | `api/base_workspace.md` | |
| `TemplateNotFoundError` | Exception | `Base/core/exceptions.py` | `api/base_workspace.md` | |
| `UnitIdConflictError` | Exception | `Base/core/exceptions.py` | `api/base_workspace.md` | |
| `ValidationError` | Exception | `Base/core/exceptions.py` | `api/base_workspace.md` | |

## Documentation Plan

1.  **Overview (`docs/overview.md`)**: High-level architecture, "Revolutionary Features", and migration guide.
2.  **Glossary (`docs/glossary.md`)**: Definitions of Manager, Handle, Wrapper, Builder, etc.
3.  **API Reference (`docs/api/*.md`)**: Detailed documentation for each subsystem.
4.  **Examples (`docs/examples/*.py`)**: Runnable scripts.
