"""Type stubs for SoundHandle - enables IDE autocomplete"""

class SoundHandle:
    """Handle for a single sound."""
    
    @property
    def id(self) -> int:
        """Get the sound ID."""
        ...
    
    # Sound attributes
    play_delay: int
    cache_time: int
    num_sound_files: int
    total_probability: int
    sound_files: list
