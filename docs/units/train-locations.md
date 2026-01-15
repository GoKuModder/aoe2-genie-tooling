# Train Locations

Train locations define where a unit can be trained (Town Center, Barracks, Castle, etc.).

## Overview

Each train location entry specifies:
- **Building Unit ID** - Which building trains this unit
- **Train Time** - How long it takes (can override unit's base train time)
- **Button ID** - UI position in the building's interface
- **Hotkey ID** - Keyboard shortcut

---

## Adding Train Locations

### `add_train_location(unit_id, train_time=0, button_id=0, hot_key_id=0)`

Add a new train location.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `unit_id` | `int` | Required | Building unit ID |
| `train_time` | `int` | `0` | Train time (0 = use unit default) |
| `button_id` | `int` | `0` | UI button position |
| `hot_key_id` | `int` | `0` | Hotkey string ID |

**Returns:** `TrainLocationHandle`

```python
unit_manager = workspace.unit_manager
unit = unit_manager.get(4)

# Train at Archery Range (ID 87)
unit.add_train_location(
    unit_id=87,
    button_id=1,
)

# Also trainable at Castle with longer time
unit.add_train_location(
    unit_id=82,       # Castle
    train_time=45,    # Override train time
    button_id=5,
)
```

---

## Getting Train Locations

### `get_train_location(train_location_id)`

Get a train location by index.

**Returns:** `TrainLocationHandle` or `None`

```python
loc = unit.get_train_location(0)
if loc:
    print(f"Trained at building {loc.unit_id}")
```

---

### `train_locations` Property

Access the full list of train locations.

```python
for loc in unit.train_locations:
    print(f"Building: {loc.unit_id}, Button: {loc.button_id}")
```

---

## Modifying Train Locations

Use the handle to modify properties:

```python
loc = unit.get_train_location(0)
loc.button_id = 3        # Move to button 3
loc.train_time = 30      # Change train time
```

---

## Removing Train Locations

### `remove_train_location(train_location_id)`

Remove a train location by index.

| Parameter | Type | Description |
|-----------|------|-------------|
| `train_location_id` | `int` | Index to remove |

**Returns:** `bool`

```python
unit.remove_train_location(0)  # Remove first location
```

---

## TrainLocationHandle Properties

| Property | Type | R/W | Description |
|----------|------|-----|-------------|
| `unit_id` | `int` | RW | Building unit ID |
| `train_time` | `int` | RW | Train time (0 = use default) |
| `button_id` | `int` | RW | UI button position |
| `hot_key_id` | `int` | RW | Hotkey string ID |

---

## Common Building IDs

| ID | Building |
|----|----------|
| 12 | Barracks |
| 45 | Dock |
| 49 | Siege Workshop |
| 68 | Mill |
| 82 | Castle |
| 84 | Market |
| 87 | Archery Range |
| 101 | Stable |
| 103 | Blacksmith |
| 104 | Monastery |
| 109 | Town Center |
| 117 | Lumber Camp |
| 234 | Krepost |
| 621 | Donjon |

---

## Button Positions

Button IDs map to UI grid positions:

```
+---+---+---+---+---+
| 1 | 2 | 3 | 4 | 5 |
+---+---+---+---+---+
| 6 | 7 | 8 | 9 |10 |
+---+---+---+---+---+
|11 |12 |13 |14 |15 |
+---+---+---+---+---+
```

Row 1: buttons 1-5
Row 2: buttons 6-10  
Row 3: buttons 11-15

---

## Example: Set Up Training for Custom Unit

```python
# Create a new unit
unit_manager = workspace.unit_manager
hero = unit_manager.create("Elite Guard", base_unit_id=38)

# Clear any inherited train locations
while len(hero.train_locations) > 0:
    hero.remove_train_location(0)

# Add new train locations
hero.add_train_location(
    unit_id=82,       # Castle
    train_time=45,
    button_id=6,      # First button, second row
)

hero.add_train_location(
    unit_id=109,      # Town Center
    train_time=60,    # Longer at TC
    button_id=10,     # Last button, second row
)

# Verify
for loc in hero.train_locations:
    print(f"Train at {loc.unit_id}, time={loc.train_time}, button={loc.button_id}")
```

---

## Example: Copy Train Locations

```python
unit_manager = workspace.unit_manager
source = unit_manager.get(4)   # Archer
target = unit_manager.get(100) # Custom unit

# Copy all train locations
for loc in source.train_locations:
    target.add_train_location(
        unit_id=loc.unit_id,
        train_time=loc.train_time,
        button_id=loc.button_id,
        hot_key_id=loc.hot_key_id,
    )
```
