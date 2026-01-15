# Graphics

The Graphics module manages sprites and animations used for unit visuals, buildings, and effects.

## Quick Example

```python
from Actual_Tools_GDP import GenieWorkspace

workspace = GenieWorkspace.load("empires2_x2_p1.dat")

# Get the graphic manager
graphic_manager = workspace.graphic_manager

# Get an existing graphic
graphic = graphic_manager.get(100)
print(f"Frames: {graphic.frame_count}, Angles: {graphic.angle_count}")

# Create a new graphic
attack_anim = graphic_manager.add_graphic(
    file_name="hero_attack.slp",
    frame_count=15,
    angle_count=8,
)
```

---

## Sub-Pages

| Page | Description |
|------|-------------|
| [Methods](graphics/methods.md) | All GraphicManager and GraphicHandle methods |
| [Attributes](graphics/attributes.md) | Complete attribute reference table |
| [Deltas](graphics/deltas.md) | Sub-graphics and layered effects |

---

## Overview

### GraphicManager (`workspace.graphic_manager`)

The manager handles graphic CRUD operations:

| Method | Description |
|--------|-------------|
| `get(graphic_id)` | Get a GraphicHandle |
| `add_graphic(file_name)` | Create a new graphic |
| `copy(source_id)` | Copy a graphic |
| `delete(graphic_id)` | Delete a graphic |
| `exists(graphic_id)` | Check if graphic exists |
| `find_by_name(name)` | Find by internal name |
| `find_by_file_name(file_name)` | Find by SLP filename |

### GraphicHandle

The handle provides attribute access and delta management:

**Key Attributes:**
- `name`, `file_name`, `slp_id`
- `frame_count`, `angle_count`, `frame_duration`
- `sound_id`, `layer`

**Collections:**
- `deltas` - Attached sub-graphics

---

## Creating Graphics

```python
graphic_manager = workspace.graphic_manager

# Simple graphic
graphic = graphic_manager.add_graphic("my_unit.slp")

# Full animation
graphic = graphic_manager.add_graphic(
    file_name="hero_attack.slp",
    frame_count=15,
    angle_count=8,
    frame_duration=0.08,
    sound_id=50,
)
```

---

## Modifying Graphics

```python
graphic = graphic_manager.get(100)

# Animation settings
graphic.frame_count = 20
graphic.angle_count = 8
graphic.frame_duration = 0.1

# Audio
graphic.sound_id = 100
```

See [Attributes](graphics/attributes.md) for all properties.

---

## Working with Deltas

Deltas are sub-graphics (shadows, flames, effects):

```python
# Add a shadow
shadow = graphic_manager.get(200)
graphic.add_delta(graphic_id=shadow.id, offset_y=5)

# List all deltas
for delta in graphic.deltas:
    print(f"Delta: {delta.sprite_id}")
```

See [Deltas](graphics/deltas.md) for details.

---

## Assigning to Units

Graphics are assigned to units via their IDs:

```python
unit_manager = workspace.unit_manager
unit = unit_manager.get(4)

# Standing graphics
unit.standing_graphic_1 = graphic.id

# Attack graphic
unit.attack_graphic = attack_animation.id

# Walking graphic
unit.walking_graphic = walking_animation.id
```
