# Validation

The `Validator` system ensures data integrity by checking attributes and references.

## Overview

The validator performs several types of checks:

1. **Attribute Allow-Lists** - Prevents typos in flattened attributes
2. **Reference Validation** - Ensures referenced IDs exist
3. **Type Validation** - Checks that correct types are used
4. **Index Bounds** - Validates list indices are in range

---

## Attribute Allow-Lists

When accessing flattened attributes on handles, the validator can catch typos:

```python
unit_manager = workspace.unit_manager
unit = unit_manager.get(4)

# Correct
unit.hit_points = 100  # ✓ Valid attribute

# Typo - would fail if validation is enabled
unit.hitpoints = 100   # ✗ Not in allow-list
```

If the attribute is not in the registered allow-list, you'll get an `AttributeError` with a helpful message suggesting the correct attribute name.

---

## Reference Validation

Before saving, you can validate that all references point to existing objects:

```python
# Validate all references
validator = workspace.validator
issues = validator.validate_all_references(workspace)

if issues:
    print("Issues found:")
    for issue in issues:
        print(f"  - {issue}")
else:
    print("All references valid!")
    workspace.save("output.dat")
```

This checks:
- Graphic IDs referenced by units exist
- Sound IDs referenced by units exist
- Effect IDs referenced by techs exist
- And more...

---

## Validation Levels

The workspace can be configured with different validation levels:

```python
from aoe2_genie_tooling import GenieWorkspace
from aoe2_genie_tooling.Base.config import ValidationLevel

# No validation (fastest)
workspace = GenieWorkspace.load("input.dat", validation=ValidationLevel.NO_VALIDATION)

# Validate only newly created objects (default)
workspace = GenieWorkspace.load("input.dat", validation=ValidationLevel.VALIDATE_NEW)

# Validate everything including existing objects
workspace = GenieWorkspace.load("input.dat", validation=ValidationLevel.VALIDATE_ALL)
```

| Level | Description | Performance |
|-------|-------------|-------------|
| `NO_VALIDATION` | Skip all validation | Fastest |
| `VALIDATE_NEW` | Only check session-created objects | Balanced |
| `VALIDATE_ALL` | Check all objects including existing | Slowest |

---

## ID Resolution

The validator provides ID resolution to accept multiple input types:

```python
# These all work when setting graphic IDs:
unit.standing_graphic_1 = 100              # Raw integer
unit.standing_graphic_1 = graphic_handle   # Handle object
unit.standing_graphic_1 = "abc-123-uuid"   # UUID string (if registered)
```

Behind the scenes, the validator resolves handles and UUIDs to integer IDs.

---

## Type Safety

The validator checks that the correct handle types are passed:

```python
# Passing wrong handle type will raise an error
effect_manager = workspace.effect_manager
effect_handle = effect_manager.get(100)

# This would fail - wrong type
unit.standing_graphic_1 = effect_handle  # ✗ Expected GraphicHandle, got EffectHandle
```

The error message will tell you exactly what type was expected vs. received.

---

## Manual Validation

You can manually validate specific things:

```python
validator = workspace.validator

# Validate a graphic ID is in range
validator.validate_graphic_id(100, max_id=len(workspace.dat.sprites))

# Validate an index is within a collection
validator.validate_index(
    index=5,
    collection=some_list,
    name="delta_id",
    hints=["Check len(graphic.deltas) before accessing"]
)
```

---

## Best Practices

### Validate Before Saving Production Files

```python
validator = workspace.validator
if not validator.validate_all_references(workspace):
    workspace.save("output.dat")
else:
    print("Fix validation issues first!")
```

### Use Typed Enums

Using enums from `Datasets` helps prevent invalid values:

```python
from aoe2_genie_tooling.Datasets import Attribute

# Good - enum catches typos at write time
effect.add_command.attribute_modifier_add(b=Attribute.HIT_POINTS)

# Risky - typo in magic number is silent
effect.add_command.attribute_modifier_add(b=99)  # Is 99 valid?
```

### Check Existence Before Access

```python
# Don't assume IDs exist
graphic_manager = workspace.graphic_manager
if graphic_manager.exists(graphic_id):
    graphic = graphic_manager.get(graphic_id)
```
