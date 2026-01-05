# A07-Map_2 Analysis

This document summarizes the structure of `map_land.py`, `map_terrain.py`, and `map_unit.py` from the `GenieDatParser` library.

## `map_land.py`

The `MapLand` class defines the structure for land elements on a map, including properties like `terrain_type`, `base_size`, and `placement_type`. It uses the `bfp_rs` library for declarative binary parsing with explicit field sizes and default values.

Key attributes include:
- `id`: A unique identifier for the land element.
- `terrain_type`: The type of terrain to be used.
- `x` and `y`: The coordinates for the land element.

## `map_terrain.py`

The `MapTerrain` class specifies the terrain composition of the map, including the percentage of different terrain types, the number of clumps, and other placement parameters.

Key attributes include:
- `percent`: The percentage of the map covered by this terrain.
- `type`: The terrain type.
- `num_clumps`: The number of clumps for this terrain.

## `map_unit.py`

The `MapUnit` class defines the placement and properties of units on the map, such as their type, grouping behavior, and initial ownership.

Key attributes include:
- `type`: The type of unit to be placed.
- `own_at_start`: The player ID of the unit's owner at the start of the game.
- `min_distance_to_players` and `max_distance_to_players`: The minimum and maximum distance from players for unit placement.
