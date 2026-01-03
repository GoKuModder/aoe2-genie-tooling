# aoe2-genie-tooling

High-level Python toolkit for editing Age of Empires II Definitive Edition DAT files.

An object-oriented API with proper wrappers that handle multi-civ propagation automatically.

## Installation

```shell
pip install aoe2-genie-tooling
```

## Why This Library?

- **Proper Objects** – Units, Graphics, Sounds return handle objects with typed properties
- **Multi-Civ Propagation** – Changes automatically apply across all civilizations
- **Attribute Flattening** – Access deeply nested properties directly (`unit.move_sound` instead of `unit.bird.move_sound`)
- **Type-Safe Datasets** – IntEnum constants for resources, tasks, attack classes

---

## Quick Start

```python
from Actual_Tools import GenieWorkspace

workspace = GenieWorkspace.load("empires2_x2_p1.dat")

# Get managers
um = workspace.genie_unit_manager()
gm = workspace.graphic_manager()
sm = workspace.sound_manager()
tm = workspace.tech_manager()
cm = workspace.civ_manager()

# Create a custom unit
unit = um.create("Elite Guard", base_unit_id=4)  # Clone from Archer
unit.hit_points = 120
unit.max_range = 6.0

workspace.save("output.dat")
```

---

## Units: Create, Clone, Move, Delete

### Creating Units

```python
um = workspace.genie_unit_manager()

# Create new unit (clones from base_unit_id)
unit = um.create(
    name="My Unit",
    base_unit_id=4,               # Clone from Archer
    unit_id=1500,                 # Optional: specific ID (auto-assigns if None)
    enable_for_civs=[0, 1, 2],    # Optional: specific civs (all if None)
)
```

### Cloning Units

```python
um = workspace.genie_unit_manager()

# Clone existing unit to a new ID
clone = um.clone_into(
    src_unit_id=4,       # Source: Archer
    dst_unit_id=2000,    # Destination ID
    name="Archer Clone",
    on_conflict="overwrite",  # "error" | "overwrite"
)
```

### Moving Units

```python
um = workspace.genie_unit_manager()

# Move unit to different ID (leaves placeholder at source)
um.move(
    src_unit_id=2000,
    dst_unit_id=2500,
    on_conflict="swap",  # "error" | "overwrite" | "swap"
)
```

### Getting Existing Units

```python
um = workspace.genie_unit_manager()

# Get handle for existing unit
archer = um.get(4)
print(archer.name)       # "Archer"
print(archer.hit_points) # 30
```

---

## Attacks & Armors

```python
from genieutils.unit import AttackOrArmor

um = workspace.genie_unit_manager()
unit = um.get(4)  # Archer

# Read current attacks
for attack in unit.attacks:
    print(f"Class {attack.class_}: {attack.amount} damage")

# Add new attack (pierce damage)
unit.add_attack(class_=3, amount=6)

# Add armor (melee armor)
unit.add_armour(class_=4, amount=2)

# Replace entire attack list
unit.attacks = [
    AttackOrArmor(class_=3, amount=10),  # Pierce
    AttackOrArmor(class_=4, amount=5),   # Melee
]
```

---

## Tasks (Unit Commands)

```python
from Datasets import Task, Resource

um = workspace.genie_unit_manager()
unit = um.get(83)  # Villager

# List all tasks
for task in unit.tasks.list_tasks():
    print(f"Task {task.id}: type={task.task_type}")

# Add a gather task
unit.tasks.add_task(
    task_type=Task.GATHER,
    resource_in=Resource.FOOD,
    resource_out=Resource.FOOD,
    work_range=0.5,
)

# Remove a task by ID
unit.tasks.remove_task(task_id=3)

# Clear all tasks
unit.tasks.clear_tasks()
```

---

## Resource Storages

```python
from Datasets import Resource, StoreMode

um = workspace.genie_unit_manager()
unit = um.get(594)  # Sheep

# Set storage slot 1: holds 100 food
unit.resource_1(type=Resource.FOOD, amount=100.0, flag=2)

# Read storage values
storage = unit.resource_storages
slot = storage.get(0)
print(f"Type: {slot.type}, Amount: {slot.amount}")
```

---

## Graphics: Create and Assign

```python
gm = workspace.graphic_manager()
um = workspace.genie_unit_manager()

# Create a new graphic
graphic = gm.add_graphic(
    file_name="my_unit_attack.slp",
    frame_count=15,
    angle_count=8,
)

print(f"Created graphic ID: {graphic.id}")

# Assign to unit
unit = um.create("Slinger", base_unit_id=4)
unit.standing_graphic = graphic.id
unit.combat.attack_graphic = graphic.id

# Copy existing graphic
copied = gm.copy(source_id=100, target_id=5000)
```

---

## Sounds: Create and Assign

```python
sm = workspace.sound_manager()
um = workspace.genie_unit_manager()

# Create a new sound
sound = sm.add_sound(filename="custom_attack.wav", probability=100)

print(f"Created sound ID: {sound.id}")

# Assign to unit
unit = um.get(4)
unit.attack_sound = sound.id
unit.move_sound = sound.id
```

---

## Complete Example: Custom Unit with Assets

```python
from Actual_Tools import GenieWorkspace
from Datasets import Resource, UnitClass
from genieutils.unit import AttackOrArmor

workspace = GenieWorkspace.load("empires2_x2_p1.dat")

# Get managers
um = workspace.genie_unit_manager()
gm = workspace.graphic_manager()
sm = workspace.sound_manager()

# 1. Create custom graphics
idle_gfx = gm.add_graphic("hero_idle.slp", frame_count=10, angle_count=8)
attack_gfx = gm.add_graphic("hero_attack.slp", frame_count=15, angle_count=8)

# 2. Create custom sound
attack_sound = sm.add_sound("hero_attack.wav")

# 3. Create the unit (clone from Knight)
hero = um.create("Hero Knight", base_unit_id=38)

# 4. Set basic stats
hero.hit_points = 200
hero.speed = 1.5
hero.class_ = UnitClass.CAVALRY

# 5. Assign graphics
hero.standing_graphic = idle_gfx.id
hero.combat.attack_graphic = attack_gfx.id

# 6. Assign sound
hero.attack_sound = attack_sound.id

# 7. Set attacks and armor
hero.attacks = [
    AttackOrArmor(class_=4, amount=15),   # Melee
    AttackOrArmor(class_=11, amount=10),  # Bonus vs Buildings
]
hero.add_armour(class_=3, amount=5)  # Pierce armor

# 8. Set cost
hero.cost.food = 100
hero.cost.gold = 80

# 9. Set resource storage (drops gold on death)
hero.resource_1(type=Resource.GOLD, amount=50.0, flag=2)

# 10. Save
workspace.save("output.dat")
workspace.save_registry("genie_edits.json")

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
- genieutils-py (auto-installed)

## License

LGPL-3.0

## Author

GoKuModder
