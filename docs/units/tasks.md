# Unit Tasks

Tasks define what actions a unit can perform - combat, gathering, building, healing, and more.

## Overview

Each task is an entry in the unit's task list with properties like:
- **Action Type** - What the task does (combat, gather, build, etc.)
- **Target Class** - What unit class can be targeted
- **Work Values** - Parameters for the task behavior
- **Work Range** - How far the task can operate

---

## Adding Tasks

### Using TaskBuilder (Recommended)

The `add_task` property provides a fluent API with named methods:

```python
unit_manager = workspace.unit_manager
unit = unit_manager.get(4)

# Add combat task
unit.add_task.combat(class_id=0)

# Add garrison task
unit.add_task.garrison(class_id=11)

# Add resource generation
unit.add_task.resource_generation(
    amount_received=0.7,
    type_resource_received=0,
)

# Add aura effect
unit.add_task.aura(
    attribute_id=0,
    max_increase=10,
    radius=4.0,
)
```

### Using Raw Parameters

For full control, use `create_task()`:

```python
unit.create_task(
    action_type=7,      # Combat
    class_id=0,         # Target archers
    work_range=8.0,
    work_value_1=1.0,
)
```

---

## TaskBuilder Methods Reference

### Basic Actions

| Method | Action Type | Description |
|--------|-------------|-------------|
| `none()` | 0 | No action |
| `move_to()` | 1 | Move to location |
| `follow()` | 2 | Follow unit |
| `garrison(class_id)` | 3 | Garrison into building |
| `explore()` | 4 | Auto-explore map |
| `gather(resource_in, resource_out)` | 5 | Gather resources |
| `graze()` | 6 | Graze (animals) |
| `combat(class_id)` | 7 | Attack enemies |
| `shoot()` | 8 | Ranged attack |
| `attack()` | 9 | Melee attack |
| `fly()` | 10 | Fly movement |
| `scare_hunt()` | 11 | Scare prey |
| `unload_boat()` | 12 | Unload transport |
| `guard()` | 13 | Guard unit |
| `siege_tower_ability()` | 14 | Siege tower |
| `escape()` | 20 | Escape |
| `make()` | 21 | Make |

### Production Actions

| Method | Action Type | Description |
|--------|-------------|-------------|
| `build()` | 101 | Construct buildings |
| `make_unit()` | 102 | Train units |
| `make_technology()` | 103 | Research tech |
| `convert(work_value_1, work_value_2)` | 104 | Convert enemies |
| `heal(work_value_1, work_range)` | 105 | Heal allies |
| `repair()` | 106 | Repair buildings |
| `auto_convert(capture_text_id)` | 107 | Auto-convert |
| `discovery_artifact()` | 108 | Discover artifact |
| `hunt(resource_in, resource_out)` | 110 | Hunt animals |
| `trade(unit_id)` | 111 | Trade with market |

### Advanced Actions

| Method | Action Type | Description |
|--------|-------------|-------------|
| `generate_wonder_victory()` | 120 | Wonder victory |
| `deselect_when_tasked_farm()` | 121 | Farm deselect |
| `loot_gather()` | 122 | Loot gathering |
| `housing()` | 123 | Housing |
| `pack()` | 124 | Pack up |
| `unpack_and_attack()` | 125 | Unpack and attack |
| `off_map_trade()` | 131 | Off-map trade |
| `pickup_unit(transform_unit_id)` | 132 | Pick up unit |
| `speed_charge(work_value_1, work_value_2)` | 133 | Speed charge |
| `transform_unit()` | 134 | Transform |
| `kidnap_unit()` | 135 | Kidnap |
| `deposit_unit(transform_unit_id)` | 136 | Deposit unit |
| `shear()` | 149 | Shear sheep |
| `regeneration()` | 150 | Regeneration |

### DE-Era Actions

| Method | Action Type | Description |
|--------|-------------|-------------|
| `resource_generation(...)` | 151 | Passive resource income |
| `movement_damage()` | 152 | Damage while moving |
| `moveable_drop_site()` | 153 | Mobile drop site |
| `pillage(...)` | 154 | Loot/pillage |
| `aura(...)` | 155 | Area buff effect |
| `additional_spawn(...)` | 156 | Spawn extra units |
| `stingers(...)` | 157 | Stinger effects |
| `hp_transformation(...)` | 158 | Transform at HP threshold |

