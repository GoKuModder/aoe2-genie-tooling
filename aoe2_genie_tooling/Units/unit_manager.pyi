"""Type stubs for UnitManager - enables IDE autocomplete"""
from typing import Any, List, Literal, Optional

from aoe2_genie_tooling.Units.unit_handle import UnitHandle


class UnitManager:
    """Manager for creating, cloning, and moving units in a DAT file."""
    
    def create(
        self,
        name: str,
        base_unit_id: Optional[int] = None,
        unit_id: Optional[int] = None,
        enable_for_civs: Optional[List[int]] = None,
        on_conflict: Literal["error", "overwrite"] = "error",
        fill_gaps: Literal["error", "placeholder"] = "placeholder",
    ) -> UnitHandle:
        """
        Create a new unit.
        
        Args:
            name: Name for the new unit
            base_unit_id: Unit ID to clone from. If None, uses first valid unit.
            unit_id: Target unit ID. If None, appends to end.
            enable_for_civs: List of civ IDs to enable for. None = all civs.
            on_conflict: "error" or "overwrite"
            fill_gaps: "error" or "placeholder"
        """
        ...
    
    def clone_into(
        self,
        dest_unit_id: int,
        src_unit_id: int,
        name: Optional[str] = None,
        enable_for_civs: Optional[List[int]] = None,
        on_conflict: Literal["error", "overwrite"] = "error",
        fill_gaps: Literal["error", "placeholder"] = "placeholder",
    ) -> UnitHandle:
        """Clone an existing unit into a specific destination ID."""
        ...
    
    def move(
        self,
        src_unit_id: int,
        dst_unit_id: int,
        on_conflict: Literal["error", "overwrite", "swap"] = "error",
        fill_gaps: Literal["error", "placeholder"] = "placeholder",
    ) -> UnitHandle:
        """Move a unit from source ID to destination ID."""
        ...
    
    def get(self, unit_id: int, civ_ids: Optional[List[int]] = None) -> UnitHandle:
        """Get a handle for an existing unit."""
        ...
    
    def get_unit(self, unit_id: int, civ_id: int = 0) -> Optional[Any]:
        """Get the raw Unit object for a specific unit ID and civ."""
        ...
    
    def exists(self, unit_id: int) -> bool:
        """Check if a unit ID exists (is not None and not a placeholder)."""
        ...
    
    def exists_raw(self, unit_id: int) -> bool:
        """Check if a unit ID exists (is not None, includes placeholders)."""
        ...
    
    def count(self) -> int:
        """Return the total number of unit slots in civ 0."""
        ...
    
    def find_by_name(self, name: str, civ_id: int = 0) -> Optional[UnitHandle]:
        """Find first unit matching name in the specified civ."""
        ...
