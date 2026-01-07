# Unit Handle & Wrappers

The `UnitHandle` is the primary object you interact with when modifying a unit. It wraps the raw unit data and provides a powerful, multi-civ aware interface.

## Mental Model

*   **Proxied Access**: A `UnitHandle` doesn't store data itself. It remembers the `unit_id` and the `workspace`. When you access a property like `unit.hit_points`, it fetches the unit from the underlying `DatFile`.
*   **Multi-Civ Write**: When you *set* a property (`unit.hit_points = 50`), the handle iterates through **all enabled civilizations** and updates the unit in each one. This ensures consistency.
*   **Wrappers as "Tabs"**: To organize the hundreds of unit attributes, `Actual_Tools_GDP` groups them into "Wrappers" that mirror the tabs in tools like AGE (Advanced Genie Editor).
    *   `unit.combat` -> Type 50 (Attack, Armor, Range)
    *   `unit.building` -> Building data (Construction time, Work rate)
    *   `unit.creation` -> Creatable data (Cost, Train time)
*   **Attribute Flattening**: For convenience, many commonly used wrapper attributes are also exposed directly on the main handle. `unit.range` is an alias for `unit.combat.max_range`.

## Public API

### UnitHandle (`Actual_Tools_GDP.Units.unit_handle`)

```python
class UnitHandle:
    # Direct Properties
    id: int
    name: str
    hit_points: int
    speed: float
    line_of_sight: float

    # Wrappers (Sub-components)
    @property
    def combat(self) -> CombatWrapper: ...
    @property
    def building(self) -> BuildingWrapper: ...
    @property
    def creation(self) -> CreationWrapper: ...
    @property
    def movement(self) -> MovementWrapper: ...
    @property
    def behavior(self) -> BehaviorWrapper: ...
    @property
    def projectile(self) -> ProjectileWrapper: ...
```

### Wrappers (`Actual_Tools_GDP.Units.wrappers`)

#### `CombatWrapper` (formerly Type 50)
Handles attack, armor, range, and reload time.
*   `base_armor`, `attack_graphic`, `max_range`, `reload_time`, `blast_width`

#### `BuildingWrapper`
Handles building-specific logic.
*   `construction_time`, `work_rate`, `garrison_capacity`, `deposit_unit_id`

#### `CreationWrapper` (formerly Creatable)
Handles training and costs.
*   `train_time`, `displayed_pierce_armour` (often stored here), `resource_costs`

#### `MovementWrapper` (formerly DeadFish)
Handles movement physics.
*   `turn_speed`, `acceleration`

#### `BehaviorWrapper` (formerly Bird)
Handles AI behavior flags and search radius.
*   `default_task_id`, `search_radius`, `work_rate_multiplier`

#### `ProjectileWrapper`
Handles projectile physics.
*   `arc`, `gravity`, `smart_mode`

## Workflows

### Accessing Nested Attributes

You can access attributes via their specific wrapper "tab":

```python
# Accessing via wrapper
unit.combat.max_range = 8.0
unit.combat.reload_time = 2.0
unit.building.work_rate = 1.5
```

### Using Flattened Attributes

For common attributes, you can skip the wrapper (if the library implements the shortcut).

```python
# Direct access (shortcuts)
unit.speed = 1.2         # Shortcut for unit.movement.speed
unit.line_of_sight = 6.0 # Shortcut for unit.base.line_of_sight
```

### Setting Properties Across Civs

```python
# This sets the HP for the unit in ALL civilizations
unit.hit_points = 100

# This sets the standing graphic for ALL civilizations
unit.standing_graphic = 500
```

## Gotchas & Invariants

*   **Missing Wrappers**: Not all units have all wrappers. A "Flag" unit might not have `combat` data. Accessing `unit.combat` on such a unit might return a wrapper that reads empty/default values or raises an error depending on the underlying structure.
*   **Typos**: If you try to access a property that doesn't exist (e.g., `unit.hitpoints` instead of `unit.hit_points`), Python will raise a standard `AttributeError`. The Validator does not check this at runtime, but your IDE should help if type hints are loaded.
*   **Delegation Order**: If an attribute name exists in multiple wrappers (rare), the `UnitHandle` has a specific resolution order (usually prioritizing the main unit struct, then combat, etc.). It's safer to use the specific wrapper if you are unsure.
*   **Read vs Write**: Reading a property (`x = unit.hit_points`) typically reads from **Civilization 0** (Gaia/Base). Writing a property updates **All Civilizations**. If your civs are desynchronized (different stats for different civs), reading might not show the full picture.

## Cross-Links

*   [Units Manager](units_manager.md)
*   [Unit Collections](units_collections.md)
