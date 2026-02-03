"""Type stubs for SoundFileHandle - enables IDE autocomplete"""
from typing import Any

class SoundFileHandle:
    """Handle for a single sound file entry within a sound."""
    
    @property
    def index(self) -> int:
        """Get the index of this file in the sound's list."""
        ...
        
    # SoundFile attributes
    filename: str
    sound_name: str
    resource_id: int
    probability: int
    civilization_id: int
    icon_set: int
