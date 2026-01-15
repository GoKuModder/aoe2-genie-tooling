# Tech Methods

Complete reference of all methods available on `TechManager` and `TechHandle`.

---

## TechManager Methods

Access via `workspace.tech_manager`

```python
# First, define the manager
tech_manager = workspace.tech_manager
```

### `get(tech_id)`

Get a tech by ID.

```python
def get(tech_id: int) -> TechHandle
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `tech_id` | `int` | The tech ID |

**Returns:** `TechHandle`

**Raises:** `InvalidIdError` if tech doesn't exist

```python
loom = tech_manager.get(22)
print(f"Research time: {loom.research_time}")
```

---

### `add_new(name="", effect_id=-1, tech_id=None)` / `create(...)`

Create a new technology.

```python
def add_new(
    name: str = "",
    effect_id: int = -1,
    tech_id: Optional[int] = None,
) -> TechHandle
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `name` | `str` | `""` | Tech name |
| `effect_id` | `int` | `-1` | Linked effect ID (-1 = none) |
| `tech_id` | `int` | `None` | Target ID. `None` = append |

**Returns:** `TechHandle`

```python
# Create with linked effect
tech = tech_manager.create("My Tech", effect_id=500)

# Create at specific ID
tech = tech_manager.create("My Tech", tech_id=800)
```

---

### `copy(source_id, target_id=None)`

Copy a tech to a new ID.

```python
def copy(source_id: int, target_id: Optional[int] = None) -> TechHandle
```

**Returns:** `TechHandle`

```python
copied = tech_manager.copy(22)  # Copy Loom
```

---

### `delete(tech_id)`

Reset a tech to blank values.

```python
def delete(tech_id: int) -> bool
```

**Returns:** `True` if deleted

---

### `exists(tech_id)`

Check if a tech exists.

```python
def exists(tech_id: int) -> bool
```

---

### `count()` / `count_active()`

Get total tech slots or non-None count.

```python
print(f"Total: {tech_manager.count()}")
```

---

### `find_by_name(name)`

Find first tech matching name.

```python
def find_by_name(name: str) -> Optional[TechHandle]
```

---

### Clipboard Operations

```python
tech_manager.copy_to_clipboard(22)
pasted = tech_manager.paste()
tech_manager.clear_clipboard()
```

---

## TechHandle Methods

### Cost Management

#### `set_cost(slot, resource_id, amount, deduct_flag=1)`

Set a cost slot.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `slot` | `int` | Required | Cost slot (0, 1, or 2) |
| `resource_id` | `int` | Required | Resource type |
| `amount` | `int` | Required | Amount required |
| `deduct_flag` | `int` | `1` | Whether to deduct |

```python
tech.set_cost(0, resource_id=0, amount=100)  # 100 food
tech.set_cost(1, resource_id=3, amount=50)   # 50 gold
```

---

### Required Techs

#### `set_required_tech(slot, tech_id)`

Set a required tech at a slot.

| Parameter | Type | Description |
|-----------|------|-------------|
| `slot` | `int` | Slot (0-5) |
| `tech_id` | `int` | Required tech ID (-1 to clear) |

```python
tech.set_required_tech(0, tech_id=101)  # Require Castle Age
tech.set_required_tech(1, tech_id=22)   # Require Loom
```

---

#### `clear_required_techs()`

Clear all required tech slots.

```python
tech.clear_required_techs()
```

---

### Research Locations

#### `add_research_location(unit_id, button_id=0, ...)`

Add a location where this tech can be researched.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `unit_id` | `int` | Required | Building unit ID |
| `button_id` | `int` | `0` | UI button position |

```python
# Research at Blacksmith
tech.add_research_location(unit_id=103, button_id=5)
```

See [Research Locations](research-locations.md) for details.

---

#### `get_research_location(index)`

Get a research location by index.

```python
loc = tech.get_research_location(0)
print(f"Research at: {loc.unit_id}")
```

---

#### `remove_research_location(index)`

Remove a research location.

```python
tech.remove_research_location(0)
```

---

#### `clear_research_locations()`

Remove all research locations.

```python
tech.clear_research_locations()
```

---

### `exists()`

Check if this tech entry exists.

```python
if tech.exists():
    print(f"Tech: {tech.name}")
```
