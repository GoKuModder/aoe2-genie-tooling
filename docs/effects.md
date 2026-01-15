# Effects

The Effects module manages technology effects - the actual game modifications that happen when a technology is researched.

## Quick Example

```python
from Actual_Tools_GDP import GenieWorkspace

workspace = GenieWorkspace.load("empires2_x2_p1.dat")

# Get the effect manager
effect_manager = workspace.effect_manager

# Get an existing effect
effect = effect_manager.get(100)

# Create a new effect
new_effect = effect_manager.add_new("Archer Upgrade")
new_effect.add_command.attribute_modifier_add(a=4, b=0, c=-1, d=10)
```

---

## Sub-Pages

| Page | Description |
|------|-------------|
| [Methods](effects/methods.md) | All EffectManager and EffectHandle methods |
| [Effect Commands](effects/effect-commands.md) | Complete command type reference |

---

## Overview

### EffectManager (`workspace.effect_manager`)

The manager handles effect CRUD operations:

| Method | Description |
|--------|-------------|
| `get(effect_id)` | Get an EffectHandle |
| `add_new(name)` | Create a new effect |
| `copy(source_id)` | Copy an effect |
| `delete(effect_id)` | Delete an effect |
| `exists(effect_id)` | Check if effect exists |
| `find_by_name(name)` | Find by name |
| `count()` | Total effect slots |

### EffectHandle

The handle provides access to a single effect:

**Properties:**
- `id` - Effect ID
- `name` - Effect name
- `commands` - List of commands

**Methods:**
- `add_command` - Fluent command builder
- `new_command(type, a, b, c, d)` - Raw command creation
- `get_command(index)` - Get command by index

---

## Effect Structure

Effects follow a two-tier structure:

1. **Effect Holder** - A named container
2. **Effect Commands** - The actual modifications inside

```
Effect (ID: 100, Name: "Fletching")
├── Command 1: +1 range for archers
├── Command 2: +1 attack for archers
└── Command 3: +1 LoS for archers
```

---

## Creating Effects

```python
effect_manager = workspace.effect_manager

# Create a new effect
effect = effect_manager.add_new("My Upgrade Effect")

# Add commands using the builder
effect.add_command.attribute_modifier_add(a=4, b=0, c=-1, d=10)  # +10 HP
effect.add_command.attribute_modifier_add(a=4, b=9, c=-1, d=2)   # +2 attack

# Or using raw parameters
effect.new_command(type=4, a=4, b=12, c=-1, d=1)  # +1 range
```

---

## Linking Effects to Techs

Effects don't do anything until linked to a technology:

```python
# Create the effect
effect = effect_manager.add_new("Elite Upgrade")
effect.add_command.attribute_modifier_add(a=4, b=0, c=-1, d=20)

# Create the tech and link
tech_manager = workspace.tech_manager
tech = tech_manager.create("Elite Research")
tech.effect_id = effect.id
tech.research_time = 45
```

See [Techs](techs.md) for technology configuration.

---

## Command Types Summary

| Type | Method | Description |
|------|--------|-------------|
| 0 | `attribute_modifier_set` | Set attribute to value |
| 1 | `resource_modifier` | Add to resource |
| 2 | `enable_disable_unit` | Enable/disable unit |
| 3 | `upgrade_unit` | Upgrade unit A → B |
| 4 | `attribute_modifier_add` | Add to attribute |
| 5 | `attribute_modifier_multiply` | Multiply attribute |
| 6 | `resource_modifier_multiply` | Multiply resource |
| 7 | `spawn_unit` | Spawn units |
| 10-18 | `team_*` | Team versions |
| 20-28 | `enemy_*` | Enemy versions |

See [Effect Commands](effects/effect-commands.md) for complete details.

---

## Managing Commands

```python
# List all commands
for cmd in effect.commands:
    print(f"Type {cmd.type}: a={cmd.a}, d={cmd.d}")

# Get specific command
cmd = effect.get_command(0)
cmd.d = 20  # Modify value

# Remove command
effect.remove_command(0)

# Clear all
effect.clear_commands()
```
