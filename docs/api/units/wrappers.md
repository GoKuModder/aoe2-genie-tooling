# Unit Wrappers

Wrappers provide organized access to unit sub-components. Each wrapper groups related properties and propagates changes across all civilizations.

## How Wrappers Work

```python
unit = um.get(4)  # Archer

# Access wrapper
combat = unit.combat  # Returns Type50Wrapper

# Read property
print(combat.max_range)  # 5.0

# Write property (applies to all civs)
combat.max_range = 7.0
```

---

## Type50Wrapper (Combat)

Access via: `unit.combat`

Controls attack statistics, damage, and armor.

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `max_range` | `float` | Maximum attack range |
| `min_range` | `float` | Minimum attack range |
| `reload_time` | `float` | Attack cooldown |
| `accuracy_percent` | `int` | Accuracy (0-100) |
| `blast_width` | `float` | Splash damage radius |
| `blast_damage` | `float` | Splash damage amount |
| `attack_graphic` | `int` | Attack animation ID |
| `attack_graphic_2` | `int` | Secondary attack graphic |
| `projectile_unit_id` | `int` | Projectile unit ID |
| `displayed_attack` | `int` | UI displayed attack |
| `displayed_range` | `float` | UI displayed range |
| `base_armor` | `int` | Base armor value |
| `attacks` | `list` | Attack entries (read-only) |
| `armours` | `list` | Armor entries (read-only) |

### Example

```python
unit = um.get(4)  # Archer

# Increase range
unit.combat.max_range = 7.0
unit.combat.displayed_range = 7.0

# Faster attack
unit.combat.reload_time = 1.5

# Better accuracy
unit.combat.accuracy_percent = 90

# Add splash damage
unit.combat.blast_width = 0.5
unit.combat.blast_damage = 2.0
```

---

## CreatableWrapper (Training)

Access via: `unit.creatable`

Controls training time, location, and costs.

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `train_time` | `int` | Training time in seconds |
| `train_location_id` | `int` | Building ID where trained |
| `button_id` | `int` | Button position (1-15) |
| `rear_attack_modifier` | `float` | Rear attack bonus |
| `flank_attack_modifier` | `float` | Flank attack bonus |
| `hero_mode` | `int` | Hero flag |
| `resource_costs` | `tuple` | Cost tuple (use CostWrapper) |

### Example

```python
unit = um.get(4)

# Training settings
unit.creatable.train_time = 20
unit.creatable.train_location_id = 12  # Archery Range
unit.creatable.button_id = 1
```

---

## CostWrapper (Resources)

Access via: `unit.cost`

Convenience wrapper for resource costs.

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `food` | `int` | Food cost |
| `wood` | `int` | Wood cost |
| `gold` | `int` | Gold cost |
| `stone` | `int` | Stone cost |

### Example

```python
unit = um.get(4)

# Set costs
unit.cost.food = 0
unit.cost.wood = 25
unit.cost.gold = 45
unit.cost.stone = 0

# Or set individually
unit.cost.gold = 50
```

---

## BirdWrapper (Movement & Tasks)

Access via: `unit.bird`

Controls movement, sounds, and task management.

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `move_sound` | `int` | Movement sound ID |
| `attack_sound` | `int` | Attack sound ID |
| `work_rate` | `float` | Gathering/work rate |
| `search_radius` | `float` | Search range |
| `drop_sites` | `list` | Drop site building IDs |
| `default_task_id` | `int` | Default task |
| `tasks` | `TasksWrapper` | Task collection |

### Example

```python
unit = um.get(83)  # Villager

# Sounds
unit.bird.move_sound = 5
unit.bird.attack_sound = 6

# Work rate
unit.bird.work_rate = 0.45

# Drop sites
unit.bird.drop_sites = [109, 68]  # Town Center, Mill
```

---

## TasksWrapper (Commands)

Access via: `unit.tasks` or `unit.bird.tasks`

Manages unit task/command collection.

### Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `add_task(...)` | `None` | Add new task |
| `list_tasks()` | `List[Task]` | Get all tasks |
| `get_task(task_id)` | `Task` | Get by ID |
| `remove_task(task_id)` | `bool` | Remove by ID |
| `copy_task(task_id)` | `None` | Copy existing task |
| `clear_tasks()` | `None` | Remove all |

