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
    slp: int                        # Alias for slp_id
    is_loaded: bool                 # Whether sprite is loaded
    force_player_color: int         # Force player color
    player_color: int               # Alias for force_player_color
    layer: int                      # Render layer
    color_table: int                # Color table (old color flag)
    transparent_selection: int      # Transparent pick mode
    bounding_box: list[int]         # Bounding box [X1, Y1, X2, Y2] (unused)
    coordinates: tuple[int, int, int, int] # Alias for bounding_box
    mirroring_mode: int             # Mirroring mode
    editor_mode: int                # Editor display flag (old)
    editor_flag: int                # Alias for editor_mode
    num_frames: int                 # Frames per angle (internal)
    frame_count: int                # Alias for num_frames
    num_facets: int                 # Angle count (internal)
    angle_count: int                # Alias for num_facets
    speed_mult: float               # Unit speed multiplier (internal)
    speed_multiplier: float         # Alias for speed_mult
    frame_rate: float               # Animation duration (internal)
    frame_duration: float           # Alias for frame_rate
    animation_duration: float       # Total animation time (frame_count * frame_duration)
    replay_delay: float             # Replay delay
    sequence_type: int              # Sequence type
    sound_id: int                   # Sound ID (single sound)
    wwise_sound_id: int             # Wwise sound ID (DE2)
    particle_effect_name: str       # Particle effect name (DE2)
    
    # Complex nested structures
    facets_have_attack_sounds: bool # Whether angle sounds are used (internal)
    angle_sounds_used: bool         # Alias for facets_have_attack_sounds
    num_deltas: int                 # Number of deltas (auto-synced from list)
    
    @property
    def deltas(self) -> list[DeltaHandle]:
        """Get all deltas as DeltaHandle objects."""
        ...
    
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
    
    def remove_delta_by_graphic(self, graphic_id: int) -> int:
        """Remove all deltas from THIS graphic that point to a specific graphic ID."""
        ...
    
    def add_delta_from_graphic(self, graphic_id: int, delta_id: int) -> Optional[DeltaHandle]:
        """Copy a delta from another graphic and add it to this graphic."""
        ...
    
    def clear_deltas(self) -> None:
        """Remove all deltas from this graphic."""
        ...
    
    def exists(self) -> bool:
        """Check if this graphic entry exists and is not None."""
        ...
    
    def add_angle_sound(
        self,
        frame_num: int = 0,
        sound_id: int = -1,
        wwise_sound_id: int = 0,
        frame_num_2: int = 0,
        sound_id_2: int = -1,
        wwise_sound_id_2: int = 0,
        frame_num_3: int = 0,
        sound_id_3: int = -1,
        wwise_sound_id_3: int = 0,
    ) -> None:
        """Add an angle sound entry."""
        ...
    
    def clear_angle_sounds(self) -> None:
        """Remove all angle sounds."""
        ...
