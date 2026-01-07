# Graphic Manager

The `GraphicManager` handles sprites (graphics), including their animation data, file references (SLP/SMP), and delta (stacked) graphics.

## Mental Model

*   **Sprites**: A "Graphic" in DAT terms is a Sprite definition. It defines how many frames, angles, and which file (SLP ID) to use.
*   **Deltas**: Graphics can be stacked. A "Delta" is a reference to *another* graphic that draws on top of the main one (e.g., a unit carrying a flag). The `GraphicManager` handles these links.
*   **Sequences**: Animations are often sequences of frames. The manager provides helpers to set frame rates and counts.

## Public API

### GraphicManager (`Actual_Tools_GDP.Graphics.graphic_manager`)

Access via `workspace.graphic_manager`.

*   `add_graphic(...)`: Creates a new graphic from scratch.
*   `get(graphic_id)`: Gets a `GraphicHandle`.
*   `copy(source_id, target_id)`: Duplicates a graphic.
*   `find_by_name(name)`: Searches by internal name.

### GraphicHandle (`Actual_Tools_GDP.Graphics.graphic_handle`)

*   `id`, `name`: Basic properties.
*   `slp_id`: The ID of the SLP file in the DRS/SLP archive.
*   `layer`: Drawing layer.
*   `frame_count`, `angle_count`: Animation settings.
*   `add_delta(...)`: Adds a sub-graphic.
*   `deltas`: List of `DeltaHandle` objects.
*   `add_angle_sound(...)`: Links sounds to animation frames.

### DeltaHandle (`Actual_Tools_GDP.Graphics.delta_handle`)

Wraps a delta entry.

*   `graphic_id`: The ID of the sub-graphic.
*   `offset_x`, `offset_y`: Pixel offsets.
*   `display_angle`: If set, only draws this delta when the unit is facing a specific angle.

## Workflows

### Creating a New Graphic

```python
# Create a new graphic for an SLP file
graphic = workspace.graphic_manager.add_graphic(
    name="My Custom Unit",
    slp_id=50100, # Reference to SLP file
    frame_count=10,
    angle_count=8,
    duration=1.0 # Animation speed
)
```

### Adding a Delta (Stacked Graphic)

This is useful for adding accessories (weapons, riders, flags) without baking them into the main sprite.

```python
# Add a flag on top of the unit
graphic.add_delta(
    graphic_id=1234, # Flag graphic
    offset_x=5,
    offset_y=-20
)
```

### Copying a Graphic

```python
# Copy the Knight's graphic to make a variation
knight_gfx = workspace.graphic_manager.get(100) # Pseudo-ID
new_gfx = workspace.graphic_manager.copy(
    source_id=knight_gfx.id,
    target_id=None # Auto-assign
)
new_gfx.name = "Dark Knight"
```

## Gotchas & Invariants

*   **SLP IDs**: The `slp_id` refers to a file inside the game's DRS archives or data folders. The DAT file does not contain the image data itself, only the reference. If the SLP doesn't exist, the unit will be invisible or crash the game.
*   **Deltas Recursion**: Deltas point to other graphics. Avoid circular references (A -> B -> A), as this can crash the engine.
*   **Angle Sounds**: These link sound IDs to specific frames of animation (e.g., footstep sound on frame 5). Ensure the sound IDs exist.

## Cross-Links

*   [Sounds](../sounds.md)
*   [Units Manager](../units_manager.md)
