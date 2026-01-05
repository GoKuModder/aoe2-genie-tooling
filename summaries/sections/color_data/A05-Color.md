# A05-Color — Color Data
Source modules: `src/sections/color_data/__init__.py`, `src/sections/color_data/color_data.py`, `src/sections/color_data/player_color_data1.py`, `src/sections/color_data/player_color_data2.py`
Purpose: This section defines the data structures for player colors in Genie Engine `.dat` files. The structures are version-dependent to support different game versions like Age of Empires 1/2, Star Wars Galactic Battlegrounds, and their Definitive Editions.
Key Objects:
- `ColorData`: The main container class that holds a list of 16 player color objects. It dynamically selects between `PlayerColorData1` and `PlayerColorData2` based on the `.dat` file version.
- `PlayerColorData1`: Defines the color structure for older game versions (e.g., AoE1 DE). It includes fields like `color_name`, `id`, `resource_id`, `minimap_color`, and `type`.
- `PlayerColorData2`: Defines the color structure for newer game versions (e.g., AoE2 DE). It has more detailed color definitions, including `id`, `player_color_base`, `outline_color`, `unit_selection_color1`, `unit_selection_color2`, `minimap_color1`, `minimap_color2`, `minimap_color3`, and `statistics_text_color`.
Binary Layout Notes: The `ColorData` struct uses a `Retriever` to select between an `Array16` of `PlayerColorData1` or `PlayerColorData2` based on the `.dat` file version. `PlayerColorData1` uses a mix of `NtStr[30]`, `i16`, `u16`, and `u8`. `PlayerColorData2` uses `i32` for all its fields.
Cross-Dependencies: `ColorData` depends on `PlayerColorData1` and `PlayerColorData2`. These modules depend on the `bfp_rs` library for binary parsing. The `ColorData` section is a component of the top-level `DatFile` structure.
Integration Notes: When parsing a `.dat` file, the `ColorData` object will be populated with either `PlayerColorData1` or `PlayerColorData2` objects based on the file's version header. This allows the parser to handle color data from different games transparently.
Open Questions: None at the moment. The structure is straightforward and well-defined.
