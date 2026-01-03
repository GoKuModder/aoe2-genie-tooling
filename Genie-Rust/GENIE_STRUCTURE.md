# Genie .dat File Structure & Findings (DE / VER 8.8)

This document summarizes the technical findings regarding the binary structure of Age of Empires II DE `.dat` files as implemented in the `Genie-Rust` loader.

## 1. Compression
- **Format**: Raw Deflate (equivalent to Python `zlib.decompress(data, wbits=-15)`).
- **Header**: No Zlib header (no `78 9C` etc.).
- **Detection**: Standard Zlib decoders will fail with "incorrect header check".

## 2. File Layout (Section Order)
1. **Header**: Version string (8 bytes). `VER 8.8` found in test file.
2. **Terrain Restrictions**: 
    - `terr_rest_size` (u16)
    - `terrains_used` (u16)
    - `float_ptr_terrain_tables` (i32 array, size `terr_rest_size`)
    - `terrain_pass_graphic_pointers` (i32 array, size `terr_rest_size`)
    - `TerrainRestriction` objects:
        - `passable_buildable_dmg_multiplier` (f32 array, size `terrains_used`)
        - `TerrainPassGraphic` objects (size `terrains_used`, 20 bytes each).
3. **Player Colours**: 16 objects (36 bytes each).
4. **Sounds**: `sound_count` (u16) + `Sound` objects.
5. **Graphics**: `graphic_count` (u16) + pointer array (i32 array, size `graphic_count`) + `Graphic` objects.
6. **Terrain Block**: Complex nested structure. Currently skipped via approx offsets.
7. **Random Maps**: Currently skipped.
8. **Effects**: `effects_count` (u32) + `Effect` objects.
9. **Unit Headers**: `unit_headers_count` (u32) + `UnitHeaders` objects.
10. **Civs**: `civ_count` (u16) + `Civ` objects (contains nested `Unit` array).
11. **Techs**: `tech_count` (u16) + `Tech` objects.
12. **Stats**: Map-related stats and `time_slice`.
13. **Tech Tree**: Optional final section.

## 3. Notable Findings & Issues
- **Alignment Drift**: Drift often occurs in `TerrainRestriction` if the `terrains_used` count is misinterpreted or if pointer arrays are skipped incorrectly.
- **Sound Count Garbage**: If the parser sees `Sound Count: 65535`, it usually means the cursor is misaligned by a few bytes (reading `FF FF` from a nearby field).
- **Unit Mixins**: `Unit` parsing requires strict branching based on `type` (10, 20, 25, 30, 40, 50, 60, 70, 80) to handle trailing fields for Buildings, Projectiles, etc.
- **Pointer Arrays**: Sections like Graphics and Civs use a "pointer array" (i32 indices) followed by the actual objects. Null pointers (0) must be handled without advancing the object parser.

## 4. Current Loader Status
- **Decompression**: Fully functional.
- **Alignment**: Drift identified at Section 2 offset for `VER 8.8`.
- **Structs**: Manual implementation preferred over codegen for complex types to ensure binary precision.
