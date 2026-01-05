# Graphic Deltas

Deltas are sub-graphics attached to a parent graphic. They're used for:
- **Shadows** – Rendered below the unit
- **Weapon effects** – Sword swing trails, arrow flash
- **Attachments** – Shields, flags, carried items
- **Damage states** – Fire, smoke overlays

---

## How Deltas Work

A delta references another graphic ID and positions it relative to the parent:

```
Parent Graphic (hero_idle.slp)
    └── Delta 0: shadow.slp at offset (0, 5)
    └── Delta 1: shield.slp at offset (-3, -2)
    └── Delta 2: flag.slp at offset (2, -8)
```

Each delta has:
- `graphic_id` – The referenced graphic
- `offset_x`, `offset_y` – Position relative to parent
- `display_angle` – Which angles to show (-1 = all)

---

## DeltaHandle

When you add or get a delta, you receive a `DeltaHandle`:

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `delta_id` | `int` | Index in parent's deltas list |
| `graphic_id` | `int` | Referenced graphic ID |
| `offset_x` | `int` | X offset from parent |
| `offset_y` | `int` | Y offset from parent |
| `display_angle` | `int` | Angle filter (-1 = all) |

---

## Adding Deltas

### Basic Delta

```python
gfx = gm.get(100)

# Add a shadow
delta = gfx.add_delta(graphic_id=200)
print(f"Delta index: {delta.delta_id}")
```

### With Offset

```python
# Shadow slightly below and behind
delta = gfx.add_delta(
    graphic_id=200,
    offset_x=0,
    offset_y=5,  # Below parent
)
```

### With Angle Filter

```python
# Only show for front-facing angles
delta = gfx.add_delta(
    graphic_id=300,
    offset_x=-5,
    offset_y=0,
    display_angle=0,  # Only angle 0
)

# Show for all angles
delta = gfx.add_delta(
    graphic_id=300,
    display_angle=-1,  # All angles
)
```

---

## Modifying Deltas

### Via DeltaHandle

```python
# Add delta
delta = gfx.add_delta(graphic_id=200)

# Modify position
delta.offset_x = 2
delta.offset_y = 4

# Change referenced graphic
delta.graphic_id = 201

# Change angle
delta.display_angle = 2
```

### Via Index

```python
# Get existing delta
delta = gfx.get_delta(0)
if delta:
    delta.offset_y += 2
```

---

## Removing Deltas

### By Index

```python
# Remove first delta
gfx.remove_delta(delta_id=0)

# Check result
success = gfx.remove_delta(delta_id=5)
if not success:
    print("Delta not found")
```

### By Graphic ID

Remove all deltas referencing a specific graphic:

```python
# Remove all shadow deltas
gfx.remove_delta_by_graphic(graphic_id=200)
```

### Clear All

```python
gfx.clear_deltas()
```

---

## Listing Deltas

### Iterate All

```python
for i, delta in enumerate(gfx.deltas):
    print(f"Delta {i}:")
    print(f"  Graphic: {delta.graphic_id}")
    print(f"  Offset: ({delta.offset_x}, {delta.offset_y})")
    print(f"  Angle: {delta.display_angle}")
```

### Count Deltas

```python
print(f"Total deltas: {len(gfx.deltas)}")
```

---

## Common Patterns

### Adding Shadow

```python
def add_shadow_to_graphic(gm, parent_id, shadow_id, y_offset=5):
    """Add a shadow delta to a graphic."""
    parent = gm.get(parent_id)
    if parent.exists():
        parent.add_delta(
            graphic_id=shadow_id,
            offset_x=0,
            offset_y=y_offset,
            display_angle=-1,
        )
        return True
    return False

# Usage
add_shadow_to_graphic(gm, parent_id=100, shadow_id=200)
```

### Copying Deltas

