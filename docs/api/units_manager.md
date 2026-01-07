# Units Manager

The `UnitManager` is your primary interface for creating, cloning, moving, and deleting units. It handles the complex logic of propagating changes across all civilizations and ensures that unit data remains consistent.

## Mental Model

*   **Multi-Civ Propagation**: A "Unit" in Age of Empires II is actually a slot (e.g., ID 4) that exists in every civilization. The `UnitManager` operates on these slots. When you create a unit, it writes to that slot in *all* civilizations (unless filtered).
*   **Deep Cloning**: When you copy a unit, the manager ensures that the new unit is a completely independent copy. Modifying the attack list of the clone will never affect the original.
*   **ID Management**: The manager handles ID allocation. If you don't specify an ID, it finds the next available slot.

## Public API

### UnitManager (`Actual_Tools_GDP.Units.unit_manager`)

Access via `workspace.unit_manager` (or `workspace.genie_unit_manager` for legacy compatibility).

```python
class UnitManager:
    def create(
        self,
        name: str,
        base_unit_id: int | None = None,
        unit_id: int | None = None,
        enable_for_civs: list[int] | None = None,
        on_conflict: str = "error",  # "error", "overwrite", "skip"
        fill_gaps: str = "placeholder", # "placeholder", "error"
    ) -> UnitHandle:
        """Creates a new unit, cloning from a base template."""

    def clone_into(
        self,
        src_unit_id: int,
        dst_unit_id: int,
        name: str | None = None,
        enable_for_civs: list[int] | None = None,
        on_conflict: str = "error",
    ) -> UnitHandle:
        """Clones an existing unit into a specific destination ID."""

    def move(
        self,
        src_unit_id: int,
        dst_unit_id: int,
        on_conflict: str = "error",
    ) -> UnitHandle:
        """Moves a unit from one ID to another, leaving a placeholder behind."""

    def get(self, unit_id: int) -> UnitHandle:
        """Gets a handle for an existing unit."""

    def count(self) -> int:
        """Returns the total number of unit slots."""

    def find_by_name(self, name: str, civ_id: int = 0) -> UnitHandle | None:
        """Finds the first unit matching the name."""
```

## Workflows

### Creating a New Unit

This is the most common operation. You pick a base unit (like an Archer) and create a modified version.

```python
# Create a "Super Archer" based on ID 4 (Archer)
hero = workspace.unit_manager.create(
    name="Super Archer",
    base_unit_id=4
)
hero.hit_points = 100
```

### Cloning to a Specific ID

Use `clone_into` when you need precise control over the destination ID, often for overriding existing units.

```python
# Overwrite the Militia (ID 74) with a Champion (ID 75)
workspace.unit_manager.clone_into(
    src_unit_id=75,
    dst_unit_id=74,
    name="Militia Replaced",
    on_conflict="overwrite"
)
```

### Moving a Unit

Moving is useful for reorganizing IDs. It copies the unit to the new ID and replaces the old slot with an empty "placeholder" unit to prevent ID shifts.

```python
workspace.unit_manager.move(src_unit_id=1000, dst_unit_id=2000)
```

### Multi-Civ Creation

You can create a unit that only exists for specific civilizations (e.g., a unique unit).

```python
# Create a unit only for Britons (1) and Franks (2)
# Other civs will have a placeholder at this ID.
u = workspace.unit_manager.create(
    name="Briton/Frank Unique",
    base_unit_id=4,
    enable_for_civs=[1, 2]
)
```

## Deep Cloning & Isolation

One of the critical features of `UnitManager` is **Deep Cloning**. In the raw data structure, Python lists are references. If you simply did `unit2.attacks = unit1.attacks`, both units would share the same attack list object. Adding an attack to `unit2` would magically add it to `unit1`.

`Actual_Tools_GDP` prevents this. The `create` and `clone_into` methods perform a deep copy of:
*   Attack lists
*   Armor lists
*   Resource storage lists
*   Task lists (and the nested task objects)

This ensures true isolation between units.

## Gotchas & Invariants

*   **ID Conflicts**: By default, `create` and `clone_into` will raise `UnitIdConflictError` if the target ID is already occupied by a real unit. Use `on_conflict="overwrite"` to force it.
*   **Gap Filling**: If you create a unit at ID 5000, but the file only goes up to ID 1000, the manager will automatically fill the gap (IDs 1001-4999) with placeholders. This is controlled by `fill_gaps`.
*   **Base Unit**: If `base_unit_id` is not provided to `create`, the manager attempts to find the *first valid unit* in the DAT file to use as a template. This ensures the new unit has valid default values instead of nulls.
*   **Performance**: Cloning a unit 40+ times (once for each civ) involves deep copying significant amounts of data. While optimized, creating thousands of units can take a few seconds.

## Cross-Links

*   [Unit Handle](units_handle.md)
*   [Unit Collections](units_collections.md)
*   [Civilizations](../civs.md)
