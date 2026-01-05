"""Type stubs for GraphicHandle - enables IDE autocomplete"""
from typing import Any, Optional
from Actual_Tools_GDP.Graphics.delta_handle import DeltaHandle

class GraphicHandle:
    """Handle for a single sprite/graphic."""
    
    @property
    def id(self) -> int:
        """Get the graphic ID."""
        ...
    
    # Common sprite attributes
    name: str                       # Internal Name
    file_name: str                  # Sprite Name  
    slp_id: int                     # SLP file ID
    is_loaded: bool                 # Whether sprite is loaded
    force_player_color: int         # Force player color
    layer: int                      # Render layer
    color_table: int                # Color table (old color flag)
    transparent_selection: int      # Transparent pick mode
    bounding_box: list[int]         # Bounding box [X1, Y1, X2, Y2] (unused)
    mirroring_mode: int             # Mirroring mode
    num_frames: int                 # Frames per angle
    num_facets: int                 # Angle count
    speed_mult: float               # Unit speed multiplier
    frame_rate: float               # Animation duration (frame rate)
    replay_delay: float             # Replay delay
    sequence_type: int              # Sequence type
    sound_id: int                   # Sound ID (single sound)
    wwise_sound_id: int             # Wwise sound ID (DE2)
    particle_effect_name: str       # Particle effect name (DE2)
    
    # Complex nested structures
    facets_have_attack_sounds: bool # Whether angle sounds are used
    num_deltas: int                 # Number of deltas (auto-synced from list)
    deltas: list[Any]               # List of SpriteDelta objects (shadows, attachments)
    facet_attack_sounds: list[Any] # List of FacetAttackSound objects (angle-specific sounds)
    
    # Delta management methods
    def add_delta(
        self,
        graphic_id: int,
        offset_x: int = 0,
        offset_y: int = 0,
        display_angle: int = -1,
    ) -> DeltaHandle:
        """Add a delta (sub-graphic) to this graphic."""
        ...
    
    def get_delta(self, delta_id: int) -> Optional[DeltaHandle]:
        """Get a delta by index."""
        ...
    
    def remove_delta(self, delta_id: int) -> bool:
        """Remove a delta by index."""
        ...
    
    def add_delta_from_graphic(self, graphic_id: int, delta_id: int) -> Optional[DeltaHandle]:
        """Copy a delta from another graphic and add it to this graphic."""
        ...
    
    def clear_deltas(self) -> None:
        """Remove all deltas from this graphic."""
        ...
