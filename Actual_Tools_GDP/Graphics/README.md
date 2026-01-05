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

#### `add_graphic(file_name, name=None, graphic_id=None, frame_count=1, angle_count=1, frame_duration=0.1, speed_multiplier=1.0) -> GraphicHandle`
Add a new graphic to the DAT file.

**Args:**
- `file_name` (str): The SLP/SMX file name (e.g., "hero_attack.slp")
- `name` (str, optional): Internal name. If None, uses file_name
- `graphic_id` (int, optional): Target ID. If None, uses next available
- `frame_count` (int): Number of animation frames (default: 1)
- `angle_count` (int): Number of angles/facings (default: 1)
- `frame_duration` (float): Duration per frame in seconds (default: 0.1)
- `speed_multiplier` (float): Animation speed multiplier (default: 1.0)

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
