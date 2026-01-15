# Graphics Module - Complete Documentation

## Overview
The Graphics module provides access to sprite/graphic data in the DAT file through `GraphicManager` and `GraphicHandle`.

## GraphicManager API

### Retrieval Methods

#### `get(graphic_id: int) -> GraphicHandle`
Get a graphic by ID. Returns handle even if graphic doesn't exist (check `.exists()`).

#### `exists(graphic_id: int) -> bool`
Check if a graphic ID exists and is not None.

#### `count() -> int`
Return total number of graphic slots (including None).

#### `count_active() -> int`
Return number of non-None graphics.

### Creation Methods

#### `add_graphic(...) -> GraphicHandle`
Add a new graphic to the DAT file with complete control over all attributes.

**Signature:**
```python
def add_graphic(
    file_name: str,
    name: Optional[str] = None,
    graphic_id: Optional[int] = None,
    slp_id: int = -1,
    is_loaded: bool = False,
    player_color: int = 0,
    layer: int = 0,
    color_table: int = -1,
    transparent_selection: int = 0,
    coordinates: tuple[int, int, int, int] = (0, 0, 0, 0),
    sound_id: int = -1,
    wwise_sound_id: int = 0,
    frame_count: int = 1,
    angle_count: int = 1,
    speed_multiplier: float = 1.0,
    frame_duration: float = 0.1,
    replay_delay: float = 0.0,
    sequence_type: int = 0,
    mirroring_mode: int = 0,
    editor_flag: int = 0,
    particle_effect_name: str = "",
    first_frame: int = 0,
) -> GraphicHandle
```

**Arguments:**
- `file_name` (str): The SLP/SMX file name
- `name` (str, optional): Internal name. If None, uses file_name
- `graphic_id` (int, optional): Target ID. If None, appends to end
- `slp_id` (int): SLP file ID (default: -1)
- `is_loaded` (bool): Whether sprite is loaded (default: False)
- `player_color` (int): Force player color (default: 0)
- `layer` (int): Rendering layer (default: 0)
- `color_table` (int): Color table/flag (default: -1)
- `transparent_selection` (int): Transparent pick mode (default: 0)
- `coordinates` (tuple): Bounding box (X1, Y1, X2, Y2) (default: (0,0,0,0))
- `sound_id` (int): Sound ID (default: -1)
- `wwise_sound_id` (int): Wwise sound ID (default: 0)
- `frame_count` (int): Number of animation frames (default: 1)
- `angle_count` (int): Number of angles/facings (default: 1)
- `speed_multiplier` (float): Animation speed multiplier (default: 1.0)
- `frame_duration` (float): Duration per frame in seconds (default: 0.1)
- `replay_delay` (float): Delay before animation replay (default: 0.0)
- `sequence_type` (int): Animation sequence type (default: 0)
- `mirroring_mode` (int): Mirroring mode (default: 0)
- `editor_flag` (int): Editor display flag (default: 0)
- `particle_effect_name` (str): Particle effect name (default: "")
- `first_frame` (int): First frame index (default: 0)

**Returns:** GraphicHandle for the new graphic

**Example:**
```python
gfx = gm.add_graphic("my_unit.slp", frame_count=10, angle_count=8)
```

### Copy/Delete Methods

#### `copy(source_id: int, target_id: int = None) -> GraphicHandle`
Copy a graphic to a new ID.

**Args:**
- `source_id` (int): ID of graphic to copy
- `target_id` (int, optional): Target ID. If None, uses next available

**Returns:** GraphicHandle for the copied graphic

**Raises:** `InvalidIdError` if source doesn't exist

#### `delete(graphic_id: int) -> bool`
Delete a graphic (set slot to None).

**Returns:** True if deleted, False if didn't exist

#### `copy_to_clipboard(graphic_id: int) -> bool`
Copy a graphic to internal clipboard.

**Returns:** True if copied, False if doesn't exist

#### `paste(target_id: int = None) -> GraphicHandle | None`
Paste graphic from clipboard to target ID.

**Returns:** GraphicHandle for pasted graphic, or None if clipboard empty

#### `clear_clipboard()`
Clear the internal clipboard.

### Search Methods

#### `find_by_name(name: str) -> GraphicHandle | None`
Find first graphic matching name (case-sensitive).

**Returns:** GraphicHandle if found, None otherwise

#### `find_by_file_name(file_name: str) -> GraphicHandle | None`
Find first graphic matching file_name.

**Returns:** GraphicHandle if found, None otherwise

### Delta Methods (Advanced)

**Deltas** are secondary graphics layered over the main graphic (e.g., shadows, attachments).

####
