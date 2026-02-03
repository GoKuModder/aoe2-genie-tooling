# Unit Methods

Complete reference of all methods available on `UnitManager` and `UnitHandle`.

---

## UnitManager Methods

Access via `workspace.unit_manager`

```python
# First, define the manager
unit_manager = workspace.unit_manager
```

### `get(unit_id, civ_ids=None)`

Retrieve a handle for an existing unit.

```python
def get(unit_id: int, civ_ids: Optional[List[int]] = None) -> UnitHandle
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `unit_id` | `int` | Required | The unit ID to retrieve |
| `civ_ids` | `List[int]` | `None` | Specific civs to include. `None` = all civs |

**Returns:** `UnitHandle`

**Raises:** `InvalidIdError` if unit doesn't exist

**Example:**
```python
# Get for all civs
archer = unit_manager.get(4)

# Get for specific civs only
britons_archer = unit_manager.get(4, civ_ids=[1])
```

---

### `create(name, base_unit_id=None, unit_id=None, enable_for_civs=None, on_conflict="error", fill_gaps="placeholder")`

Create a new unit by cloning an existing template.

```python
def create(
    name: str,
    base_unit_id: Optional[int] = None,
    unit_id: Optional[int] = None,
    enable_for_civs: Optional[List[int]] = None,
    on_conflict: Literal["error", "overwrite"] = "error",
    fill_gaps: Literal["error", "placeholder"] = "placeholder",
) -> UnitHandle
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `name` | `str` | Required | Name for the new unit |
| `base_unit_id` | `int` | `None` | Unit ID to clone from. `None` = first valid unit |
| `unit_id` | `int` | `None` | Target slot ID. `None` = append to end |
| `enable_for_civs` | `List[int]` | `None` | Civs to enable for. `None` = all civs |
| `on_conflict` | `str` | `"error"` | What to do if `unit_id` is occupied |
| `fill_gaps` | `str` | `"placeholder"` | How to handle gaps in ID sequence |

**Returns:** `UnitHandle`

**Raises:**
- `UnitIdConflictError` if `on_conflict="error"` and ID occupied
- `TemplateNotFoundError` if `base_unit_id` doesn't exist
- `GapNotAllowedError` if `fill_gaps="error"` and gaps would be created

**Example:**
```python
# Basic creation
hero = unit_manager.create("Hero Unit", base_unit_id=38)

# Create at specific ID
hero = unit_manager.create("Hero", base_unit_id=38, unit_id=2000)

# Overwrite existing
hero = unit_manager.create("Hero", unit_id=100, on_conflict="overwrite")

# Create for specific civs
unique = unit_manager.create("Briton Unique", enable_for_civs=[1])
```

---

### `clone_into(dest_unit_id, source_unit_id, name=None, enable_for_civs=None, on_conflict="error", fill_gaps="placeholder")`

Clone a unit into a specific destination ID.

```python
def clone_into(
    dest_unit_id: int,
    source_unit_id: int,
    name: Optional[str] = None,
    enable_for_civs: Optional[List[int]] = None,
    on_conflict: Literal["error", "overwrite"] = "error",
    fill_gaps: Literal["error", "placeholder"] = "placeholder",
) -> UnitHandle
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `dest_unit_id` | `int` | Required | Target unit ID |
| `source_unit_id` | `int` | Required | Source unit to clone |
| `name` | `str` | `None` | New name. `None` = keep source name |
| `enable_for_civs` | `List[int]` | `None` | Civs to enable for |
| `on_conflict` | `str` | `"error"` | Conflict handling |
| `fill_gaps` | `str` | `"placeholder"` | Gap handling |

**Returns:** `UnitHandle`

**Example:**
```python
# Clone Archer (4) to slot 2500
new_archer = unit_manager.clone_into(2500, 4, name="Super Archer")
```

---

### `move(src_unit_id, dst_unit_id, on_conflict="error", fill_gaps="placeholder")`

Move a unit from one ID to another.

```python
def move(
    src_unit_id: int,
    dst_unit_id: int,
    on_conflict: Literal["error", "overwrite", "swap"] = "error",
    fill_gaps: Literal["error", "placeholder"] = "placeholder",
) -> UnitHandle
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `src_unit_id` | `int` | Required | Source unit ID |
| `dst_unit_id` | `int` | Required | Destination unit ID |
| `on_conflict` | `str` | `"error"` | `"swap"` exchanges positions |
| `fill_gaps` | `str` | `"placeholder"` | Gap handling |

**Returns:** `UnitHandle` for the moved unit

**Example:**
```python
moved = unit_manager.move(100, 200)
swapped = unit_manager.move(100, 200, on_conflict="swap")
```

---

### `exists(unit_id)`

Check if a unit ID exists and is not a placeholder.

```python
def exists(unit_id: int) -> bool
```

**Returns:** `True` if unit exists and is a real unit (not placeholder)

**Example:**
```python
if unit_manager.exists(4):
    archer = unit_manager.get(4)
```

---

