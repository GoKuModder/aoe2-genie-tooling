# Getting Started

This guide will walk you through installing `aoe2_genie_tooling` and making your first DAT file modification.

## Installation

```bash
pip install aoe2-genie-tooling
```

## Loading a DAT File

The entry point for all operations is the `GenieWorkspace` class:

```python
from aoe2_genie_tooling import GenieWorkspace

# Load from file path
workspace = GenieWorkspace.load("path/to/empires2_x2_p1.dat")

# Or load from the game directory (Windows)
workspace = GenieWorkspace.load(
    r"C:\Program Files (x86)\Steam\steamapps\common\AoE2DE\resources\_common\dat\empires2_x2_p1.dat"
)
```

## Understanding the Manager Pattern

`GenieWorkspace` provides access to specialized managers for each data type:

| Manager | Access | Purpose |
|---------|--------|---------|
| `UnitManager` | `workspace.unit_manager` | Create, get, clone units |
| `EffectManager` | `workspace.effect_manager` | Manage technology effects |
| `TechManager` | `workspace.tech_manager` | Manage technologies |
| `GraphicManager` | `workspace.graphic_manager` | Manage sprites/animations |
| `SoundManager` | `workspace.sound_manager` | Manage audio |
| `CivManager` | `workspace.civ_manager` | Manage civilizations |

Each manager returns **Handle** objects that provide a high-level interface for modifying game data.

## Your First Edit

Let's modify the Archer's hit points:

```python
from aoe2_genie_tooling import GenieWorkspace

# Load the DAT file
workspace = GenieWorkspace.load("empires2_x2_p1.dat")

# Get the Archer (Unit ID 4)
unit_manager = workspace.unit_manager
archer = unit_manager.get(4)

# Modify hit points (applies to ALL civilizations automatically)
archer.hit_points = 50

print(f"Archer HP is now: {archer.hit_points}")
```

## Creating a New Unit

Create a custom unit by cloning an existing one:

```python
# Create a new unit based on the Knight (ID 38)
unit_manager = workspace.unit_manager
elite_knight = unit_manager.create(
    name="Elite Knight",
    base_unit_id=38,  # Clone from Knight
)

# Customize the new unit
elite_knight.hit_points = 200
elite_knight.max_range = 0  # Melee unit

# Add attacks
elite_knight.add_attack(class_=4, amount=20)  # Base attack
elite_knight.add_attack(class_=21, amount=10)  # Bonus vs buildings

print(f"Created unit at ID: {elite_knight.id}")
```

## Saving Changes

Save your modifications to a new file:

```python
# Save to a new file
workspace.save("modded_empires2.dat")

# Or overwrite the original (use with caution!)
workspace.save("empires2_x2_p1.dat")
```

## Next Steps

Now that you understand the basics, explore the detailed documentation for each manager:

- **[Units](units.md)** – Complete unit creation and modification guide
- **[Effects](effects.md)** – Creating technology effects
- **[Techs](techs.md)** – Research and upgrade technologies
- **[Graphics](graphics.md)** – Sprite and animation management
- **[Sounds](sounds.md)** – Audio file management
