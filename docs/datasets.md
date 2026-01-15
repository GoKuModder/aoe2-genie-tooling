# Datasets

The Datasets module provides typed enumerations and constants for common game values.

Using these enums instead of raw integers makes code more readable and reduces errors.

## Quick Example

```python
from Actual_Tools_GDP import GenieWorkspace
from Actual_Tools_GDP.Datasets import Attribute, Resource, Task, UnitClass

workspace = GenieWorkspace.load("empires2_x2_p1.dat")

# Use enums instead of magic numbers
unit = workspace.unit_manager.get(4)

# Instead of: effect.add_command.attribute_modifier_add(a=4, b=0, c=-1, d=10)
effect.add_command.attribute_modifier_add(
    a=4,
    b=Attribute.HIT_POINTS,  # Much clearer than "0"
    c=-1,
    d=10
)
```

---

## Attribute

Unit attribute IDs used in effect commands.

```python
from Actual_Tools_GDP.Datasets import Attribute
```

| Enum | Value | Description |
|------|-------|-------------|
| `HIT_POINTS` | 0 | Maximum HP |
| `LINE_OF_SIGHT` | 1 | Vision range |
| `GARRISON_CAPACITY` | 2 | Garrison slots |
| `UNIT_SIZE_X` | 3 | Collision X |
| `UNIT_SIZE_Y` | 4 | Collision Y |
| `MOVEMENT_SPEED` | 5 | Speed |
| `ROTATION_SPEED` | 6 | Turn speed |
| `ARMOR` | 8 | Base armor |
| `ATTACK` | 9 | Base attack |
| `ATTACK_RELOAD_TIME` | 10 | Attack speed |
| `ACCURACY_PERCENT` | 11 | Hit chance |
| `MAX_RANGE` | 12 | Attack range |
| `WORK_RATE` | 13 | Gather/build rate |
| `RESOURCE_CAPACITY` | 14 | Carry capacity |
| `PROJECTILE_UNIT` | 16 | Projectile unit ID |
| `ICON_ID` | 17 | Icon index |
| `TRAIN_TIME` | 19 | Creation time |
| `TRAIN_LOCATION` | 20 | Where trained |
| `BLAST_WIDTH` | 21 | Area damage width |
| `BONUS_DAMAGE_RESISTANCE` | 24 | Cavalry armor |
| ... | ... | See full list in source |

### Usage

```python
# In effect commands
effect.add_command.attribute_modifier_add(
    a=4,                         # Archer unit ID
    b=Attribute.MAX_RANGE,       # Range attribute
    c=-1,
    d=2                          # +2 range
)

effect.add_command.attribute_modifier_multiply(
    a=-1,                        # All units
    b=Attribute.MOVEMENT_SPEED,  # Speed
    c=-1,
    d=1.1                        # +10% speed
)
```

---

## Resource

Resource type IDs.

```python
from Actual_Tools_GDP.Datasets import Resource
```

| Enum | Value | Description |
|------|-------|-------------|
| `FOOD` | 0 | Food |
| `WOOD` | 1 | Wood |
| `STONE` | 2 | Stone |
| `GOLD` | 3 | Gold |
| `POPULATION_HEADROOM` | 4 | Available pop space |
| `CONVERSION_RANGE` | 5 | Monk range |
| `CURRENT_AGE` | 6 | Current age |
| `RELICS_CAPTURED` | 7 | Relics held |
| `TRADE_BONUS` | 8 | Trade profit |
| `CURRENT_POPULATION` | 11 | Current pop |
| `CORPSE_DECAY_TIME` | 12 | Decay timer |
| `BONUS_POPULATION_CAP` | 32 | Pop cap bonus |
| ... | ... | See full list |

### Usage

```python
# Set starting resources
civ.resource[Resource.FOOD] = 500
civ.resource[Resource.GOLD] = 200

# In effect commands
effect.add_command.resource_modifier(
    a=Resource.GOLD,
    d=500  # +500 gold
)
```

---

## Task

Unit task/action type IDs for TaskBuilder.

```python
from Actual_Tools_GDP.Datasets import Task
```

