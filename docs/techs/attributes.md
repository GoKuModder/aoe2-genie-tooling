# Tech Attributes

Complete reference of all attributes available on `TechHandle`.

## Core Attributes

| Attribute | Type | R/W | Description |
|-----------|------|-----|-------------|
| `id` | `int` | R | Tech ID (read-only) |
| `name` | `str` | RW | Internal tech name |
| `effect_id` | `int` | RW | Linked effect ID (-1 = none) |
| `research_time` | `int` | RW | Time to research (seconds) |

### Usage

```python
tech_manager = workspace.tech_manager
tech = tech_manager.get(22)

# Read
print(f"ID: {tech.id}")
print(f"Name: {tech.name}")
print(f"Research time: {tech.research_time}")

# Write
tech.name = "Custom Loom"
tech.research_time = 30
tech.effect_id = 500
```

---

## Display Attributes

| Attribute | Type | R/W | Description |
|-----------|------|-----|-------------|
| `icon_id` | `int` | RW | Icon index |
| `button_id` | `int` | RW | UI button position |
| `name_str_id` | `int` | RW | Language file name string ID |
| `description_str_id` | `int` | RW | Language file description ID |
| `help_str_id` | `int` | RW | Language file help text ID |
| `hotkey_str_id` | `int` | RW | Hotkey string ID |
| `tech_tree_str_id` | `int` | RW | Tech tree description ID |

### Usage

```python
tech.icon_id = 15           # Set icon
tech.name_str_id = 5000     # Language string for name
tech.hotkey_str_id = 5001   # Language string for hotkey
```

---

## Configuration Attributes

| Attribute | Type | R/W | Description |
|-----------|------|-----|-------------|
| `type` | `int` | RW | Tech type |
| `civilization_id` | `int` | RW | Civ restriction (-1 = all civs) |
| `min_required_techs` | `int` | RW | Minimum prerequisites needed |
| `full_tech_tree_mode` | `int` | RW | Full tech tree behavior |
| `repeatable` | `int` | RW | Can research multiple times (0/1) |
| `location_unit_id` | `int` | RW | Research location (pre-DE) |

### Usage

```python
# Make civ-specific
tech.civilization_id = 1  # Britons only

# Make repeatable
tech.repeatable = 1

# Require at least 2 prerequisite techs
tech.min_required_techs = 2
```

---

## Cost Attributes

Techs have 3 cost slots accessible via properties:

| Attribute | Type | Description |
|-----------|------|-------------|
| `cost_1` | `TechCost` | First cost slot |
| `cost_2` | `TechCost` | Second cost slot |
| `cost_3` | `TechCost` | Third cost slot |
| `costs` | `List[TechCost]` | All 3 cost slots |

### TechCost Properties

| Property | Type | Description |
|----------|------|-------------|
| `resource_id` | `int` | Resource type |
| `quantity` | `int` | Amount required |
| `deduct_flag` | `int` | Whether to deduct |

### Setting Costs

Use the `set_cost()` method:

```python
# 100 food
tech.set_cost(slot=0, resource_id=0, amount=100)

# 50 gold
tech.set_cost(slot=1, resource_id=3, amount=50)

# 75 wood
tech.set_cost(slot=2, resource_id=1, amount=75)
```

### Reading Costs

```python
cost = tech.cost_1
print(f"Resource: {cost.resource_id}, Amount: {cost.quantity}")

# Or iterate all
for i, cost in enumerate(tech.costs):
    if cost.quantity > 0:
        print(f"Slot {i}: {cost.quantity} of resource {cost.resource_id}")
```

---

## Required Tech Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `required_tech_ids` | `List[int]` | 6 slots for prerequisite techs |

**Note:** Use `set_required_tech()` and `clear_required_techs()` to modify.

```python
# Read
reqs = tech.required_tech_ids
for i, req_id in enumerate(reqs):
    if req_id != -1:
        print(f"Slot {i}: requires tech {req_id}")

# Set
tech.set_required_tech(slot=0, tech_id=101)  # Require Castle Age
tech.set_required_tech(slot=1, tech_id=22)   # Require Loom

# Clear
tech.clear_required_techs()
```

---

## Research Locations

| Attribute | Type | Description |
|-----------|------|-------------|
| `research_locations` | `List[ResearchLocationHandle]` | Where tech can be researched |

See [Research Locations](research-locations.md) for methods.

```python
for loc in tech.research_locations:
    print(f"Can research at building {loc.unit_id}")
```

---

## Common Resource IDs

| ID | Resource |
|----|----------|
| 0 | Food |
| 1 | Wood |
| 2 | Stone |
| 3 | Gold |

---

## Common Tech IDs

| ID | Tech |
|----|------|
| 22 | Loom |
| 101 | Castle Age |
| 102 | Imperial Age |
| 17 | Fletching |
| 211 | Iron Casting |
| 212 | Blast Furnace |

---

## Example: Configure Complete Tech

```python
tech_manager = workspace.tech_manager
tech = tech_manager.create("Elite Upgrade")

# Basic info
tech.name = "Elite Upgrade"
tech.research_time = 45
tech.icon_id = 10

# Costs
tech.set_cost(0, resource_id=0, amount=200)  # 200 food
tech.set_cost(1, resource_id=3, amount=150)  # 150 gold

# Requirements
tech.set_required_tech(0, tech_id=101)  # Castle Age
tech.min_required_techs = 1

# Link effect
effect_manager = workspace.effect_manager
effect = effect_manager.add_new("Elite Upgrade Effect")
effect.add_command.attribute_modifier_add(a=4, b=0, c=-1, d=20)
tech.effect_id = effect.id

# Research location
tech.add_research_location(unit_id=87, button_id=5)
```
