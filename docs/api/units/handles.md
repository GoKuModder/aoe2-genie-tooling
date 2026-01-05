# Handles

Handles are index-aware wrappers for collection items. They contain both the data and the item's position in the parent list.

## Why Handles?

When you add an attack to a unit, you need to know:
1. The attack data (class, amount)
2. The index for later removal

Handles provide both:

```python
attack = unit.add_attack(class_=3, amount=6)
print(attack.attack_id)  # Index in attacks list
print(attack.class_)     # 3
print(attack.amount)     # 6

# Later, remove by index
unit.remove_attack(attack.attack_id)
```

---

## AttackHandle

Wraps an attack entry with its index.

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `attack_id` | `int` | Index in attacks list |
| `class_` | `int` | Attack class (damage type) |
| `amount` | `int` | Damage amount |

### Example

```python
# Add attack
attack = unit.add_attack(class_=4, amount=10)
print(f"Attack {attack.attack_id}: class={attack.class_}, amount={attack.amount}")

# Modify
attack.amount = 15

# Get by class
melee = unit.get_attack_by_class(class_=4)
if melee:
    melee.amount += 5
```

---

## ArmourHandle

Wraps an armor entry with its index.

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `armour_id` | `int` | Index in armours list |
| `class_` | `int` | Armor class (defense type) |
| `amount` | `int` | Defense amount |

### Example

```python
# Add armor
armor = unit.add_armour(class_=3, amount=2)
print(f"Armor {armor.armour_id}: class={armor.class_}, amount={armor.amount}")

# Modify
armor.amount = 5
```

---

## TaskHandle

Wraps a task with its index.

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `task_id` | `int` | Index in tasks list |
| `task_type` | `int` | Task type |
| `id` | `int` | Task's internal ID |
| `is_default` | `int` | Default task flag |
| `resource_in` | `int` | Input resource |
| `resource_out` | `int` | Output resource |
| `work_value_1` | `float` | Work amount |
| `work_range` | `float` | Work range |
| `enabled` | `int` | Enabled flag |
| ... | ... | All Task properties |

### Example

```python
# Add task
task = unit.add_task(task_type=7, id=10, work_value_1=0.5)
print(f"Task at index {task.task_id}, type={task.task_type}")

# Modify
task.work_value_1 = 1.0
task.enabled = 1

# Get by index
task = unit.get_task(0)
```

---

## DamageGraphicHandle

Wraps a damage graphic state.

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `damage_graphic_id` | `int` | Index in damage_graphics |
| `graphic_id` | `int` | Graphic to display |
| `damage_percent` | `int` | HP threshold (0-100) |
| `apply_mode` | `int` | Apply mode |

### Example

```python
# Add damage state at 50% HP
dmg = unit.add_damage_graphic(graphic_id=450, damage_percent=50)
print(f"Damage graphic {dmg.damage_graphic_id} at {dmg.damage_percent}%")

# Modify
dmg.graphic_id = 451

# Remove
unit.remove_damage_graphic(dmg.damage_graphic_id)
```

---

## TrainLocationHandle

Wraps a training location.

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `train_location_id` | `int` | Index in train_locations |
| `unit_id` | `int` | Building unit ID |
| `train_time` | `int` | Training time |
| `button_id` | `int` | Button position |
| `hot_key_id` | `int` | Hotkey ID |

### Example

```python
# Add training at Barracks
loc = unit.add_train_location(unit_id=12, train_time=30, button_id=1)
print(f"Trains at building {loc.unit_id}")

# Modify
loc.train_time = 25
```

---

## DropSiteHandle

Wraps a drop site reference.

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `drop_site_id` | `int` | Index in drop_sites |
| `unit_id` | `int` | Building unit ID |

### Example

```python
# Add Town Center as drop site
site = unit.add_drop_site(unit_id=109)
print(f"Drop site {site.drop_site_id}: building {site.unit_id}")

# Change to Mill
site.unit_id = 68
```

---

## Complete Example

```python
um = workspace.genie_unit_manager()
unit = um.get(4)  # Archer

# Track all handles
attack_handles = []
armor_handles = []

# Add attacks
for class_, amount in [(3, 6), (8, 2), (11, 1)]:
    handle = unit.add_attack(class_=class_, amount=amount)
    attack_handles.append(handle)
    print(f"Added attack {handle.attack_id}: class={class_}, amount={amount}")

# Modify via handle
attack_handles[0].amount = 10  # Increase pierce damage

# Add armor
armor = unit.add_armour(class_=3, amount=0)
armor.amount = 2  # Modify via handle

# Print all
print("\nFinal attacks:")
for atk in unit.attacks:
    print(f"  Class {atk.class_}: {atk.amount}")

print("\nFinal armor:")
for arm in unit.armours:
    print(f"  Class {arm.class_}: {arm.amount}")
```
