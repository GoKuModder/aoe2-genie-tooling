# Effect Commands

Complete reference of all effect command types available through `EffectCommandBuilder`.

## Overview

Effect commands define what happens when a technology is researched. Each command has:
- **Type** - What kind of modification
- **Parameters A, B, C** - Integer parameters (meaning varies by type)
- **Parameter D** - Float value (usually the actual modifier amount)

---

## Using EffectCommandBuilder

Access via the `add_command` property:

```python
effect_manager = workspace.effect_manager
effect = effect_manager.get(100)

# Add commands using named methods
effect.add_command.attribute_modifier_add(a=4, b=0, c=-1, d=10)
effect.add_command.enable_disable_unit(a=100, b=1)
```

---

## Attribute Modifiers

These commands modify unit attributes.

### `attribute_modifier_set(a, b, c, d)` - Type 0

Set an attribute to a specific value.

| Parameter | Description |
|-----------|-------------|
| `a` | Unit ID |
| `b` | Attribute ID (see Datasets) |
| `c` | Class ID (-1 = all) |
| `d` | Value to set |

```python
# Set Archer HP to 50
effect.add_command.attribute_modifier_set(a=4, b=0, c=-1, d=50)
```

---

### `attribute_modifier_add(a, b, c, d)` - Type 4

Add to an attribute value.

| Parameter | Description |
|-----------|-------------|
| `a` | Unit ID |
| `b` | Attribute ID |
| `c` | Class ID (-1 = all) |
| `d` | Amount to add (can be negative) |

```python
# +10 HP to Archer
effect.add_command.attribute_modifier_add(a=4, b=0, c=-1, d=10)

# -5 range to Archer
effect.add_command.attribute_modifier_add(a=4, b=12, c=-1, d=-5)
```

---

### `attribute_modifier_multiply(a, b, c, d)` - Type 5

Multiply an attribute value.

| Parameter | Description |
|-----------|-------------|
| `a` | Unit ID |
| `b` | Attribute ID |
| `c` | Class ID (-1 = all) |
| `d` | Multiplier (1.0 = no change) |

```python
# +20% speed (multiply by 1.2)
effect.add_command.attribute_modifier_multiply(a=4, b=5, c=-1, d=1.2)

# -10% HP (multiply by 0.9)
effect.add_command.attribute_modifier_multiply(a=4, b=0, c=-1, d=0.9)
```

---

## Resource Modifiers

### `resource_modifier(a, b, c, d)` - Type 1

Modify a resource value.

| Parameter | Description |
|-----------|-------------|
| `a` | Resource ID |
| `d` | Amount to add |

```python
# +500 food
effect.add_command.resource_modifier(a=0, d=500)

# +200 gold
effect.add_command.resource_modifier(a=3, d=200)
```

---

### `resource_modifier_multiply(a, b, c, d)` - Type 6

Multiply a resource value.

| Parameter | Description |
|-----------|-------------|
| `a` | Resource ID |
| `d` | Multiplier |

```python
# Double current gold
effect.add_command.resource_modifier_multiply(a=3, d=2.0)
```

---

## Unit Commands

### `enable_disable_unit(a, b, c, d)` - Type 2

Enable or disable a unit.

| Parameter | Description |
|-----------|-------------|
| `a` | Unit ID |
| `b` | Mode (0=disable, 1=enable) |

```python
# Enable unit 100
effect.add_command.enable_disable_unit(a=100, b=1)

# Disable unit 100
effect.add_command.enable_disable_unit(a=100, b=0)
```

---

### `upgrade_unit(a, b, c, d)` - Type 3

Upgrade one unit to another.

| Parameter | Description |
|-----------|-------------|
| `a` | Source unit ID |
| `b` | Destination unit ID |

```python
# Upgrade Archer (4) to Elite Archer (100)
effect.add_command.upgrade_unit(a=4, b=100)
```

---

### `spawn_unit(a, b, c, d)` - Type 7

Spawn units when effect is applied.

| Parameter | Description |
|-----------|-------------|
| `a` | Unit ID to spawn |
| `b` | Count |

```python
# Spawn 5 militia
effect.add_command.spawn_unit(a=74, b=5)
```

