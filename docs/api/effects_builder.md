# Effect Command Builder

The `EffectCommandBuilder` is a fluent interface for adding commands to an effect. It replaces the error-prone process of looking up "Effect Type IDs" with explicit method calls.

## Mental Model

*   **Fluent Interface**: Accessed via `effect.add_command`.
*   **Categories**: Commands are grouped by target (Self, Team, Enemy, Neutral, Gaia).
*   **Type Safety**: Methods like `attribute_modifier_add` clearly indicate intent, unlike `type=4`.

## Public API

### EffectCommandBuilder (`Actual_Tools_GDP.Effects.effect_command_builder`)

Access via `effect.add_command`.

#### Core Commands (Self / Player)

*   `attribute_modifier_set/add/multiply(...)`: Modify unit stats (HP, Attack, etc.).
*   `resource_modifier(...)`: Modify resource stockpiles.
*   `enable_disable_unit(...)`: Enable/disable units (tech tree).
*   `upgrade_unit(...)`: Upgrade a unit to another ID (e.g., Militia -> Man-at-Arms).
*   `research_tech(...)`: Force research a tech.
*   `tech_cost_modifier(...)`: Change tech costs.

#### Team Commands

*   `team_attribute_modifier(...)`: Apply to team members.
*   `team_resource_modifier(...)`: Apply to team members.

#### Enemy/Neutral/Gaia Commands

*   `enemy_...`: Apply to enemies.
*   `neutral_...`: Apply to neutral players.
*   `gaia_...`: Apply to Gaia (nature).

## Workflows

### Modifying Unit Attributes

This is the most common use case (e.g., Blacksmith upgrades).

```python
from Actual_Tools_GDP.Datasets import Attribute, UnitClass

# +1 Range for Archers
effect.add_command.attribute_modifier_add(
    a=UnitClass.ARCHER,
    b=Attribute.MAX_RANGE,
    d=1.0
)
```

### Upgrading a Unit

```python
# Militia (74) -> Man-at-Arms (75)
effect.add_command.upgrade_unit(
    a=74, # From
    b=75  # To
)
```

### Enabling/Disabling Units

Used for Civ Bonuses that unlock units.

```python
# Enable Hand Cannoneer
effect.add_command.enable_disable_unit(
    a=UnitClass.HAND_CANNONEER,
    b=1 # 1 = Enable
)
```

## Gotchas & Invariants

*   **Parameter Mapping**: The builder maps parameters to `A`, `B`, `C`, `D`.
    *   `attribute_modifier`: A=Unit/Class, B=Attribute, D=Value.
    *   `resource_modifier`: A=Resource, B=Mode, D=Value.
    *   `upgrade_unit`: A=From, B=To.
*   **Float vs Int**: Attribute modifiers usually use `D` (float) for the value, even for integer attributes like Armor.
*   **Legacy Types**: The builder supports all DE command types, including legacy AOK/AOC types that may behave oddly.

## Cross-Links

*   [Effects Handle](effects_handle.md)
*   [Datasets](datasets.md)
