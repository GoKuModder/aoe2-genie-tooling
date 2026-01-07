# Task Builder

The `TaskBuilder` provides a fluent, type-safe API for adding tasks (commands) to units. Instead of remembering magic numbers for `task_type` and `action_type`, you call named methods.

## Mental Model

*   **Fluent Interface**: Accessed via `unit.add_task`.
*   **Auto-Completion**: IDEs can suggest methods like `.combat()`, `.move()`, `.build()`.
*   **Abstraction**: Hides the complexity of configuring the generic `UnitTask` structure for specific behaviors.

## Public API

### TaskBuilder (`Actual_Tools_GDP.Units.task_builder`)

Access via `unit.add_task`.

Common methods:

*   `combat(class_id, ...)`: Adds an attack task.
*   `move(...)`: Adds a move task.
*   `build(...)`: Adds a build task (villagers).
*   `gather(...)`: Adds a gather task (villagers).
*   `heal(...)`: Adds a heal task (monks).
*   `train(...)`: Adds a train task (buildings).
*   `research(...)`: Adds a research task (buildings).
*   `guard(...)`: Adds a guard task.
*   `follow(...)`: Adds a follow task.
*   `patrol(...)`: Adds a patrol task.
*   `idle(...)`: Adds an idle task.

## Workflows

### Adding a Combat Task

```python
from Actual_Tools_GDP.Datasets import UnitClass

# Add combat task targeting Archers
unit.add_task.combat(
    class_id=UnitClass.ARCHER,
    work_range=5.0
)
```

### Adding a Build Task

```python
# Villager build task
unit.add_task.build(
    work_range=1.0,
    work_value1=1.0 # Build rate
)
```

### Adding a Gather Task

```python
from Actual_Tools_GDP.Datasets import Resource

# Gather Wood
unit.add_task.gather(
    resource_in=Resource.WOOD,
    resource_out=Resource.WOOD,
    work_range=0.5,
    work_value1=0.8 # Gather rate
)
```

### Raw Task Creation

If a specific helper method doesn't exist, you can fallback to the generic `create`:

```python
# Manually specifying type and action
unit.add_task.create(
    task_type=123,
    action_type=1,
    work_value1=50
)
```

## Gotchas & Invariants

*   **Task Order**: The order of tasks matters for some AI behaviors, though generally the engine finds the correct task by its `task_type` or `action_type`.
*   **Defaults**: Most builder methods set sensible defaults for `action_type` and internal flags, but you can override them via `**kwargs`.

## Cross-Links

*   [Unit Collections](units_collections.md)
*   [Datasets](datasets.md)
