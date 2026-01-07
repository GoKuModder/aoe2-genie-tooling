"""
UnitManager - Production-quality unit management for AoE2 DAT files.

Ported from GenieUnitManager (genieutils-py) to work with GenieDatParser.

This module provides create(), clone_into(), and move() methods that return
UnitHandle objects for intuitive, multi-civ unit editing.

Example:
    # Create new unit based on Archer
    handle = manager.create("My Unit", base_unit_id=4)
    handle.hit_points = 50

    # Clone unit into specific ID
    handle = manager.clone_into(dest_unit_id=1500, base_unit_id=4, name="Clone")

    # Move unit to new ID
    manager.move(src_unit_id=100, dst_unit_id=1501)
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, List, Literal, Optional

if TYPE_CHECKING:
    from Actual_Tools_GDP.Base.workspace import GenieWorkspace
    from Actual_Tools_GDP.Units.unit_handle import UnitHandle

__all__ = ['UnitManager']


class UnitManager:
    """
    Manager for creating, cloning, and moving units in a DAT file.

    All operations return UnitHandle objects that allow tab-style property
    access with automatic multi-civ propagation.

    Key features:
    - No explicit apply()/commit step - changes are immediate
    - Placeholder-based capacity extension (no None gaps)
    - Multi-civ support with per-civ override capability
    """

    def __init__(self, workspace: GenieWorkspace) -> None:
        """Initialize UnitManager with workspace reference."""
        self.workspace = workspace

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
        from Actual_Tools_GDP.Base.core.exceptions import (
            GapNotAllowedError,
            InvalidIdError,
            TemplateNotFoundError,
            UnitIdConflictError,
        )
        from Actual_Tools_GDP.Units.unit_handle import UnitHandle

        civs = self.workspace.dat.civilizations

        # Determine target ID
        if unit_id is None:
            unit_id = self._allocate_next_unit_id()
        else:
            self._validate_id_positive(unit_id, "unit_id")

        # Determine civs to enable
        if enable_for_civs is None:
            enable_for_civs = list(range(len(civs)))

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
        new_unit = self._clone_unit(template)
        new_unit.id = unit_id
        try:
            new_unit.name = name
        except Exception:
            pass
        new_unit.enabled = True

        # Insert into civs
        for civ_id, civ in enumerate(civs):
            if civ_id in enable_for_civs:
                civs[civ_id].units[unit_id] = self._clone_unit(new_unit)
            # Note: For civs not in enable_for_civs, we keep existing value or placeholder

        # Track and register
        self._track_unit(name, unit_id, base_unit_id)

        return UnitHandle(self.workspace, unit_id, enable_for_civs)

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
        from Actual_Tools_GDP.Base.core.exceptions import (
            InvalidIdError,
            UnitIdConflictError,
        )
        from Actual_Tools_GDP.Units.unit_handle import UnitHandle

        self._validate_id_positive(dest_unit_id, "dest_unit_id")
        self._validate_id_positive(base_unit_id, "base_unit_id")

        civs = self.workspace.dat.civilizations

        # Determine civs
        if enable_for_civs is None:
            enable_for_civs = list(range(len(civs)))

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
        for civ_id, civ in enumerate(civs):
            if civ_id in enable_for_civs:
                # Get civ-specific source if available
                civ_source = civ.units[base_unit_id] if base_unit_id < len(civ.units) else None
                if civ_source is None:
                    civ_source = source

                new_unit = self._clone_unit(civ_source)
                new_unit.id = dest_unit_id
                if name is not None:
                    try:
                        new_unit.name = name
                    except Exception:
                        pass
                new_unit.enabled = True

                civ.units[dest_unit_id] = new_unit

        # Track and register
        final_name = name if name else source.name
        self._track_unit_clone(final_name, dest_unit_id, base_unit_id)

        return UnitHandle(self.workspace, dest_unit_id, enable_for_civs)

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
        from Actual_Tools_GDP.Base.core.exceptions import (
            InvalidIdError,
            UnitIdConflictError,
        )

        self._validate_id_positive(src_unit_id, "src_unit_id")
        self._validate_id_positive(dst_unit_id, "dst_unit_id")

        if not self.exists(src_unit_id):
            raise InvalidIdError(f"Source unit ID {src_unit_id} does not exist.")

        civs = self.workspace.dat.civilizations

        # Ensure capacity at destination
        self._ensure_capacity_all_civs(dst_unit_id, fill_gaps)

        dst_exists = self.exists(dst_unit_id)

        if dst_exists and on_conflict == "error":
            raise UnitIdConflictError(
                f"Destination unit ID {dst_unit_id} already exists. "
                "Use on_conflict='overwrite' or 'swap'."
            )

        # Create placeholder factory for source slot
        placeholder_factory = self._create_unit_placeholder_factory()

        for civ in civs:
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

        # Track
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
        from Actual_Tools_GDP.Base.core.exceptions import InvalidIdError
        from Actual_Tools_GDP.Units.unit_handle import UnitHandle

        if not self.exists(unit_id):
            raise InvalidIdError(f"Unit ID {unit_id} does not exist.")

        if civ_ids is None:
            civ_ids = list(range(len(self.workspace.dat.civilizations)))

        return UnitHandle(self.workspace, unit_id, civ_ids)

    def get_unit(self, unit_id: int, civ_id: int = 0) -> Optional[Any]:
        """
        Get the raw Unit object for a specific unit ID and civ.

        Args:
            unit_id: The unit ID
            civ_id: The civilization ID (default 0)

        Returns:
            The Unit object, or None if not found
        """
        civs = self.workspace.dat.civilizations
        if civ_id < 0 or civ_id >= len(civs):
            return None

        civ_units = civs[civ_id].units
        if 0 <= unit_id < len(civ_units):
            return civ_units[unit_id]
        return None

    def exists(self, unit_id: int) -> bool:
        """
        Check if a unit ID exists (is not None and not a placeholder) in any civ.

        A "placeholder" unit is detected by: enabled=0 AND name="" AND hit_points=1
        This allows distinguishing real units from capacity placeholders.
        """
        for civ in self.workspace.dat.civilizations:
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
        for civ in self.workspace.dat.civilizations:
            if 0 <= unit_id < len(civ.units):
                if civ.units[unit_id] is not None:
                    return True
        return False

    def count(self) -> int:
        """Return the total number of unit slots in civ 0."""
        civs = self.workspace.dat.civilizations
        if not civs:
            return 0
        return len(civs[0].units)

    def find_by_name(self, name: str, civ_id: int = 0) -> Optional[UnitHandle]:
        """
        Find first unit matching name in the specified civ.

        Args:
            name: Unit name to search for
            civ_id: Civilization ID to search in (default 0)

        Returns:
            UnitHandle for the unit, or None if not found
        """
        from Actual_Tools_GDP.Units.unit_handle import UnitHandle

        civs = self.workspace.dat.civilizations
        if civ_id < 0 or civ_id >= len(civs):
            return None

        for i, unit in enumerate(civs[civ_id].units):
            if unit is not None and not self._is_placeholder(unit):
                unit_name = ""
                try:
                    unit_name = unit.name
                except Exception:
                    pass
                if unit_name == name:
                    return UnitHandle(self.workspace, i)
        return None

    # -------------------------
    # Internal Helpers
    # -------------------------

    def _allocate_next_unit_id(self) -> int:
        """Allocates the next unit ID based on civ[0]'s unit list length."""
        civs = self.workspace.dat.civilizations
        if not civs:
            return 0
        return len(civs[0].units)

    def _validate_id_positive(self, id_value: int, name: str = "ID") -> None:
        """Validates that an ID is non-negative."""
        from Actual_Tools_GDP.Base.core.exceptions import InvalidIdError
        if id_value < 0:
            raise InvalidIdError(f"{name} {id_value} cannot be negative.")

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
        from Actual_Tools_GDP.Base.core.exceptions import GapNotAllowedError

        civs = self.workspace.dat.civilizations

        needs_extension = any(
            required_index >= len(civ.units)
            for civ in civs
        )

        if needs_extension and fill_gaps == "error":
            max_len = max(len(civ.units) for civ in civs)
            raise GapNotAllowedError(
                f"Unit ID {required_index} exceeds current max ID {max_len - 1}. "
                "Use fill_gaps='placeholder' to extend with placeholders."
            )

        # Create placeholder factory
        placeholder_factory = self._create_unit_placeholder_factory()

        for civ in civs:
            while len(civ.units) <= required_index:
                placeholder = placeholder_factory()
                placeholder.id = len(civ.units)
                civ.units.append(placeholder)

    def _get_template(self, base_unit_id: Optional[int]) -> Any:
        """
        Get a template unit for cloning.

        If base_unit_id is specified, returns that unit.
        Otherwise, finds the first valid non-placeholder unit.
        """
        from Actual_Tools_GDP.Base.core.exceptions import (
            InvalidIdError,
            TemplateNotFoundError,
        )

        if base_unit_id is not None:
            template = self.get_unit(base_unit_id)
            if template is None:
                raise InvalidIdError(f"Base unit ID {base_unit_id} not found.")
            return template

        # Find first valid non-placeholder unit
        template = self._find_first_valid_unit()
        if template is None:
            raise TemplateNotFoundError(
                "Cannot create unit: no valid template unit found in DAT file."
            )
        return template

    def _find_first_valid_unit(self) -> Optional[Any]:
        """Finds the first non-None, non-placeholder unit across all civs."""
        for civ in self.workspace.dat.civilizations:
            if civ and civ.units:
                for unit in civ.units:
                    if unit is not None and not self._is_placeholder(unit):
                        return unit
        return None

    def _is_placeholder(self, unit: Any) -> bool:
        """
        Check if a unit is a placeholder (disabled, empty name, 1 HP).
        """
        try:
            return (
                unit.enabled == 0 and
                unit.name == "" and
                unit.hit_points == 1
            )
        except Exception:
            return False

    def _get_max_id(self) -> int:
        """
        Get the highest occupied (non-placeholder) unit ID across all civs.

        Returns -1 if no real units exist.
        """
        max_id = -1
        for civ in self.workspace.dat.civilizations:
            for i in range(len(civ.units) - 1, -1, -1):
                unit = civ.units[i]
                if unit is not None and not self._is_placeholder(unit):
                    if i > max_id:
                        max_id = i
                    break
        return max_id

    def _create_unit_placeholder_factory(self) -> Callable[[], Any]:
        """Returns a factory function that creates placeholder units."""
        from Actual_Tools_GDP.Base.core.exceptions import TemplateNotFoundError

        template = self._find_first_valid_unit()
        if template is None:
            raise TemplateNotFoundError(
                "Cannot create placeholder factory: no valid template unit found."
            )

        def factory() -> Any:
            placeholder = self._clone_unit(template)
            try:
                placeholder.name = ""
            except Exception:
                pass
            placeholder.enabled = False
            placeholder.hit_points = 1
            return placeholder

        return factory

    def _clone_unit(self, source: Any) -> Any:
        """
        Clone a Unit object manually to avoid pickle issues/shared references.

        Copies all public attributes from source to a new Unit instance,
        using deepcopy to ensure isolation (fixing shared list issues).
        Fallbacks to shallow copy for lists/task_info if deepcopy fails.
        """
        from sections.civilization.unit import Unit
        import copy

        new_unit = Unit(ver=source.ver)

        # Copy all public attributes
        for name in dir(source):
            if name.startswith("_"):
                continue
            try:
                attr = getattr(source, name)
                if callable(attr):
                    continue
                
                # Special handling for known container types that must be independent
                # 1. Lists (attacks, etc.)
                if isinstance(attr, list):
                    try:
                        val = copy.deepcopy(attr)
                    except Exception:
                        # Fallback: Shallow copy the list so appends are independent
                        val = list(attr)
                    setattr(new_unit, name, val)
                    continue
                
                # 2. task_info (Nested object with list)
                if name == "task_info" and attr is not None:
                    try:
                        val = copy.deepcopy(attr)
                    except Exception:
                        # Fallback: Copy object + shallow copy tasks list
                        try:
                            val = copy.copy(attr)
                            if hasattr(val, "tasks") and isinstance(val.tasks, list):
                                val.tasks = list(val.tasks)
                        except Exception:
                            val = attr
                    setattr(new_unit, name, val)
                    continue

                # Default handling for other attributes
                try:
                    val = copy.deepcopy(attr)
                except Exception:
                    # Fallback if uncopyable
                    val = attr

                # Try to set on new unit
                try:
                    setattr(new_unit, name, val)
                except (AttributeError, Exception):
                    pass
            except Exception:
                pass

        return new_unit

    # -------------------------
    # Tracking Helpers
    # -------------------------

    def _track_unit(self, name: str, unit_id: int, base_unit_id: Optional[int] = None) -> None:
        """Log and register a unit creation."""
        self.workspace.logger.success(f"Created unit '{name}' at ID {unit_id}", "units")
        self.workspace.registry.register_unit(name, unit_id, base_unit_id=base_unit_id)

    def _track_unit_clone(self, name: str, unit_id: int, source_id: int) -> None:
        """Log and register a unit clone."""
        self.workspace.logger.success(f"Cloned unit '{name}' from {source_id} to {unit_id}", "units")
        self.workspace.registry.register_unit(name, unit_id, base_unit_id=source_id)

    def _track_unit_move(self, src_id: int, dst_id: int) -> None:
        """Log a unit move (no registry needed)."""
        self.workspace.logger.info(f"Moved unit from {src_id} to {dst_id}", "units")
