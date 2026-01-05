# Graphics Module - Complete Documentation

## Overview
The Graphics module provides access to sprite/graphic data in the DAT file through `GraphicManager` and `GraphicHandle`.

## Usage

```python
from Actual_Tools_GDP.Base.workspace import GenieWorkspace

# Load workspace
workspace = GenieWorkspace.load("empires2_x2_p1.dat")

# Access graphics
graphic = workspace.graphic_manager.get(1)
print(f"Total graphics: {workspace.graphic_manager.count()}")  # 17068

# Read attributes
print(graphic.name)           # "ArcheryRange EAST Age2 (Rubble)"
print(graphic.file_name)      # "b_east_archery_range_age2_rubble_x1"
print(graphic.slp_id)         # 13
print(graphic.frame_rate)     # Animation frame rate

# Modify attributes
graphic.frame_rate = 0.5
graphic.speed_mult = 2.0
graphic.layer = 10

# Save changes
workspace.save("output.dat", validate=False)
```

## Available Sprite Attributes

### Identity
- `id` - Sprite ID (int)
- `name` - Sprite name (str)
- `file_name` - SLP filename (str)

### Graphics File
- `slp_id` - SLP file ID (int)
- `is_loaded` - Whether sprite is loaded (bool)

### Visual Properties
- `force_player_color` - Force player color 0/1 (int)
- `layer` - Rendering layer (int)
- `color_table` - Color table ID (int)
- `transparent_selection` - Transparent selection mode (int)
- `bounding_box` - Bounding box [x1,y1,x2,y2] (list[int])
- `mirroring_mode` - Mirroring mode (int)

### Animation
- `num_frames` - Number of frames (int)
- `num_facets` - Number of facets (int)
- `speed_mult` - Speed multiplier (float)
- `frame_rate` - Animation frame rate (float)
- `replay_delay` - Replay delay in seconds (float)
- `sequence_type` - Sequence type (int)

### Audio
- `sound_id` - Sound ID (int)
- `facets_have_attack_sounds` - Whether facets have attack sounds (bool)

### Advanced
- `num_deltas` - Number of deltas (int)

## Implementation Files

- `Graphics/graphic_manager.py` - Manager class
- `Graphics/graphic_handle.py` - Handle wrapper class  
- `Graphics/__init__.py` - Module exports

## Architecture

```
GenieWorkspace
  └─ graphic_manager: GraphicManager
       └─ get(id) -> GraphicHandle
            └─ _sprite: Sprite (from GenieDatParser)
```

**Pattern**: Top-to-bottom dependency injection
- Manager receives `workspace` reference
- Handle accesses data via `workspace.dat.sprites[id]`
- Direct attribute access through `__getattr__`/`__setattr__`

## Test Results

✅ Load DAT file (17,068 graphics)
✅ Get graphic by ID
✅ Read all sprite attributes  
✅ Modify sprite attributes
✅ Save changes to DAT file

**Status**: COMPLETE AND VERIFIED