### `exists_raw(unit_id)`

Check if a unit ID slot is occupied (including placeholders).

```python
def exists_raw(unit_id: int) -> bool
```

**Returns:** `True` if slot is not `None` (includes placeholders)

---

### `count()`

Get total number of unit slots.

```python
def count() -> int
```

**Example:**
```python
print(f"Total slots: {unit_manager.count()}")
```

---

### `find_by_name(name, civ_id=0)`

Find the first unit matching a name.

```python
def find_by_name(name: str, civ_id: int = 0) -> Optional[UnitHandle]
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `name` | `str` | Required | Unit name to search |
| `civ_id` | `int` | `0` | Civ to search in |

**Returns:** `UnitHandle` or `None`

**Example:**
```python
archer = unit_manager.find_by_name("ARCHR")
if archer:
    print(f"Found at ID: {archer.id}")
```

---

## UnitHandle Methods

### Attack Methods

| Method | Description |
|--------|-------------|
| `add_attack(class_, amount)` | Add attack entry, returns `AttackHandle` |
| `get_attack_by_id(attack_id)` | Get attack by index |
| `get_attack_by_class(class_)` | Get attack by damage class |
| `remove_attack(attack_id)` | Remove attack by index |
| `set_attack(class_, amount)` | Update or add attack for class |

See [Attacks & Armours](attacks-armours.md) for details.

---

### Armour Methods

| Method | Description |
|--------|-------------|
| `add_armour(class_, amount)` | Add armour entry, returns `ArmourHandle` |
| `get_armour_by_id(armour_id)` | Get armour by index |
| `get_armour_by_class(class_)` | Get armour by damage class |
| `remove_armour(armour_id)` | Remove armour by index |
| `set_armour(class_, amount)` | Update or add armour for class |

See [Attacks & Armours](attacks-armours.md) for details.

---

### Task Methods

| Method | Description |
|--------|-------------|
| `add_task` (property) | Returns `TaskBuilder` for fluent API |
| `create_task(...)` | Add task with raw parameters |
| `get_task(task_id)` | Get task by index |
| `get_tasks_list()` | Get all tasks as handles |
| `remove_task(task_id)` | Remove task by index |

See [Tasks](tasks.md) for details.

---

### Damage Graphic Methods

| Method | Description |
|--------|--------------|
| `add_damage_graphic(graphic_id, damage_percent, apply_mode)` | Add damage state graphic |
| `get_damage_graphic(damage_graphic_id)` | Get damage graphic by index |
| `remove_damage_graphic(damage_graphic_id)` | Remove damage graphic |
| `remove_all_damage_graphics()` | Clear all damage graphics |

**Example:**
```python
# Show burning graphic at 25% HP
unit.add_damage_graphic(graphic_id=500, damage_percent=25, apply_mode=0)

# Clear all damage graphics
unit.remove_all_damage_graphics()
```

---

### Train Location Methods

| Method | Description |
|--------|-------------|
| `add_train_location(unit_id, train_time, button_id, hot_key_id)` | Add train location |
| `get_train_location(train_location_id)` | Get by index |
| `remove_train_location(train_location_id)` | Remove by index |

See [Train Locations](train-locations.md) for details.

---

### Drop Site Methods

| Method | Description |
|--------|-------------|
| `add_drop_site(unit_id)` | Add drop site building |
| `get_drop_site(drop_site_id)` | Get by index |
| `remove_drop_site(drop_site_id)` | Remove by index |

**Example:**
```python
# Add Town Center and Mill as drop sites
unit.add_drop_site(109)  # Town Center
unit.add_drop_site(68)   # Mill
```

---

### Resource Storage Methods

| Method | Description |
|--------|-------------|
| `resource_1(type, amount, flag)` | Set resource slot 1 |
| `resource_2(type, amount, flag)` | Set resource slot 2 |
| `resource_3(type, amount, flag)` | Set resource slot 3 |

**Parameters:**
- `type` - Resource type (0=food, 1=wood, etc.)
- `amount` - Amount carried
- `flag` - Storage flag (2=give on death, etc.)

**Example:**
```python
# Villager carries 10 food
unit.resource_1(type=0, amount=10.0, flag=2)
```

---

### Utility Methods

| Method | Description |
|--------|--------------|
| `invalidate_cache()` | Clear cached data (call after changing `civ_ids`) |
| `change_unit_type(new_type)` | Safely change unit type (structures sync at save) |

---

### `change_unit_type(new_type)`

Safely change a unit's type. Automatically handles structure synchronization (e.g., adding `building_info` when converting to Building type 80).

```python
def change_unit_type(new_type: int) -> None
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `new_type` | `int` | Target unit type (10-80) |

**Example:**
```python
# Convert a Creatable (70) to Building (80)
unit = unit_manager.get(500)
unit.change_unit_type(80)
workspace.save("modded.dat")  # Structures sync during save
```

**Note:** Structure synchronization happens automatically during `workspace.save()`. The system adds missing required structures without removing existing ones (game tolerates both).
