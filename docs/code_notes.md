# Code Notes – aoe2-genie-tooling

> Living documentation of Actual_Tools and Datasets packages.

---

## Run Log

### 2026-01-01 18:10 UTC+2
- **Files reviewed**:
  - `Actual_Tools/Units/unit_handle.py` (658 lines)
  - `Actual_Tools/Units/unit_manager.py` (441 lines)
  - `Actual_Tools/Units/handles.py` (407 lines, 6 handle classes)
  - `Actual_Tools/Units/wrappers/` (10 wrappers)
  - `Actual_Tools/Graphics/graphic_manager.py` (331 lines)
  - `Actual_Tools/Graphics/graphic_handle.py` (573 lines)
- **Notes changes**:
  - Deep documentation of Units and Graphics modules
  - Documented all handle and wrapper classes
  - Captured method signatures and design patterns

---

## 1. Project Overview

**Purpose**: High-level Python toolkit for editing AoE2 DE `.dat` files with object-oriented wrappers.

**Design principles**:
- **Multi-civ propagation**: Changes apply to all civilizations automatically
- **Attribute flattening**: Access nested properties directly (`unit.move_sound` → `bird.move_sound`)
- **Handle pattern**: Collection items return Handle objects with their index

---

## 2. Units Module

### 2.1 UnitHandle (`Units/unit_handle.py`)

Central accessor for unit data. Wraps one or more `genieutils.unit.Unit` objects.

**Constructor**:
```python
UnitHandle(unit_id: int, dat_file: DatFile, civ_ids: Optional[List[int]] = None)
```

**Core behavior**:
- `_get_units()` – Returns list of Unit objects for enabled civs (cached)
- `_primary_unit` – First unit (reads come from here)
- `__getattr__/__setattr__` – Flattens access through `_COMPONENTS = ("bird", "dead_fish", "type_50", "projectile", "creatable", "building")`

**Wrapper properties** (return wrapper objects):
| Property | Wrapper Class | Source Component |
|----------|---------------|------------------|
| `.combat` | `Type50Wrapper` | `unit.type_50` |
| `.creatable` | `CreatableWrapper` | `unit.creatable` |
| `.cost` | `CostWrapper` | `unit.creatable.resource_costs` |
| `.bird` | `BirdWrapper` | `unit.bird` |
| `.dead_fish` | `DeadFishWrapper` | `unit.dead_fish` |
| `.projectile` | `ProjectileWrapper` | `unit.projectile` |
| `.building` | `BuildingWrapper` | `unit.building` |
| `.resource_storages` | `ResourceStoragesWrapper` | `unit.resource_storages` |
| `.damage_graphics` | `DamageGraphicsWrapper` | `unit.damage_graphics` |
| `.tasks` | `TasksWrapper` | `unit.bird.tasks` |

**Collection methods** (return Handle objects):

| Method | Returns | Description |
|--------|---------|-------------|
| `add_attack(class_, amount)` | `AttackHandle` | Add attack entry |
| `get_attack_by_id(id)` | `AttackHandle` | Get by index |
| `get_attack_by_class(class_)` | `AttackHandle` | Get by class |
| `set_attack(class_, amount)` | `AttackHandle` | Update or add |
| `remove_attack(id)` | `bool` | Remove by index |
| `add_armour(...)` | `ArmourHandle` | Same pattern |
| `add_task(...)` | `TaskHandle` | Add task with all params |
| `add_damage_graphic(...)` | `DamageGraphicHandle` | Add damage state |
| `add_train_location(...)` | `TrainLocationHandle` | Add training bldg |
| `add_drop_site(unit_id)` | `DropSiteHandle` | Add drop site |

---

### 2.2 GenieUnitManager (`Units/unit_manager.py`)

Unit CRUD operations. Extends `ToolBase`.

**Key methods**:

```python
# Create new unit (clones from template)
def create(
    name: str,
    base_unit_id: Optional[int] = None,  # Clone source
    unit_id: Optional[int] = None,       # Target ID
    enable_for_civs: Optional[List[int]] = None,
    on_conflict: Literal["error", "overwrite"] = "error",
    fill_gaps: Literal["error", "placeholder"] = "placeholder",
) -> UnitHandle

# Clone to specific ID
def clone_into(
    dest_unit_id: int,
    base_unit_id: int,
    name: Optional[str] = None,
    ...
) -> UnitHandle

# Move unit (swaps IDs)
def move(
    src_unit_id: int,
    dst_unit_id: int,
    on_conflict: Literal["error", "overwrite", "swap"] = "error",
    ...
) -> None

# Get existing unit
def get(unit_id: int, civ_ids: Optional[List[int]] = None) -> UnitHandle

# Check existence (excludes placeholders)
def exists(unit_id: int) -> bool
```

**Placeholder detection**:
```python
_is_placeholder(unit) = (unit.enabled == 0 and unit.name == "" and unit.hit_points == 1)
```

**Invariants**:
- Unit tables have identical length across all civs
- Gaps filled with placeholder units (not None)

---

### 2.3 Handle Classes (`Units/handles.py`)

Index-aware wrappers for collection items. Include their list index for removal.

| Handle | Wraps | Key Properties |
|--------|-------|----------------|
| `AttackHandle` | `AttackOrArmor` | `attack_id`, `class_`, `amount` |
| `ArmourHandle` | `AttackOrArmor` | `armour_id`, `class_`, `amount` |
| `TaskHandle` | `Task` | `task_id`, + all Task attrs |
| `DamageGraphicHandle` | `DamageGraphic` | `damage_graphic_id`, `graphic_id`, `damage_percent` |
| `TrainLocationHandle` | `TrainLocation` | `train_location_id`, `unit_id`, `button_id` |
| `DropSiteHandle` | `int` (list ref) | `drop_site_id`, `unit_id` |

