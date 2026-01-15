# Effect Methods

Complete reference of all methods available on `EffectManager` and `EffectHandle`.

---

## EffectManager Methods

Access via `workspace.effect_manager`

```python
# First, define the manager
effect_manager = workspace.effect_manager
```

### `get(effect_id)`

Get an effect by ID.

```python
def get(effect_id: int) -> EffectHandle
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `effect_id` | `int` | The effect ID |

**Returns:** `EffectHandle`

**Raises:** `InvalidIdError` if effect doesn't exist

```python
effect = effect_manager.get(100)
print(f"Name: {effect.name}, Commands: {len(effect.commands)}")
```

---

### `add_new(name="", effect_id=None)` / `create(...)`

Create a new effect holder.

```python
def add_new(
    name: str = "",
    effect_id: Optional[int] = None,
) -> EffectHandle
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `name` | `str` | `""` | Effect name |
| `effect_id` | `int` | `None` | Target ID. `None` = append |

**Returns:** `EffectHandle`

```python
# Create at next available ID
effect = effect_manager.add_new("Archer Upgrade")

# Create at specific ID
effect = effect_manager.add_new("My Effect", effect_id=500)
```

---

### `copy(source_id, target_id=None)`

Copy an effect to a new ID.

```python
def copy(source_id: int, target_id: Optional[int] = None) -> EffectHandle
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `source_id` | `int` | Required | Effect to copy |
| `target_id` | `int` | `None` | Destination. `None` = append |

**Returns:** `EffectHandle`

```python
copied = effect_manager.copy(100)
print(f"Copied to ID: {copied.id}")
```

---

### `delete(effect_id)`

Reset an effect to blank values.

```python
def delete(effect_id: int) -> bool
```

**Returns:** `True` if deleted

```python
effect_manager.delete(100)
```

---

### `exists(effect_id)`

Check if an effect exists.

```python
def exists(effect_id: int) -> bool
```

```python
if effect_manager.exists(100):
    effect = effect_manager.get(100)
```

---

### `count()` / `count_active()`

Get total effect slots or count of non-None effects.

```python
print(f"Total slots: {effect_manager.count()}")
print(f"Active effects: {effect_manager.count_active()}")
```

---

### `find_by_name(name)`

Find first effect matching name.

```python
def find_by_name(name: str) -> Optional[EffectHandle]
```

**Returns:** `EffectHandle` or `None`

```python
effect = effect_manager.find_by_name("Fletching")
```

---

### Clipboard Operations

```python
# Copy to clipboard
effect_manager.copy_to_clipboard(100)

# Paste from clipboard
pasted = effect_manager.paste()  # Append
pasted = effect_manager.paste(target_id=600)  # At specific ID

# Clear clipboard
effect_manager.clear_clipboard()
```

---

## EffectHandle Methods

### `new_command(type, a, b, c, d)`

Add a raw effect command.

```python
def new_command(
    type: int = 0,
    a: int = -1,
    b: int = -1,
    c: int = -1,
    d: float = 0.0,
) -> CommandHandle
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `type` | `int` | `0` | Command type ID |
| `a` | `int` | `-1` | Parameter A (unit/attribute) |
| `b` | `int` | `-1` | Parameter B (value/amount) |
| `c` | `int` | `-1` | Parameter C (class/civ) |
| `d` | `float` | `0.0` | Parameter D (float value) |

**Returns:** `CommandHandle`

```python
effect.new_command(type=4, a=4, b=0, c=-1, d=10)
```

---

### `add_command` Property

Returns an `EffectCommandBuilder` for fluent command creation.

See [Effect Commands](effect-commands.md) for all builder methods.

```python
effect.add_command.attribute_modifier_add(a=4, b=0, c=-1, d=10)
```

---

### `get_command(index)`

Get a command by index.

```python
def get_command(index: int) -> Optional[CommandHandle]
```

**Returns:** `CommandHandle` or `None`

```python
cmd = effect.get_command(0)
print(f"Type: {cmd.type}, A: {cmd.a}")
```

---

### `commands` Property

Get all commands as a list of handles.

```python
for cmd in effect.commands:
    print(f"Type {cmd.type}: a={cmd.a}, b={cmd.b}, d={cmd.d}")
```

---

### `copy_command(index, target_index=None)`

Copy a command within this effect.

```python
def copy_command(index: int, target_index: Optional[int] = None) -> Optional[CommandHandle]
```

**Returns:** `CommandHandle` for the copy

```python
copied = effect.copy_command(0)  # Copy first to end
```

---

### `move_command(source_index, target_index)`

Reorder a command.

```python
def move_command(source_index: int, target_index: int) -> bool
```

**Returns:** `True` if moved

```python
effect.move_command(0, 2)  # Move first to position 2
```

---

### `remove_command(index)`

Remove a command by index.

```python
def remove_command(index: int) -> bool
```

**Returns:** `True` if removed

```python
effect.remove_command(0)  # Remove first command
```

---

### `clear_commands()`

Remove all commands.

```python
effect.clear_commands()
```

---

### `exists()`

Check if this effect entry exists.

```python
def exists() -> bool
```

```python
if effect.exists():
    print(f"Effect has {len(effect.commands)} commands")
```

---

## CommandHandle Properties

| Property | Type | R/W | Description |
|----------|------|-----|-------------|
| `type` | `int` | RW | Command type ID |
| `a` | `int` | RW | Parameter A |
| `b` | `int` | RW | Parameter B |
| `c` | `int` | RW | Parameter C |
| `d` | `float` | RW | Parameter D |

```python
cmd = effect.get_command(0)
cmd.d = 20  # Change value
cmd.a = 38  # Change target unit
```
