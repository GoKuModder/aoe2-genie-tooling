"""
ResourceAccessor - Provides clean API for per-civilization resource values.

Note: Adding/removing resources must be done at the manager level since
resources are global across all civilizations.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from Actual_Tools_GDP.Civilizations.civ_handle import CivHandle

__all__ = ["ResourceAccessor"]


class ResourceAccessor:
    """
    Accessor for per-civilization resource values.
    
    Usage:
        civ.resource.get(0)               # Get value at index 0
        civ.resource.set(0, 200.0)        # Set value at index 0
        civ.resource[0]                   # Get via indexing
        civ.resource[0] = 200.0           # Set via indexing
        
    Note: To add/remove resources globally, use CivManager.add_resource() and
          CivManager.remove_resource() - these apply to ALL civilizations.
    """
    
    def __init__(self, civ_handle: CivHandle) -> None:
        self._civ_handle = civ_handle
        self._civ = civ_handle._civ
    
    def __iter__(self):
        """Iterate over resources."""
        return iter(self._civ.resources)
    
    def __len__(self) -> int:
        """Get number of resources."""
        return len(self._civ.resources)

    def __getitem__(self, index: int) -> float:
        """Get resource by index."""
        return self._civ.resources[index]

    def __setitem__(self, index: int, value: float) -> None:
        """Set resource by index."""
        self._civ.resources[index] = value

    def get(self, index: int) -> Optional[float]:
        """Get a resource value by index."""
        if 0 <= index < len(self._civ.resources):
            return self._civ.resources[index]
        return None

    def set(self, index: int, value: float) -> bool:
        """
        Set a resource value by index.
        
        Args:
            index: Resource index
            value: New value
            
        Returns:
            True if set, False if index out of range
        """
        if 0 <= index < len(self._civ.resources):
            self._civ.resources[index] = value
            return True
        return False