| Enum | Value | Description |
|------|-------|-------------|
| `NONE` | 0 | No action |
| `MOVE_TO` | 1 | Move to location |
| `FOLLOW` | 2 | Follow unit |
| `GARRISON` | 3 | Garrison |
| `EXPLORE` | 4 | Auto-explore |
| `GATHER` | 5 | Gather resource |
| `GRAZE` | 6 | Graze (animals) |
| `COMBAT` | 7 | Attack |
| `SHOOT` | 8 | Ranged attack |
| `ATTACK` | 9 | Melee attack |
| `FLY` | 10 | Fly |
| `SCARE_HUNT` | 11 | Scare prey |
| `UNLOAD` | 12 | Unload transport |
| `GUARD` | 13 | Guard unit |
| `BUILD` | 101 | Construct building |
| `MAKE_UNIT` | 102 | Train unit |
| `MAKE_TECH` | 103 | Research tech |
| `CONVERT` | 104 | Convert enemy |
| `HEAL` | 105 | Heal friendly |
| `REPAIR` | 106 | Repair building |
| `TRADE` | 111 | Trade with market |
| `RESOURCE_GENERATION` | 151 | Passive income |
| `AURA` | 155 | Area buff |
| ... | ... | See TaskBuilder for all types |

### Usage

```python
# When using raw create_task
unit.create_task(action_type=Task.COMBAT, class_id=0)

# TaskBuilder uses these internally
unit.add_task.combat(class_id=0)  # Same as Task.COMBAT
```

---

## UnitClass

Unit class IDs for targeting.

```python
from Actual_Tools_GDP.Datasets import UnitClass
```

| Enum | Value | Description |
|------|-------|-------------|
| `ARCHER` | 0 | Archers |
| `INFANTRY` | 1 | Infantry |
| `CAVALRY` | 2 | Cavalry |
| `SIEGE` | 3 | Siege weapons |
| `BUILDING` | 11 | Buildings |
| `VILLAGER` | 4 | Villagers |
| `MONK` | 18 | Monks |
| `SHIP` | 22 | Ships |
| `WALL` | 27 | Walls |
| `GATE` | 28 | Gates |
| `TOWER` | 52 | Towers |
| ... | ... | See full list |

### Usage

```python
# Tasks targeting a class
unit.add_task.combat(class_id=UnitClass.INFANTRY)

# Effect commands targeting a class
effect.add_command.attribute_modifier_add(
    a=-1,                    # All units in class
    b=Attribute.HIT_POINTS,
    c=UnitClass.CAVALRY,     # Target cavalry
    d=20                     # +20 HP
)
```

---

## Effect (Command Types)

Effect command type IDs.

```python
from Actual_Tools_GDP.Datasets import Effect
```

| Enum | Value | Description |
|------|-------|-------------|
| `ATTRIBUTE_MODIFIER_SET` | 0 | Set attribute |
| `RESOURCE_MODIFIER` | 1 | Modify resource |
| `ENABLE_DISABLE_UNIT` | 2 | Enable/disable |
| `UPGRADE_UNIT` | 3 | Upgrade unit |
| `ATTRIBUTE_MODIFIER_ADD` | 4 | Add to attribute |
| `ATTRIBUTE_MODIFIER_MULTIPLY` | 5 | Multiply attribute |
| `RESOURCE_MODIFIER_MULTIPLY` | 6 | Multiply resource |
| `SPAWN_UNIT` | 7 | Spawn units |
| `MODIFY_TECH` | 8 | Modify tech |
| `TEAM_ATTRIBUTE_MODIFIER_SET` | 10 | Team set attr |
| `TEAM_RESOURCE_MODIFIER` | 11 | Team resource |
| `TEAM_ENABLE_DISABLE_UNIT` | 12 | Team enable |
| `TEAM_UPGRADE_UNIT` | 13 | Team upgrade |
| ... | ... | See EffectCommandBuilder |

### Usage

```python
# When using raw new_command
effect.new_command(type=Effect.ATTRIBUTE_MODIFIER_ADD, a=4, b=0, d=10)

# EffectCommandBuilder is clearer
effect.add_command.attribute_modifier_add(a=4, b=0, d=10)
```

---

## Importing Multiple Datasets

```python
from Actual_Tools_GDP.Datasets import (
    Attribute,
    Resource,
    Task,
    UnitClass,
    Effect,
)

# Now use them throughout your code
unit.hit_points = 100
effect.add_command.attribute_modifier_add(
    a=4,
    b=Attribute.MAX_RANGE,
    c=UnitClass.ARCHER,
    d=2
)
```

---

## Benefits of Using Datasets

1. **Readability**: `Attribute.HIT_POINTS` is clearer than `0`
2. **Autocomplete**: IDEs can suggest values
3. **Error Prevention**: Typos become syntax errors instead of silent bugs
4. **Documentation**: Enums serve as inline documentation
