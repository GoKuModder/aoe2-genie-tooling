# A14-Terrain_2.md

## Analysis of `terrain_border.py`, `terrain_unit.py`, and `terrain_animation.py`

This document summarizes the data structures defined in the `terrain_border.py`, `terrain_unit.py`, and `terrain_animation.py` files from the `GenieDatParser` project. These classes are used to parse terrain-related data from Genie Engine `.dat` files.

### `terrain_border.py`

The `TerrainBorder` class defines the structure for a terrain border, which is used to create graphical transitions between different terrain types.

- **`enabled`**: A boolean flag that indicates whether the border is enabled.
- **`random`**: An integer that likely controls some random variation in the border's appearance.
- **`internal_name`**: A 13-byte string for the internal name of the border.
- **`slp_filename`**: A 13-byte string for the filename of the SLP graphic used for the border.
- **`slp_id`**: A 32-bit integer that is the ID of the SLP graphic.
- **`_slp_ptr`**: A 4-byte pointer to the SLP data (likely populated at runtime).
- **`sound_id`**: A 32-bit integer for the sound ID associated with the border.
- **`color`**: An array of 3 unsigned 8-bit integers representing the color of the border.
- **`animation`**: A nested `TerrainAnimation` object that defines the animation properties of the border.
- **`frames`**: A large array of `TerrainSpriteFrame` objects (19 * 12 = 228 frames) that define the individual sprite frames used to render the border in different tiling configurations.
- **`draw_tile`**: An 8-bit integer that likely controls how the border tile is drawn.
- **`_padding`**: An 8-bit integer for padding.
- **`underlay_terrain`**: A 16-bit unsigned integer that specifies the terrain to be drawn underneath the border.
- **`border_style`**: A 16-bit integer that likely specifies the style of the border.

### `terrain_unit.py`

The `TerrainUnit` class defines the properties of units that can be placed on a terrain, such as trees, rocks, or other decorations.

- **`mask`**: A 16-bit integer that is only present in game versions 7.1 and later. Its purpose is not immediately clear from the definition, but it is likely a bitmask for some property.
- **`type`**: A 16-bit integer that specifies the type of the unit.
- **`density`**: A 16-bit integer that controls the density of the unit on the terrain.
- **`centralized`**: A boolean flag that, if true, indicates that the unit should be placed in the center of the tile.

### `terrain_animation.py`

The `TerrainAnimation` class defines the animation properties for terrain elements, such as water or animated borders.

- **`enabled`**: A boolean flag that indicates whether the animation is enabled.
- **`num_frames`**: A 16-bit integer for the number of frames in the animation.
- **`num_pause_frames`**: A 16-bit integer for the number of frames to pause between animation cycles.
- **`frame_interval`**: A 32-bit float that specifies the time interval between frames.
- **`replay_delay`**: A 32-bit float that specifies the delay before the animation replays.
- **`frame`**: A 16-bit integer for the current frame of the animation.
- **`draw_frame`**: A 16-bit integer for the frame that is currently being drawn.
- **`animate_last`**: A 32-bit float that likely stores the time of the last animation update.
- **`change_frame_flag`**: A boolean flag that indicates whether the frame should be changed.
- **`draw_flag`**: A boolean flag that indicates whether the animation should be drawn.
