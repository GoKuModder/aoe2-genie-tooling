# Graphic Attributes

Complete reference of all attributes available on `GraphicHandle`.

## Core Attributes

| Attribute | Type | R/W | Description |
|-----------|------|-----|-------------|
| `id` | `int` | R | Graphic ID (read-only) |
| `name` | `str` | RW | Internal name |
| `file_name` | `str` | RW | SLP/SMX filename |
| `slp_id` | `int` | RW | SLP file ID |

### Usage

```python
graphic = workspace.graphic_manager.get(100)

# Read
print(f"ID: {graphic.id}")
print(f"Name: {graphic.name}")
print(f"File: {graphic.file_name}")

# Write
graphic.name = "CUSTOM_GRAPHIC"
graphic.file_name = "custom.slp"
```

---

## Animation Attributes

| Attribute | Type | R/W | Description |
|-----------|------|-----|-------------|
| `frame_count` | `int` | RW | Number of animation frames |
| `angle_count` | `int` | RW | Number of angles/facets |
| `frame_duration` | `float` | RW | Duration per frame (seconds) |
| `animation_duration` | `float` | RW | Total animation time (auto-calculates frame_rate) |
| `speed_multiplier` | `float` | RW | Animation speed multiplier (use 0.0 for static) |
| `replay_delay` | `float` | RW | Delay before replay |
| `first_frame` | `int` | RW | Starting frame index |
| `sequence_type` | `int` | RW | Animation sequence type |

### Aliases

Some attributes have alternate names for convenience:

| Alias | Original |
|-------|----------|
| `frame_count` | `num_frames` |
| `angle_count` | `num_facets` |
| `frame_duration` | `frame_rate` |
| `speed_multiplier` | `speed_mult` |

### Usage

```python
# Animation configuration
graphic.frame_count = 15
graphic.angle_count = 8
graphic.frame_duration = 0.08  # 80ms per frame
graphic.speed_multiplier = 0.0  # Recommended: 0.0 for static graphics

# Alternative: Set total animation time (auto-calculates frame_duration)
graphic.animation_duration = 1.2  # 1.2 seconds total
# Internally: frame_duration = 1.2 / 15 = 0.08 seconds
```

---

## Rendering Attributes

| Attribute | Type | R/W | Description |
|-----------|------|-----|-------------|
| `layer` | `int` | RW | Rendering layer |
| `player_color` | `int` | RW | Force player color ID (-1 = use default) |
| `transparent_selection` | `int` | RW | Transparent pick mode |
| `mirroring_mode` | `int` | RW | Angle mirroring behavior |
| `rainbow` | `int` | RW | Rainbow mode (DE) |
| `editor_flag` | `int` | RW | Editor mode flags |

### Coordinates (Bounding Box)

| Attribute | Type | R/W | Description |
|-----------|------|-----|-------------|
| `coordinates` | `tuple` | RW | Bounding box (X1, Y1, X2, Y2) |

```python
# Set bounding box
graphic.coordinates = (0, 0, 64, 64)

# Read
x1, y1, x2, y2 = graphic.coordinates
```

---

## Audio Attributes

| Attribute | Type | R/W | Description |
|-----------|------|-----|-------------|
| `sound_id` | `int` | RW | Attached sound ID |
| `wwise_sound_id` | `int` | RW | Wwise sound ID (DE) |
| `angle_sounds_used` | `bool` | RW | Per-angle attack sounds |

### Usage

```python
graphic.sound_id = 50
graphic.angle_sounds_used = True
```

---

## Attack Sounds

Graphics can have up to 3 attack sounds triggered at specific frames:

| Property | Description |
|----------|-------------|
| `attack_sound_1` | First attack sound |
| `attack_sound_2` | Second attack sound |
| `attack_sound_3` | Third attack sound |

Use `set_attack_sounds()` method to configure all at once.

---

## Delta Attributes

Deltas are accessed via methods. See [Deltas](deltas.md).

```python
# Get all deltas
for delta in graphic.deltas:
    print(f"Delta: {delta.sprite_id}")
```

---

## Common Graphic Types

| Layer | Typical Use |
|-------|-------------|
| 0 | Default |
| 5 | Terrain |
| 10 | Shadows |
| 20 | Units |
| 30 | Buildings |
| 40 | Effects/Projectiles |

---

## Example: Configure Animation

```python
# Get or create graphic
graphic = workspace.graphic_manager.add_graphic("hero_walk.slp")

# Animation setup
graphic.frame_count = 10
graphic.angle_count = 8
graphic.frame_duration = 0.1  # 100ms per frame
graphic.speed_multiplier = 1.0

# Rendering
graphic.layer = 20  # Unit layer
graphic.player_color = -1  # Use player's color

# Sound
graphic.sound_id = 100  # Walking sound
```

---

## Example: Mirror Graphics

Mirroring reduces file size by reusing frames:

```python
# Enable mirroring (uses half the angles, mirrors the rest)
graphic.mirroring_mode = 1
graphic.angle_count = 8  # Only need 5, game mirrors for 8
```

---

## Version-Specific Attributes

Some attributes are only available in certain game versions:

| Attribute | Version |
|-----------|---------|
| `wwise_sound_id` | DE only |
| `rainbow` | DE only |
| `old_sound_id` | Pre-DE |
