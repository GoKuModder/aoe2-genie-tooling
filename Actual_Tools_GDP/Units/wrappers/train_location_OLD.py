"""
TrainLocationHandle - Wrapper for unit train location entries.

Train locations define where a unit can be trained (which building) and its
button configuration in the build menu.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, List, Optional

if TYPE_CHECKING:
    # TODO: Removed genie-rust dependency - needs migration to GenieDatParser
    # from genie_rust import Unit
    pass

__all__ = ["TrainLocationHandle", "TrainLocationsWrapper"]


@dataclass
class TrainLocationHandle:
    """
    Handle for a single train location entry.

    Defines where a unit can be trained and how it appears in the UI.

    Attributes:
        unit_id: Building unit ID that can train this unit
        train_time: Time to train (in seconds * 1.0)
        button_id: Button position in building UI (0-based)
        hotkey_id: Hotkey ID for this button
    """
    unit_id: int = -1
    train_time: int = 0
    button_id: int = 0
    hotkey_id: int = -1

    @classmethod
    def from_raw(cls, raw_train_loc: Any) -> "TrainLocationHandle":
        """Create from raw genieutils train location object."""
        if raw_train_loc is None:
            return cls()
        return cls(
            unit_id=getattr(raw_train_loc, "unit_id", -1),
            train_time=getattr(raw_train_loc, "train_time", 0),
            button_id=getattr(raw_train_loc, "button_id", 0),
            hotkey_id=getattr(raw_train_loc, "hotkey_id", -1),
        )

    @property
    def exists(self) -> bool:
        """True if this train location has a valid building assigned."""
        return self.unit_id >= 0


class TrainLocationsWrapper:
    """
    Wrapper for managing unit train locations.

    Train locations define which buildings can create this unit.
    For example, Archer can be trained at Archery Range.

    Usage:
        locs = unit.creatable.train_locations_wrapper
        locs.add(unit_id=12, train_time=35, button_id=0)
        locs[0].unit_id  # Get first location's building
    """

    def __init__(self, units: List["Unit"]) -> None:
        """
        Initialize with list of units to modify.

        Args:
            units: List of Unit objects with creatable component
        """
        self._units = units

    def _get_raw_locations(self) -> Optional[List]:
        """Get raw train_locations list from first unit."""
        if self._units and self._units[0].creatable:
            return self._units[0].creatable.train_locations
        return None

    def __len__(self) -> int:
        """Number of train locations."""
        raw = self._get_raw_locations()
        return len(raw) if raw else 0

    def __getitem__(self, index: int) -> TrainLocationHandle:
        """Get train location at index."""
        raw = self._get_raw_locations()
        if raw and 0 <= index < len(raw):
            return TrainLocationHandle.from_raw(raw[index])
        raise IndexError(f"Train location index {index} out of range")

    def __iter__(self):
        """Iterate over all train locations."""
        raw = self._get_raw_locations()
        if raw:
            for loc in raw:
                yield TrainLocationHandle.from_raw(loc)

    def all(self) -> List[TrainLocationHandle]:
        """Get all train locations as list of handles."""
        return list(self)

    def active(self) -> List[TrainLocationHandle]:
        """Get only train locations with valid unit_id."""
        return [loc for loc in self if loc.exists]

    def add(self, unit_id: int, train_time: int = 0, button_id: int = 0, hotkey_id: int = -1) -> None:
        """
        Add a new train location.

        Args:
            unit_id: Building that can train this unit
            train_time: Time to train
            button_id: Button position in building
            hotkey_id: Hotkey for the button
        """
        # This would need access to the actual genieutils structure
        # For now, this is a placeholder that shows the intended API
        raise NotImplementedError(
            "Adding train locations requires modifying the underlying genieutils structure. "
            "Currently read-only."
        )

    def clear(self, index: int) -> None:
        """Clear a train location by setting unit_id to -1."""
        raw = self._get_raw_locations()
        if raw and 0 <= index < len(raw):
            for unit in self._units:
                if unit.creatable and unit.creatable.train_locations:
                    unit.creatable.train_locations[index].unit_id = -1

    def clear_all(self) -> None:
        """Clear all train locations."""
        for i in range(len(self)):
            self.clear(i)
