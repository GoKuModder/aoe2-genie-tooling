# Unit Collections

Unit lists like Attacks, Armors, Tasks, and Resource Storages are managed through special "Collection Managers". These allow you to add, remove, and modify items across all civilizations simultaneously.

## Mental Model

*   **Synchronized Lists**: Just like scalar properties (`unit.hit_points`), adding an item to a list (e.g., `unit.attacks.add(...)`) adds it to the unit in **every enabled civilization**.
*   **Collection Managers**: Accessed via properties like `unit.attacks`, `unit.tasks`, `unit.armours`. They behave like Python lists (supports `len()`, iteration, indexing) but return **Handles**.
*   **Handles**: Items within collections are wrapped in lightweight handles (e.g., `AttackHandle`, `TaskHandle`) that allow you to modify their properties directly.

## Public API

### Collection Managers

All managers (`AttacksManager`, `TasksManager`, etc.) share a common interface:

*   `__len__()`: Returns count (e.g., `len(unit.attacks)`).
*   `__getitem__(index)`: Returns a Handle (e.g., `unit.attacks[0]`).
*   `__iter__()`: Allows looping (e.g., `for attack in unit.attacks:`).
*   `add(**kwargs)`: Adds a new item. Parameters depend on the item type.
*   `remove(index)`: Removes the item at the specific index.
*   `clear()`: Removes all items.

### Specific Managers & Handles

#### Attacks (`Actual_Tools_GDP.Units.unit_collections.attacks`)
*   **Manager**: `AttacksManager`
*   **Handle**: `AttackHandle`
    *   `class_` (int): Attack class (use `UnitClass` enum).
    *   `amount` (float): Damage amount.

#### Armours (`Actual_Tools_GDP.Units.unit_collections.armours`)
*   **Manager**: `ArmoursManager`
*   **Handle**: `ArmourHandle`
    *   `class_` (int): Armor class.
    *   `amount` (int): Armor amount.

#### Tasks (`Actual_Tools_GDP.Units.unit_collections.tasks`)
*   **Manager**: `TasksManager`
*   **Handle**: `TaskHandle`
    *   `task_type` (int), `id` (int), `work_range` (float), `resource_in/out` (int), etc.
    *   **Note**: Prefer using `TaskBuilder` (see below) for creating tasks.

#### Resource Storages (`Actual_Tools_GDP.Units.unit_collections.resources`)
*   **Manager**: `ResourcesManager`
*   **Handle**: `ResourceHandle`
    *   `type` (int), `amount` (float), `flag` (int - storage mode).

## Workflows

### Modifying Attacks

```python
# Clear existing attacks
unit.attacks.clear()

# Add Pierce (3) damage
unit.attacks.add(class_=3, amount=10)

# Add Bonus vs Cavalry (8)
unit.attacks.add(class_=8, amount=5)

# Modify the first attack
unit.attacks[0].amount = 12
```

### Modifying Armor

```python
# Loop through armor
for armor in unit.armours:
    if armor.class_ == 3: # Pierce Armor
        armor.amount += 2
```

### Managing Resource Storage

This is how you define what resources a unit carries (like villagers) or drops on death (like wolves).

```python
from Actual_Tools_GDP.Datasets import Resource, StoreMode

# Make unit drop 50 Gold on death
# Slot 1 is typically used for drops/carry
unit.resource_storages.add(
    type=Resource.GOLD,
    amount=50.0,
    flag=StoreMode.DROP
)
```

## Gotchas & Invariants

*   **Index Consistency**: The library assumes that the list length and order are consistent across all civilizations for a given unit. If one civ has 3 attacks and another has 2, the behavior is undefined (usually reads from Civ 0). The `UnitManager` tries to enforce this during creation/cloning.
*   **Raw Objects**: The underlying backend uses classes like `UnitAttack`, `UnitArmor`. The handles abstract these. You rarely need to touch the raw objects.
*   **Task IDs**: Tasks have an internal `id` field. The `TasksManager` usually auto-assigns this to match the index (0, 1, 2...) if you pass `id=-1`.

## Cross-Links

*   [Task Builder](task_builder.md)
*   [Unit Handle](units_handle.md)
