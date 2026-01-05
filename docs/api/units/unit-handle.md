# UnitHandle

The `UnitHandle` class is the primary interface for reading and modifying unit data. It wraps one or more `genieutils.unit.Unit` objects and propagates changes across all civilizations.

## Constructor

```python
UnitHandle(unit_id: int, dat_file: DatFile, civ_ids: Optional[List[int]] = None)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `unit_id` | `int` | The unit ID to wrap |
| `dat_file` | `DatFile` | The source DAT file |
| `civ_ids` | `List[int]` | Civilizations to affect. `None` = all |

!!! note "Creating UnitHandles"
    You typically don't create `UnitHandle` directly. Use `GenieUnitManager.get()` or `.create()` instead.

---

## Basic Properties

```python
um = workspace.genie_unit_manager()
unit = um.get(4)  # Archer

# Read-only
print(unit.id)    # 4
print(unit.name)  # "Archer"

# Writable
unit.name = "Elite Archer"
unit.hit_points = 50
unit.speed = 1.2
```

### Common Flattened Properties

These properties are accessible directly on `UnitHandle`:

| Property | Type | Source | Description |
|----------|------|--------|-------------|
| `name` | `str` | Unit | Unit name |
| `hit_points` | `int` | Unit | Max HP |
| `speed` | `float` | Unit | Movement speed |
| `line_of_sight` | `float` | Unit | Vision range |
| `garrison_capacity` | `int` | Unit | Max garrison |
| `icon_id` | `int` | Unit | Icon graphic ID |
| `standing_graphic` | `int` | Unit | Idle graphic ID |
| `dying_graphic` | `int` | Unit | Death graphic ID |
| `move_sound` | `int` | Bird | Movement sound ID |
| `attack_sound` | `int` | Bird | Attack sound ID |
| `max_range` | `float` | Type50 | Attack range |
| `reload_time` | `float` | Type50 | Attack cooldown |
| `attack_graphic` | `int` | Type50 | Attack animation ID |
| `train_time` | `int` | Creatable | Training time |
| `train_location_id` | `int` | Creatable | Where trained |

---

## Wrapper Properties

Access specialized wrappers for grouped properties:

```python
unit = um.get(4)

# Combat stats (Type50)
unit.combat.max_range = 7.0
unit.combat.reload_time = 2.0
unit.combat.accuracy_percent = 80

# Training info (Creatable)
unit.creatable.train_time = 35
unit.creatable.train_location_id = 12  # Archery Range

# Cost (convenience wrapper)
unit.cost.food = 0
unit.cost.wood = 25
unit.cost.gold = 45

# Movement (Bird)
unit.bird.move_sound = 5
unit.bird.attack_sound = 6
unit.bird.work_rate = 0.8

# Building (for buildings)
unit.building.garrison_type = 2
unit.building.construction_graphic = 100
```

### Available Wrappers

| Property | Wrapper Class | Purpose |
|----------|---------------|---------|
| `.combat` | `Type50Wrapper` | Attack stats, range, armor |
| `.creatable` | `CreatableWrapper` | Training, costs, button |
| `.cost` | `CostWrapper` | Food/wood/gold/stone costs |
| `.bird` | `BirdWrapper` | Movement, sounds, tasks |
| `.dead_fish` | `DeadFishWrapper` | Walking graphics, rotation |
| `.projectile` | `ProjectileWrapper` | Projectile behavior |
| `.building` | `BuildingWrapper` | Construction, garrison |
| `.resource_storages` | `ResourceStoragesWrapper` | Resource carrying |
| `.damage_graphics` | `DamageGraphicsWrapper` | Damage visuals |
| `.tasks` | `TasksWrapper` | Unit commands/abilities |

---

## Attacks and Armor

### Adding Attacks

```python
unit = um.get(4)

# Add a new attack
attack = unit.add_attack(class_=3, amount=6)  # Pierce damage
print(f"Added attack at index {attack.attack_id}")

# Add bonus damage vs cavalry
unit.add_attack(class_=8, amount=4)  # Bonus vs Cavalry
```

### Modifying Attacks

```python
# Get attack by class
attack = unit.get_attack_by_class(class_=3)
if attack:
    attack.amount = 10  # Increase pierce damage

# Or use set_attack (updates existing or adds new)
unit.set_attack(class_=3, amount=10)
```

### Reading All Attacks

```python
for attack in unit.attacks:
    print(f"Class {attack.class_}: {attack.amount} damage")
```

### Replacing All Attacks

```python
from genieutils.unit import AttackOrArmor