### add_task Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `task_type` | `int` | Task type (see Datasets.Task) |
| `id` | `int` | Task ID |
| `resource_in` | `int` | Input resource type |
| `resource_out` | `int` | Output resource type |
| `work_value_1` | `float` | Work amount |
| `work_range` | `float` | Work range |
| `working_graphic_id` | `int` | Animation while working |
| `enabled` | `int` | 1=enabled, 0=disabled |

### Example

```python
from Datasets import Task, Resource

unit = um.get(83)  # Villager

# List current tasks
for task in unit.tasks.list_tasks():
    print(f"Task {task.id}: type={task.task_type}")

# Add gather task
unit.tasks.add_task(
    task_type=Task.GATHER,
    id=100,
    resource_in=Resource.GOLD,
    resource_out=Resource.GOLD,
    work_value_1=0.4,
    work_range=0.5,
)

# Remove a task
unit.tasks.remove_task(task_id=3)
```

---

## ResourceStoragesWrapper

Access via: `unit.resource_storages`

Manages resource carrying capacity.

### Methods

| Method | Description |
|--------|-------------|
| `resource_1(type, amount, flag)` | Set slot 1 |
| `resource_2(type, amount, flag)` | Set slot 2 |
| `resource_3(type, amount, flag)` | Set slot 3 |
| `get(slot)` | Get storage slot |
| `set(slot, type, amount, flag)` | Set any slot |

### Flags (StoreMode)

| Flag | Description |
|------|-------------|
| `0` | No change |
| `1` | Keep resource |
| `2` | Give resource on death |

### Example

```python
from Datasets import Resource, StoreMode

sheep = um.get(594)

# Sheep carries 100 food, gives on death
sheep.resource_storages.resource_1(
    type=Resource.FOOD,
    amount=100.0,
    flag=StoreMode.GIVE_ONLY
)
```

---

## BuildingWrapper

Access via: `unit.building`

Controls building-specific properties.

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `construction_graphic` | `int` | Building animation |
| `snow_graphic` | `int` | Snow variant |
| `garrison_type` | `int` | What can garrison |
| `garrison_heal_rate` | `float` | Heal rate inside |
| `tech_id` | `int` | Associated tech |
| `construction_sound` | `int` | Build sound |
| `transform_unit` | `int` | Transform into |
| `pile_unit` | `int` | Rubble unit |

### Example

```python
building = um.get(12)  # Barracks

# Garrison settings
building.building.garrison_type = 15  # All military
building.building.garrison_heal_rate = 0.5

# Construction
building.building.construction_sound = 100
```

---

## DamageGraphicsWrapper

Access via: `unit.damage_graphics`

Manages visual damage states.

### Methods

| Method | Description |
|--------|-------------|
| `add_damage_graphic(graphic_id, damage_percent, apply_mode)` | Add state |
| `remove_damage_graphic(index)` | Remove by index |

### Example

```python
building = um.get(12)

# Add 50% damage state
building.damage_graphics.add_damage_graphic(
    graphic_id=450,
    damage_percent=50,
)

# Add 25% damage state  
building.damage_graphics.add_damage_graphic(
    graphic_id=451,
    damage_percent=25,
)
```

---

## ProjectileWrapper

Access via: `unit.projectile`

Controls projectile behavior (for arrow/projectile units).

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `projectile_type` | `int` | Projectile type |
| `smart_mode` | `int` | Smart targeting |
| `hit_mode` | `int` | Hit detection mode |
| `vanish_mode` | `int` | Disappear mode |
| `projectile_arc` | `float` | Arc height |

### Example

```python
arrow = um.get(359)  # Arrow unit

arrow.projectile.projectile_arc = 0.5
arrow.projectile.smart_mode = 1
```

---

## DeadFishWrapper

Access via: `unit.dead_fish`

Controls movement graphics and rotation.

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `walking_graphic` | `int` | Walk animation |
| `running_graphic` | `int` | Run animation |
| `rotation_speed` | `float` | Turn speed |
| `turn_radius` | `float` | Turn radius |

### Example

```python
unit = um.get(4)

unit.dead_fish.rotation_speed = 0.5
unit.dead_fish.turn_radius = 0.0
```
