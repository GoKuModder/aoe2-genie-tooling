# Datasets

Type-safe IntEnum constants for Genie Editor data.

## Available Datasets

```python
from Datasets import (
    Resource,      # FOOD, WOOD, GOLD, STONE, etc.
    UnitClass,     # INFANTRY, ARCHER, CAVALRY, etc.
    Attribute,     # Object attributes for effects
    Task,          # GATHER, BUILD, ATTACK, etc.
    StoreMode,     # Resource storage flags
    Effect,        # Effect types
    TechModifier,  # Tech modification types
)
```

## Resource

```python
from Datasets import Resource

Resource.FOOD    # 0
Resource.WOOD    # 1
Resource.STONE   # 2
Resource.GOLD    # 3
```

## UnitClass

```python
from Datasets import UnitClass

UnitClass.ARCHER      # 0
UnitClass.INFANTRY    # 6
UnitClass.CAVALRY     # 12
```

## Task

```python
from Datasets import Task

Task.GATHER  # 1
Task.BUILD   # 101
Task.ATTACK  # 107
```

## Usage Example

```python
from Datasets import Resource, UnitClass

unit.class_ = UnitClass.CAVALRY
unit.resource_1(type=Resource.GOLD, amount=50.0, flag=2)
```