---

## Tech Commands

### `modify_tech(a, b, c, d)` - Type 8

Modify technology parameters.

| Parameter | Description |
|-----------|-------------|
| `a` | Tech ID |
| `b` | Modifier type |
| `c` | Value |
| `d` | Value |

---

## Team Commands (Types 10-18)

Apply to all allies. Same parameters as their non-team equivalents.

| Method | Type | Base Equivalent |
|--------|------|-----------------|
| `team_attribute_modifier_set(...)` | 10 | Type 0 |
| `team_resource_modifier(...)` | 11 | Type 1 |
| `team_enable_disable_unit(...)` | 12 | Type 2 |
| `team_upgrade_unit(...)` | 13 | Type 3 |
| `team_attribute_modifier_add(...)` | 14 | Type 4 |
| `team_attribute_modifier_multiply(...)` | 15 | Type 5 |
| `team_resource_modifier_multiply(...)` | 16 | Type 6 |
| `team_spawn_unit(...)` | 17 | Type 7 |
| `team_modify_tech(...)` | 18 | Type 8 |

```python
# All allies get +1 range on archers
effect.add_command.team_attribute_modifier_add(a=4, b=12, c=-1, d=1)
```

---

## Enemy Commands (Types 20-28)

Apply to all enemies. Same parameters as base equivalents.

| Method | Type | Base Equivalent |
|--------|------|-----------------|
| `enemy_attribute_modifier_set(...)` | 20 | Type 0 |
| `enemy_resource_modifier(...)` | 21 | Type 1 |
| `enemy_enable_disable_unit(...)` | 22 | Type 2 |
| `enemy_upgrade_unit(...)` | 23 | Type 3 |
| `enemy_attribute_modifier_add(...)` | 24 | Type 4 |
| `enemy_attribute_modifier_multiply(...)` | 25 | Type 5 |
| `enemy_resource_modifier_multiply(...)` | 26 | Type 6 |
| `enemy_spawn_unit(...)` | 27 | Type 7 |
| `enemy_modify_tech(...)` | 28 | Type 8 |

```python
# All enemies lose 100 gold
effect.add_command.enemy_resource_modifier(a=3, d=-100)
```

---

## Neutral Commands (Types 30-37)

Apply to neutral units/players.

| Method | Type |
|--------|------|
| `neutral_attribute_modifier_set(...)` | 30 |
| `neutral_resource_modifier(...)` | 31 |
| `neutral_enable_disable_unit(...)` | 32 |
| `neutral_upgrade_unit(...)` | 33 |
| `neutral_attribute_modifier_add(...)` | 34 |
| `neutral_attribute_modifier_multiply(...)` | 35 |
| `neutral_resource_modifier_multiply(...)` | 36 |
| `neutral_spawn_unit(...)` | 37 |

---

## Common Attribute IDs

| ID | Attribute |
|----|-----------|
| 0 | Hit Points |
| 1 | Line of Sight |
| 2 | Garrison Capacity |
| 5 | Movement Speed |
| 8 | Base Armor |
| 9 | Attack |
| 10 | Attack Reload Time |
| 11 | Accuracy Percent |
| 12 | Max Range |
| 13 | Work Rate |
| 14 | Resource Capacity |
| 19 | Train Time |
| 21 | Blast Width |

See [Datasets](../datasets.md) for complete list.

---

## Example: Complete Tech Effect

```python
# Create effect for "Elite Archers" tech
effect_manager = workspace.effect_manager
effect = effect_manager.add_new("Elite Archers Effect")

# +20 HP
effect.add_command.attribute_modifier_add(a=4, b=0, c=-1, d=20)

# +2 attack
effect.add_command.attribute_modifier_add(a=4, b=9, c=-1, d=2)

# +1 range
effect.add_command.attribute_modifier_add(a=4, b=12, c=-1, d=1)

# -0.2 reload time (faster)
effect.add_command.attribute_modifier_add(a=4, b=10, c=-1, d=-0.2)

# Link to tech
tech_manager = workspace.tech_manager
tech = tech_manager.create("Elite Archers")
tech.effect_id = effect.id
tech.research_time = 45
```
