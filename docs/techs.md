# Techs

The Techs module manages technologies - research items that trigger effects when completed.

## Quick Example

```python
from Actual_Tools_GDP import GenieWorkspace

workspace = GenieWorkspace.load("empires2_x2_p1.dat")

# Get the tech manager
tech_manager = workspace.tech_manager

# Get an existing tech
loom = tech_manager.get(22)
print(f"Loom research time: {loom.research_time}")

# Create a new tech
tech = tech_manager.create("Super Upgrade", effect_id=500)
tech.research_time = 60
tech.set_cost(0, resource_id=0, amount=100)  # 100 food
```

---

## Sub-Pages

| Page | Description |
|------|-------------|
| [Methods](techs/methods.md) | All TechManager and TechHandle methods |
| [Attributes](techs/attributes.md) | Complete attribute reference table |
| [Research Locations](techs/research-locations.md) | Where techs are researched |

---

## Overview

### TechManager (`workspace.tech_manager`)

The manager handles tech CRUD operations:

| Method | Description |
|--------|-------------|
| `get(tech_id)` | Get a TechHandle |
| `create(name, effect_id)` | Create a new tech |
| `copy(source_id)` | Copy a tech |
| `delete(tech_id)` | Delete a tech |
| `exists(tech_id)` | Check if tech exists |
| `find_by_name(name)` | Find by name |
| `count()` | Total tech slots |

### TechHandle

The handle provides attribute access and configuration:

**Key Attributes:**
- `name`, `effect_id`, `research_time`
- `icon_id`, `button_id`
- `civilization_id`, `min_required_techs`

**Collections:**
- `costs` - Resource costs (3 slots)
- `required_tech_ids` - Prerequisites (6 slots)
- `research_locations` - Where it's researched

---

## Creating Techs

```python
tech_manager = workspace.tech_manager

# Basic creation
tech = tech_manager.create("My Tech")

# With linked effect
tech = tech_manager.create("My Tech", effect_id=500)

# At specific ID
tech = tech_manager.create("My Tech", tech_id=800)
```

---

## Linking Effects

Techs trigger effects when researched:

```python
# Create effect first
effect_manager = workspace.effect_manager
effect = effect_manager.add_new("My Effect")
effect.add_command.attribute_modifier_add(a=4, b=0, c=-1, d=10)

# Link to tech
tech = tech_manager.create("My Research")
tech.effect_id = effect.id
```

See [Effects](effects.md) for effect configuration.

---

## Setting Costs

```python
# 3 cost slots available
tech.set_cost(0, resource_id=0, amount=200)  # 200 food
tech.set_cost(1, resource_id=3, amount=150)  # 150 gold
tech.set_cost(2, resource_id=1, amount=100)  # 100 wood
```

---

## Setting Prerequisites

```python
# 6 requirement slots
tech.set_required_tech(0, tech_id=101)  # Castle Age
tech.set_required_tech(1, tech_id=22)   # Loom

# How many must be researched
tech.min_required_techs = 2  # Both required
```

---

## Research Locations

```python
# Add where tech can be researched
tech.add_research_location(unit_id=103, button_id=5)  # Blacksmith
tech.add_research_location(unit_id=209, button_id=8)  # University
```

See [Research Locations](techs/research-locations.md) for details.
