"""
SoundFileHandle - Wrapper for individual SoundFile objects.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from aoe2_genie_tooling.Sounds.sound_handle import SoundHandle

__all__ = ["SoundFileHandle"]


class SoundFileHandle:
    """
    Handle for a single sound file entry within a sound.
    """
    
    def __init__(self, parent_handle: SoundHandle, file_id: int) -> None:
        """
        Initialize SoundFileHandle.
        
        Args:
            parent_handle: The SoundHandle owning this file
            file_id: Index in the sound_files list
        """
        object.__setattr__(self, '_parent', parent_handle)
        object.__setattr__(self, '_id', file_id)
        # Access the raw Sound object from parent and get the SoundFile
        object.__setattr__(self, '_file', parent_handle._sound.sound_files[file_id])
    
    @property
    def index(self) -> int:
        """Get the index of this file in the sound's list."""
        return self._id
    
    @property
    def filename(self) -> str:
        """Get filename with version fallback."""
        try:
            return self._file.filename
        except Exception:
            try:
                return self._file.sound_name
            except Exception:
                return ""

    @filename.setter
    def filename(self, value: str) -> None:
        """Set filename with version fallback."""
        try:
            self._file.filename = value
        except Exception:
            try:
                self._file.sound_name = value
            except Exception:
                pass

    @property
    def sound_name(self) -> str:
        """Get sound_name with version fallback."""
        try:
            return self._file.sound_name
        except Exception:
            try:
                return self._file.filename
            except Exception:
                return ""

    @sound_name.setter
    def sound_name(self, value: str) -> None:
        """Set sound_name with version fallback."""
        try:
            self._file.sound_name = value
        except Exception:
            try:
                self._file.filename = value
            except Exception:
                pass

    def __getattr__(self, name: str) -> Any:
        return getattr(self._file, name)
    
    def __setattr__(self, name: str, value: Any) -> None:
        if name.startswith('_'):
            object.__setattr__(self, name, value)
        else:
            setattr(self._file, name, value)

    def __repr__(self) -> str:
        return f"SoundFileHandle(index={self._id}, filename='{getattr(self, 'filename', 'Unknown')}')"
