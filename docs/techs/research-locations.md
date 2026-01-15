# Research Locations

Research locations define where a technology can be researched (Blacksmith, University, Castle, etc.).

## Overview

Each research location entry specifies:
- **Building Unit ID** - Which building researches this tech
- **Button ID** - UI position in the building's interface

---

## Adding Research Locations

### `add_research_location(unit_id, button_id=0, ...)`

Add a new research location.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `unit_id` | `int` | Required | Building unit ID |
| `button_id` | `int` | `0` | UI button position |

**Returns:** `ResearchLocationHandle`

```python
tech_manager = workspace.tech_manager
tech = tech_manager.get(17)  # Fletching

# Research at Blacksmith
tech.add_research_location(
    unit_id=103,
    button_id=1,
)

# Also researchable at University
tech.add_research_location(
    unit_id=209,    # University
    button_id=5,
)
```

---

## Getting Research Locations

### `get_research_location(index)`

Get a research location by index.

**Returns:** `ResearchLocationHandle` or `None`

```python
loc = tech.get_research_location(0)
if loc:
    print(f"Researched at building {loc.unit_id}")
```

---

### `research_locations` Property

Access the full list of research locations.

```python
for loc in tech.research_locations:
    print(f"Building: {loc.unit_id}, Button: {loc.button_id}")
```

---

## Modifying Research Locations

Use the handle to modify properties:

```python
loc = tech.get_research_location(0)
loc.button_id = 3  # Move to button 3
```

---

## Removing Research Locations

### `remove_research_location(index)`

Remove a research location by index.

| Parameter | Type | Description |
|-----------|------|-------------|
| `index` | `int` | Index to remove |

**Returns:** `bool`

```python
tech.remove_research_location(0)  # Remove first location
```

---

### `clear_research_locations()`

Remove all research locations.

```python
tech.clear_research_locations()
```

---

## ResearchLocationHandle Properties

| Property | Type | R/W | Description |
|----------|------|-----|-------------|
| `unit_id` | `int` | RW | Building unit ID |
| `button_id` | `int` | RW | UI button position |

---

## Common Building IDs for Research

| ID | Building | Typical Techs |
|----|----------|---------------|
| 12 | Barracks | Infantry upgrades |
| 45 | Dock | Ship upgrades |
| 49 | Siege Workshop | Siege upgrades |
| 82 | Castle | Unique techs |
| 84 | Market | Trade upgrades |
| 87 | Archery Range | Archer upgrades |
| 101 | Stable | Cavalry upgrades |
| 103 | Blacksmith | Attack/armor upgrades |
| 104 | Monastery | Monk upgrades |
| 109 | Town Center | Age advances, Loom |
| 209 | University | Economy/siege techs |
| 235 | Mining Camp | Mining upgrades |
| 117 | Lumber Camp | Wood upgrades |
| 68 | Mill | Farm upgrades |

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

---

## Example: Set Up Research Locations

```python
# Create a new tech
tech_manager = workspace.tech_manager
tech = tech_manager.create("Advanced Smithing")
tech.research_time = 60

# Clear any inherited locations
tech.clear_research_locations()

# Add research at Blacksmith
tech.add_research_location(
    unit_id=103,    # Blacksmith
    button_id=6,    # First button, second row
)

# Also at University
tech.add_research_location(
    unit_id=209,    # University
    button_id=10,
)

# Verify
for loc in tech.research_locations:
    print(f"Research at {loc.unit_id}, button={loc.button_id}")
```

---

## Pre-DE vs DE Research Locations

In older versions, techs had a single `location_unit_id` property. In DE, techs use the research locations list, which supports multiple buildings:

```python
# For DE
tech.add_research_location(unit_id=103, button_id=1)

# For pre-DE (if needed)
tech.location_unit_id = 103
```
