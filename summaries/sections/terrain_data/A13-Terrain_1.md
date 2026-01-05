# A13-Terrain_1 — Terrain Data

**Source modules**: `GenieDatParser/src/sections/terrain_data/terrain.py`, `GenieDatParser/src/sections/terrain_data/terrain_data.py`

## Purpose
These modules define the binary structure for terrain definitions within the Genie Engine's `.dat` file format. `Terrain` represents a single terrain type (grass, water, etc.), while `TerrainData` is the container that holds all terrain definitions, tile sizes, and terrain borders.

## Key Objects

### `Terrain` (terrain.py)
A `BaseStruct` class representing a single terrain entry with attributes:
- **Identity**: `enabled`, `random`, `type`, `internal_name`, `slp_filename`, `slp_id`
- **Editor**: `hide_in_editor`, `str_id` (string table reference)
- **Rendering**: `blend_priority`, `blend_mode`, `overlay_mask_name`
- **Minimap Colors**: `map_color_high`, `map_color_medium`, `map_color_low`, `map_color_cliff_left`, `map_color_cliff_right`
- **Pathfinding**: `passable_terrain`, `impassable_terrain`
- **Animation**: `animation` (TerrainAnimation), `elevation_sprites` (Array[19][TerrainSpriteFrame])
- **Layout**: `terrain_to_draw`, `rows`, `cols`, `borders` (version-dependent array)
- **Units**: `units` (StackedAttrArray[30][TerrainUnit]), `num_units_used`
- **Audio (DE)**: `sound_id`, `wwise_sound_id`, `wwise_stop_sound_id`

### `TerrainData` (terrain_data.py)
A `BaseStruct` class serving as the container for all terrain data:
- **Tile Config**: `tile_sizes` (Array[19][TileSize])
- **Terrains**: `terrains` (version-dependent: 32 for AoE1/AoK, 42 for AoC, 100 for HD, 55 for SWGB, 200 for DE2)
- **Borders**: `terrain_border` (Array[16][TerrainBorder]) - only for versions up to SWGB
- **Map Bounds**: `_map_min_x`, `_map_min_y`, `_map_max_x`, `_map_max_y` (floats)
- **Tile Dimensions**: `_tile_width`, `_tile_height`, `_tile_half_height`, `_tile_half_width`, `_elev_height`

## Binary Layout Notes
- Heavy use of `RetrieverCombiner` to unify version-specific fields into single attributes (e.g., `internal_name` combines DE2, AoE2, DE1, AoE1, SWGB variants).
- Version branching via `min_ver`/`max_ver` for different game editions:
  - AoE1: `Version(3, 7)` - 32 terrains
  - DE1: `Version(4, 5)` - 96 terrains
  - AoK: `Version(5, 7, 0)` - 32 terrains
  - AoC: `Version(5, 7, 1)` - 42 terrains
  - HD: `Version(5, 7, 2)` - 100 terrains
  - SWGB: `Version(5, 9)` - 55 terrains
  - DE2: `Version(7, 1)` - 200 terrains
- The `borders` array size varies by version (32, 42, 55, 96, or 100 entries).
- `elevation_sprites` is a fixed array of 19 `TerrainSpriteFrame` objects for rendering different elevation levels.

## Cross-Dependencies
- `bfp_rs`: Core binary format parsing library.
- `sections.terrain_data.terrain_sprite_frame`: `TerrainSpriteFrame` for elevation graphics.
- `sections.terrain_data.terrain_animation`: `TerrainAnimation` for animated terrains.
- `sections.terrain_data.terrain_unit`: `TerrainUnit` for objects placed on terrain.
- `sections.terrain_data.terrain_border`: `TerrainBorder` for terrain edge blending.
- `sections.terrain_data.tile_size`: `TileSize` for tile dimension definitions.

## Integration Notes
`TerrainData` is instantiated as part of the larger `DatFile` parsing hierarchy. The `terrains` list contains all terrain definitions, indexed by terrain ID. When modifying terrain properties (e.g., changing minimap colors or passability), changes are made to individual `Terrain` objects within this list. The `terrain_border` system (pre-DE2) handles visual blending between adjacent terrain types.

## Open Questions
- The `phantom` field purpose is unclear - appears in multiple versions but usage undefined.
- Many internal fields prefixed with `_` (e.g., `_vtable_ptr`, `_map_ptr`, `_search_map_ptr`) are runtime pointers with no meaningful value in the file format.
- The relationship between `terrain_to_draw`, `rows`, and `cols` needs clarification for understanding terrain tile rendering.
- SWGB-specific "blob" fields (`_terrain_blob0_swgb`, `_terrain_blob1_swgb`) purpose is unknown.
