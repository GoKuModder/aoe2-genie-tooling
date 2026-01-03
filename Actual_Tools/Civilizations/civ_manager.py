"""
CivilizationsManager - Manager for querying civilizations.

This module provides the CivilizationsManager class for accessing
civilization data in the Genie Engine DAT file.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from genieutils.civ import Civ

from Actual_Tools.Civilizations.civ_handle import CivHandle
from Actual_Tools.Shared.tool_base import ToolBase

if TYPE_CHECKING:
    from genieutils.datfile import DatFile

__all__ = ["CivilizationsManager"]


class CivilizationsManager(ToolBase):
    """
    Manager for querying civilizations in a DAT file.
    
    Provides access to civilization data.
    
    Example:
        >>> cm = workspace.civ_manager()
        >>> britons = cm.get(1)
        >>> print(britons.name)
    """

    def __init__(self, dat_file: DatFile) -> None:
        super().__init__(dat_file)

    # =========================================================================
    # RETRIEVAL
    # =========================================================================

    def get(self, civ_id: int) -> CivHandle:
        """
        Get a CivHandle by ID.
        
        Args:
            civ_id: The civilization ID.
        
        Returns:
            CivHandle (check .exists() if unsure).
        """
        return CivHandle(civ_id, self.dat_file)
    
    def get_raw(self, civ_id: int) -> Optional[Civ]:
        """Get raw Civ object by ID."""
        if 0 <= civ_id < len(self.dat_file.civs):
            return self.dat_file.civs[civ_id]
        return None

    def get_by_name(self, name: str) -> Optional[CivHandle]:
        """
        Get a civilization by name.
        
        Args:
            name: The civilization name to search for.
        
        Returns:
            CivHandle, or None if not found.
        """
        for i, civ in enumerate(self.dat_file.civs):
            if civ.name == name:
                return CivHandle(i, self.dat_file)
        return None

    def all(self) -> List[CivHandle]:
        """Get all civilizations as handles."""
        return [CivHandle(i, self.dat_file) for i in range(len(self.dat_file.civs))]
    
    def all_raw(self) -> List[Civ]:
        """Get all raw Civ objects."""
        return self.dat_file.civs

    def count(self) -> int:
        """Return the total number of civilizations."""
        return len(self.dat_file.civs)

    def names(self) -> List[str]:
        """Get all civilization names."""
        return [civ.name for civ in self.dat_file.civs]
    
    def exists(self, civ_id: int) -> bool:
        """Check if a civ ID exists."""
        return 0 <= civ_id < len(self.dat_file.civs)
