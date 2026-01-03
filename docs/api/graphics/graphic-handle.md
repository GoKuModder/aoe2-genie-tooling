# GraphicHandle

The `GraphicHandle` class provides direct access to graphic properties. Unlike `UnitHandle`, graphics don't have civ-specific versions.

## Constructor

```python
GraphicHandle(graphic_id: int, dat_file: DatFile)
```

!!! note
    Use `GraphicManager.get()` or `.add_graphic()` instead of creating directly.

---

## Basic Properties

```python
gm = workspace.graphic_manager()
gfx = gm.get(100)

# Check existence first
if gfx.exists():
    print(f"ID: {gfx.id}")
    print(f"Name: {gfx.name}")
    print(f"File: {gfx.file_name}")
```

### Core Properties

| Property | Type | Description |
|----------|------|-------------|
| `id` | `int` | Graphic ID (read-only) |
| `name` | `str` | Internal name |
| `file_name` | `str` | SLP/SMX file name |
| `slp` | `int` | SLP resource ID |

### Animation Properties

| Property | Type | Description |
|----------|------|-------------|
| `frame_count` | `int` | Number of frames |
| `angle_count` | `int` | Number of angles/facings |
| `frame_duration` | `float` | Duration per frame (seconds) |
| `speed_multiplier` | `float` | Animation speed multiplier |
| `replay_delay` | `float` | Delay before replay |
| `sequence_type` | `int` | Sequence type |
| `mirroring_mode` | `int` | Mirroring mode |

### Sound Properties

| Property | Type | Description |
|----------|------|-------------|
| `sound_id` | `int` | Associated sound ID |
| `wwise_sound_id` | `int` | Wwise sound ID |
| `angle_sounds_used` | `int` | Whether angle sounds active |

### Visual Properties

| Property | Type | Description |
|----------|------|-------------|
| `layer` | `int` | Render layer |
| `player_color` | `int` | Player color index |
| `transparent_selection` | `int` | Transparent selection flag |
| `coordinates` | `tuple` | Bounding box (x1, y1, x2, y2) |
| `editor_flag` | `int` | Editor display flag |

### Effects

| Property | Type | Description |
|----------|------|-------------|
| `particle_effect_name` | `str` | Particle effect |

---

## Example: Modifying Properties

```python
gm = workspace.graphic_manager()
gfx = gm.get(100)

# Animation speed
gfx.frame_count = 20
gfx.frame_duration = 0.06  # Faster
gfx.speed_multiplier = 1.5

# Add sound
gfx.sound_id = 50

# Rendering
gfx.layer = 10
gfx.player_color = 1  # Red
```

---

## Deltas (Sub-Graphics)

Deltas are child graphics attached to a parent (e.g., shadows, weapons).

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `deltas` | `List[GraphicDelta]` | List of deltas |

### Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `add_delta(...)` | `DeltaHandle` | Add a delta |
| `get_delta(delta_id)` | `DeltaHandle` | Get by index |
| `remove_delta(delta_id)` | `bool` | Remove by index |
| `remove_delta_by_graphic(gfx_id)` | `bool` | Remove by graphic ID |
| `clear_deltas()` | `None` | Remove all deltas |

### Example

```python
# Get graphic
gfx = gm.get(100)

# Add shadow delta
shadow = gfx.add_delta(
    graphic_id=200,  # Shadow graphic
    offset_x=0,
    offset_y=5,
    display_angle=-1,  # All angles
)
print(f"Added delta at index {shadow.delta_id}")

# Modify delta
shadow.offset_y = 3

# List all deltas
for delta in gfx.deltas:
    print(f"Delta: graphic={delta.graphic_id}, offset=({delta.offset_x}, {delta.offset_y})")
```

See [Deltas](deltas.md) for complete delta documentation.

---

## Angle Sounds

Per-angle sound triggers for directional audio.

### Methods

| Method | Description |
|--------|-------------|
| `add_angle_sound(...)` | Add angle sound entry |
| `clear_angle_sounds()` | Remove all |

### Example

```python
# Add angle sound
gfx.add_angle_sound(
    frame_num=5,
    sound_id=100,
)

# Clear all
gfx.clear_angle_sounds()
```

---

## Complete Example

```python
from Actual_Tools import GenieWorkspace

workspace = GenieWorkspace.load("empires2_x2_p1.dat")
gm = workspace.graphic_manager()

# Create attack animation
attack = gm.add_graphic(
    file_name="hero_attack.slp",
    frame_count=15,
    angle_count=8,
)

# Configure animation
attack.frame_duration = 0.07
attack.speed_multiplier = 1.2
attack.replay_delay = 0.0

# Add sound
attack.sound_id = 50
attack.wwise_sound_id = 12345

# Add shadow delta
shadow = gm.find_by_name("SHADOW_CAVALRY")
if shadow:
    delta = attack.add_delta(
        graphic_id=shadow.id,
        offset_x=0,
        offset_y=3,
    )
    print(f"Added shadow at delta index {delta.delta_id}")

# Add weapon flash delta
flash = gm.find_by_name("WEAPON_FLASH")
if flash:
    attack.add_delta(
        graphic_id=flash.id,
        offset_x=-5,
        offset_y=-10,
        display_angle=0,  # Only front-facing
    )

# Print summary
print(f"Graphic {attack.id}:")
print(f"  File: {attack.file_name}")
print(f"  Frames: {attack.frame_count} @ {attack.frame_duration}s")
print(f"  Deltas: {len(attack.deltas)}")

workspace.save("output.dat")
```
