# Civilization Attributes

Complete reference of all attributes available on `CivHandle`.

## Core Attributes

| Attribute | Type | R/W | Description |
|-----------|------|-----|-------------|
| `id` | `int` | R | Civilization ID (read-only) |
| `name` | `str` | RW | Civilization name |
| `tech_tree_effect_id` | `int` | RW | Effect applied at game start |
| `team_bonus_effect_id` | `int` | RW | Effect for team bonus |
| `icon_set` | `int` | RW | Icon set used (building/unit graphics) |
| `player_type` | `int` | RW | Player type value |

### Usage

```python
civ = workspace.civ_manager.get(1)

# Read
print(f"ID: {civ.id}")
print(f"Name: {civ.name}")
print(f"Tech Tree Effect: {civ.tech_tree_effect_id}")

# Write
civ.name = "Custom Britons"
civ.tech_tree_effect_id = 500
civ.icon_set = 1
```

---

## Effect Linking

### Tech Tree Effect

The `tech_tree_effect_id` points to an effect that applies at game start. This is how civilization bonuses work.

```python
# Create a civ bonus effect
bonus = workspace.effect_manager.add_new("Britons Bonus")
bonus.add_command.attribute_modifier_add(a=4, b=12, c=-1, d=1)  # +1 range archers

# Link to civ
britons = workspace.civ_manager.get(1)
britons.tech_tree_effect_id = bonus.id
```

### Team Bonus Effect

The `team_bonus_effect_id` points to an effect that applies to all allies.

```python
# Create team bonus effect
team_bonus = workspace.effect_manager.add_new("Britons Team Bonus")
team_bonus.add_command.attribute_modifier_add(a=87, b=12, c=-1, d=2)  # +2 range archery

# Link to civ
britons.team_bonus_effect_id = team_bonus.id
```

---

## Standard Civilization IDs

| ID | Civilization |
|----|--------------|
| 0 | Gaia |
| 1 | Britons |
| 2 | Franks |
| 3 | Goths |
| 4 | Teutons |
| 5 | Japanese |
| 6 | Chinese |
| 7 | Byzantines |
| 8 | Persians |
| 9 | Saracens |
| 10 | Turks |
| 11 | Vikings |
| 12 | Mongols |
| 13 | Celts |
| 14 | Spanish |
| 15 | Aztecs |
| 16 | Mayans |
| 17 | Huns |
| 18 | Koreans |
| 19 | Italians |
| 20 | Indians |
| 21 | Incas |
| 22 | Magyars |
| 23 | Slavs |
| 24 | Portuguese |
| 25 | Ethiopians |
| 26 | Malians |
| 27 | Berbers |
| 28 | Khmer |
| 29 | Malay |
| 30 | Burmese |
| 31 | Vietnamese |
| ... | (DE civs continue) |

---

## Resource Attributes

Resources are accessed via the `resource` accessor or `resources` list.

### Using ResourceAccessor

```python
civ = workspace.civ_manager.get(1)

# Get by index
food = civ.resource[0]
wood = civ.resource[1]
stone = civ.resource[2]
gold = civ.resource[3]

# Set by index
civ.resource[0] = 500  # 500 food
civ.resource[3] = 200  # 200 gold

# Using methods
food = civ.resource.get(0)
civ.resource.set(0, 500)
```

### Common Resource Indices

| Index | Resource |
|-------|----------|
| 0 | Food |
| 1 | Wood |
| 2 | Stone |
| 3 | Gold |
| 4 | Population Headroom |
| 5 | Conversion Range |
| 6 | Current Age |
| 7 | Relics Captured |
| 11 | Current Population |
| 32 | Bonus Population Cap |

See [Datasets](../datasets.md) for full resource list.

---

## Direct Resources Access

For bulk operations, access the raw resources list:

```python
# Get all resources
all_res = civ.resources  # List[float]

# Iterate
for i, value in enumerate(all_res[:10]):
    print(f"Resource {i}: {value}")
```

**Note:** Modifying this list directly affects the civ.

---

## Units Attribute

Each civ has its own units list:

```python
# Direct access (not recommended)
units = civ.units

# Better: Use UnitManager with civ_ids
archer = workspace.unit_manager.get(4, civ_ids=[1])
```

---

## Example: Configure Custom Civ

```python
# Clone Britons
custom = workspace.civ_manager.copy(1)
custom.name = "Elite Britons"

# Create custom tech tree effect
bonus = workspace.effect_manager.add_new("Elite Britons Bonus")
bonus.add_command.attribute_modifier_multiply(a=-1, b=0, c=-1, d=1.1)  # +10% HP all
custom.tech_tree_effect_id = bonus.id

# Set starting resources
custom.resource[0] = 300  # Food
custom.resource[1] = 300  # Wood
custom.resource[2] = 200  # Stone
custom.resource[3] = 200  # Gold

print(f"Created custom civ at ID: {custom.id}")
```
