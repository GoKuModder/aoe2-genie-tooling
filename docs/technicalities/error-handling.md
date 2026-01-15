# Error Handling

`Actual_Tools_GDP` provides specific exception types to help you handle errors gracefully.

## Exception Types

### InvalidIdError

Raised when an ID is out of range or references a non-existent object.

```python
from Actual_Tools_GDP.Base.core.exceptions import InvalidIdError

try:
    unit = workspace.unit_manager.get(99999)  # ID doesn't exist
except InvalidIdError as e:
    print(f"Invalid ID: {e}")
```

**Common Causes:**
- Requesting a unit/graphic/sound ID that doesn't exist
- Using an ID that's out of range
- Referencing a deleted object

**Properties:**
- `e.hints` - List of suggestions for fixing the issue
- `e.context` - Additional context about where the error occurred
- `e.action_description` - What was being attempted

---

### ValidationError

Raised when data validation fails.

```python
from Actual_Tools_GDP.Base.core.exceptions import ValidationError

try:
    # Some operation that fails validation
    pass
except ValidationError as e:
    print(f"Validation failed: {e}")
```

---

### TemplateNotFoundError

Raised when trying to clone from a non-existent template.

```python
from Actual_Tools_GDP.Base.core.exceptions import TemplateNotFoundError

try:
    # Trying to clone from a unit that doesn't exist
    unit = workspace.unit_manager.create("New Unit", base_unit_id=99999)
except TemplateNotFoundError as e:
    print(f"Template not found: {e}")
```

---

### UnitIdConflictError

Raised when creating a unit at an ID that's already occupied.

```python
from Actual_Tools_GDP.Base.core.exceptions import UnitIdConflictError

try:
    # ID 4 (Archer) already exists
    unit = workspace.unit_manager.create("New Unit", unit_id=4, on_conflict="error")
except UnitIdConflictError as e:
    print(f"ID conflict: {e}")
```

**Solution:** Use `on_conflict="overwrite"` or choose a different ID.

---

### GapNotAllowedError

Raised when an operation would create gaps in ID sequences.

```python
from Actual_Tools_GDP.Base.core.exceptions import GapNotAllowedError

try:
    # Creating at ID 5000 when max is 2000 would create gaps
    unit = workspace.unit_manager.create("New Unit", unit_id=5000, fill_gaps="error")
except GapNotAllowedError as e:
    print(f"Gap error: {e}")
```

**Solution:** Use `fill_gaps="placeholder"` to auto-fill gaps with placeholders.

---

## Best Practices

### Check Before Operating

```python
# Check existence first
if workspace.unit_manager.exists(unit_id):
    unit = workspace.unit_manager.get(unit_id)
else:
    print(f"Unit {unit_id} doesn't exist")

# Or use find_by_name which returns None
unit = workspace.unit_manager.find_by_name("ARCHR")
if unit:
    unit.hit_points = 100
```

### Use try/except for Critical Operations

```python
from Actual_Tools_GDP.Base.core.exceptions import InvalidIdError, TemplateNotFoundError

def create_custom_unit(workspace, name, base_id):
    try:
        unit = workspace.unit_manager.create(name, base_unit_id=base_id)
        return unit
    except TemplateNotFoundError:
        print(f"Base unit {base_id} doesn't exist, using default")
        unit = workspace.unit_manager.create(name)
        return unit
    except InvalidIdError as e:
        print(f"Failed to create unit: {e}")
        return None
```

### Validate Before Saving

```python
# Check for issues before saving
issues = workspace.validator.validate_all_references(workspace)
if issues:
    print("Validation issues found:")
    for issue in issues:
        print(f"  - {issue}")
else:
    workspace.save("output.dat")
```

---

## Importing Exceptions

```python
from Actual_Tools_GDP.Base.core.exceptions import (
    GenieToolsError,        # Base exception for all library errors
    InvalidIdError,
    ValidationError,
    TemplateNotFoundError,
    UnitIdConflictError,
    GapNotAllowedError,
)
```

`GenieToolsError` is the base class - catch it to handle any library exception:

```python
try:
    # Any library operation
    pass
except GenieToolsError as e:
    print(f"Library error: {e}")
```
