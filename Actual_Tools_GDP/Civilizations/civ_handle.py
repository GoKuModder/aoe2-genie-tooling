"""
CivHandle - High-level wrapper for Civilization objects.

Provides attribute access for civilizations.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional, Tuple

from Actual_Tools_GDP.Shared.dat_adapter import Civ

if TYPE_CHECKING:
    from Actual_Tools_GDP.Shared.dat_adapter import DatFile
    from Actual_Tools_GDP.Shared.dat_adapter import Unit

__all__ = ["CivHandle"]


class CivHandle:
    """
    High-level wrapper for Civilization objects.
    
    Provides attribute access for civilizations.
    
    Example:
        >>> civ = cm.get(1)  # Britons
        >>> print(civ.name)
        >>> civ.icon_set = 2
    """
    
    __slots__ = ("_civ_id", "_dat_file")
    
    def __init__(self, civ_id: int, dat_file: DatFile) -> None:
        if civ_id < 0:
            raise ValueError(f"civ_id must be non-negative, got {civ_id}")
        object.__setattr__(self, "_civ_id", civ_id)
        object.__setattr__(self, "_dat_file", dat_file)
    
    def __repr__(self) -> str:
        c = self._civ
        name = c.name if c else "<not found>"
        return f"CivHandle(id={self._civ_id}, name={name!r})"
    
    # =========================================================================
    # CORE ACCESS
    # =========================================================================
    
    @property
    def _civ(self) -> Optional[Civ]:
        """Get the underlying Civ object."""
        if 0 <= self._civ_id < len(self._dat_file.civs):
            return self._dat_file.civs[self._civ_id]
        return None
    
    def exists(self) -> bool:
        """Check if this civ exists."""
        return self._civ is not None
    
    # =========================================================================
    # BASIC PROPERTIES
    # =========================================================================
    
    @property
    def id(self) -> int:
        """Civilization ID."""
        return self._civ_id
    
    @property
    def name(self) -> str:
        """Civilization name."""
        c = self._civ
        return c.name if c else ""
    
    @name.setter
    def name(self, value: str) -> None:
        c = self._civ
        if c:
            c.name = value
    
    @property
    def icon_set(self) -> int:
        """Icon set ID."""
        c = self._civ
        return c.icon_set if c else 0
    
    @icon_set.setter
    def icon_set(self, value: int) -> None:
        c = self._civ
        if c:
            c.icon_set = value
    
    @property
    def tech_tree_id(self) -> int:
        """Tech tree ID."""
        c = self._civ
        return c.tech_tree_id if c else -1
    
    @tech_tree_id.setter
    def tech_tree_id(self, value: int) -> None:
        c = self._civ
        if c:
            c.tech_tree_id = value
    
    @property
    def team_bonus_id(self) -> int:
        """Team bonus tech ID."""
        c = self._civ
        return c.team_bonus_id if c else -1
    
    @team_bonus_id.setter
    def team_bonus_id(self, value: int) -> None:
        c = self._civ
        if c:
            c.team_bonus_id = value
    
    @property
    def units(self) -> List[Optional[Unit]]:
        """Unit list for this civ."""
        c = self._civ
        return c.units if c else []
    
    @property
    def unit_count(self) -> int:
        """Number of unit slots."""
        c = self._civ
        return len(c.units) if c else 0
    
    @property
    def resources(self) -> List[float]:
        """Starting resources."""
        c = self._civ
        return c.resources if c else []
    
    @resources.setter
    def resources(self, value: List[float]) -> None:
        c = self._civ
        if c:
            c.resources = value
    
    # =========================================================================
    # UNIT ACCESS
    # =========================================================================
    
    def get_unit(self, unit_id: int) -> Optional[Unit]:
        """Get a unit from this civ."""
        c = self._civ
        if c and 0 <= unit_id < len(c.units):
            return c.units[unit_id]
        return None
    
    def unit_exists(self, unit_id: int) -> bool:
        """Check if a unit exists in this civ."""
        c = self._civ
        if c and 0 <= unit_id < len(c.units):
            return c.units[unit_id] is not None
        return False
    
    # =========================================================================
    # DYNAMIC ACCESS
    # =========================================================================
    
    def __getattr__(self, name: str) -> Any:
        c = self._civ
        if c and hasattr(c, name):
            return getattr(c, name)
        raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}'")
    
    def __setattr__(self, name: str, value: Any) -> None:
        if name in self.__slots__:
            object.__setattr__(self, name, value)
            return
        c = self._civ
        if c and hasattr(c, name):
            setattr(c, name, value)
            return
        raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}'")
