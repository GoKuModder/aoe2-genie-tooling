# Actual_Tools_GDP Overview

`Actual_Tools_GDP` is a production-quality toolkit for editing Age of Empires II Definitive Edition DAT files. It wraps the high-performance `GenieDatParser` (Rust backend) with a Pythonic, object-oriented API designed for safety, productivity, and correctness.

## Core Philosophy

The library is built on four main pillars:

1.  **Safety**: Prevents common errors like invalid IDs, shared reference bugs, and silent failures.
2.  **Productivity**: Uses fluent interfaces and auto-complete friendly APIs to speed up development.
3.  **Correctness**: Handles multi-civilization data propagation automatically, ensuring your changes apply consistently across the game.
4.  **Abstraction**: Hides the raw, complex structure of the Genie Engine behind logical wrappers and handles.

## Architecture

The library is organized into a hierarchy:

1.  **Workspace (`GenieWorkspace`)**: The root object that holds the DAT file and manages all subsystems.
2.  **Managers (`*Manager`)**: Controllers for specific data types (Units, Effects, Techs). They handle creation, deletion, and searching.
3.  **Handles (`*Handle`)**: wrappers around individual data objects (e.g., a specific Unit or Tech). They provide direct access to attributes.
4.  **Wrappers (`*Wrapper`)**: Logical groupings of attributes on a Handle (e.g., `unit.combat`, `unit.building`) to organize the massive amount of data.
5.  **Builders (`*Builder`)**: Fluent interfaces for constructing complex objects like Tasks or Effect Commands.

## Key Features

### 1. Multi-Civilization Support
In the raw engine, unit data is often duplicated across civilizations. `Actual_Tools_GDP` abstracts this away. When you create or modify a unit using `UnitManager`, the changes are automatically propagated to all relevant civilizations.

### 2. Attribute Flattening
Instead of navigating deep, obscure structures like `unit.type50.projectile.smart_mode`, you can access properties directly via logical wrappers: `unit.projectile.smart_mode` or `unit.combat.attack_graphic`.

### 3. Fluent Builders
Constructing tasks and effects is simplified with builders:
```python
# Instead of manual ID lookups:
unit.add_task.combat(class_id=UnitClass.ARCHER)

# Instead of cryptic effect parameters:
effect.add_command.attribute_modifier_multiply(a=Attribute.HIT_POINTS, b=-1, c=9, d=1.5)
```

### 4. Deep Cloning
The `UnitManager` creates true deep copies of units, ensuring that modifying a clone's task list or attack table never accidentally affects the original unit.

## Migration Guide

If you are migrating from raw `genieutils` or older versions of `Actual_Tools`:

*   **Import Changes**: All imports should now come from `Actual_Tools_GDP`.
*   **Method Renames**: `add_task` -> `unit.add_task.create(...)`.
*   **Wrapper Names**: `Type50` is now `CombatWrapper`, `Creatable` is `CreationWrapper`, etc.
*   **Enums**: Use `Actual_Tools_GDP.Datasets` for all constants (Resource, UnitClass, etc.).
