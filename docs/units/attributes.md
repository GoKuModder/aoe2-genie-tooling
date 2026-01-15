# Unit Attributes

Complete reference of all attributes available on `UnitHandle`.

## How to Read This Table

| Column | Description |
|--------|-------------|
| **Attribute** | Property name to use in code |
| **Type** | Data type (int, float, str, etc.) |
| **R/W** | Read-only (R) or Read/Write (RW) |
| **Source** | Which component the attribute comes from |
| **Description** | What the attribute controls |

---

## Core Attributes

These are direct properties of the Unit object.

| Attribute | Type | R/W | Description |
|-----------|------|-----|-------------|
| `id` | `int` | R | Unit ID (read-only) |
| `name` | `str` | RW | Internal unit name |
| `type` | `int` | RW | Unit type (10=living, 20=animal, 30=eye candy, 40=animated, 50=combat, 60=projectile, 70=creatable, 80=building) |
| `hit_points` | `int` | RW | Maximum HP |
| `line_of_sight` | `float` | RW | Vision range in tiles |
| `garrison_capacity` | `int` | RW | Number of units that can garrison |
| `speed` | `float` | RW | Movement speed |
| `class_` | `int` | RW | Unit class (0=archer, 1=infantry, etc.) |
| `enabled` | `int` | RW | Whether unit is enabled (0=disabled, 1=enabled) |
| `icon_id` | `int` | RW | Icon index in the icon SLP |
| `train_sound` | `int` | RW | Sound ID when unit starts training |
| `damage_sound` | `int` | RW | Sound ID when unit takes damage |

### Usage

```python
unit_manager = workspace.unit_manager
unit = unit_manager.get(4)

# Read
print(f"HP: {unit.hit_points}")
print(f"Speed: {unit.speed}")

# Write
unit.hit_points = 100
unit.speed = 1.5
unit.name = "CustomArcher"
```

---

## Movement/Behavior Attributes

Flattened attributes controlling search behavior, work rates, and movement.

| Attribute | Type | R/W | Description |
|-----------|------|-----|-------------|
| `default_task_id` | `int` | RW | Default task index (-1 = none) |
| `search_radius` | `float` | RW | Range for auto-target search |
| `work_rate` | `float` | RW | Base work/gather rate |
| `attack_sound` | `int` | RW | Sound ID when attacking |
| `move_sound` | `int` | RW | Sound ID when moving |
| `walking_graphic` | `int` | RW | Graphic ID for walking animation |
| `rotation_speed` | `float` | RW | How fast the unit turns |

### Usage

```python
unit.search_radius = 12.0
unit.work_rate = 0.35
unit.move_sound = 50
unit.walking_graphic = 1000
unit.rotation_speed = 0.5
```

---

## Type50 Attributes (Combat)

Flattened from the `type_50` (combat) component. Controls ranged combat.

| Attribute | Type | R/W | Description |
|-----------|------|-----|-------------|
| `base_armor` | `int` | RW | Base armor value (most armor comes from armours list) |
| `max_range` | `float` | RW | Maximum attack range |
| `min_range` | `float` | RW | Minimum attack range |
| `reload_time` | `float` | RW | Time between attacks (seconds) |
| `projectile_unit_id` | `int` | RW | Unit ID of projectile fired |
| `attack_graphic` | `int` | RW | Graphic ID for attack animation |
| `displayed_attack` | `int` | RW | Attack value shown in UI |
| `displayed_range` | `float` | RW | Range value shown in UI |
| `displayed_melee_armor` | `int` | RW | Melee armor shown in UI |
| `displayed_pierce_armor` | `int` | RW | Pierce armor shown in UI |
| `accuracy_percent` | `int` | RW | Hit chance (0-100) |
| `blast_width` | `float` | RW | Area damage radius |
| `blast_level` | `int` | RW | Blast damage falloff |

### Usage

```python
unit.max_range = 8.0
unit.reload_time = 1.5
unit.projectile_unit_id = 189  # Crossbow bolt
unit.accuracy_percent = 90
```

---

## Projectile Attributes

For projectile units (type 60). Flattened from `projectile` component.

| Attribute | Type | R/W | Description |
|-----------|------|-----|-------------|
| `projectile_type` | `int` | RW | Projectile behavior type |
| `smart_mode` | `int` | RW | Smart targeting mode |
| `hit_mode` | `int` | RW | What the projectile can hit |
| `vanish_mode` | `int` | RW | How projectile disappears |
| `projectile_arc` | `float` | RW | Arc height of trajectory |

### Usage

```python
unit_manager = workspace.unit_manager
projectile = unit_manager.get(189)
projectile.projectile_arc = 0.5
projectile.smart_mode = 1
```

---

## Creatable Attributes (Training)

For trainable units (type 70+). Flattened from `creatable` component.

| Attribute | Type | R/W | Description |
|-----------|------|-----|-------------|
| `hero_mode` | `int` | RW | Hero flags (regeneration, etc.) |
| `garrison_graphic` | `int` | RW | Graphic when garrisoned |
| `train_time` | `int` | RW | Time to train (seconds) |
| `button_id` | `int` | RW | UI button position |

### Usage

```python
unit.train_time = 20
unit.button_id = 1
unit.hero_mode = 1  # Enable hero regeneration
```

---

## Building Attributes

For buildings (type 80). Flattened from `building` component.

| Attribute | Type | R/W | Description |
|-----------|------|-----|-------------|
| `construction_graphic_id` | `int` | RW | Graphic during construction |
| `garrison_type` | `int` | RW | Types of units that can garrison |
| `tech_id` | `int` | RW | Tech required to build |

### Usage

```python
unit_manager = workspace.unit_manager
building = unit_manager.get(109)  # Town Center
building.garrison_type = 14  # Infantry + villagers
```

---

## Collection Attributes

These return lists/managers rather than single values. See dedicated pages for details.

| Attribute | Type | Description | See Page |
|-----------|------|-------------|----------|
| `attacks` | `AttacksManager` | Attack damage by class | [Attacks & Armours](attacks-armours.md) |
| `armours` | `ArmoursManager` | Armor by class | [Attacks & Armours](attacks-armours.md) |
| `tasks` | `TasksManager` | Unit tasks/actions | [Tasks](tasks.md) |
| `costs` | `CostsManager` | Training costs | - |
| `train_locations` | List | Where unit is trained | [Train Locations](train-locations.md) |
| `drop_sites` | List | Resource drop sites | Methods page |

---

## Wrapper Access

For organized access to related attributes, use wrappers:

| Wrapper | Access | Description |
|---------|--------|-------------|
| `combat` | `unit.combat` | Type50 combat attributes |
| `creatable` | `unit.creatable` | Training attributes |
| `building` | `unit.building` | Building-specific |
| `projectile` | `unit.projectile` | Projectile behavior |

```python
# These are equivalent:
unit.max_range = 8.0
unit.combat.max_range = 8.0
```

Wrappers are useful for grouping related operations:

```python
# Configure all combat settings together
unit.combat.max_range = 8.0
unit.combat.reload_time = 1.5
unit.combat.accuracy_percent = 85
unit.combat.attack_graphic = some_graphic.id
```
