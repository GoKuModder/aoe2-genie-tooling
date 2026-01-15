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

    def _clone_base_struct(self, source: Any, depth: int = 0, debug: bool = False) -> Any:
        """
        Recursively clone a bfp_rs.BaseStruct object.
        
        Creates a new instance of the same class and copies all attributes.
        Handles nested BaseStruct objects and lists recursively.
        
        NOTE: bfp_rs.Retriever list fields (like attacks, armors, tasks) use
        copy semantics - setattr copies items into internal storage. We must
        use getattr(new_obj, name).extend(cloned_items) to populate lists.
        """
        indent = "  " * depth
        if source is None:
            return None
            
        # Get the class to instantiate
        cls = source.__class__
        
        # Create new instance (bfp_rs.BaseStruct types need ver argument)
        try:
            if hasattr(source, 'ver'):
                new_obj = cls(ver=source.ver)
            else:
                new_obj = cls()
            if debug:
                print(f"{indent}Created new {cls.__name__}: id {id(source)} -> {id(new_obj)}")
        except Exception as e:
            # If we can't create a new instance, return the original (last resort)
            if debug:
                print(f"{indent}FAILED to create {cls.__name__}: {e}")
            return source
        
        # Copy all public attributes
        for name in dir(source):
            if name.startswith("_"):
                continue
            if name == "ver":  # Already set in constructor
                continue
            try:
                attr = getattr(source, name)
                if callable(attr):
                    continue
                
                # Special handling for lists: bfp_rs.Retriever uses copy semantics
                # We need to extend the new object's list with cloned items
                if isinstance(attr, list):
                    try:
                        target_list = getattr(new_obj, name)
                        if isinstance(target_list, list):
                            # Clone each item and extend the target list
                            cloned_items = [self._clone_value(item, depth + 1, debug) for item in attr]
                            target_list.extend(cloned_items)
                            if debug:
                                print(f"{indent}  Extended {name} with {len(cloned_items)} items")
                            continue
                    except Exception:
                        pass
                
                # For non-list attributes, recursively clone and setattr
                val = self._clone_value(attr, depth + 1, debug)
                
                try:
                    setattr(new_obj, name, val)
                except Exception:
                    pass
            except Exception:
                pass
        
        return new_obj
    
    def _clone_value(self, value: Any, depth: int = 0, debug: bool = False) -> Any:
        """
        Clone a single value, handling lists and BaseStruct objects recursively.
        """
        indent = "  " * depth
        if value is None:
            return None
        
        # Handle lists - create new list with cloned items
        if isinstance(value, list):
            if debug:
                print(f"{indent}Cloning list of {len(value)} items")
            new_list = [self._clone_value(item, depth + 1, debug) for item in value]
            if debug:
                print(f"{indent}  Original list id: {id(value)}, New list id: {id(new_list)}")
            return new_list
        
        # Handle bfp_rs.BaseStruct objects (have 'ver' attribute and are not primitives)
        if hasattr(value, 'ver') and hasattr(value, '__class__'):
            # Additional check: make sure it's not a primitive type masquerading
            if not isinstance(value, (int, float, str, bool)):
                if debug:
                    print(f"{indent}Cloning BaseStruct: {type(value).__name__}")
                return self._clone_base_struct(value, depth, debug)
        
        # For primitives (int, float, str, bool, etc.), return as-is
        return value

    def _clone_unit(self, source: Any) -> Any:
        """
        Clone a Unit object manually to avoid shared references.
        
        Due to bfp_rs.Retriever behavior:
        - Nested BaseStruct fields (combat_info, task_info) have separate internal storage
        - Assigning cloned objects doesn't update their nested list storage
        - We must modify the new Unit's existing nested fields IN-PLACE
        - List fields use clear() + extend() with cloned items
        - type_ MUST be set first to trigger proper struct initialization
        """
        from sections.civilization.unit import Unit

        new_unit = Unit(ver=source.ver)
        
        # CRITICAL: Set type_ FIRST to trigger proper nested struct initialization
        # The disable_types() callback in bfp_rs sets structs to None based on type
        # If we set type_ after creation, the correct structs will be initialized
        try:
            new_unit.type_ = source.type_
        except Exception:
            pass
        
        # Nested struct fields that need special in-place handling
        NESTED_STRUCT_FIELDS = {
            'combat_info', 'task_info', 'animation_info', 'movement_info',
            'creation_info', 'projectile_info', 'building_info'
        }

        # Copy all public attributes
        for name in dir(source):
            if name.startswith("_"):
                continue
            if name == "ver":  # Already set in constructor
                continue
            if name == "type_":  # Already set above
                continue
            try:
                attr = getattr(source, name)
                if callable(attr):
                    continue
                
                # Handle nested struct fields with in-place modification
                if name in NESTED_STRUCT_FIELDS:
                    if attr is not None:
                        target = getattr(new_unit, name)
                        
                        # CRITICAL: Check if target IS the same object as source
                        # This can happen due to bfp_rs internal storage behavior
                        # If so, we MUST create a new struct instance
                        if target is attr or target is None:
                            try:
                                cls = attr.__class__
                                new_struct = cls(ver=source.ver)
                                setattr(new_unit, name, new_struct)
                                target = getattr(new_unit, name)
                                # If still the same (setattr didn't work), warn
                                if target is attr:
                                    # Last resort: can't create independent struct
                                    pass
                            except Exception:
                                target = None
                        
                        if target is not None and target is not attr:
                            self._copy_struct_inplace(attr, target)
                    continue
                
                # Handle lists at Unit level (resources, damage_sprites)
                if isinstance(attr, list):
                    target_list = getattr(new_unit, name)
                    if isinstance(target_list, list):
                        cloned_items = [self._clone_item(item) for item in attr]
                        # CRITICAL: Always use setattr to trigger bfp_rs copy semantics!
                        # Using clear()+extend() does NOT work because bfp_rs lists
                        # share internal storage even when Python wrapper IDs differ.
                        try:
                            setattr(new_unit, name, cloned_items)
                        except Exception:
                            # Fallback: clear and extend (may still cause issues)
                            target_list.clear()
                            target_list.extend(cloned_items)
                    continue
                
                # Scalar values - use setattr
                try:
                    setattr(new_unit, name, attr)
                except Exception:
                    pass
            except Exception:
                pass

        return new_unit
    
    def _copy_struct_inplace(self, source: Any, target: Any) -> None:
        """
        Copy attributes from source struct into target struct IN-PLACE.
        
        Lists are handled carefully to ensure no shared references:
        - If target_list IS source_list (same object), use setattr to force new list
        - Otherwise, use clear() + extend() for in-place update
        """
        for name in dir(source):
            if name.startswith("_"):
                continue
            if name == "ver":
                continue
            try:
                attr = getattr(source, name)
                if callable(attr):
                    continue
                
                # Handle lists - ensure no shared references
                if isinstance(attr, list):
                    source_list = attr
                    target_list = getattr(target, name)
                    if isinstance(target_list, list):
                        cloned_items = [self._clone_item(item) for item in source_list]
                        # CRITICAL: Always use setattr to trigger bfp_rs copy semantics!
                        # Using clear()+extend() does NOT work because bfp_rs lists
                        # share internal storage even when Python wrapper IDs differ.
                        # setattr with a new list forces bfp_rs to copy into independent storage.
                        try:
                            setattr(target, name, cloned_items)
                        except Exception:
                            # Last resort: clear and extend (may still cause issues)
                            target_list.clear()
                            target_list.extend(cloned_items)
                    continue
                
                # Handle nested structs recursively
                if hasattr(attr, 'ver') and not isinstance(attr, (int, float, str, bool)):
                    target_nested = getattr(target, name)
                    if target_nested is not None:
                        self._copy_struct_inplace(attr, target_nested)
                    continue
                
                # Scalar values
                try:
                    setattr(target, name, attr)
                except Exception:
                    pass
            except Exception:
                pass
    
    def _clone_item(self, item: Any) -> Any:
        """Clone a single item (for list contents like DamageClass, UnitTask)."""
        if item is None:
            return None
        
        # For BaseStruct items, create new instance and copy attributes
        if hasattr(item, 'ver') and not isinstance(item, (int, float, str, bool)):
            cls = item.__class__
            try:
                new_item = cls(ver=item.ver) if hasattr(item, 'ver') else cls()
                # Copy all public attributes
                for name in dir(item):
                    if name.startswith("_") or name == "ver":
                        continue
                    try:
                        attr = getattr(item, name)
                        if not callable(attr):
                            setattr(new_item, name, attr)
                    except Exception:
                        pass
                return new_item
            except Exception:
                return item
        
        # Primitives returned as-is
        return item

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