unit.attacks = [
    AttackOrArmor(class_=3, amount=8),   # Pierce
    AttackOrArmor(class_=4, amount=5),   # Melee
    AttackOrArmor(class_=11, amount=3),  # Bonus vs Buildings
]
```

### Armor (Same Pattern)

```python
# Add armor
armor = unit.add_armour(class_=3, amount=2)  # Pierce armor

# Get/set armor
unit.set_armour(class_=4, amount=3)  # Melee armor

# Read all armor
for arm in unit.armours:
    print(f"Class {arm.class_}: {arm.amount} defense")
```

---

## Tasks

Tasks define what actions a unit can perform (gather, build, attack, etc.).

### Adding Tasks

```python
from Datasets import Task, Resource

unit = um.get(83)  # Villager

# Add a gather task
task = unit.add_task(
    task_type=Task.GATHER,
    resource_in=Resource.FOOD,
    resource_out=Resource.FOOD,
    work_range=0.5,
    work_value_1=0.4,  # Gather rate
)
print(f"Added task at index {task.task_id}")
```

### Using TasksWrapper

```python
# List all tasks
for task in unit.tasks.list_tasks():
    print(f"Task {task.id}: type={task.task_type}")

# Remove a task
unit.tasks.remove_task(task_id=3)

# Clear all tasks
unit.tasks.clear_tasks()

# Add via wrapper
unit.tasks.add_task(
    task_type=7,
    id=10,
    work_value_1=1.0,
)
```

---

## Resource Storages

Control what resources a unit can carry (e.g., sheep carry food).

```python
from Datasets import Resource, StoreMode

unit = um.get(594)  # Sheep

# Set storage slot 1: 100 food
unit.resource_1(type=Resource.FOOD, amount=100.0, flag=StoreMode.GIVE_ONLY)

# Or use the wrapper
unit.resource_storages.resource_1(type=Resource.FOOD, amount=100.0, flag=1)
unit.resource_storages.resource_2(type=Resource.WOOD, amount=50.0, flag=0)

# Read storage
storage = unit.resource_storages
slot0 = storage.get(0)
print(f"Slot 0: type={slot0.type}, amount={slot0.amount}")
```

---

## Damage Graphics

Define how the unit looks when damaged.

```python
# Add damage state at 50% HP
dmg = unit.add_damage_graphic(graphic_id=450, damage_percent=50)
print(f"Added at index {dmg.damage_graphic_id}")

# Add another at 25% HP
unit.add_damage_graphic(graphic_id=451, damage_percent=25)

# Remove
unit.remove_damage_graphic(damage_graphic_id=0)
```

---

## Train Locations

Define where a unit can be trained.

```python
# Add training at Barracks (ID 12)
loc = unit.add_train_location(
    unit_id=12,
    train_time=30,
    button_id=1,
    hot_key_id=16389,
)

# Remove
unit.remove_train_location(train_location_id=0)
```

---

## Drop Sites

Define where a unit can deposit gathered resources.

```python
# Add Town Center as drop site
unit.add_drop_site(unit_id=109)

# Add Mill
unit.add_drop_site(unit_id=68)

# Remove
unit.remove_drop_site(drop_site_id=0)
```

---

## Complete Example

```python
from Actual_Tools import GenieWorkspace
from Datasets import Resource, UnitClass
from genieutils.unit import AttackOrArmor

workspace = GenieWorkspace.load("empires2_x2_p1.dat")
um = workspace.genie_unit_manager()
gm = workspace.graphic_manager()
sm = workspace.sound_manager()

# Create hero unit
hero = um.create("Champion Knight", base_unit_id=38)

# Basic stats
hero.hit_points = 250
hero.speed = 1.6
hero.line_of_sight = 6
hero.class_ = UnitClass.CAVALRY

# Combat stats
hero.combat.max_range = 0
hero.combat.reload_time = 1.8
hero.combat.displayed_attack = 18

# Attacks
hero.attacks = [
    AttackOrArmor(class_=4, amount=18),  # Melee
    AttackOrArmor(class_=8, amount=6),   # Bonus vs Cavalry
]

# Armor
hero.add_armour(class_=3, amount=4)  # Pierce
hero.add_armour(class_=4, amount=6)  # Melee

# Cost
hero.cost.food = 80
hero.cost.gold = 100

# Training
hero.creatable.train_time = 25
hero.creatable.train_location_id = 82  # Stable

# Graphics and sounds
attack_gfx = gm.add_graphic("hero_attack.slp", frame_count=15)
hero.combat.attack_graphic = attack_gfx.id

attack_snd = sm.add_sound("hero_attack.wav")
hero.bird.attack_sound = attack_snd.id

# Save
workspace.save("output.dat")
print(f"Created {hero.name} at ID {hero.id}")
```
