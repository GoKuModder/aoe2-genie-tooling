"""
ValidationMixin - Helper mixin for attribute validation in UnitHandle.

Provides methods to validate and set attributes with proper error handling:
- Reference validation (deferred to save time)
- Enum/Bitmask validation (immediate)
- Source tracking for error messages
"""
from __future__ import annotations

import traceback
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    # TODO: Removed genie-rust dependency - needs migration to GenieDatParser
    # from genie_rust import Unit
    pass

__all__ = ["ValidationMixin"]


class ValidationMixin:
    """
    Mixin providing validation helpers for UnitHandle setters.

    Methods:
        _set_reference: Set a reference attribute with deferred validation
        _set_enum: Set enum/bitmask with immediate validation
        _set_value: Set a plain value (no validation)
    """

    # Expected to be provided by the class using this mixin
    _units: List["Unit"]

    def _set_reference(
        self,
        attr_path: str,  # e.g., "attack_graphic" or "type_50.attack_graphic"
        value: Union[int, Any],  # int ID or Handle object
        target_type: str,  # "GraphicHandle", "SoundHandle", etc.
    ) -> None:
        """
        Set a reference attribute with deferred validation.

        Creates a DeferredReference that will be validated at save time.

        Args:
            attr_path: Attribute path (flattened, e.g., "attack_graphic")
            value: Value to set (int ID or Handle)
            target_type: Type of reference (GraphicHandle, SoundHandle, etc.)

        Raises:
            TypeError: If value is not int or expected Handle type
        """
        from .manifest_loader import serializer, DeferredReference

        # Extract ID from Handle if needed
        actual_id = value
        if not isinstance(value, int):
            # Try to get ID from Handle object
            if hasattr(value, 'id'):
                actual_id = value.id
            elif hasattr(value, '_id'):
                actual_id = value._id
            else:
                # Get source for error
                stack = traceback.extract_stack()
                source_frame = stack[-2] if len(stack) >= 2 else stack[-1]
                source_info = f"{source_frame.filename}:{source_frame.lineno} - {source_frame.line}"

                raise TypeError(
                    f"{attr_path}: Expected int or {target_type}, got {type(value).__name__}\n"
                    f"  Source: {source_info}"
                )

        # Create deferred reference for validation at save time
        ref = DeferredReference.create(target_type, actual_id, attr_path)
        serializer.add_deferred(ref)

        # Set the value on all units
        self._set_unit_attr(attr_path, actual_id)

    def _set_enum(
        self,
        attr_path: str,  # e.g., "garrison_type" or "building.garrison_type"
        value: int,
        manifest_attr_id: Optional[int] = None,  # Attribute ID from manifest
        manifest_attr_name: Optional[str] = None,  # Or attribute name
    ) -> None:
        """
        Set enum/bitmask attribute with immediate validation.

        Args:
            attr_path: Attribute path
            value: Value to set
            manifest_attr_id: Attribute ID from manifest.csv (optional)
            manifest_attr_name: Attribute name from manifest.csv (optional)

        Raises:
            EnumValueError: If value is not valid for the enum/bitmask
        """
        from .manifest_loader import manifest

        # Get manifest entry
        entry = None
        if manifest_attr_id is not None:
            entry = manifest.get(manifest_attr_id)
        elif manifest_attr_name is not None:
            entry = manifest.get_by_name(manifest_attr_name)

        if entry and entry.is_enum:
            # Capture source location for error message
            stack = traceback.extract_stack()
            source_frame = stack[-2] if len(stack) >= 2 else stack[-1]
            source_info = f"{source_frame.filename}:{source_frame.lineno} - {source_frame.line}"

            # Validate immediately (will raise EnumValueError if invalid)
            manifest.validate_enum_value(entry, value, source_info)

        # Set the value
        self._set_unit_attr(attr_path, value)

    def _set_value(
        self,
        attr_path: str,
        value: Any,
    ) -> None:
        """
        Set a plain value attribute (no validation).

        Args:
            attr_path: Attribute path
            value: Value to set
        """
        self._set_unit_attr(attr_path, value)

    def _set_unit_attr(self, attr_path: str, value: Any) -> None:
        """
        Set attribute value on all units.

        Handles nested paths like "type_50.attack_graphic".

        Args:
            attr_path: Dot-separated path to attribute
            value: Value to set
        """
        for unit in self._units:
            if not unit:
                continue

            # Split path and navigate to target
            parts = attr_path.split('.')
            target = unit

            # Navigate to parent object
            for part in parts[:-1]:
                target = getattr(target, part, None)
                if target is None:
                    break

            # Set final attribute
            if target is not None:
                setattr(target, parts[-1], value)

    def _get_unit_attr(self, attr_path: str) -> Any:
        """
        Get attribute value from first unit.

        Args:
            attr_path: Dot-separated path to attribute

        Returns:
            Attribute value or None
        """
        if not self._units or not self._units[0]:
            return None

        parts = attr_path.split('.')
        target = self._units[0]

        for part in parts:
            target = getattr(target, part, None)
            if target is None:
                return None

        return target
