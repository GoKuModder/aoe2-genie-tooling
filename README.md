# Actual_Tools_GDP

High-level Python toolkit for editing Age of Empires II Definitive Edition DAT files.

This library provides a safe, object-oriented API for modifying the binary data of AoE2. It handles the complexity of the Genie Engine (pointer arithmetic, shared lists, multi-civilization data) so you can focus on modding logic.

## Key Features

*   **Safe ID Management**: Automatically finds free IDs, tracks creation, and prevents conflicts.
*   **Multi-Civ Propagation**: Changes to a unit (stats, graphics) are automatically applied to all civilizations.
*   **Deep Cloning**: Creating a unit makes a true copy. Modifying the clone's attack list never breaks the original unit.
*   **Fluent Builders**: Add tasks and effects using readable methods (`.add_task.combat()`) instead of magic numbers.
*   **Attribute Flattening**: Access deeply nested properties directly (`unit.hit_points`) instead of traversing internal structures.

## Installation

```shell
pip install Actual_Tools_GDP
```

(Note: Requires a local installation of `GenieDatParser` backend if not packaged together).

## Quick Start

```python
from Actual_Tools_GDP import GenieWorkspace
from Actual_Tools_GDP.Datasets import UnitClass, Resource

# 1. Load the DAT file
workspace = GenieWorkspace.load("empires2_x2_p1.dat")

# 2. Access Managers
um = workspace.unit_manager
gm = workspace.graphic_manager
em = workspace.effect_manager

# 3. Create a custom unit (cloned from Archer)
hero = um.create("Super Archer", base_unit_id=4)
hero.hit_points = 100
hero.speed = 1.2

# 4. Create an effect (Blacksmith Upgrade style)
effect = em.add_new("Super Arrows")
effect.add_command.attribute_modifier_add(
    a=UnitClass.ARCHER,
    b=Attribute.ATTACK,
    d=2.0
)

# 5. Save
workspace.save("empires2_x2_p1_modded.dat")
```

## Documentation

Full documentation is available in the `docs/` directory.

*   [Overview](docs/overview.md): Architecture and key concepts.
*   [API Reference](docs/api/index.md): Detailed class and method documentation.
    *   [Units](docs/api/units_manager.md)
    *   [Effects](docs/api/effects_manager.md)
    *   [Graphics](docs/api/graphics.md)
    *   [Techs](docs/api/techs.md)
*   [Examples](docs/examples/): Runnable Python scripts.

## Migration Guide

If you are upgrading from older versions or `genieutils`:

1.  **Imports**: Change `from Actual_Tools import ...` to `from Actual_Tools_GDP import ...`.
2.  **Datasets**: Import Enums from `Actual_Tools_GDP.Datasets` instead of `Datasets` root package.
3.  **Task Creation**: Use `unit.add_task.combat(...)` instead of `unit.tasks.add_task(...)` for better type safety (though both work).
4.  **Wrappers**: Access component data via `unit.combat`, `unit.building`, etc., instead of `unit.type50` or `unit.type80`.

## Architecture

*   **Workspace**: The root object. Owns the data.
*   **Managers**: Controllers for creating/finding objects (UnitManager, TechManager).
*   **Handles**: Wrappers for individual objects (UnitHandle).
*   **Registry**: Tracks created UUIDs for cross-tool compatibility.

## License

LGPL-3.0
