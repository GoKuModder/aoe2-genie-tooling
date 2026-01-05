# A02-Civ_Unit — Civilization
Source modules: `GenieDatParser/src/sections/civilization/unit.py`
Purpose: This module defines the binary structure of a "Unit" entity within the Genie Engine's `.dat` file format. It uses the `bfp_rs` library to map class attributes to the specific byte-level layout of the data, accounting for different versions of the `.dat` file format (e.g., Age of Empires 1, Age of Empires 2, HD, DE).
Key Objects: 
- `Unit`: A `BaseStruct` class that represents a single unit. Its attributes are defined using `Retriever` and `RetrieverCombiner` objects from the `bfp_rs` library, which specify the data type, version constraints, and default values for each field in the binary structure.
Binary Layout Notes: 
- The file uses `Retriever` objects to define each field's size, type (e.g., `i16`, `f32`, `str16`), and byte order (little-endian).
- Versioning is heavily used (`min_ver`, `max_ver`) to handle variations in the `.dat` format across different game versions. `RetrieverCombiner` is used to create a single logical attribute from multiple version-specific fields.
- Conditional parsing is implemented using `on_read` hooks. For example, the `disable_types` function dynamically includes or excludes nested structures (`AnimationInfo`, `CombatInfo`, etc.) based on the value of the `type_` field.
- Dynamic length fields (like `_name_aoe1`) are handled with `on_read` and `on_write` hooks that sync a length field with the actual data field.
Cross-Dependencies: 
- `bfp_rs`: The core library used for binary format parsing.
- `sections.civilization.type_info`: Imports several `*Info` classes (`AnimationInfo`, `MovementInfo`, `TaskInfo`, etc.) which are nested substructures within the `Unit` object.
- `sections.civilization.unit_damage_sprite`: Imports `UnitDamageSprite` for handling damage graphics.
- `sections.civilization.unit_resource`: Imports `UnitResource` for defining resource costs and storage.
Integration Notes: The `Unit` class is designed to be part of a larger parsing system. It is likely instantiated and managed by a higher-level class (such as `DatFile` as seen in the `README.md`) that reads the entire `.dat` file and iterates through the civilization/unit data sections. The `on_write` hooks (e.g., `sync_ids`) ensure data consistency when modifying and saving the file.
Open Questions: 
- The `scx_trigger_data1` and `scx_trigger_data2` fields are marked with a `todo: investigate this`, indicating their purpose is not fully understood.
- The exact conditions under which the various nested `*Info` substructures are enabled or disabled could be further analyzed to fully map out the unit type system.
- The integration with the Wwise audio engine (indicated by `wwise_*` fields) is a modern addition for Definitive Edition and its specific usage could be explored.
