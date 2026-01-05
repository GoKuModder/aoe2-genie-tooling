# A15-Tab_Unit — Tables & Units

**Source modules:**
*   `src/sections/terrain_table_data/terrain_table_data.py`
*   `src/sections/terrain_table_data/terrain_table.py`
*   `src/sections/terrain_table_data/terrain_pass_graphic.py`
*   `src/sections/unit_data/unit_data.py`
*   `src/sections/unit_data/unit_line.py`
*   `src/sections/unit_data/unit_task.py`

**Purpose:**
This set of modules defines the data structures for terrain interaction tables and unit definitions within the Genie Engine `.dat` file.
*   `terrain_table_data`: Defines how different units are affected by and interact with various terrain types. This includes damage multipliers and graphical representations for movement.
*   `unit_data`: Defines the fundamental properties of units, including their names, types, and the tasks they can perform.

**Key Objects:**
*   `TerrainTableData`: The top-level container for terrain interaction data. It holds a list of `TerrainTable` objects, one for each unit class.
*   `TerrainTable`: Contains lists of damage multipliers and `TerrainPassGraphic` objects, indexed by terrain type.
*   `TerrainPassGraphic`: Specifies the sprite IDs used for units moving across different terrain types (entering, exiting, walking).
*   `UnitData`: The main container for unit information, holding lists of `UnitLine` and `UnitTask` objects.
*   `UnitLine`: Defines a line of units (e.g., the Militia line) with a shared name and a list of unit IDs belonging to it.
*   `UnitTask`: A detailed structure defining a single action a unit can perform, such as gathering resources, attacking, or building. It includes properties for resource costs, work rates, targeting parameters, and associated sound/sprite IDs.

**Binary Layout Notes:**
*   The structures heavily utilize the `bfp_rs` library for declarative binary parsing.
*   `TerrainTableData` uses `num_terrain_tables` and `num_used_terrains` read from the file to dynamically determine the repetition count for its internal lists. This is a common pattern in the parser.
*   `UnitData` uses version-aware `Retriever` fields to handle different `.dat` file versions, particularly for `unit_lines` and `tasks`. The `tasks` field is a nested array structure (`Array32[Option8[Array16[UnitTask]]]`), indicating a complex layout with optional and repeated data blocks.
*   Pointers (`_terrain_table_float_pttrs`, `_terrain_pass_graphic_ptrs`) are present but their dereferencing logic is handled by the `bfp_rs` framework's `on_read` callbacks, abstracting the manual pointer-following from the class definition.

**Cross-Dependencies:**
*   `TerrainTableData` is a high-level section, likely included directly in the main `DatFile` structure.
*   The `num_used_terrains` value in `TerrainTableData` is used by `TerrainTable` to determine the size of its `passable_buildable_dmg_mult` and `terrain_pass_graphics` lists. This shows a tight coupling where a parent's attribute dictates a child's structure.
*   `UnitData` and its sub-objects are fundamental data structures referenced by many other parts of the `.dat` file, particularly `Civilization` data, which defines which units are available.

**Integration Notes:**
*   When modifying terrain interactions, a developer must ensure that the `num_terrain_tables` and `num_used_terrains` counts are kept in sync with the actual list lengths to prevent parsing errors or data corruption on save.
*   The `UnitTask` structure is highly detailed and central to defining unit behavior. Adding or modifying unit abilities would involve creating or altering these `UnitTask` objects.
*   The use of `RetrieverCombiner` in `TerrainPassGraphic` for `replication_amount` shows a pattern for handling fields that have moved between different file versions, providing a unified public API.

**Open Questions:**
*   The exact purpose of `work_mode` in `UnitTask` is marked as "unused?". Is this legacy data, or does it have a subtle effect?
*   What is the significance of the various pointer fields in `TerrainTableData`? How are they resolved during parsing, and are they just for reading, or do they need to be managed when writing?
*   How are `UnitLine` objects associated with the actual `Unit` objects defined elsewhere in the file? Is it by the `id` field or by convention?
