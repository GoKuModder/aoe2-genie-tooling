# A03-Civ_TypeA — Civilization
Source modules: `building_info.py`, `combat_info.py`, `creation_info.py`

## Purpose
These modules define the data structures for building-specific, combat-related, and unit creation attributes within the Genie Engine `.dat` file. They are part of a larger system for parsing version-aware civilization and unit data.

## Key Objects
- **`BuildingInfo`**: Defines attributes specific to buildings, such as construction/destruction sprites, garrison capabilities, and attached annexes.
- **`CombatInfo`**: Defines combat-related attributes, including attack values, armor classes, weapon offsets, and reload times. It uses a `RetrieverCombiner` to handle different `base_armor` values across various game versions.
- **`CreationInfo`**: Defines attributes related to unit creation, such as resource costs, training times, and hero-specific properties.
- **`TrainLocation`**: A nested structure within `CreationInfo` that specifies where a unit can be trained and the associated UI button.

## Binary Layout Notes
- All three modules heavily rely on the `bfp_rs` library for declarative binary parsing.
- The `Retriever` class is used to define fields with their corresponding data types (e.g., `i16`, `f32`) and version constraints (`min_ver`, `max_ver`). This allows the parser to adapt to different `.dat` file versions.
- Default values and factory functions (`default`, `default_factory`) are specified to handle missing data in older file versions.
- Structures like `Array` and `Array16` are used to parse sequences of nested objects, such as `DamageClass` lists in `CombatInfo` and `UnitCost` lists in `CreationInfo`.

## Cross-Dependencies
- These modules are clearly intended to be part of a larger, composite data structure representing a unit or civilization. They likely do not stand alone.
- They import and use other low-level data structures from within the same `type_info` directory, such as `BuildingAnnex`, `LootingTable`, `DamageClass`, and `UnitCost`.

## Integration Notes
- When integrating these modules, the top-level parser must provide the correct `Version` object to ensure that fields are read correctly according to the `.dat` file's version.
- The `RetrieverCombiner` in `CombatInfo` demonstrates a pattern for handling fields that have different data types or locations across major file versions.
- The use of `default_factory` with lambda functions is a key pattern for initializing nested structures and lists.

## Open Questions
- It is not immediately clear how these individual `Info` classes are aggregated. What is the parent object that contains `BuildingInfo`, `CombatInfo`, and `CreationInfo` instances?
- The exact context for the `Version` object (e.g., from which part of the `.dat` file it's derived) is not specified within these modules and is likely managed by a higher-level parser.
