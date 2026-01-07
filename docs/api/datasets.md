# Datasets & Constants

The `Actual_Tools_GDP.Datasets` module provides helpful Enums and constants for working with Genie Engine data.

## Usage

```python
from Actual_Tools_GDP.Datasets import Attribute, UnitClass

# Use Enum instead of magic numbers
unit.attribute_modifier(
    attr=Attribute.HIT_POINTS,
    value=10
)

if unit.class_ == UnitClass.ARCHERY:
    print("It's an archery unit")
```

## Available Enums

### Attributes
- `Attribute`: IDs for unit attributes (e.g., `HIT_POINTS`, `LINE_OF_SIGHT`).
- `GarrisonType`
- `HeroStatus`
- `UnitTrait`

### Units
- `UnitClass`: IDs for unit classes (e.g., `INFANTRY`, `ARCHERY`).
- `UnitType`: IDs for unit types.

### Techs & Effects
- `Effect`: IDs for effect types.
- `TechModifier`: IDs for modification types (Add, Multiply, Set).
- `TechCostType`: IDs for cost types.
- `TechType`

### Resources
- `Resource`: IDs for resources (e.g., `FOOD`, `WOOD`, `GOLD`).
- `StoreMode`

### Tasks
- `Task`: IDs for unit tasks (e.g., `BUILD`, `ATTACK`).
- `TargetDiplomacy`
