"""
SoundManager - Manager for creating and modifying sounds.

This module provides the SoundManager class for managing sounds
in the Genie Engine DAT file.
"""
from __future__ import annotations

import copy
from typing import TYPE_CHECKING, Optional

from genieutils.sound import Sound, SoundItem

from Actual_Tools.Sounds.sound_handle import SoundHandle
from Actual_Tools_GDP.Shared.tool_base import ToolBase, tracks_creation
from Actual_Tools.exceptions import InvalidIdError, TemplateNotFoundError

if TYPE_CHECKING:
    from genieutils.datfile import DatFile

__all__ = ["SoundManager"]


class SoundManager(ToolBase):
    """
    Manager for creating and modifying sounds in a DAT file.
    
    Provides methods to add, copy, delete sounds.
    
    Example:
        >>> sm = workspace.sound_manager()
        >>> sound = sm.create("attack.wav")
        >>> sound.add_item("attack2.wav", probability=50)
    """

    def __init__(self, dat_file: DatFile) -> None:
        super().__init__(dat_file)

    # =========================================================================
    # CREATION
    # =========================================================================

    @tracks_creation("sound", name_param="filename")
    def create(
        self,
        filename: str,
        resource_id: int = 0,
        probability: int = 100,
        sound_id: Optional[int] = None,
    ) -> SoundHandle:
        """
        Create a new Sound with a single item.
        
        Args:
            filename: Sound filename (e.g., "attack.wav").
            resource_id: Resource ID for the sound.
            probability: Playback probability (0-100).
            sound_id: Target ID. If None, appends to end.
        
        Returns:
            SoundHandle for the new sound.
        """
        if not filename:
            raise ValueError("filename cannot be empty.")
        
        self.validate_range(probability, 0, 100, "probability")
        
        if sound_id is None:
            sound_id = self.allocate_next_sound_id()
        else:
            self.validate_id_positive(sound_id, "sound_id")
        
        item = SoundItem(
            filename=filename,
            resource_id=resource_id,
            probability=probability,
            civilization=-1,
            icon_set=0,
        )
        
        new_sound = Sound(
            id=sound_id,
            play_delay=0,
            cache_time=0,
            total_probability=probability,
            items=[item],
        )
        
        self.ensure_capacity(self.dat_file.sounds, sound_id)
        self.dat_file.sounds[sound_id] = new_sound
        
        return SoundHandle(sound_id, self.dat_file)
    
    # Backwards compatibility
    def add_sound(
        self,
        filename: str,
        resource_id: int = 0,
        probability: int = 100,
        sound_id: Optional[int] = None,
    ) -> SoundHandle:
        """Alias for create(). Deprecated."""
        return self.create(filename, resource_id, probability, sound_id)
    
    def copy(
        self,
        source_id: int,
        sound_id: Optional[int] = None,
    ) -> SoundHandle:
        """
        Copy an existing sound.
        
        Args:
            source_id: ID of sound to copy.
            sound_id: Target ID. If None, appends to end.
        
        Returns:
            SoundHandle for the copied sound.
        """
        if not self.exists(source_id):
            raise TemplateNotFoundError(f"Sound {source_id} not found.")
        
        source = self.dat_file.sounds[source_id]
        cloned = copy.deepcopy(source)
        
        if sound_id is None:
            sound_id = self.allocate_next_sound_id()
        else:
            self.validate_id_positive(sound_id, "sound_id")
        
        cloned.id = sound_id
        
        self.ensure_capacity(self.dat_file.sounds, sound_id)
        self.dat_file.sounds[sound_id] = cloned
        
        return SoundHandle(sound_id, self.dat_file)

    # =========================================================================
    # RETRIEVAL
    # =========================================================================

    def get(self, sound_id: int) -> SoundHandle:
        """
        Get a SoundHandle by ID.
        
        Args:
            sound_id: The sound ID.
        
        Returns:
            SoundHandle (check .exists() if unsure).
        """
        return SoundHandle(sound_id, self.dat_file)
    
    def get_raw(self, sound_id: int) -> Optional[Sound]:
        """Get raw Sound object by ID."""
        if 0 <= sound_id < len(self.dat_file.sounds):
            return self.dat_file.sounds[sound_id]
        return None

    def exists(self, sound_id: int) -> bool:
        """Check if a sound ID exists."""
        return (
            0 <= sound_id < len(self.dat_file.sounds)
            and self.dat_file.sounds[sound_id] is not None
        )

    def count(self) -> int:
        """Return total number of sound slots."""
        return len(self.dat_file.sounds)
    
    def count_active(self) -> int:
        """Return number of non-None sounds."""
        return sum(1 for s in self.dat_file.sounds if s is not None)
    
    # =========================================================================
    # DELETION
    # =========================================================================
    
    def delete(self, sound_id: int) -> bool:
        """
        Delete a sound (set slot to None).
        
        Args:
            sound_id: ID of sound to delete.
        
        Returns:
            True if deleted, False if didn't exist.
        """
        if not self.exists(sound_id):
            return False
        
        self.dat_file.sounds[sound_id] = None
        return True
