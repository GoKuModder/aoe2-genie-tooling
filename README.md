# aoe2-genie-tooling

High-level Python toolkit for editing Age of Empires II Definitive Edition DAT files.

An object-oriented API with proper wrappers that handle multi-civ propagation automatically.

## Installation

```shell
pip install aoe2-genie-tooling
```

## Documentation

Full documentation is available in the `docs/` directory or at [https://gokumodder.github.io/aoe2-genie-tooling/](https://gokumodder.github.io/aoe2-genie-tooling/).

## Why This Library?

- **Proper Objects** – Units, Graphics, Sounds return handle objects with typed properties
- **Multi-Civ Propagation** – Changes automatically apply across all civilizations
- **Attribute Flattening** – Access deeply nested properties directly (`unit.move_sound` instead of `unit.bird.move_sound`)
- **Type-Safe Datasets** – IntEnum constants for resources, tasks, attack classes
- **Fluent Builders** - Easy-to-use builders for tasks (`unit.add_task.combat()`) and effects

---

## Quick Start

```python
from Actual_Tools_GDP import GenieWorkspace

# Load workspace
workspace = GenieWorkspace.load("empires2_x2_p1.dat")

# Get managers
unit_manager = workspace.unit_manager
graphic_manager = workspace.graphic_manager
sound_manager = workspace.sound_manager
tech_manager = workspace.tech_manager
civ_manager = workspace.civ_manager

# Create a custom unit
unit = unit_manager.create("Elite Guard", base_unit_id=4)  # Clone from Archer
unit.hit_points = 120
unit.max_range = 6.0

# Save changes
workspace.save("output.dat")
```

---

## Units: Create, Clone, Move, Delete

### Creating Units

```python
unit_manager = workspace.unit_manager

# Create new unit (clones from base_unit_id)
unit = unit_manager.create(
    name="My Unit",
    base_unit_id=4,               # Clone from Archer
    unit_id=1500,                 # Optional: specific ID (auto-assigns if None)
    enable_for_civs=[0, 1, 2],    # Optional: specific civs (all if None)
)
```

### Cloning Units

```python
unit_manager = workspace.unit_manager

# Clone existing unit to a new ID
clone = unit_manager.clone_into(
    src_unit_id=4,       # Source: Archer
    dst_unit_id=2000,    # Destination ID
    name="Archer Clone",
    on_conflict="overwrite",  # "error" | "overwrite"
)
```

### Moving Units

```python
unit_manager = workspace.unit_manager

# Move unit to different ID (leaves placeholder at source)
unit_manager.move(
    src_unit_id=2000,
    dst_unit_id=2500,
    on_conflict="swap",  # "error" | "overwrite" | "swap"
)
```

### Getting Existing Units

```python
unit_manager = workspace.unit_manager

# Get handle for existing unit
archer = unit_manager.get(4)
print(archer.name)       # "Archer"
print(archer.hit_points) # 30
```

---

## Attacks & Armors

```python
unit_manager = workspace.unit_manager
unit = unit_manager.get(4)  # Archer

# Read current attacks
for attack in unit.attacks:
    print(f"Class {attack.class_}: {attack.amount} damage")

# Add new attack (pierce damage)
unit.add_attack(class_=3, amount=6)

# Add armor (melee armor)
unit.add_armour(class_=4, amount=2)
```

---

## Tasks (Unit Commands)

```python
from Datasets import Task, Resource

unit_manager = workspace.unit_manager
unit = unit_manager.get(83)  # Villager

# List all tasks
for task in unit.tasks.list_tasks():
    print(f"Task {task.id}: type={task.task_type}")

# Add a gather task using builder
unit.add_task.gather(
    resource_in=Resource.FOOD,
    resource_out=Resource.FOOD,
    work_range=0.5,
)

# Remove a task by ID
unit.remove_task(0)

# Clear all tasks
unit.clear_tasks()
```

---

## Graphics: Create and Assign

```python
graphic_manager = workspace.graphic_manager
unit_manager = workspace.unit_manager

# Create a new graphic
graphic = graphic_manager.add_graphic(
    file_name="my_unit_attack.slp",
    frame_count=15,
    angle_count=8,
)

print(f"Created graphic ID: {graphic.id}")

# Assign to unit
unit = unit_manager.create("Slinger", base_unit_id=4)
unit.standing_graphic_1 = graphic.id
unit.attack_graphic = graphic.id
```

---

## Sounds: Create and Assign

```python
sound_manager = workspace.sound_manager
unit_manager = workspace.unit_manager

# Create a new sound
sound = sound_manager.add_new("Custom Attack")
sound.new_sound(filename="custom_attack.wav", probability=100)

print(f"Created sound ID: {sound.id}")

# Assign to unit
unit = unit_manager.get(4)
unit.attack_sound = sound.id
unit.move_sound = sound.id
```

---

## Complete Example: Custom Unit with Assets

```python
from Actual_Tools_GDP import GenieWorkspace
from Datasets import Resource, UnitClass

workspace = GenieWorkspace.load("empires2_x2_p1.dat")

# Get managers
unit_manager = workspace.unit_manager
graphic_manager = workspace.graphic_manager
sound_manager = workspace.sound_manager

# 1. Create custom graphics
idle_gfx = graphic_manager.add_graphic("hero_idle.slp", frame_count=10, angle_count=8)
attack_gfx = graphic_manager.add_graphic("hero_attack.slp", frame_count=15, angle_count=8)

# 2. Create custom sound
attack_sound = sound_manager.add_new("hero_attack")
attack_sound.new_sound("hero_attack.wav")

# 3. Create the unit (clone from Knight)
hero = unit_manager.create("Hero Knight", base_unit_id=38)

# 4. Set basic stats
hero.hit_points = 200
hero.speed = 1.5
hero.class_ = UnitClass.CAVALRY

# 5. Assign graphics
hero.standing_graphic_1 = idle_gfx.id
hero.attack_graphic = attack_gfx.id

# 6. Assign sound
hero.attack_sound = attack_sound.id

# 7. Set attacks and armor
hero.set_attack(class_=4, amount=15)   # Melee
hero.set_attack(class_=11, amount=10)  # Bonus vs Buildings
hero.add_armour(class_=3, amount=5)    # Pierce armor

# 8. Set cost
hero.cost.food = 100
hero.cost.gold = 80

# 9. Set resource storage (drops gold on death)
hero.resource_1(type=Resource.GOLD, amount=50.0, flag=2)

# 10. Save
workspace.save("output.dat")

print(f"Created Hero Knight at ID {hero.id}")
```

---

## Datasets (Constants)

```python
from Datasets import (
    Resource,      # FOOD, WOOD, GOLD, STONE, etc.
    UnitClass,     # INFANTRY, ARCHER, CAVALRY, etc.
    Attribute,     # Object attributes for effects
    Task,          # GATHER, BUILD, ATTACK, etc.
    StoreMode,     # Resource storage flags
)

unit.class_ = UnitClass.ARCHER
```

---

## Exceptions

| Exception | When Raised |
|-----------|-------------|
| `UnitIdConflictError` | Target ID exists with `on_conflict="error"` |
| `GapNotAllowedError` | Would create gaps with `fill_gaps="error"` |
| `InvalidIdError` | Negative or non-existent ID |
| `TemplateNotFoundError` | No template unit for cloning |
| `ValidationError` | Workspace validation failed |

---

## Requirements

- Python 3.11+
- GenieDatParser (local dependency - Rust-backed DAT parser)

## License

LGPL-3.0

## Author

GoKuModder
