# Sound Methods

Complete reference of all methods available on `SoundManager` and `SoundHandle`.

---

## SoundManager Methods

Access via `workspace.sound_manager`

```python
# First, define the manager
sound_manager = workspace.sound_manager
```

### `get(sound_id)`

Get a sound by ID.

```python
def get(sound_id: int) -> SoundHandle
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `sound_id` | `int` | The sound ID |

**Returns:** `SoundHandle`

**Raises:** `InvalidIdError` if sound doesn't exist

```python
sound = sound_manager.get(50)
print(f"Files: {len(sound.files)}")
```

---

### `add_new(name="", sound_id=None)` / `create(...)`

Create a new sound holder.

```python
def add_new(
    name: str = "",
    sound_id: Optional[int] = None,
) -> SoundHandle
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `name` | `str` | `""` | Sound name |
| `sound_id` | `int` | `None` | Target ID. `None` = append |

**Returns:** `SoundHandle`

```python
# Create at next available ID
sound = sound_manager.add_new("AttackSound")

# Create at specific ID
sound = sound_manager.add_new("MySound", sound_id=600)
```

---

### `copy(source_id, target_id=None)`

Copy a sound to a new ID.

```python
def copy(source_id: int, target_id: Optional[int] = None) -> SoundHandle
```

**Returns:** `SoundHandle`

```python
copied = sound_manager.copy(50)
```

---

### `delete(sound_id)`

Delete a sound (sets slot to None).

```python
def delete(sound_id: int) -> bool
```

**Returns:** `True` if deleted

---

### `exists(sound_id)`

Check if a sound exists.

```python
def exists(sound_id: int) -> bool
```

---

### `count()` / `count_active()`

Get total slots or non-None count.

```python
print(f"Total: {sound_manager.count()}")
```

---

### `find_by_name(name)`

Find first sound matching name.

```python
def find_by_name(name: str) -> Optional[SoundHandle]
```

---

### `find_by_file_name(file_name)`

Find first sound containing a specific audio file.

```python
def find_by_file_name(file_name: str) -> Optional[SoundHandle]
```

```python
sound = sound_manager.find_by_file_name("attack.wav")
```

---

### Clipboard Operations

```python
sound_manager.copy_to_clipboard(50)
pasted = sound_manager.paste()
sound_manager.clear_clipboard()
```

---

## SoundHandle Methods

### `new_sound(filename, sound_name="", probability=100, ...)`

Add a new audio file to this sound group.

```python
def new_sound(
    filename: str = "",
    sound_name: str = "",
    resource_id: int = -1,
    probability: int = 100,
    civilization_id: int = -1,
    icon_set: int = -1,
) -> SoundFileHandle
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `filename` | `str` | `""` | Physical filename (e.g., "attack.wav") |
| `sound_name` | `str` | `""` | Internal name (DE only) |
| `probability` | `int` | `100` | Play probability (0-100) |
| `civilization_id` | `int` | `-1` | Civ filter (-1 = all) |
| `resource_id` | `int` | `-1` | Resource ID |
| `icon_set` | `int` | `-1` | Icon set filter |

**Returns:** `SoundFileHandle`

```python
sound.new_sound(filename="attack_01.wav", probability=50)
sound.new_sound(filename="attack_02.wav", probability=50)
```

**Alias:** `add_file(...)` works the same.

---

### `get_file(index)`

Get a sound file by index.

```python
def get_file(index: int) -> Optional[SoundFileHandle]
```

**Returns:** `SoundFileHandle` or `None`

```python
file = sound.get_file(0)
print(f"Filename: {file.filename}")
```

**Alias:** `get_sound(index)`

---

### `files` / `sounds` Property

Get all sound files as handles.

```python
for file in sound.files:
    print(f"{file.filename}: {file.probability}%")
```

---

### `copy_sound(index, target_index=None)`

Copy a sound file within this group.

```python
def copy_sound(index: int, target_index: Optional[int] = None) -> Optional[SoundFileHandle]
```

**Returns:** `SoundFileHandle`

---

### `move_sound(source_index, target_index)`

Reorder a sound file.

```python
def move_sound(source_index: int, target_index: int) -> bool
```

**Returns:** `True` if moved

---

### `remove_file(index)`

Remove a sound file by index.

```python
def remove_file(index: int) -> bool
```

**Returns:** `True` if removed

**Alias:** `remove_sound(index)`

---

### `clear_files()`

Remove all audio files.

```python
sound.clear_files()
```

---

### `exists()`

Check if this sound entry exists.

```python
if sound.exists():
    print(f"Sound has {len(sound.files)} files")
```
