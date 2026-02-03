# Graphic Methods

Complete reference of all methods available on `GraphicManager` and `GraphicHandle`.

---

## GraphicManager Methods

Access via `workspace.graphic_manager`

```python
# First, define the manager
graphic_manager = workspace.graphic_manager
```

### `get(graphic_id)`

Get a graphic by ID.

```python
def get(graphic_id: int) -> GraphicHandle
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `graphic_id` | `int` | The graphic ID |

**Returns:** `GraphicHandle`

**Raises:** `InvalidIdError` if graphic doesn't exist or is None

```python
graphic = graphic_manager.get(100)
print(f"Name: {graphic.name}, Frames: {graphic.frame_count}")
```

---

### `add_graphic(file_name, name=None, graphic_id=None, ...)`

Create a new graphic entry.

```python
def add_graphic(
    file_name: str,
    name: Optional[str] = None,
    graphic_id: Optional[int] = None,
    slp_id: int = -1,
    frame_count: int = 1,
    angle_count: int = 1,
    frame_duration: float = 0.1,
    speed_multiplier: float = 1.0,
    sound_id: int = -1,
    layer: int = 0,
    ...
) -> GraphicHandle
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `file_name` | `str` | Required | SLP/SMX filename |
| `name` | `str` | `None` | Internal name (uses file_name if None) |
| `graphic_id` | `int` | `None` | Target ID. `None` = append |
| `slp_id` | `int` | `-1` | SLP file ID |
| `frame_count` | `int` | `1` | Animation frames |
| `angle_count` | `int` | `1` | Number of angles |
| `frame_duration` | `float` | `0.1` | Duration per frame |
| `speed_multiplier` | `float` | `0.0` | Animation speed (0.0 recommended) |
| `sound_id` | `int` | `-1` | Attached sound |
| `layer` | `int` | `0` | Rendering layer |

**Returns:** `GraphicHandle`

```python
# Simple graphic
graphic = graphic_manager.add_graphic("my_unit.slp")

# Full animation settings
graphic = graphic_manager.add_graphic(
    file_name="hero_attack.slp",
    frame_count=15,
    angle_count=8,
    frame_duration=0.08,
    sound_id=50,
)
```

---

### `copy(source_id, target_id=None)`

Copy a graphic to a new ID.

```python
def copy(source_id: int, target_id: Optional[int] = None) -> GraphicHandle
```

**Returns:** `GraphicHandle`

```python
copied = graphic_manager.copy(100)
print(f"Copied to ID: {copied.id}")
```

---

### `delete(graphic_id)`

Delete a graphic (sets slot to None).

```python
def delete(graphic_id: int) -> bool
```

**Returns:** `True` if deleted

---

### `exists(graphic_id)`

Check if a graphic exists and is not None.

```python
def exists(graphic_id: int) -> bool
```

---

### `count()` / `count_active()`

Get total slots or non-None count.

```python
print(f"Total: {graphic_manager.count()}")
print(f"Active: {graphic_manager.count_active()}")
```

---

### `find_by_name(name)`

Find first graphic matching internal name.

```python
def find_by_name(name: str) -> Optional[GraphicHandle]
```

```python
archer_stand = graphic_manager.find_by_name("ARCHR_STAND")
```

---

### `find_by_file_name(file_name)`

Find first graphic matching SLP/SMX filename.

```python
def find_by_file_name(file_name: str) -> Optional[GraphicHandle]
```

```python
graphic = graphic_manager.find_by_file_name("u_arc_ARCHER.slp")
```

---

### `remove_delta_by_graphic(graphic_id)`

Remove all deltas referencing a specific graphic from ALL graphics.

```python
def remove_delta_by_graphic(graphic_id: int) -> int
```

**Returns:** `int` - Total deltas removed

```python
# Remove all shadow deltas
removed = graphic_manager.remove_delta_by_graphic(200)
print(f"Removed {removed} shadow deltas")
```

---

### Clipboard Operations

```python
graphic_manager.copy_to_clipboard(100)
pasted = graphic_manager.paste()
graphic_manager.clear_clipboard()
```

---

## GraphicHandle Methods

### Delta Methods

#### `add_delta(graphic_id, offset_x=0, offset_y=0, display_angle=-1)`

Add a delta (sub-graphic) to this graphic.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `graphic_id` | `int` | Required | Graphic ID to attach |
| `offset_x` | `int` | `0` | X offset from parent |
| `offset_y` | `int` | `0` | Y offset from parent |
| `display_angle` | `int` | `-1` | Angle filter (-1 = all) |

**Returns:** `DeltaHandle`

```python
delta = graphic.add_delta(
    graphic_id=200,  # Shadow graphic
    offset_x=0,
    offset_y=5,
)
```

---

#### `get_delta(delta_id)`

Get a delta by index.

```python
def get_delta(delta_id: int) -> Optional[DeltaHandle]
```

```python
delta = graphic.get_delta(0)
print(f"Delta graphic: {delta.sprite_id}")
```

---

#### `deltas` Property

Get all deltas as handles.

```python
for delta in graphic.deltas:
    print(f"Delta: {delta.sprite_id} at ({delta.offset_x}, {delta.offset_y})")
```

---

#### `remove_delta(delta_id)`

Remove a delta by index.

```python
def remove_delta(delta_id: int) -> bool
```

```python
graphic.remove_delta(0)  # Remove first delta
```

---

#### `clear_deltas()`

Remove all deltas.

```python
graphic.clear_deltas()
```

---

### Sound Methods

#### `set_attack_sounds(...)`

Set attack sounds for this graphic (deprecated, use `add_angle_sound`).

```python
graphic.set_attack_sounds(
    frame_num_1=5,     # Frame to trigger sound 1
    sound_id_1=50,     # Sound ID
    wwise_sound_id_1=0,
    frame_num_2=10,
    sound_id_2=51,
    ...
)
```

---

#### `add_angle_sound(...)`

Add an angle-specific sound entry with up to 3 sounds per angle.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `frame_num` | `int` | `0` | Frame to trigger sound 1 |
| `sound_id` | `int` | `-1` | Sound ID 1 |
| `wwise_sound_id` | `int` | `0` | Wwise sound ID 1 (DE) |
| `frame_num_2` | `int` | `0` | Frame to trigger sound 2 |
| `sound_id_2` | `int` | `-1` | Sound ID 2 |
| `wwise_sound_id_2` | `int` | `0` | Wwise sound ID 2 (DE) |
| `frame_num_3` | `int` | `0` | Frame to trigger sound 3 |
| `sound_id_3` | `int` | `-1` | Sound ID 3 |
| `wwise_sound_id_3` | `int` | `0` | Wwise sound ID 3 (DE) |

```python
# Add attack sounds for all angles
for i in range(graphic.angle_count):
    graphic.add_angle_sound(
        frame_num=5,
        sound_id=50,
    )
```

---

#### `clear_angle_sounds()`

Remove all angle-specific sounds.

```python
graphic.clear_angle_sounds()
```

---

### `exists()`

Check if this graphic entry exists.

```python
if graphic.exists():
    print(f"Graphic: {graphic.name}")
```

