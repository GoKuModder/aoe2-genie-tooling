# Units API

Manage units (creatures, buildings, objects) using `UnitManager` and `UnitHandle`.

## Mental Model

Units in the Genie Engine are complex.
1.  **Multi-Civ Existence**: A "Unit" (like an Archer) exists in *every* civilization's data table. If you change the Archer's HP, you usually want it to change for Britons, Franks, Goths, etc. `UnitHandle` automatically propagates changes to all enabled civilizations.
2.  **Attribute Flattening**: A raw unit struct is deeply nested (`unit.type_50.hit_points`, `unit.bird.resource_storage`). The `UnitHandle` flattens this, so you just write `unit.hit_points` or `unit.resource_storage`.
3.  **Cloning = Deep Copy**: When you create a new unit, we perform a deep copy. This is critical because units contain lists (like `attacks` or `tasks`). If we did a shallow copy, changing the attack of your new unit would accidentally change the attack of the original unit it was copied from.

## Common Workflows

### Modifying an Existing Unit
```python
archer = workspace.unit_manager.get(4)
archer.hit_points = 45  # Updates all civs
archer.name = "Better Archer"
```

### Creating a New Unit (Auto-ID)
Use `create` when you don't care about the specific ID, just that it's new.
```python
# Creates a copy of unit 4 at the next available slot
super_archer = workspace.unit_manager.create("Super Archer", base_unit_id=4)
print(super_archer.id)
```

### creating a Unit at Specific ID
Use `clone_into` when you need a specific ID (e.g., replacing a placeholder or overwriting a unit).
```python
# Clones unit 4 into slot 100, overwriting whatever was there
workspace.unit_manager.clone_into(dest_unit_id=100, base_unit_id=4, name="Specific Archer")
```

### Adding Tasks (Fluent API)
Tasks define behaviors like attacking, building, or gathering.
```python
unit = workspace.unit_manager.get(4)

# Use the builder for typed access
unit.add_task.combat(
    class_id=4,    # Target class
    work_range=5   # Attack range
)
```

## When to use X vs Y

| Operation | Method | Use Case |
| :--- | :--- | :--- |
| **New Unit** | `create()` | You just want a new unit and don't care about the ID number. |
| **Specific ID** | `clone_into()` | You are replacing a specific unit or filling a known slot. |
| **Move Unit** | `move()` | You want to reorder units (swaps IDs). |

## Gotchas & Invariants

*   **Civilization Isolation**: By default, `UnitHandle` affects *all* civilizations. If you want to change a unit for only *one* civ, you must create the handle with that specific civ ID: `workspace.unit_manager.get(4, civ_ids=[1])`.
*   **Deep Copy Performance**: `create` and `clone_into` perform deep copies. This is safer but slightly slower than reference copying. Always prefer these methods over manual manipulation of the underlying list to avoid "spooky action at a distance" where units share attack lists.
*   **Gap Filling**: `create` and `clone_into` will automatically fill gaps with placeholder units if you write to a high ID (e.g., ID 2000 when max is 1000). This ensures the `.dat` file structure remains valid (no `None` gaps allowed).

## UnitManager

Access via `workspace.unit_manager`.

### Methods

#### `get(unit_id: int) -> UnitHandle`
Get a handle for an existing unit.

#### `create(name: str, base_unit_id: Optional[int] = None, unit_id: Optional[int] = None, ...) -> UnitHandle`
Create a new unit.
- **name**: Name of the new unit.
- **base_unit_id**: ID of the unit to clone (template). If `None`, uses a default.
- **unit_id**: Target unit ID. If `None`, appends to the end.
- **on_conflict**: Behavior if ID exists (`"error"` or `"overwrite"`).

#### `clone_into(dest_unit_id: int, base_unit_id: int, name: Optional[str] = None, ...) -> UnitHandle`
Clones a specific unit into a specific destination ID.

#### `move(src_unit_id: int, dst_unit_id: int, ...)`
Moves a unit from one ID to another.

## UnitHandle

A wrapper around the unit data that handles multi-civ updates.

### Attributes
Common attributes (flattened):
- `name` (str)
- `hit_points` (int)
- `line_of_sight` (int)
- `garrison_capacity` (int)
- `standing_graphic` (tuple)

### Methods

#### `add_task(...) -> TaskBuilder`
Adds a task (action) to the unit. Returns a builder for configuration.
