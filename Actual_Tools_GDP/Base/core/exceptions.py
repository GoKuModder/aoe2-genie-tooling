"""
Custom exceptions for Actual_Tools_GDP.

Exception hierarchy:
    GenieToolsError (base)
    ├── ValidationError (attribute/type validation failures)
    ├── InvalidIdError (ID out of valid range)
    ├── UnitIdConflictError (ID already exists)
    ├── GapNotAllowedError (gaps in ID sequence)
    └── TemplateNotFoundError (base template not found)
"""
from __future__ import annotations

__all__ = [
    "GenieToolsError",
    "ValidationError",
    "InvalidIdError",
    "UnitIdConflictError",
    "GapNotAllowedError",
    "TemplateNotFoundError",
]


class GenieToolsError(Exception):
    """Base exception for all Actual_Tools_GDP errors."""
    pass


class ValidationError(GenieToolsError):
    """
    Raised when attribute validation fails.
    
    Examples:
    - Invalid Handle type passed to attribute
    - Flattened attribute not in allow-list
    - Reference ID does not exist
    """
    pass


class InvalidIdError(GenieToolsError):
    """
    Raised when an ID is out of valid range.
    
    Examples:
    - Negative ID
    - ID exceeds maximum for the data type
    """
    pass


class UnitIdConflictError(GenieToolsError):
    """
    Raised when attempting to create/move to an ID that already exists.
    
    Examples:
    - create(unit_id=50) when ID 50 already exists with on_conflict="error"
    - move(dst=100) when ID 100 is occupied
    """
    pass


class GapNotAllowedError(GenieToolsError):
    """
    Raised when a gap would be created in the ID sequence.
    
    Examples:
    - create(unit_id=500) when max ID is 200 and fill_gaps="error"
    """
    pass


class TemplateNotFoundError(GenieToolsError):
    """
    Raised when a base template unit/graphic/sound is not found.
    
    Examples:
    - create(base_unit_id=999999) when unit 999999 doesn't exist
    """
    pass
