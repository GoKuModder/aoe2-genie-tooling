# GenieUnitManager

The `GenieUnitManager` class handles unit CRUD operations: create, clone, move, and retrieve units.

## Getting the Manager

```python
from Actual_Tools import GenieWorkspace

workspace = GenieWorkspace.load("empires2_x2_p1.dat")
um = workspace.genie_unit_manager()
```

---

## Methods

### create()

Create a new unit by cloning from an existing template.

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

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | `str` | Name for the new unit |
| `base_unit_id` | `int` | Unit to clone from. `None` = first valid unit |
| `unit_id` | `int` | Target ID. `None` = auto-assign next available |
| `enable_for_civs` | `List[int]` | Civ IDs to enable. `None` = all civs |
| `on_conflict` | `str` | `"error"` or `"overwrite"` if ID exists |
| `fill_gaps` | `str` | `"error"` or `"placeholder"` for gaps |

#### Examples

```python
# Basic creation (auto-assigns ID)
unit = um.create("My Archer", base_unit_id=4)
print(f"Created at ID {unit.id}")

# Create at specific ID
hero = um.create("Hero", base_unit_id=38, unit_id=1500)

# Overwrite if exists
um.create("Replacement", base_unit_id=4, unit_id=100, on_conflict="overwrite")

# Enable only for specific civs
um.create("Britons Archer", base_unit_id=4, enable_for_civs=[1])  # Britons only
```

---

### clone_into()

Clone an existing unit to a specific destination ID.

```python
def clone_into(
    dest_unit_id: int,
    base_unit_id: int,
    name: Optional[str] = None,
    enable_for_civs: Optional[List[int]] = None,
    on_conflict: Literal["error", "overwrite"] = "error",
    fill_gaps: Literal["error", "placeholder"] = "placeholder",
) -> UnitHandle
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `dest_unit_id` | `int` | Target unit ID for the clone |
| `base_unit_id` | `int` | Source unit ID to clone from |
| `name` | `str` | Name for clone. `None` = keep original name |
| `enable_for_civs` | `List[int]` | Civ IDs. `None` = all civs |
| `on_conflict` | `str` | `"error"` or `"overwrite"` |
| `fill_gaps` | `str` | `"error"` or `"placeholder"` |

#### Examples

```python
# Clone Archer to ID 2000
clone = um.clone_into(dest_unit_id=2000, base_unit_id=4, name="Archer Copy")

# Clone without renaming
um.clone_into(dest_unit_id=2001, base_unit_id=4)  # Keeps "Archer" name

# Overwrite existing
um.clone_into(dest_unit_id=100, base_unit_id=4, on_conflict="overwrite")
```

---

### move()

Move a unit from one ID to another.

```python
def move(
    src_unit_id: int,
    dst_unit_id: int,
    on_conflict: Literal["error", "overwrite", "swap"] = "error",
    fill_gaps: Literal["error", "placeholder"] = "placeholder",
) -> None
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `src_unit_id` | `int` | Source unit ID |
| `dst_unit_id` | `int` | Destination unit ID |
| `on_conflict` | `str` | `"error"`, `"overwrite"`, or `"swap"` |
| `fill_gaps` | `str` | `"error"` or `"placeholder"` |

!!! note "Placeholder at Source"
    After moving, the source ID contains a placeholder unit (not `None`) to maintain table integrity.

#### Examples

```python
# Move unit 100 to ID 2000
um.move(src_unit_id=100, dst_unit_id=2000)

# Overwrite destination
um.move(src_unit_id=100, dst_unit_id=200, on_conflict="overwrite")

# Swap two units
um.move(src_unit_id=100, dst_unit_id=200, on_conflict="swap")
```

---

### get()

Get a handle for an existing unit.

```python
def get(unit_id: int, civ_ids: Optional[List[int]] = None) -> UnitHandle
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `unit_id` | `int` | The unit ID to retrieve |
| `civ_ids` | `List[int]` | Civ IDs to include. `None` = all |

#### Examples

```python
# Get unit for all civs
archer = um.get(4)

# Get for specific civs only
britons_archer = um.get(4, civ_ids=[1])  # Only Britons
```

---

### exists()

Check if a unit ID exists (excludes placeholders).

```python
def exists(unit_id: int) -> bool
```

#### Example

```python
if um.exists(1500):
    unit = um.get(1500)
else:
    unit = um.create("New Unit", base_unit_id=4, unit_id=1500)
```

---

### count()

Return total number of unit slots.

```python
def count() -> int
```

#### Example

```python
print(f"Total unit slots: {um.count()}")
```

---

## Conflict Handling

When creating or moving units, conflicts can occur if the target ID already exists.

| Mode | Behavior |
|------|----------|
| `"error"` | Raises `UnitIdConflictError` |
| `"overwrite"` | Replaces existing unit |
| `"swap"` | Exchanges source and destination (move only) |

```python
# Safe creation with error handling
try:
    unit = um.create("Test", base_unit_id=4, unit_id=100)
except UnitIdConflictError:
    print("ID 100 already exists!")
    unit = um.get(100)
```

---

## Gap Filling

When creating units at IDs beyond current capacity, gaps may need to be filled.

| Mode | Behavior |
|------|----------|
| `"placeholder"` | Fills gaps with disabled placeholder units |
| `"error"` | Raises `GapNotAllowedError` |

Placeholders are detected by: `enabled=0`, `name=""`, `hit_points=1`

```python
# This will fill IDs up to 5000 with placeholders
um.create("Far Unit", base_unit_id=4, unit_id=5000, fill_gaps="placeholder")
```

---

## Complete Example

```python
from Actual_Tools import GenieWorkspace
from Actual_Tools.exceptions import UnitIdConflictError

workspace = GenieWorkspace.load("empires2_x2_p1.dat")
um = workspace.genie_unit_manager()

# Check current count
print(f"Current unit count: {um.count()}")

# Create a series of heroes
for i in range(3):
    unit_id = 2900 + i
    
    if um.exists(unit_id):
        print(f"ID {unit_id} exists, overwriting...")
        
    hero = um.create(
        name=f"Hero {i+1}",
        base_unit_id=38,
        unit_id=unit_id,
        on_conflict="overwrite",
    )
    hero.hit_points = 150 + (i * 50)
    print(f"Created {hero.name} at ID {hero.id} with {hero.hit_points} HP")

# Clone one hero
clone = um.clone_into(dest_unit_id=2910, base_unit_id=2900, name="Hero Clone")
print(f"Cloned to {clone.name} at ID {clone.id}")

# Move a unit
um.move(src_unit_id=2900, dst_unit_id=2920, on_conflict="overwrite")
print("Moved Hero 1 to ID 2920")

workspace.save("output.dat")
```
