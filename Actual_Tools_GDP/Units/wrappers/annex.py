"""
AnnexHandle - Wrapper for building annex entries.

Annexes define attached building units (like the corners of a Wonder).
Each annex has a unit_id and positioning info.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, List, Optional, Tuple

if TYPE_CHECKING:
    # TODO: Removed genie-rust dependency - needs migration to GenieDatParser
    # from genie_rust import Unit
    pass

__all__ = ["AnnexHandle", "AnnexesWrapper"]


@dataclass
class AnnexHandle:
    """
    Handle for a single building annex.

    An annex defines an attached unit that spawns with the building.
    For example, Wonder corner pieces.

    Attributes:
        unit_id: The unit ID to spawn as annex (-1 = none)
        misplacement_x: X offset from building center
        misplacement_y: Y offset from building center
    """
    unit_id: int = -1
    misplacement_x: float = 0.0
    misplacement_y: float = 0.0

    @classmethod
    def from_raw(cls, raw_annex: Any) -> "AnnexHandle":
        """Create from raw genieutils annex object."""
        if raw_annex is None:
            return cls()
        return cls(
            unit_id=getattr(raw_annex, "unit_id", -1),
            misplacement_x=getattr(raw_annex, "misplacement_x", 0.0),
            misplacement_y=getattr(raw_annex, "misplacement_y", 0.0),
        )

    def to_tuple(self) -> Tuple[int, float, float]:
        """Convert to tuple format for storage."""
        return (self.unit_id, self.misplacement_x, self.misplacement_y)

    @property
    def exists(self) -> bool:
        """True if this annex has a valid unit assigned."""
        return self.unit_id >= 0


class AnnexesWrapper:
    """
    Wrapper for managing building annexes.

    Buildings can have up to 4 annexes (attached units).
    This wrapper provides easy access to read/write annexes.

    Usage:
        annexes = unit.building.annexes_wrapper
        annexes[0].unit_id = 500  # Set first annex
        annexes.add(unit_id=501, x=1.0, y=1.0)  # Add annex
    """

    MAX_ANNEXES = 4

    def __init__(self, units: List["Unit"]) -> None:
        """
        Initialize with list of units to modify.

        Args:
            units: List of Unit objects with building component
        """
        self._units = units

    def _get_raw_annexes(self) -> Optional[Tuple]:
        """Get raw annexes tuple from first unit."""
        if self._units and self._units[0].building:
            return self._units[0].building.annexes
        return None

    def __len__(self) -> int:
        """Number of active annexes (with unit_id >= 0)."""
        raw = self._get_raw_annexes()
        if not raw:
            return 0
        return sum(1 for a in raw if hasattr(a, 'unit_id') and a.unit_id >= 0)

    def __getitem__(self, index: int) -> AnnexHandle:
        """Get annex at index (0-3)."""
        if index < 0 or index >= self.MAX_ANNEXES:
            raise IndexError(f"Annex index must be 0-{self.MAX_ANNEXES-1}")

        raw = self._get_raw_annexes()
        if raw and index < len(raw):
            return AnnexHandle.from_raw(raw[index])
        return AnnexHandle()  # Empty annex

    def __iter__(self):
        """Iterate over all annexes."""
        for i in range(self.MAX_ANNEXES):
            yield self[i]

    def all(self) -> List[AnnexHandle]:
        """Get all annexes as list of handles."""
        return [self[i] for i in range(self.MAX_ANNEXES)]

    def active(self) -> List[AnnexHandle]:
        """Get only annexes with valid unit_id."""
        return [a for a in self if a.exists]

    def set(self, index: int, unit_id: int, x: float = 0.0, y: float = 0.0) -> None:
        """
        Set an annex at the given index.

        Args:
            index: Annex slot (0-3)
            unit_id: Unit ID to spawn
            x: X offset from building center
            y: Y offset from building center
        """
        if index < 0 or index >= self.MAX_ANNEXES:
            raise IndexError(f"Annex index must be 0-{self.MAX_ANNEXES-1}")

        for unit in self._units:
            if unit.building and unit.building.annexes:
                annexes = list(unit.building.annexes)
                if index < len(annexes):
                    # Update existing annex
                    annexes[index].unit_id = unit_id
                    annexes[index].misplacement_x = x
                    annexes[index].misplacement_y = y

    def clear(self, index: int) -> None:
        """Clear an annex by setting unit_id to -1."""
        self.set(index, -1, 0.0, 0.0)

    def clear_all(self) -> None:
        """Clear all annexes."""
        for i in range(self.MAX_ANNEXES):
            self.clear(i)
