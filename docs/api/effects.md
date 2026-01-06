# Effects API

The Effects API provides control over effect entries (TechEffects) in AoE2 DAT files.

Effects follow a two-tier structure:
1. **Effect Holder**: A slot in the "mega-list" with a name (e.g., effect ID 100).
2. **Effect Commands**: A list of one or more commands inside that holder (e.g., modify attack, enable unit).

## Quick Example

```python
em = workspace.effect_manager

# 1. Create a holder (slot)
holder = em.add_new(name="Upgrade Archer")

# 2. Add effect commands to the holder
holder.new_command(type=5, a=4, b=10, d=2.0)  # Modify attribute
holder.new_command(type=1, a=100)               # Enable unit

# 3. Link effect to a technology
tech.effect_id = holder.id
```

## EffectManager Methods

| Method | Description |
|--------|-------------|
| `add_new(name, ...)` | Create a new effect holder |
| `get(effect_id)` | Get effect holder by ID |
| `exists(effect_id)` | Check if effect exists |
| `count()` | Total effect slots |
| `find_by_name(name)` | Find holder by name |
| `copy(source_id, target_id)` | Copy effect to new ID |
| `copy_to_clipboard(id)` | Copy holder to clipboard |
| `paste(target_id)` | Paste from clipboard |
| `delete(effect_id)` | Reset slot to blank |

## EffectHolder (`EffectHandle`) Methods

| Method | Description |
|--------|-------------|
| `name` (property) | Effect name |
| `commands` (property) | List of commands in holder |
| `new_command(type, a, b, c, d)` | Add a new command |
| `get_command(index)` | Get command by index |
| `copy_command(index, target)` | Duplicate command |
| `move_command(src, dst)` | Reorder commands |
| `remove_command(index)` | Delete command |
| `clear_commands()` | Remove all commands |

## CommandHandle Properties

| Property | Type | Description |
|----------|------|-------------|
| `type` | `int` | Command type ID |
| `a` | `int` | Parameter A (unit/class/attribute) |
| `b` | `int` | Parameter B (value/amount) |
| `c` | `int` | Parameter C (civ/class) |
| `d` | `float` | Parameter D (float) |
