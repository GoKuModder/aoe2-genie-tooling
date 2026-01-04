"""Type stubs for GraphicHandle - provides IDE autocomplete."""
from typing import List, Optional, Tuple

from genieutils.graphic import GraphicDelta, GraphicAngleSound


class DeltaHandle:
    """Wrapper for GraphicDelta with index."""
    delta_id: int
    graphic_id: int
    offset_x: int
    offset_y: int
    display_angle: int


class GraphicHandle:
    # Basic
    id: int
    name: str
    file_name: str
    particle_effect_name: str
    
    # SLP/Resource
    slp: int
    is_loaded: int
    old_color_flag: int
    
    # Rendering
    layer: int
    player_color: int
    transparent_selection: int
    coordinates: Tuple[int, int, int, int]
    mirroring_mode: int
    editor_flag: int
    
    # Sound
    sound_id: int
    wwise_sound_id: int
    angle_sounds_used: int
    
    # Animation
    frame_count: int
    angle_count: int
    speed_multiplier: float
    frame_duration: float
    replay_delay: float
    sequence_type: int
    
    # Collections
    deltas: List[GraphicDelta]
    angle_sounds: List[GraphicAngleSound]
    
    # Methods
    def exists(self) -> bool: ...
    def add_delta(self, graphic_id: int, offset_x: int = 0, offset_y: int = 0, display_angle: int = -1) -> Optional[DeltaHandle]: ...
    def remove_delta(self, delta_id: int) -> bool: ...
    def remove_delta_by_graphic(self, graphic_id: int) -> bool: ...
    def get_delta(self, delta_id: int) -> Optional[DeltaHandle]: ...
    def clear_deltas(self) -> None: ...
    def add_angle_sound(self, frame_num: int = 0, sound_id: int = -1, wwise_sound_id: int = 0, frame_num_2: int = 0, sound_id_2: int = -1, wwise_sound_id_2: int = 0, frame_num_3: int = 0, sound_id_3: int = -1, wwise_sound_id_3: int = 0) -> None: ...
    def clear_angle_sounds(self) -> None: ...