```python
def copy_deltas(source_gfx, target_gfx):
    """Copy all deltas from source to target."""
    for delta in source_gfx.deltas:
        target_gfx.add_delta(
            graphic_id=delta.graphic_id,
            offset_x=delta.offset_x,
            offset_y=delta.offset_y,
            display_angle=delta.display_angle,
        )

# Usage
archer_gfx = gm.get(100)  # Has deltas
hero_gfx = gm.get(1000)   # Empty
copy_deltas(archer_gfx, hero_gfx)
```

### Replacing a Delta Graphic

```python
def replace_delta_graphic(gfx, old_id, new_id):
    """Replace all deltas pointing to old_id with new_id."""
    for delta in gfx.deltas:
        if delta.graphic_id == old_id:
            delta.graphic_id = new_id

# Usage
replace_delta_graphic(gfx, old_id=200, new_id=201)
```

### Adjusting All Delta Offsets

```python
def shift_all_deltas(gfx, dx, dy):
    """Shift all deltas by dx, dy."""
    for delta in gfx.deltas:
        delta.offset_x += dx
        delta.offset_y += dy

# Usage
shift_all_deltas(gfx, dx=0, dy=2)  # Move all down
```

---

## Via GraphicManager

You can also manage deltas through the manager:

```python
# Add delta
gm.add_graphic_delta(
    graphic_id=100,       # Parent
    delta_graphic_id=200, # Delta
    offset_x=0,
    offset_y=5,
)

# Remove delta
gm.remove_graphic_delta(
    graphic_id=100,
    delta_id=0,
)
```

---

## Complete Example: Unit with Full Delta Setup

```python
from Actual_Tools import GenieWorkspace

workspace = GenieWorkspace.load("empires2_x2_p1.dat")
gm = workspace.graphic_manager()
um = workspace.genie_unit_manager()

# Find reference graphics
shadow = gm.find_by_name("SHADOW_CAVALRY")
flame = gm.find_by_name("FLAME_EFFECT")

# Create hero graphics
idle = gm.add_graphic("hero_idle.slp", frame_count=10, angle_count=8)
walk = gm.add_graphic("hero_walk.slp", frame_count=15, angle_count=8)
attack = gm.add_graphic("hero_attack.slp", frame_count=12, angle_count=8)

# Add shadow to all graphics
for gfx in [idle, walk, attack]:
    if shadow:
        gfx.add_delta(
            graphic_id=shadow.id,
            offset_x=0,
            offset_y=4,
        )
        print(f"Added shadow to graphic {gfx.id}")

# Add flame effect to attack (front angles only)
if flame:
    for angle in [0, 1, 7]:  # Front-ish angles
        d = attack.add_delta(
            graphic_id=flame.id,
            offset_x=-8 if angle == 7 else (8 if angle == 1 else 0),
            offset_y=-5,
            display_angle=angle,
        )
        print(f"Added flame for angle {angle}")

# Verify deltas
print(f"\nIdle deltas: {len(idle.deltas)}")
print(f"Walk deltas: {len(walk.deltas)}")
print(f"Attack deltas: {len(attack.deltas)}")

# Create unit with these graphics
hero = um.create("Flame Knight", base_unit_id=38)
hero.standing_graphic = idle.id
hero.dead_fish.walking_graphic = walk.id
hero.combat.attack_graphic = attack.id

workspace.save("output.dat")
print(f"\nCreated hero at ID {hero.id}")
```

---

## Delta Rendering Order

Deltas are rendered in list order:
1. First delta = rendered first (behind)
2. Last delta = rendered last (on top)

```python
# Add shadow first (behind)
gfx.add_delta(graphic_id=shadow_id, offset_y=5)

# Add flame last (on top)
gfx.add_delta(graphic_id=flame_id, offset_x=0, offset_y=-10)
```

To reorder, clear and re-add in desired order:

```python
# Store current deltas
deltas_data = [
    (d.graphic_id, d.offset_x, d.offset_y, d.display_angle)
    for d in gfx.deltas
]

# Clear
gfx.clear_deltas()

# Re-add in new order (reversed)
for gid, ox, oy, angle in reversed(deltas_data):
    gfx.add_delta(graphic_id=gid, offset_x=ox, offset_y=oy, display_angle=angle)
```
