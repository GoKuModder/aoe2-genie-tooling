# Graphic Deltas

Deltas are sub-graphics attached to a parent graphic. Common uses include shadows, flames, and layered effects.

## Overview

A delta is an attachment that:
- References another graphic ID
- Has X/Y offset from parent
- Can be filtered by angle
- Renders relative to the parent

---

## Adding Deltas

### `add_delta(graphic_id, offset_x=0, offset_y=0, display_angle=-1)`

Add a new delta to a graphic.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `graphic_id` | `int` | Required | Graphic ID to attach |
| `offset_x` | `int` | `0` | X offset from parent |
| `offset_y` | `int` | `0` | Y offset from parent |
| `display_angle` | `int` | `-1` | Angle filter (-1 = show for all angles) |

**Returns:** `DeltaHandle`

```python
graphic_manager = workspace.graphic_manager
graphic = graphic_manager.get(100)

# Add a shadow delta
shadow_graphic = graphic_manager.get(200)
delta = graphic.add_delta(
    graphic_id=shadow_graphic.id,
    offset_x=0,
    offset_y=5,
)

# Add a flame effect
flame = workspace.graphic_manager.add_graphic("flame.slp")
graphic.add_delta(
    graphic_id=flame.id,
    offset_x=10,
    offset_y=-20,
)
```

---

## Getting Deltas

### `get_delta(delta_id)`

Get a delta by index.

**Returns:** `DeltaHandle` or `None`

```python
delta = graphic.get_delta(0)
if delta:
    print(f"Delta graphic: {delta.sprite_id}")
    print(f"Offset: ({delta.offset_x}, {delta.offset_y})")
```

---

### `deltas` Property

Get all deltas as a list of handles.

```python
for i, delta in enumerate(graphic.deltas):
    print(f"Delta {i}: graphic={delta.sprite_id}, pos=({delta.offset_x}, {delta.offset_y})")
```

---

## Modifying Deltas

Use the handle to modify properties:

```python
delta = graphic.get_delta(0)

# Change position
delta.offset_x = 5
delta.offset_y = -10

# Change referenced graphic
delta.sprite_id = 300

# Change angle filter
delta.display_angle = 3  # Only show for angle 3
```

---

## Removing Deltas

### `remove_delta(delta_id)`

Remove a delta by index.

| Parameter | Type | Description |
|-----------|------|-------------|
| `delta_id` | `int` | Index of delta to remove |

**Returns:** `bool`

```python
graphic.remove_delta(0)  # Remove first delta
```

---

### `clear_deltas()`

Remove all deltas from a graphic.

```python
graphic.clear_deltas()
```

---

### Manager: `remove_delta_by_graphic(graphic_id)`

Remove all deltas that reference a specific graphic from ALL graphics.

```python
# Remove all references to shadow graphic (ID 200)
graphic_manager = workspace.graphic_manager
removed = graphic_manager.remove_delta_by_graphic(200)
print(f"Removed {removed} shadow deltas from all graphics")
```

This is useful when deleting a graphic to ensure no dangling references.

---

## DeltaHandle Properties

| Property | Type | R/W | Description |
|----------|------|-----|-------------|
| `sprite_id` | `int` | RW | Referenced graphic ID |
| `offset_x` | `int` | RW | X offset from parent |
| `offset_y` | `int` | RW | Y offset from parent |
| `display_angle` | `int` | RW | Angle filter (-1 = all) |

---

## Common Delta Uses

### Shadows

```python
# Add shadow to unit graphic
graphic_manager = workspace.graphic_manager
shadow = graphic_manager.find_by_name("UNIT_SHADOW")
unit_graphic.add_delta(
    graphic_id=shadow.id,
    offset_x=0,
    offset_y=3,  # Shadow slightly below
)
```

### Fire/Flames

```python
# Add fire to damaged building
graphic_manager = workspace.graphic_manager
fire = graphic_manager.find_by_name("BUILDING_FIRE")
building_graphic.add_delta(
    graphic_id=fire.id,
    offset_x=15,
    offset_y=-30,  # Above building
)
```

### Layered Effects

```python
# Add glow effect
graphic_manager = workspace.graphic_manager
glow = graphic_manager.add_graphic("hero_glow.slp")
hero_graphic.add_delta(
    graphic_id=glow.id,
    offset_x=0,
    offset_y=0,
)
```

---

## Angle-Specific Deltas

Use `display_angle` to show deltas only for certain facing directions:

```python
# Shield only visible from front angles
for angle in [0, 1, 7]:  # Front-facing angles
    graphic.add_delta(
        graphic_id=shield_graphic.id,
        offset_x=5,
        offset_y=0,
        display_angle=angle,
    )
```

**Note:** Angle -1 means "show for all angles".

---

## Example: Create Composite Graphic

```python
# Main unit graphic
graphic_manager = workspace.graphic_manager
main = graphic_manager.add_graphic(
    file_name="hero_idle.slp",
    frame_count=10,
    angle_count=8,
)

# Add shadow
shadow = graphic_manager.find_by_name("UNIT_SHADOW")
main.add_delta(graphic_id=shadow.id, offset_y=3)

# Add weapon overlay
weapon = graphic_manager.add_graphic("hero_weapon.slp")
main.add_delta(graphic_id=weapon.id, offset_x=5, offset_y=-10)

# Add glow effect
glow = graphic_manager.add_graphic("hero_glow.slp")
main.add_delta(graphic_id=glow.id)

# Verify
print(f"Created graphic with {len(main.deltas)} deltas")
```

---

## Coordinate System

Offsets use the isometric coordinate system:
- **Positive X** = Right
- **Negative X** = Left
- **Positive Y** = Down (toward viewer)
- **Negative Y** = Up (away from viewer)

```
     -Y (up)
       |
-X ----+---- +X
       |
     +Y (down)
```
