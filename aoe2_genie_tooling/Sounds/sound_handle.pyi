"""Type stubs for SoundHandle - enables IDE autocomplete"""
from typing import Any, Optional
from aoe2_genie_tooling.Sounds.sound_file_handle import SoundFileHandle

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
    sound_files: list[Any]
    
    @property
    def sounds(self) -> list[SoundFileHandle]:
        """Get all actual sound entries inside this holder."""
        ...

    @property
    def files(self) -> list[SoundFileHandle]:
        """Alias for sounds."""
        ...

    def new_sound(
        self,
        filename: str = "",
        sound_name: str = "",
        resource_id: int = -1,
        probability: int = 100,
        civilization_id: int = -1,
        icon_set: int = -1,
        **kwargs: Any
    ) -> SoundFileHandle:
        """Add a new actual sound file entry to this holder."""
        ...

    def add_file(
        self,
        filename: str = "",
        sound_name: str = "",
        resource_id: int = -1,
        probability: int = 100,
        civilization_id: int = -1,
        icon_set: int = -1,
        **kwargs: Any
    ) -> SoundFileHandle:
        """Alias for new_sound."""
        ...

    def get_file(self, index: int) -> Optional[SoundFileHandle]:
        """Get a sound file by index."""
        ...

    def get_sound(self, index: int) -> Optional[SoundFileHandle]:
        """Alias for get_file."""
        ...

    def copy_sound(self, index: int, target_index: Optional[int] = None) -> Optional[SoundFileHandle]:
        """Copy a sound entry within this holder."""
        ...

    def move_sound(self, source_index: int, target_index: int) -> bool:
        """Move a sound entry to a new position within this holder."""
        ...

    def remove_sound(self, index: int) -> bool:
        """Remove a sound file entry."""
        ...

    def remove_file(self, index: int) -> bool:
        """Remove a sound file entry."""
        ...

    def clear_files(self) -> None:
        """Remove all sound file entries."""
        ...

    def exists(self) -> bool:
        """Check if this sound entry exists and is not None."""
        ...
