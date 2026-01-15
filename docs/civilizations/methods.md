# Civilization Methods

Complete reference of all methods available on `CivManager` and `CivHandle`.

---

## CivManager Methods

Access via `workspace.civ_manager`

```python
# First, define the manager
civ_manager = workspace.civ_manager
```

### `get(civ_id)`

Get a civilization by ID.

```python
def get(civ_id: int) -> CivHandle
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `civ_id` | `int` | The civilization ID |

**Returns:** `CivHandle`

**Raises:** `InvalidIdError` if civ doesn't exist

```python
britons = civ_manager.get(1)
print(f"Civ: {britons.name}")
```

---

### `add_new(name="", civ_id=None)` / `create(...)`

Create a new civilization.

```python
def add_new(
    name: str = "",
    civ_id: Optional[int] = None,
) -> CivHandle
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `name` | `str` | `""` | Civ name |
| `civ_id` | `int` | `None` | Target ID. `None` = append |

**Returns:** `CivHandle`

```python
custom = civ_manager.create("Custom Civ")
```

---

### `copy(source_id, target_id=None)`

Copy a civilization to a new ID.

```python
def copy(source_id: int, target_id: Optional[int] = None) -> CivHandle
```

**Returns:** `CivHandle`

```python
# Clone Britons
custom = civ_manager.copy(1)
custom.name = "Elite Britons"
```

---

### `exists(civ_id)`

Check if a civ exists.

```python
def exists(civ_id: int) -> bool
```

---

### `count()`

Get total number of civilizations.

```python
print(f"Total civs: {civ_manager.count()}")
```

---

### `find_by_name(name)`

Find first civ matching name.

```python
def find_by_name(name: str) -> Optional[CivHandle]
```

```python
britons = civ_manager.find_by_name("Britons")
```

---

### Clipboard Operations

```python
civ_manager.copy_to_clipboard(1)
pasted = civ_manager.paste()
civ_manager.clear_clipboard()
```

---

## Global Resource Methods

Resources are stored per-civ, but the number of slots is global.

### `add_resource(default_value=0.0)`

Add a new resource slot to ALL civilizations.

```python
def add_resource(default_value: float = 0.0) -> int
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `default_value` | `float` | `0.0` | Initial value for all civs |

**Returns:** `int` - Index of the new resource

```python
new_index = civ_manager.add_resource(default_value=100)
print(f"New resource at index: {new_index}")
```

---

### `remove_resource(index)`

Remove a resource slot from ALL civilizations.

```python
def remove_resource(index: int) -> bool
```

**Returns:** `True` if removed

```python
civ_manager.remove_resource(300)
```

---

### `resource_count()`

Get the number of resource slots.

```python
def resource_count() -> int
```

```python
print(f"Resource slots: {civ_manager.resource_count()}")
```

---

### `clear_resources()`

Remove all resources from ALL civilizations.

**Warning:** Use with extreme caution!

```python
civ_manager.clear_resources()
```

---

## CivHandle Methods

### Resource Access

#### `resource` Property

Returns a `ResourceAccessor` for per-civ resource values.

```python
civ = civ_manager.get(1)

# Via indexing
food = civ.resource[0]
civ.resource[0] = 500

# Via methods
food = civ.resource.get(0)
civ.resource.set(0, 500)
```

---

#### `resources` Property

Direct access to the raw resources list.

```python
all_res = civ.resources  # List of floats
```

---

### Unit Access

#### `units` Property

Get the raw units list for this civilization.

```python
units = civ.units  # List of Unit objects
```

**Note:** Prefer using `UnitManager` with `civ_ids` for proper handle-based access.

---

### `exists()`

Check if this civilization entry exists.

```python
if civ.exists():
    print(f"Civ: {civ.name}")
```
