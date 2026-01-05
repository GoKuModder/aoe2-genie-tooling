"""
Validator - Validation helpers for attribute safety and type checking.

Responsibilities:
- Attribute allow-list enforcement (prevent typos)
- Type validation for Handle objects
- Reference validation (graphics, sounds exist)
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional, Set

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
    # Reference Validation (Placeholder)
    # -------------------------
    
    def validate_graphic_id(self, graphic_id: int, max_id: int) -> bool:
        """
        Validate that a graphic ID exists.
        
        Args:
            graphic_id: ID to validate
            max_id: Maximum valid ID
            
        Returns:
            True if valid
            
        Raises:
            ValueError: If ID out of range
        """
        if graphic_id < 0 or graphic_id >= max_id:
            raise ValueError(f"Invalid graphic ID: {graphic_id} (max: {max_id - 1})")
        return True
    
    def validate_sound_id(self, sound_id: int, max_id: int) -> bool:
        """
        Validate that a sound ID exists.
        
        Args:
            sound_id: ID to validate
            max_id: Maximum valid ID
            
        Returns:
            True if valid
            
        Raises:
            ValueError: If ID out of range
        """
        if sound_id < 0 or sound_id >= max_id:
            raise ValueError(f"Invalid sound ID: {sound_id} (max: {max_id - 1})")
        return True
