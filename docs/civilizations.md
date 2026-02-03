# Civilizations

The Civilizations module manages civilization data including resources, unit availability, and civ bonuses.

## Quick Example

```python
from aoe2_genie_tooling import GenieWorkspace

workspace = GenieWorkspace.load("empires2_x2_p1.dat")

# Get the civ manager
civ_manager = workspace.civ_manager

# Get a civilization
britons = civ_manager.get(1)
print(f"Civ: {britons.name}")

# Access civ resources
wood = britons.resource[1]  # Wood starting amount
britons.resource[1] = 300   # Set starting wood to 300
```

---

## Sub-Pages

| Page | Description |
|------|-------------|
| [Methods](civilizations/methods.md) | All CivManager and CivHandle methods |
| [Attributes](civilizations/attributes.md) | Complete attribute reference table |

---

## Overview

### CivManager (`workspace.civ_manager`)

The manager handles civilization operations:

| Method | Description |
|--------|-------------|
| `get(civ_id)` | Get a CivHandle |
| `create(name)` | Create a new civ |
| `copy(source_id)` | Copy a civ |
| `exists(civ_id)` | Check if civ exists |
| `find_by_name(name)` | Find by name |
| `count()` | Total civs |
| `add_resource(value)` | Add global resource slot |

### CivHandle

The handle provides attribute access and resource management:

**Key Attributes:**
- `name`, `tech_tree_effect_id`, `team_bonus_effect_id`
- `icon_set`, `player_type`

**Collections:**
- `resource` - Per-civ resource accessor
- `resources` - Raw resources list

---

## Civ Bonuses

Civilization bonuses are implemented via effects:

```python
# Create bonus effect
effect_manager = workspace.effect_manager
bonus = effect_manager.add_new("Britons Bonus")
bonus.add_command.attribute_modifier_add(a=4, b=12, c=-1, d=1)  # +1 range archers

# Link to civ
britons = civ_manager.get(1)
britons.tech_tree_effect_id = bonus.id
```

See [Effects](effects.md) for effect configuration.

---

## Resource Management

Resources are stored per-civ:

```python
civ = civ_manager.get(1)

# Read
food = civ.resource[0]
gold = civ.resource[3]

# Write
civ.resource[0] = 500  # 500 starting food
civ.resource[3] = 200  # 200 starting gold
```

---

## Global Resource Slots

The number of resource slots is global (same for all civs):

```python
# Add a new resource type
new_index = civ_manager.add_resource(default_value=100)

# Count slots
print(f"Resource slots: {civ_manager.resource_count()}")
```

---

## Civ-Specific Unit Changes

```python
# Get unit for specific civ
unit_manager = workspace.unit_manager
britons_archer = unit_manager.get(4, civ_ids=[1])
britons_archer.hit_points = 45  # Only affects Britons

# Regular get affects all civs
all_archers = unit_manager.get(4)
```
