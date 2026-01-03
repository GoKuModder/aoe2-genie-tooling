# Units API Overview

The Units API provides complete control over unit data in AoE2 DE DAT files.

## Architecture

```
GenieWorkspace
    └── genie_unit_manager() → GenieUnitManager
                                    └── create() / get() → UnitHandle
                                                              ├── .combat → Type50Wrapper
                                                              ├── .bird → BirdWrapper
                                                              ├── .creatable → CreatableWrapper
                                                              ├── .cost → CostWrapper
                                                              ├── .building → BuildingWrapper
                                                              ├── .tasks → TasksWrapper
                                                              └── .resource_storages → ResourceStoragesWrapper
```

## Key Concepts

### Multi-Civ Propagation
When you modify a `UnitHandle`, changes apply to **all civilizations** automatically:

```python
um = workspace.genie_unit_manager()
unit = um.get(4)  # Archer

# This changes the Archer's HP for ALL civs
unit.hit_points = 50
```

### Attribute Flattening
Access deeply nested properties directly on the handle:

```python
# Instead of: unit.bird.move_sound = 5
unit.move_sound = 5

# Instead of: unit.type_50.max_range = 7.0
unit.max_range = 7.0
```

### Handle Pattern
Collection items (attacks, tasks, etc.) return Handle objects with their index:

```python
attack = unit.add_attack(class_=3, amount=6)
print(attack.attack_id)  # Index in attacks list
print(attack.class_)     # 3
print(attack.amount)     # 6
```

## Quick Reference

| Class | Purpose |
|-------|---------|
| [GenieUnitManager](unit-manager.md) | Create, clone, move, delete units |
| [UnitHandle](unit-handle.md) | Access and modify unit properties |
| [Wrappers](wrappers.md) | Type50, Bird, Creatable, Building, etc. |
| [Handles](handles.md) | Attack, Armour, Task, DamageGraphic handles |

## Basic Usage

```python
from Actual_Tools import GenieWorkspace

workspace = GenieWorkspace.load("empires2_x2_p1.dat")
um = workspace.genie_unit_manager()

# Create a new unit
hero = um.create("Hero Knight", base_unit_id=38)
hero.hit_points = 200
hero.speed = 1.5

# Modify existing unit
archer = um.get(4)
archer.max_range = 7.0

# Add attacks and armor
hero.add_attack(class_=4, amount=15)  # Melee
hero.add_armour(class_=3, amount=5)   # Pierce armor

workspace.save("output.dat")
```