---

### 2.4 Wrappers (`Units/wrappers/`)

All wrappers follow the same pattern:
1. Receive `List[Unit]` in constructor
2. `_get_*()` reads from first unit
3. `_set_all(attr, value)` writes to all units

| Wrapper | Component | Notable Properties |
|---------|-----------|-------------------|
| `Type50Wrapper` | `type_50` | `max_range`, `reload_time`, `attack_graphic`, `attacks`, `armours` |
| `CreatableWrapper` | `creatable` | `train_time`, `train_location_id`, `button_id`, `resource_costs` |
| `CostWrapper` | `creatable.resource_costs` | `food`, `wood`, `gold`, `stone` (convenience) |
| `BirdWrapper` | `bird` | `move_sound`, `attack_sound`, `work_rate`, `drop_sites`, `.tasks` |
| `DeadFishWrapper` | `dead_fish` | `walking_graphic`, `rotation_speed`, `turn_radius` |
| `ProjectileWrapper` | `projectile` | `projectile_type`, `smart_mode`, `hit_mode`, `projectile_arc` |
| `BuildingWrapper` | `building` | `construction_graphic`, `garrison_type`, `annexes`, `looting_table` |
| `TasksWrapper` | `bird.tasks` | `add_task()`, `remove_task()`, `list_tasks()`, `clear_tasks()` |
| `ResourceStoragesWrapper` | `resource_storages` | `resource_1()`, `resource_2()`, `resource_3()`, `get()`, `set()` |
| `DamageGraphicsWrapper` | `damage_graphics` | `add_damage_graphic()`, `remove_damage_graphic()` |

---

## 3. Graphics Module

### 3.1 GraphicManager (`Graphics/graphic_manager.py`)

Graphic CRUD operations. Extends `ToolBase`.

**Key methods**:
```python
# Create new graphic
def add_graphic(
    file_name: str,
    name: Optional[str] = None,
    graphic_id: Optional[int] = None,
    frame_count: int = 1,
    angle_count: int = 1,
    frame_duration: float = 0.1,
) -> GraphicHandle

# Copy graphic
def copy(source_id: int, target_id: Optional[int] = None) -> GraphicHandle

# Delete graphic (sets slot to None)
def delete(graphic_id: int) -> bool

# Search
def find_by_name(name: str) -> Optional[GraphicHandle]
def find_by_file_name(file_name: str) -> Optional[GraphicHandle]

# Clipboard operations
def copy_to_clipboard(graphic_id: int) -> bool
def paste(target_id: Optional[int] = None) -> Optional[GraphicHandle]
```

**Note**: Graphics don't have civ-specific versions. Each exists once in `dat_file.graphics`.

---

### 3.2 GraphicHandle (`Graphics/graphic_handle.py`)

Direct access to Graphic properties.

**Constructor**:
```python
GraphicHandle(graphic_id: int, dat_file: DatFile)
```

**Key properties** (read/write):
- `name`, `file_name`, `slp`
- `frame_count`, `angle_count`, `frame_duration`, `speed_multiplier`
- `sound_id`, `wwise_sound_id`
- `layer`, `player_color`, `coordinates`
- `deltas` (list of `GraphicDelta`)
- `angle_sounds` (list of `GraphicAngleSound`)

**Delta methods**:
```python
add_delta(graphic_id, offset_x=0, offset_y=0, display_angle=-1) -> DeltaHandle
remove_delta(delta_id: int) -> bool
remove_delta_by_graphic(graphic_id: int) -> bool
get_delta(delta_id: int) -> DeltaHandle
clear_deltas() -> None
```

**DeltaHandle** properties: `delta_id`, `graphic_id`, `offset_x`, `offset_y`, `display_angle`

---

## 4. Key Patterns

### Attribute Flattening
`UnitHandle.__getattr__` searches through component names to find where an attribute lives:
```python
_COMPONENTS = ("bird", "dead_fish", "type_50", "projectile", "creatable", "building")
```
Allows: `unit.move_sound = 5` instead of `unit.bird.move_sound = 5`

### Multi-Civ Propagation
All wrappers iterate over `self._units` (list of Unit from different civs) and apply changes to each.

### Handle Pattern
Collection items (attacks, tasks, etc.) return Handle objects containing both the data and the index, enabling:
- Direct property access
- Safe removal by index

---

## 5. Files Index (Units & Graphics)

| File | Lines | Purpose |
|------|-------|---------|
| `Units/unit_handle.py` | 658 | UnitHandle with attribute flattening |
| `Units/unit_manager.py` | 441 | create/clone/move/get operations |
| `Units/handles.py` | 407 | 6 handle classes for collections |
| `Units/wrappers/__init__.py` | 30 | Exports 10 wrapper classes |
| `Units/wrappers/type_50.py` | 348 | Combat stats wrapper |
| `Units/wrappers/creatable.py` | 481 | Training/creation wrapper |
| `Units/wrappers/bird.py` | 157 | Movement/tasks wrapper |
| `Units/wrappers/building.py` | 273 | Building stats wrapper |
| `Units/wrappers/tasks.py` | 242 | Tasks collection wrapper |
| `Graphics/graphic_manager.py` | 331 | add/copy/delete graphics |
| `Graphics/graphic_handle.py` | 573 | GraphicHandle + DeltaHandle |

---

## 6. Open Questions

1. How do wrappers handle units without the corresponding component (e.g., non-building unit accessing `.building`)?
   - *Observed*: Returns `None` or empty defaults gracefully
2. Is there a mechanism to copy all graphics/sounds from one unit to another?
3. What happens when `invalidate_cache()` is not called after modifying `civ_ids`?

---

*End of Code Notes*
