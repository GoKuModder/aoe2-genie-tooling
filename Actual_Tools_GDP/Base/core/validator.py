"""
Validator - Validation helpers for attribute safety and type checking.

Responsibilities:
- Attribute allow-list enforcement (prevent typos)
- Type validation for Handle objects
- Reference validation (graphics, sounds exist)
- ID resolution (int, Handle, or UUID)
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Set, Sized, Type

from Actual_Tools_GDP.Base.core.exceptions import InvalidIdError
from Actual_Tools_GDP.Base.core.typed_ids import TypedId, GraphicId, DeltaIndex
from Actual_Tools_GDP.Base.core.field_metadata import FieldReference

if TYPE_CHECKING:
    from Actual_Tools_GDP.Base.workspace import GenieWorkspace

__all__ = ["Validator"]


class Validator:
    """
    Validation system for attribute safety and type checking.
    
    Features:
    - Flattening safety: Enforces allow-lists for flattened attributes
    - Type validation: Ensures Handle objects are used correctly
    - Reference validation: Checks IDs exist before save
    - ID resolution: Converts Handle/UUID to int
    """
    
    def __init__(self) -> None:
        """Initialize validator with empty state."""
        # Allow-lists for flattened attributes (populated by Handles)
        self._allow_lists: Dict[str, Set[str]] = {}
    
    # -------------------------
    # Allow-List Management
    # -------------------------
    
    def register_allow_list(self, handle_type: str, allowed_attrs: Set[str]) -> None:
        """
        Register flattened attribute allow-list for a Handle type.
        
        Args:
            handle_type: Type of handle (e.g., "UnitHandle")
            allowed_attrs: Set of allowed flattened attribute names
            
        Example:
            validator.register_allow_list("UnitHandle", {
                "hit_points", "move_sound", "attack_graphic"
            })
        """
        self._allow_lists[handle_type] = allowed_attrs
    
    def is_allowed_attr(self, handle_type: str, attr_name: str) -> bool:
        """
        Check if an attribute is allowed for flattening.
        
        Args:
            handle_type: Type of handle
            attr_name: Attribute name to check
            
        Returns:
            True if allowed, False otherwise
        """
        if handle_type not in self._allow_lists:
            return True  # No restrictions if not registered
        return attr_name in self._allow_lists[handle_type]
    
    def validate_attr(self, handle_type: str, attr_name: str) -> None:
        """
        Validate that an attribute is allowed.
        
        Args:
            handle_type: Type of handle
            attr_name: Attribute name
            
        Raises:
            AttributeError: If attribute not in allow-list
        """
        if not self.is_allowed_attr(handle_type, attr_name):
            raise AttributeError(
                f"{handle_type} has no flattened attribute '{attr_name}'. "
                f"Check for typos or use direct access (e.g., handle.bird.{attr_name})"
            )
    
    # -------------------------
    # Type Validation
    # -------------------------
    
    def validate_handle_type(
        self,
        value: Any,
        expected_type: str,
        attr_name: str
    ) -> int:
        """
        Validate that a value is the correct Handle type and extract ID.
        
        Args:
            value: Value to validate (int or Handle)
            expected_type: Expected handle type (e.g., "GraphicHandle")
            attr_name: Attribute name for error message
            
        Returns:
            The extracted ID (int)
            
        Raises:
            TypeError: If value is wrong type
        """
        # Accept raw integers
        if isinstance(value, int):
            return value
        
        # Accept Handle objects
        if hasattr(value, 'id'):
            return value.id
        elif hasattr(value, '_id'):
            return value._id
        
        # Reject everything else
        raise TypeError(
            f"{attr_name}: Expected int or {expected_type}, "
            f"got {type(value).__name__}"
        )
    
    # -------------------------
    # ID Resolution
    # -------------------------
    
    def resolve_id(
        self,
        value: Any,
        obj_type: str,
        workspace: GenieWorkspace,
        *,
        expected_handle_type: Optional[type] = None,
        param_name: str = "id",
    ) -> int:
        """
        Resolve a value to an integer ID.
        
        Accepts:
        - int: passed through
        - Handle object: extracts .id (validates type if expected_handle_type set)
        - str (UUID): looks up in Registry
        
        Args:
            value: int, UUID string, or Handle object
            obj_type: "units", "graphics", "sounds", etc.
            workspace: The GenieWorkspace for Registry access
            expected_handle_type: If set, validates Handle is this type
            param_name: Parameter name for error messages
            
        Returns:
            Resolved integer ID
            
        Raises:
            InvalidIdError: If UUID not found, wrong Handle type, or cannot resolve
        """
        # Handle object - validate type first
        if hasattr(value, 'id') or hasattr(value, '_id'):
            # Type check if expected type specified
            if expected_handle_type is not None:
                if not isinstance(value, expected_handle_type):
                    actual_type = type(value).__name__
                    expected_name = expected_handle_type.__name__
                    raise InvalidIdError(
                        f"Expected {expected_name}, got {actual_type}",
                        action_description=f"Wrong Handle type passed to '{param_name}'",
                        context=f"Parameter: {param_name}",
                        hints=[
                            f"You passed a {actual_type} where {expected_name} was expected",
                            f"Make sure you're passing the correct object type",
                            f"If using .id property, pass the Handle object directly instead",
                        ],
                    )
            
            # Extract ID
            if hasattr(value, 'id'):
                return value.id
            return value._id
        
        # UUID string
        if isinstance(value, str):
            resolved = workspace.registry.get_id_by_uuid(obj_type, value)
            if resolved is None:
                raise InvalidIdError(f"UUID '{value}' not found in {obj_type}")
            return resolved
        
        # Raw integer (including TypedId subclasses)
        if isinstance(value, int):
            # Check for typed ID mismatches (e.g., DeltaIndex passed where GraphicId expected)
            if isinstance(value, TypedId):
                actual_type = type(value).__name__
                # DeltaIndex passed to graphic_id parameter?
                if isinstance(value, DeltaIndex) and obj_type == "graphics":
                    raise InvalidIdError(
                        f"Expected GraphicId or int, got {actual_type}",
                        action_description=f"Wrong ID type passed to '{param_name}'",
                        context=f"Parameter: {param_name}",
                        hints=[
                            f"You passed a {actual_type} where a GraphicId was expected",
                            f"This usually means you're passing delta.delta_id to a graphic_id parameter",
                            f"Use the correct property or wrap with GraphicId() if intentional",
                        ],
                    )
                # GraphicId passed to delta_id parameter? (Would be caught by validate_index, but check here too)
            return int(value)  # Convert to int to strip type wrapper
            
        return value
        
        # Check if it's a Handle-like object without .id (like DeltaHandle)
        actual_type = type(value).__name__
        if "Handle" in actual_type:
            raise InvalidIdError(
                f"{actual_type} cannot be used here",
                action_description=f"Wrong Handle type passed to '{param_name}'",
                context=f"Parameter: {param_name}",
                hints=[
                    f"{actual_type} does not have an 'id' property",
                    f"You may be passing the wrong object type",
                    f"Check the method's expected parameter types",
                ],
            )
        
        raise InvalidIdError(f"Cannot resolve {actual_type} to ID")
    
    # -------------------------
    # Index Validation
    # -------------------------
    
    def validate_index(
        self,
        index: int,
        collection: Sized,
        name: str,
        *,
        context: Optional[str] = None,
        current_items: Optional[List[str]] = None,
        hints: Optional[List[str]] = None,
        action_description: Optional[str] = None,
    ) -> None:
        """
        Validate list/collection index bounds.
        
        Args:
            index: Index to check
            collection: List or sized object
            name: Name for error message (e.g., "delta_id")
            context: Optional context string
            current_items: Optional list of current items for display
            hints: Optional list of hints
            action_description: Human-readable description of what was attempted
            
        Raises:
            InvalidIdError: If index out of bounds
        """
        if index < 0 or index >= len(collection):
            max_valid = len(collection) - 1 if len(collection) > 0 else "N/A (empty)"
            
            # Build error with rich context
            raise InvalidIdError(
                f"{name} {index} out of range (valid: 0-{max_valid})",
                context=context,
                current_items=current_items or [],
                hints=hints or [
                    f"Check len(graphic.deltas) before accessing",
                    f"Use graphic.deltas to see available items",
                ],
                action_description=action_description or f"Attempt to access invalid {name}",
            )
    
    # -------------------------
    # Reference Validation
    # -------------------------
    
    def validate_graphic_id(self, graphic_id: int, max_id: int) -> bool:
        """
        Validate that a graphic ID is in range.
        
        Args:
            graphic_id: ID to validate
            max_id: Maximum valid ID (exclusive)
            
        Returns:
            True if valid
            
        Raises:
            InvalidIdError: If ID out of range
        """
        if graphic_id < 0 or graphic_id >= max_id:
            raise InvalidIdError(f"Invalid graphic ID: {graphic_id} (max: {max_id - 1})")
        return True
    
    def validate_sound_id(self, sound_id: int, max_id: int) -> bool:
        """
        Validate that a sound ID is in range.
        
        Args:
            sound_id: ID to validate
            max_id: Maximum valid ID (exclusive)
            
        Returns:
            True if valid
            
        Raises:
            InvalidIdError: If ID out of range
        """
        if sound_id < 0 or sound_id >= max_id:
            raise InvalidIdError(f"Invalid sound ID: {sound_id} (max: {max_id - 1})")
        return True
    
    # -------------------------
    # Reference Validation (On Assignment)
    # -------------------------

    def validate_reference(
        self, 
        workspace: GenieWorkspace,
        field_name: str, 
        value: int, 
        field_ref: FieldReference
    ) -> None:
        """
        Validate a reference field assignment.
        
        Args:
            workspace: The GenieWorkspace instance
            field_name: Name of field being set (for error messages)
            value: ID being assigned
            field_ref: Metadata about this field
            
        Raises:
            ValueError: If validation fails
        """
        # 1. Skip if no workspace (lazy validation)
        if workspace is None:
            return

        # 2. Check nullability
        if value == field_ref.null_value:
            if not field_ref.nullable:
                raise ValueError(
                    f"Field '{field_name}' cannot be null (value {value} references {field_ref.target_type})"
                )
            return  # Null is allowed
            
        # 3. Check valid range if specified
        if field_ref.valid_range:
            min_val, max_val = field_ref.valid_range
            if not (min_val <= value <= max_val):
                raise ValueError(
                    f"Field '{field_name}' value {value} is out of valid range [{min_val}, {max_val}]"
                )
        
        # 4. Check if referenced object exists
        try:
            manager = getattr(workspace, field_ref.manager_name)
        except AttributeError:
            raise ValueError(
                f"Validation Error: Manager '{field_ref.manager_name}' (required for '{field_name}') not found in workspace"
            )

        # Check existence
        exists = False
        if hasattr(manager, "exists"):
            exists = manager.exists(value)
        else:
            # Fallback
            try:
                obj = manager.get(value)
                exists = obj is not None
            except Exception:
                exists = False
        
        if not exists:
            self._raise_ref_error(field_name, value, field_ref.target_type)

    def _raise_ref_error(self, field: str, value: int, target_type: str) -> None:
        """Helper to raise consistent error message."""
        raise ValueError(
            f"Field '{field}' references non-existent {target_type} ID: {value}"
        )

    @staticmethod
    def get_field_value(obj: Any, field_path: str) -> Any:
        """
        Get value from possibly nested field path.
        
        Example:
            get_field_value(unit, "combat.attack_graphic")
        """
        parts = field_path.split(".")
        current = obj
        for part in parts:
            if current is None:
                return None
            current = getattr(current, part, None)
        return current

    # -------------------------
    # Full Validation (Save Time)
    # -------------------------
    
    def validate_all_references(
        self,
        workspace: GenieWorkspace,
        validate_existing: bool = False,
    ) -> List[str]:
        """
        Validate all references at save time.
        
        Args:
            workspace: The GenieWorkspace to validate
            validate_existing: If True, check ALL objects. If False, only check
                              session-created objects (Registry entries with _is_existing=False).
            
        Returns:
            List of issue descriptions (empty if valid)
        """
        issues: List[str] = []
        
        # Get counts for range checks
        num_graphics = len(workspace.dat.sprites)
        num_sounds = len(workspace.dat.sounds)
        
        # Validate session-created objects via Registry
        for entry in workspace.registry.graphics:
            if validate_existing or not entry.get("_is_existing", False):
                gfx_id = entry.get("id")
                if gfx_id is not None:
                    # Check if graphic still exists
                    if gfx_id < 0 or gfx_id >= num_graphics:
                        issues.append(f"Graphic '{entry.get('name')}' ID {gfx_id} out of range")
                    elif workspace.dat.sprites[gfx_id] is None:
                        issues.append(f"Graphic '{entry.get('name')}' ID {gfx_id} is None")
        
        for entry in workspace.registry.sounds:
            if validate_existing or not entry.get("_is_existing", False):
                snd_id = entry.get("id")
                if snd_id is not None:
                    if snd_id < 0 or snd_id >= num_sounds:
                        issues.append(f"Sound '{entry.get('name')}' ID {snd_id} out of range")
        
        # If validate_existing, also check non-Registry references
        # This would iterate all sprites, units, etc. and check their references
        # (Implementation can be expanded as needed)
        
        return issues
