# Actual_Tools_GDP

**Production-quality tools layer for editing Age of Empires 2 DAT files.**

This library provides a high-level, Pythonic interface for editing Genie Engine data files (`.dat`). It acts as a robust wrapper around the high-performance `GenieDatParser` (Rust backend), offering intuitive "Managers", "Handles", and validation systems.

## Target Users
*   **Modders**: Who want to script complex data changes (new units, balance patches) without manual hex editing.
*   **Tool Developers**: Who need a stable API to build GUIs or other tools on top of.

## Installation

This package requires the `GenieDatParser` backend to be present.

```bash
# Clone the repo and its submodules (important for backend)
git clone --recursive <repository-url>
cd Actual_Tools_GDP

# Install dependencies
pip install .
```

## Quickstart

Minimal example to load a DAT file, change a unit's HP, and save.

```python
from Actual_Tools_GDP import GenieWorkspace

# 1. Load the DAT file
# ValidationLevel.VALIDATE_NEW is default (checks only your changes)
workspace = GenieWorkspace.load("empires2_x2_p1.dat")

# 2. Access the Unit Manager
# All data is accessed via managers on the workspace object
units = workspace.unit_manager

# 3. Edit a Unit
# Get ID 4 (Archer), change HP across ALL civilizations automatically
archer = units.get(4)
archer.hit_points = 45
print(f"Updated Archer HP to {archer.hit_points}")

# 4. Save
workspace.save("my_mod.dat")
```

## Common Workflows

### 1. Creating a New Unit
Use `create()` when you want a new unit and don't care about the specific ID. It clones a template (base unit) and finds the next available slot.

```python
# Create "Super Archer" based on ID 4
new_unit = workspace.unit_manager.create("Super Archer", base_unit_id=4)
new_unit.hit_points = 100
print(f"Created unit at ID {new_unit.id}")
```

### 2. Adding Effects (Tech Bonuses)
Effects are containers for commands. Use the fluent `add_command` builder.

```python
# Create effect container
bonus = workspace.effect_manager.create("New Civ Bonus")

# Add command: Archers (Class 903) get +1 Attack
bonus.add_command.attribute_modifier_add(
    a=903,  # Unit Class
    b=9,    # Attribute (Attack)
    d=1.0   # Amount
)
```

### 3. Modifying Techs
Change costs or research times.

```python
loom = workspace.tech_manager.get(22)
loom.research_time = 20  # Seconds
loom.cost_1.amount = 40  # Gold cost
```

### 4. Cloning for Specific IDs
Use `clone_into()` when you need to overwrite a specific slot (e.g., replacing a placeholder).

```python
# Overwrite ID 100 with a copy of ID 4
workspace.unit_manager.clone_into(
    dest_unit_id=100,
    base_unit_id=4,
    name="Replacement Archer"
)
```

## Documentation

*   [Overview](docs/overview.md)
*   **API Reference**:
    *   [Workspace](docs/api/workspace.md)
    *   [Units](docs/api/units.md)
    *   [Techs](docs/api/techs.md)
    *   [Effects](docs/api/effects.md)
    *   [Graphics](docs/api/graphics.md)
    *   [Sounds](docs/api/sounds.md)
    *   [Civilizations](docs/api/civs.md)
    *   [Datasets](docs/api/datasets.md)

## Stability Notes

*   **Stable**: `UnitManager`, `TechManager`, `EffectManager` APIs are considered stable.
*   **Experimental**: `TerrainManager` is currently not implemented.
*   **Internal**: Classes starting with `_` or located in `core` are internal.
