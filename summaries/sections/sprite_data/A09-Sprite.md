# Section Analysis: `sprite_data`

## Overview

The `sprite_data` section defines the structures for handling game sprites, which are the visual representations of units, buildings, and other game objects. It includes data for sprite animations, sounds, and transformations. The structures are designed to be version-aware, supporting various Genie Engine games.

## File Breakdown

### `__init__.py`

- **Purpose**: This file serves as the package initializer for the `sprite_data` section.
- **Exports**: It makes the primary data structures (`Sprite`, `FacetAttackSound`, `SpriteDelta`) available for other parts of the parser to import.

### `facet_attack_sound.py`

- **Purpose**: Defines the `FacetAttackSound` class.
- **Structure**:
    - Represents a set of three attack sounds that can be associated with a sprite facet (angle).
    - Each sound has a `sound_delay`, a legacy `sound_id`, and a modern `wwise_sound_id`.
    - The `wwise_sound_id` is version-dependent and only present in newer game versions (7.1+).

### `sprite.py`

- **Purpose**: Defines the main `Sprite` class, which is the central structure for sprite data.
- **Structure**:
    - **Version-Aware**: Handles different data layouts for multiple game versions (AoE1, AoE2, SWGB, DE). It uses version-gated fields to parse the correct data.
    - **Unified API**: Uses `RetrieverCombiner` to provide a consistent `name` and `file_name` property across different game versions.
    - **Core Attributes**: Contains essential sprite information like `slp_id`, `layer`, `bounding_box`, `frame_rate`, and animation properties.
    - **Nested Data**: Manages lists of `SpriteDelta` and `FacetAttackSound` objects.
    - **Dynamic Repeats**: Uses `on_read` and `on_write` callbacks to dynamically set the number of repeated nested structures (`deltas` and `facet_attack_sounds`) based on count fields (`num_deltas`, `num_facets`), ensuring data integrity.

### `sprite_delta.py`

- **Purpose**: Defines the `SpriteDelta` class.
- **Structure**:
    - Represents a transformation applied to a sprite, often used for attaching one sprite to another (e.g., a shield to a unit).
    - Contains the `sprite_id` of the attached sprite.
    - Defines the `offset_x`, `offset_y`, and `display_angle` to position and rotate the attached sprite relative to its parent.
    - Includes padding and a pointer field for internal use by the engine.

## Summary

The `sprite_data` section provides a robust, version-aware system for parsing and representing sprite information. The `Sprite` class is the core component, aggregating animation data, sound references, and a list of `SpriteDelta` transformations. The design effectively abstracts the complexity of different file formats behind a consistent API.