---

## Detailed Method Examples

### `combat(class_id=-1, **kwargs)`

Makes the unit attack enemies.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `class_id` | `int` | `-1` | Target class (-1 = all) |

```python
# Attack all units
unit.add_task.combat()

# Attack only infantry
unit.add_task.combat(class_id=1)
```

---

### `garrison(class_id=-1, **kwargs)`

Makes the unit able to garrison.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `class_id` | `int` | `-1` | Building class to garrison in |

```python
unit.add_task.garrison(class_id=11)  # Garrison in buildings
```

---

### `gather(resource_in=-1, resource_out=-1, **kwargs)`

Makes the unit gather resources.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `resource_in` | `int` | `-1` | Resource type gathered |
| `resource_out` | `int` | `-1` | Resource type returned |

```python
# Gather food
unit.add_task.gather(resource_in=0, resource_out=0)
```

---

### `heal(work_value_1=0.0, work_range=0.0, **kwargs)`

Makes the unit heal allies.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `work_value_1` | `float` | `0.0` | Heal amount per tick |
| `work_range` | `float` | `0.0` | Heal range |

```python
unit.add_task.heal(work_value_1=1.0, work_range=4.0)
```

---

### `resource_generation(...)`

Passive resource generation (Feitoria-style).

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `amount_received` | `float` | `0.0` | Amount per tick |
| `type_resource_received` | `int` | `-1` | Resource type (0=food, etc.) |
| `productivity_resource` | `int` | `-1` | Multiplier resource |
| `target_unit_id` | `int` | `-1` | Target unit filter |
| `target_class_id` | `int` | `-1` | Target class filter |

```python
# Generate 0.7 food per tick
unit.add_task.resource_generation(
    amount_received=0.7,
    type_resource_received=0,
)

# Generate all resources (Feitoria)
unit.add_task.resource_generation(amount_received=0.5, type_resource_received=0)
unit.add_task.resource_generation(amount_received=0.5, type_resource_received=1)
unit.add_task.resource_generation(amount_received=0.5, type_resource_received=2)
unit.add_task.resource_generation(amount_received=0.5, type_resource_received=3)
```

---

### `aura(...)`

Area buff effect (like Centurion aura).

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `attribute_id` | `float` | `0.0` | Attribute to buff |
| `max_increase` | `float` | `0.0` | Maximum bonus |
| `required_units` | `float` | `0.0` | Units needed |
| `radius` | `float` | `0.0` | Effect radius |
| `affected_players` | `int` | `0` | Diplomacy filter |
| `proceeding_graphic` | `int` | `-1` | Visual effect |
| `icon_id` | `int` | `0` | Icon |
| `tooltip_short` | `int` | `-1` | Short tooltip string ID |
| `tooltip_long` | `int` | `-1` | Long tooltip string ID |
| `flags` | `int` | `0` | Behavior flags |

```python
# +10 attack aura in 4 tile radius
unit.add_task.aura(
    attribute_id=9,      # Attack
    max_increase=10,
    radius=4.0,
    affected_players=1,  # Allies
)
```

---

## Managing Tasks

### Get All Tasks

```python
tasks = unit.get_tasks_list()
for task in tasks:
    print(f"Task {task.action_type}")
```

### Get Single Task

```python
task = unit.get_task(0)  # First task
print(f"Action: {task.action_type}")
```

### Remove Task

```python
unit.remove_task(0)  # Remove first task
```

---

## TaskHandle Properties

| Property | Type | Description |
|----------|------|-------------|
| `action_type` | `int` | Task action type |
| `class_id` | `int` | Target class |
| `unit_id` | `int` | Target unit ID |
| `terrain_id` | `int` | Target terrain |
| `resource_in` | `int` | Input resource |
| `resource_out` | `int` | Output resource |
| `work_value_1` | `float` | Work parameter 1 |
| `work_value_2` | `float` | Work parameter 2 |
| `work_range` | `float` | Work range |
| `enabled` | `int` | Task enabled (0/1) |
| `proceeding_graphic` | `int` | Visual effect graphic |
| `carry_check` | `int` | Carry check flag |
| `search_wait_time` | `float` | Wait time between searches |

```python
task = unit.get_task(0)
task.work_range = 8.0
task.enabled = 1
```
