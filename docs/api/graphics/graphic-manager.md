# GraphicManager

The `GraphicManager` class handles graphic CRUD operations: create, copy, delete, and search.

## Getting the Manager

```python
from Actual_Tools import GenieWorkspace

workspace = GenieWorkspace.load("empires2_x2_p1.dat")
gm = workspace.graphic_manager()
```

---

## Methods

### add_graphic()

Create a new graphic entry.

```python
def add_graphic(
    file_name: str,
    name: Optional[str] = None,
    graphic_id: Optional[int] = None,
    frame_count: int = 1,
    angle_count: int = 1,
    frame_duration: float = 0.1,
    speed_multiplier: float = 1.0,
) -> GraphicHandle
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `file_name` | `str` | SLP/SMX file name |
| `name` | `str` | Internal name. `None` = use file_name |
| `graphic_id` | `int` | Target ID. `None` = auto-assign |
| `frame_count` | `int` | Number of animation frames |
| `angle_count` | `int` | Number of angles/facings |
| `frame_duration` | `float` | Duration per frame (seconds) |
| `speed_multiplier` | `float` | Animation speed |

#### Examples

```python
# Basic creation
gfx = gm.add_graphic("my_unit.slp")
print(f"ID: {gfx.id}")

# With animation settings
attack_gfx = gm.add_graphic(
    file_name="hero_attack.slp",
    frame_count=15,
    angle_count=8,
    frame_duration=0.08,
)

# At specific ID
gm.add_graphic("custom.slp", graphic_id=20000)
```

---

### get()

Get a handle for an existing graphic.

```python
def get(graphic_id: int) -> GraphicHandle
```

!!! note
    Returns a handle even if the graphic doesn't exist. Check `.exists()` to verify.

#### Example

```python
gfx = gm.get(100)
if gfx.exists():
    print(f"Name: {gfx.name}")
    print(f"Frames: {gfx.frame_count}")
```

---

### copy()

Copy a graphic to a new ID.

```python
def copy(source_id: int, target_id: Optional[int] = None) -> GraphicHandle
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `source_id` | `int` | ID of graphic to copy |
| `target_id` | `int` | Destination ID. `None` = auto-assign |

#### Example

```python
# Copy to auto-assigned ID
copied = gm.copy(source_id=100)
print(f"Copied to ID {copied.id}")

# Copy to specific ID
gm.copy(source_id=100, target_id=5000)
```

---

### delete()

Delete a graphic (sets slot to `None`).

```python
def delete(graphic_id: int) -> bool
```

#### Example

```python
if gm.delete(5000):
    print("Deleted successfully")
else:
    print("Graphic didn't exist")
```

---

### exists()

Check if a graphic ID exists and is not `None`.

```python
def exists(graphic_id: int) -> bool
```

#### Example

```python
if gm.exists(100):
    gfx = gm.get(100)
```

---

### find_by_name()

Find first graphic matching name.

```python
def find_by_name(name: str) -> Optional[GraphicHandle]
```

#### Example

```python
gfx = gm.find_by_name("ARCHER_ATTACK")
if gfx:
    print(f"Found at ID {gfx.id}")
```

---

### find_by_file_name()

Find first graphic matching file name.

```python
def find_by_file_name(file_name: str) -> Optional[GraphicHandle]
```

#### Example

```python
gfx = gm.find_by_file_name("archer_attack.slp")
if gfx:
    print(f"Found at ID {gfx.id}")
```

---

### count() / count_active()

Get total slots and active (non-None) count.

```python
def count() -> int      # Total slots
def count_active() -> int  # Non-None slots
```

#### Example

```python
print(f"Total: {gm.count()}, Active: {gm.count_active()}")
```

---

## Clipboard Operations

### copy_to_clipboard()

Copy a graphic to internal clipboard.

```python
def copy_to_clipboard(graphic_id: int) -> bool
```

### paste()

Paste from clipboard to new ID.

```python
def paste(target_id: Optional[int] = None) -> Optional[GraphicHandle]
```

### clear_clipboard()

Clear the internal clipboard.

```python
def clear_clipboard() -> None
```

#### Example

```python
# Copy archer attack to clipboard
gm.copy_to_clipboard(100)

# Paste multiple times
for i in range(5):
    pasted = gm.paste()
    print(f"Pasted to ID {pasted.id}")

# Clean up
gm.clear_clipboard()
```

---

## Delta Management via Manager

You can also add/remove deltas through the manager:

```python
# Add delta to graphic 100
gm.add_graphic_delta(
    graphic_id=100,
    delta_graphic_id=200,  # Shadow
    offset_x=0,
    offset_y=5,
)

# Remove delta by index
gm.remove_graphic_delta(graphic_id=100, delta_id=0)
```

---

## Complete Example

```python
from Actual_Tools import GenieWorkspace

workspace = GenieWorkspace.load("empires2_x2_p1.dat")
gm = workspace.graphic_manager()

print(f"Graphics: {gm.count_active()} / {gm.count()}")

# Create new graphics
idle_gfx = gm.add_graphic(
    file_name="hero_idle.slp",
    frame_count=10,
    angle_count=8,
    frame_duration=0.1,
)

attack_gfx = gm.add_graphic(
    file_name="hero_attack.slp",
    frame_count=15,
    angle_count=8,
    frame_duration=0.08,
)

death_gfx = gm.add_graphic(
    file_name="hero_death.slp",
    frame_count=20,
    angle_count=8,
)

print(f"Created: idle={idle_gfx.id}, attack={attack_gfx.id}, death={death_gfx.id}")

# Add shadow to idle
shadow_gfx = gm.find_by_name("SHADOW_UNIT")
if shadow_gfx:
    idle_gfx.add_delta(
        graphic_id=shadow_gfx.id,
        offset_x=0,
        offset_y=2,
    )
    print("Added shadow delta")

# Copy existing graphic for modification
crossbow_attack = gm.find_by_file_name("x_crossbow_attack.slp")
if crossbow_attack:
    copied = gm.copy(source_id=crossbow_attack.id)
    copied.name = "HERO_CROSSBOW_ATTACK"
    copied.speed_multiplier = 1.5  # Faster animation
    print(f"Copied to ID {copied.id}")

workspace.save("output.dat")
```
