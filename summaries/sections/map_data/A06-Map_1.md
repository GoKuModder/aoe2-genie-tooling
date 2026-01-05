# Analysis of `map_data`, `map_info1`, and `map_info2` (Corrected)

This document analyzes the structure of the map data section in the `GenieDatParser` library, focusing on the relationship between `map_data.py`, `map_info1.py`, and `map_info2.py`. This version corrects a previous misunderstanding of the parsing logic.

## Overview

The map data is structured in a hierarchical format where a top-level container specifies the number of map entries, followed by parallel structures for metadata and the actual map data.

- **`MapData` (`map_data.py`):** The top-level container that defines the number of maps present.
- **`MapInfo1` (`map_info1.py`):** A metadata block for each map, containing pointers and counts.
- **`MapInfo2` (`map_info2.py`):** The primary data block containing the actual terrain, unit, and elevation data for each map.

## Detailed Breakdown

### 1. `MapData` (The Container)

The `MapData` class serves as the entry point for the entire map section. Its primary role is to establish how many maps need to be parsed.

- `num_maps: u32`: This field is critical. An `on_read` callback (`map_repeats`) uses this value to dynamically set the repetition count for the `map_info1` and `map_info2` lists. The parser will read exactly `num_maps` instances of `MapInfo1` and `num_maps` instances of `MapInfo2` sequentially.

```python
# sections/map_data/map_data.py

def map_repeats():
    return [
        set_repeat(ret(MapData.map_info1)).from_(MapData.num_maps),
        set_repeat(ret(MapData.map_info2)).from_(MapData.num_maps),
    ]

class MapData(BaseStruct):
    num_maps: int             = Retriever(u32, on_read = map_repeats)
    _map_ptr: bytes           = Retriever(Bytes[4])
    map_info1: list[MapInfo1] = Retriever(MapInfo1, repeat = 0)
    map_info2: list[MapInfo2] = Retriever(MapInfo2, repeat = 0)
```

### 2. `MapInfo1` (The Header/Metadata)

The `MapInfo1` class defines a block of metadata. It contains several fields that appear to be duplicated in `MapInfo2`, including counts (`_num_terrains`, `_num_units`) and pointers.

A comment in the source (`# all duplicate info. yES`) confirms this redundancy. While these fields provide a summary, **they do not directly drive the parsing of `MapInfo2`**. They are likely used for reference, validation, or by a different part of the game engine.

### 3. `MapInfo2` (The Self-Contained Data Block)

The `MapInfo2` class defines the structure that holds the actual map data. **Crucially, its parsing logic is self-contained.** It does not depend on the counts or pointers from `MapInfo1`.

- `MapInfo2` has its own count fields (e.g., `num_terrains: u32`).
- An `on_read` callback (e.g., `set_terrains_repeat`) on this local count field is used to set the repetition for its corresponding data list (e.g., `terrains: list[MapTerrain]`).

This means that `MapInfo2` first reads an integer specifying the number of terrains, and then immediately uses that integer to read the list of terrains.

```python
# sections/map_data/map_info2.py

def set_terrains_repeat():
    # This callback uses the value of `MapInfo2.num_terrains` to set the repeat count for `MapInfo2.terrains`
    return [
        set_repeat(ret(MapInfo2.terrains)).from_(MapInfo2.num_terrains)
    ]

class MapInfo2(BaseStruct):
    # ...
    # This is the count field that drives the parsing of the 'terrains' list below.
    num_terrains: int               = Retriever(u32, on_read = set_terrains_repeat)
    _terrain_ptr: bytes             = Retriever(Bytes[4])
    terrains: list[MapTerrain]      = Retriever(MapTerrain, repeat = 0)
    # ...
```

## Conclusion (Corrected)

The parsing of map data follows a clear pattern:
1.  **Read Map Count:** `MapData` reads `num_maps`.
2.  **Read Metadata and Data Blocks:** The parser reads `num_maps` instances of `MapInfo1` (metadata) and then `num_maps` instances of `MapInfo2` (data).
3.  **Self-Contained Parsing:** The parsing of the data arrays within each `MapInfo2` block is driven by its own internal count fields. The parallel `MapInfo1` block, while containing duplicate information, is not used to control the reading of `MapInfo2`'s data structures. The two are structurally parallel but functionally decoupled during the parsing phase.
