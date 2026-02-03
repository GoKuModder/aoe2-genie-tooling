# Units

The Units module provides comprehensive tools for creating, modifying, and managing units in AoE2 DAT files.

## Quick Example

```python
from aoe2_genie_tooling import GenieWorkspace

workspace = GenieWorkspace.load("empires2_x2_p1.dat")

# Get the unit manager
unit_manager = workspace.unit_manager

# Get an existing unit
archer = unit_manager.get(4)
archer.hit_points = 50

# Create a new unit
hero = unit_manager.create("Super Knight", base_unit_id=38)
hero.hit_points = 300
hero.add_attack(class_=4, amount=25)
```

---

## Sub-Pages

| Page | Description |
|------|-------------|
| [Methods](units/methods.md) | All UnitManager and UnitHandle methods |
| [Attributes](units/attributes.md) | Complete attribute reference table |
| [Tasks](units/tasks.md) | TaskBuilder and task management |
| [Attacks & Armours](units/attacks-armours.md) | Damage and armor by class |
| [Train Locations](units/train-locations.md) | Where units are trained |

---

## Overview

### UnitManager (`workspace.unit_manager`)

The manager handles unit CRUD operations:

| Method | Description |
|--------|-------------|
| `get(unit_id)` | Get a UnitHandle for an existing unit |
| `create(name, base_unit_id)` | Create a new unit by cloning |
| `clone_into(dest_id, source_id)` | Clone to specific ID |
| `move(src_id, dst_id)` | Move unit between IDs |
| `exists(unit_id)` | Check if unit exists |
| `find_by_name(name)` | Find by internal name |
| `count()` | Total unit slots |

### UnitHandle

The handle provides attribute access and collection management:

**Key Attributes:**
- `hit_points`, `speed`, `line_of_sight`
- `max_range`, `reload_time`, `accuracy_percent`
- `attack_graphic`, `projectile_unit_id`

**Collections:**
- `attacks` / `armours` - Damage and armor values
- `tasks` - What the unit can do
- `train_locations` - Where it's trained

---

## Multi-Civ Propagation

By default, changes apply to ALL civilizations:

```python
# This affects all civs
archer = unit_manager.get(4)
archer.hit_points = 50  # All archer instances updated
```

For civ-specific changes:

```python
# Only affects Britons
britons_archer = unit_manager.get(4, civ_ids=[1])
britons_archer.hit_points = 45
```

---

## Creating Units

```python
# Basic creation
hero = unit_manager.create("Hero", base_unit_id=38)

# At specific ID
hero = unit_manager.create("Hero", base_unit_id=38, unit_id=2000)

# For specific civs only
briton_unique = unit_manager.create("Briton Hero", enable_for_civs=[1])
```

See [Methods](units/methods.md) for full parameter details.

---

## Modifying Units

```python
unit = unit_manager.get(4)

# Direct attributes
unit.hit_points = 100
unit.max_range = 8.0
unit.speed = 1.2

# Collections
unit.add_attack(class_=4, amount=10)
unit.set_armour(class_=3, amount=5)

# Tasks
unit.add_task.combat(class_id=0)
unit.add_task.garrison(class_id=11)
```

See [Attributes](units/attributes.md) for all available properties.
