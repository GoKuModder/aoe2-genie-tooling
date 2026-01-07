# Datasets (Constants)

The `Actual_Tools_GDP.Datasets` package contains `IntEnum` classes that represent the various magic numbers used by the Genie Engine. Using these is strongly recommended over raw integers for readability and safety.

## Mental Model

*   **Typed Constants**: Instead of remembering that `Class 4` is Archer, use `UnitClass.ARCHER`.
*   **Safety**: IDEs can show you available options, preventing typos.
*   **Documentation**: The Enums often contain comments explaining obscure flags (like `Attribute.SMART_PROJECTILE`).

## Public API

### Common Datasets

*   `Resource`: Resource IDs (Gold, Wood, Food, but also stats like `ATHEISM` or `ENABLE_MONK_CONVERSION`).
*   `UnitClass`: Unit Classes (Archer, Infantry, Cavalry, etc.).
*   `Attribute`: Object Attributes for effect commands (Hit Points, Range, Line of Sight).
*   `Task`: Unit Task Types (Task 101 = Build, etc.).
*   `Effect`: Effect Command Types (Type 10 = Research Tech, etc.). Note: `TaskBuilder` and `EffectCommandBuilder` hide these mostly.
*   `TechModifier`: Modes for tech cost modification (Set, Add, Subtract).
*   `StoreMode`: Flags for resource storage (Carry vs Drop).

## Workflows

### Using Attributes in Effects

```python
from Actual_Tools_GDP.Datasets import Attribute, UnitClass

# Add +10 HP to Archers
effect.add_command.attribute_modifier_add(
    a=UnitClass.ARCHER,
    b=Attribute.HIT_POINTS,
    d=10.0
)
```

### Checking Unit Class

```python
from Actual_Tools_GDP.Datasets import UnitClass

if unit.class_ == UnitClass.CAVALRY:
    print("This is a cavalry unit")
```

### Setting Resource Storage Mode

```python
from Actual_Tools_GDP.Datasets import StoreMode, Resource

# Unit drops food when killed (like a Sheep)
unit.resource_storages.add(
    type=Resource.FOOD,
    amount=100,
    flag=StoreMode.DROP # 2
)
```

## Gotchas & Invariants

*   **Version Differences**: Some constants (especially higher IDs) are only valid for Definitive Edition. The library includes comprehensive lists, but using a DE-only constant on an older dataset might do nothing or cause a crash.
*   **Missing Values**: If you find a magic number not in the Enum, you can still use the raw integer. The library accepts `int` where Enums are expected.

## Cross-Links

*   [Unit Collections](../units/units_collections.md)
*   [Effects Manager](../effects/effects_manager.md)
