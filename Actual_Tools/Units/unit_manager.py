"""
GenieUnitManager - Production-quality unit management for AoE2 DAT files.

This module provides create(), clone_into(), and move() methods that return
UnitHandle objects for intuitive, multi-civ unit editing.

Example:
    # Create new unit based on Archer
    handle = manager.create("My Unit", base_unit_id=4)
    handle.stats.hit_points = 50
    
    # Clone unit into specific ID
    handle = manager.clone_into(dest_unit_id=1500, base_unit_id=4, name="Clone")
    
    # Move unit to new ID
    manager.move(src_unit_id=100, dst_unit_id=1501)
"""
from __future__ import annotations

import copy
from typing import TYPE_CHECKING, List, Literal, Optional

from Actual_Tools.Shared.tool_base import ToolBase
from Actual_Tools.Units.unit_handle import UnitHandle
from Actual_Tools.exceptions import (
    GapNotAllowedError,
    InvalidIdError,
    TemplateNotFoundError,
    UnitIdConflictError,
)

if TYPE_CHECKING:
    from genieutils.datfile import DatFile
    from genieutils.unit import Unit

__all__ = ['GenieUnitManager']


class GenieUnitManager(ToolBase):
    """
    Manager for creating, cloning, and moving units in a DAT file.
    
    All operations return UnitHandle objects that allow tab-style property
    access with automatic multi-civ propagation.
    
    Key features:
    - No explicit apply()/commit step - changes are immediate
    - Placeholder-based capacity extension (no None gaps)
    - Multi-civ support with per-civ override capability
    """

    def __init__(self, dat_file: DatFile) -> None:
        super().__init__(dat_file)

    # -------------------------
    # Core CRUD Operations
    # -------------------------

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
            enable_for_civs: List of civ IDs to enable for. If None, all civs.
            on_conflict: "error" to raise if ID exists, "overwrite" to replace
            fill_gaps: "error" to raise if gaps needed, "placeholder" to fill gaps
        
        Returns:
            UnitHandle for editing the created unit across all enabled civs
        
        Raises:
            UnitIdConflictError: If on_conflict="error" and ID already exists
            GapNotAllowedError: If fill_gaps="error" and gaps would be created
            TemplateNotFoundError: If no template unit can be found
            InvalidIdError: If unit_id is negative
        """
        # Determine target ID
        if unit_id is None:
            unit_id = self.allocate_next_unit_id()
        else:
            self.validate_id_positive(unit_id, "unit_id")
        
        # Determine civs to enable
        if enable_for_civs is None:
            enable_for_civs = list(range(len(self.dat_file.civs)))
        
        # Check capacity for all civs
        self._ensure_capacity_all_civs(unit_id, fill_gaps)
        
        # Check conflict
        if self.exists(unit_id):
            if on_conflict == "error":
                raise UnitIdConflictError(
                    f"Unit ID {unit_id} already exists. Use on_conflict='overwrite' to replace."
                )
            # overwrite -> proceed
        
        # Get or create template
        template = self._get_template(base_unit_id)
        
        # Create new unit from template
        new_unit = copy.deepcopy(template)
        new_unit.id = unit_id
        new_unit.name = name
        new_unit.enabled = 1
        
        # Insert into civs
        for civ_id, civ in enumerate(self.dat_file.civs):
            if civ_id in enable_for_civs:
                civ.units[unit_id] = copy.deepcopy(new_unit)
            # Note: For civs not in enable_for_civs, we keep existing value or placeholder
        
        # Log and register
        self._track_unit(name, unit_id, base_unit_id)
        
        return UnitHandle(unit_id, self.dat_file, enable_for_civs)

    def clone_into(
        self,
        dest_unit_id: int,
        base_unit_id: int,
        name: Optional[str] = None,
        enable_for_civs: Optional[List[int]] = None,
        on_conflict: Literal["error", "overwrite"] = "error",
        fill_gaps: Literal["error", "placeholder"] = "placeholder",
    ) -> UnitHandle:
        """
        Clone an existing unit into a specific destination ID.
        
        This is the primary method for creating units at specific IDs
        with full control over placement.
        
        Args:
            dest_unit_id: Target unit ID for the clone
            base_unit_id: Source unit ID to clone from
            name: Name for the clone. If None, keeps original name.
            enable_for_civs: List of civ IDs. If None, all civs.
            on_conflict: "error" to raise if dest exists, "overwrite" to replace
            fill_gaps: "error" to raise if gaps needed, "placeholder" to fill gaps
        
        Returns:
            UnitHandle for editing the cloned unit
        """
        self.validate_id_positive(dest_unit_id, "dest_unit_id")
        self.validate_id_positive(base_unit_id, "base_unit_id")
        
        # Determine civs
        if enable_for_civs is None:
            enable_for_civs = list(range(len(self.dat_file.civs)))
        
        # Ensure capacity
        self._ensure_capacity_all_civs(dest_unit_id, fill_gaps)
        
        # Check conflict
        if self.exists(dest_unit_id):
            if on_conflict == "error":
                raise UnitIdConflictError(
                    f"Unit ID {dest_unit_id} already exists. Use on_conflict='overwrite' to replace."
                )
        
        # Get source unit
        source = self.get_unit(base_unit_id)
        if source is None:
            raise InvalidIdError(f"Base unit ID {base_unit_id} not found.")
        
        # Clone into each civ
        for civ_id, civ in enumerate(self.dat_file.civs):
            if civ_id in enable_for_civs:
                # Get civ-specific source if available
                civ_source = civ.units[base_unit_id] if base_unit_id < len(civ.units) else None
                if civ_source is None:
                    civ_source = source
                
                new_unit = copy.deepcopy(civ_source)
                new_unit.id = dest_unit_id
                if name is not None:
                    new_unit.name = name
                new_unit.enabled = 1
                
                civ.units[dest_unit_id] = new_unit
        
        # Log and register
        final_name = name if name else source.name
        self._track_unit_clone(final_name, dest_unit_id, base_unit_id)
        
        return UnitHandle(dest_unit_id, self.dat_file, enable_for_civs)

    def move(
        self,
        src_unit_id: int,
        dst_unit_id: int,
        on_conflict: Literal["error", "overwrite", "swap"] = "error",
        fill_gaps: Literal["error", "placeholder"] = "placeholder",
    ) -> None:
        """
        Move a unit from source ID to destination ID.
        
        After move, source ID will contain a placeholder (not None).
        This maintains the "no gaps" invariant.
        
        Args:
            src_unit_id: Source unit ID to move from
            dst_unit_id: Destination unit ID to move to
            on_conflict: 
                "error" - raise if dst exists
                "overwrite" - replace dst with src
                "swap" - exchange src and dst units
            fill_gaps: "error" to raise if gaps needed, "placeholder" to fill
        
        Raises:
            UnitIdConflictError: If on_conflict="error" and dst exists
            InvalidIdError: If src doesn't exist or IDs are invalid
        """
        self.validate_id_positive(src_unit_id, "src_unit_id")
        self.validate_id_positive(dst_unit_id, "dst_unit_id")
        
        if not self.exists(src_unit_id):
            raise InvalidIdError(f"Source unit ID {src_unit_id} does not exist.")
        
        # Ensure capacity at destination
        self._ensure_capacity_all_civs(dst_unit_id, fill_gaps)
        
        dst_exists = self.exists(dst_unit_id)
        
        if dst_exists and on_conflict == "error":
            raise UnitIdConflictError(
                f"Destination unit ID {dst_unit_id} already exists. "
                "Use on_conflict='overwrite' or 'swap'."
            )
        
        # Create placeholder factory for source slot
        placeholder_factory = self.create_unit_placeholder_factory()
        
        for civ in self.dat_file.civs:
            src_unit = civ.units[src_unit_id] if src_unit_id < len(civ.units) else None
            dst_unit = civ.units[dst_unit_id] if dst_unit_id < len(civ.units) else None
            
            if on_conflict == "swap":
                # Swap src and dst
                if src_unit is not None:
                    src_unit.id = dst_unit_id
                if dst_unit is not None:
                    dst_unit.id = src_unit_id
                
                civ.units[dst_unit_id] = src_unit if src_unit is not None else placeholder_factory()
                civ.units[src_unit_id] = dst_unit if dst_unit is not None else placeholder_factory()
            else:
                # Move (or overwrite)
                if src_unit is not None:
                    moved_unit = src_unit
                    moved_unit.id = dst_unit_id
                    civ.units[dst_unit_id] = moved_unit
                    
                    # Replace source with placeholder (not None!)
                    placeholder = placeholder_factory()
                    placeholder.id = src_unit_id
                    civ.units[src_unit_id] = placeholder
                else:
                    # src was None for this civ, ensure dst has placeholder
                    if civ.units[dst_unit_id] is None:
                        placeholder = placeholder_factory()
                        placeholder.id = dst_unit_id
                        civ.units[dst_unit_id] = placeholder
        
        # Log
        self._track_unit_move(src_unit_id, dst_unit_id)

    # -------------------------
    # Query Operations
    # -------------------------

    def get(self, unit_id: int, civ_ids: Optional[List[int]] = None) -> UnitHandle:
        """
        Get a handle for an existing unit.
        
        Args:
            unit_id: The unit ID to get
            civ_ids: List of civ IDs to include. If None, all civs.
        
        Returns:
            UnitHandle for the unit
        
        Raises:
            InvalidIdError: If unit doesn't exist
        """
        if not self.exists(unit_id):
            raise InvalidIdError(f"Unit ID {unit_id} does not exist.")
        
        if civ_ids is None:
            civ_ids = list(range(len(self.dat_file.civs)))
        
        return UnitHandle(unit_id, self.dat_file, civ_ids)

    def get_unit(self, unit_id: int, civ_id: int = 0) -> Optional[Unit]:
        """
        Get the raw Unit object for a specific unit ID and civ.
        
        Args:
            unit_id: The unit ID
            civ_id: The civilization ID (default 0)
        
        Returns:
            The Unit object, or None if not found
        """
        if civ_id < 0 or civ_id >= len(self.dat_file.civs):
            return None
        
        civ_units = self.dat_file.civs[civ_id].units
        if 0 <= unit_id < len(civ_units):
            return civ_units[unit_id]
        return None

    def exists(self, unit_id: int) -> bool:
        """
        Check if a unit ID exists (is not None and not a placeholder) in any civ.
        
        A "placeholder" unit is detected by: enabled=0 AND name="" AND hit_points=1
        This allows distinguishing real units from capacity placeholders.
        """
        for civ in self.dat_file.civs:
            if 0 <= unit_id < len(civ.units):
                unit = civ.units[unit_id]
                if unit is not None:
                    # Check if it's a placeholder
                    if not self._is_placeholder(unit):
                        return True
        return False

    def exists_raw(self, unit_id: int) -> bool:
        """
        Check if a unit ID exists (is not None) in any civ.
        
        Unlike exists(), this returns True for placeholders too.
        """
        for civ in self.dat_file.civs:
            if 0 <= unit_id < len(civ.units):
                if civ.units[unit_id] is not None:
                    return True
        return False

    def count(self) -> int:
        """Return the total number of unit slots in civ 0."""
        if not self.dat_file.civs:
            return 0
        return len(self.dat_file.civs[0].units)

    # -------------------------
    # Internal Helpers
    # -------------------------

    def _ensure_capacity_all_civs(
        self,
        required_index: int,
        fill_gaps: Literal["error", "placeholder"],
    ) -> None:
        """
        Ensure all civs have capacity for the required index.
        
        If fill_gaps="placeholder", fills with valid placeholder units.
        If fill_gaps="error", raises if extension is needed.
        """
        needs_extension = any(
            required_index >= len(civ.units)
            for civ in self.dat_file.civs
        )
        
        if needs_extension and fill_gaps == "error":
            max_len = max(len(civ.units) for civ in self.dat_file.civs)
            raise GapNotAllowedError(
                f"Unit ID {required_index} exceeds current max ID {max_len - 1}. "
                "Use fill_gaps='placeholder' to extend with placeholders."
            )
        
        # Create placeholder factory
        placeholder_factory = self.create_unit_placeholder_factory()
        
        for civ in self.dat_file.civs:
            current_len = len(civ.units)
            while len(civ.units) <= required_index:
                placeholder = placeholder_factory()
                placeholder.id = len(civ.units)
                civ.units.append(placeholder)

    def _get_template(self, base_unit_id: Optional[int]) -> Unit:
        """
        Get a template unit for cloning.
        
        If base_unit_id is specified, returns that unit.
        Otherwise, finds the first valid non-placeholder unit.
        """
        if base_unit_id is not None:
            template = self.get_unit(base_unit_id)
            if template is None:
                raise InvalidIdError(f"Base unit ID {base_unit_id} not found.")
            return template
        
        # Find first valid non-placeholder unit
        template = self.find_first_valid_unit()
        if template is None:
            raise TemplateNotFoundError(
                "Cannot create unit: no valid template unit found in DAT file."
            )
        return template

    def _is_placeholder(self, unit: Unit) -> bool:
        """
        Check if a unit is a placeholder (disabled, empty name, 1 HP).
        """
        return (
            unit.enabled == 0 and
            unit.name == "" and
            unit.hit_points == 1
        )

    def _get_max_id(self) -> int:
        """
        Get the highest occupied (non-placeholder) unit ID across all civs.
        
        Returns -1 if no real units exist.
        """
        max_id = -1
        for civ in self.dat_file.civs:
            for i in range(len(civ.units) - 1, -1, -1):
                unit = civ.units[i]
                if unit is not None and not self._is_placeholder(unit):
                    if i > max_id:
                        max_id = i
                    break
        return max_id
