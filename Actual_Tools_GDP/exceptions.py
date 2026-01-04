"""
Centralized exceptions for Actual_Tools.

All custom exceptions used across the tools layer are defined here
for consistent error handling and clear, actionable error messages.

Exception Hierarchy:
    GenieToolsError (base)
    ├── UnitIdConflictError - ID already exists
    ├── GapNotAllowedError - would create None gaps
    ├── InvalidIdError - negative or out-of-range ID
    ├── ValidationError - workspace validation failed
    └── TemplateNotFoundError - no template for cloning
"""

__all__ = [
    "GenieToolsError",
    "GapNotAllowedError",
    "InvalidIdError",
    "TemplateNotFoundError",
    "UnitIdConflictError",
    "ValidationError",
]


class GenieToolsError(Exception):
    """
    Base exception for all Actual_Tools errors.
    
    All custom exceptions in this package inherit from this class,
    allowing catch-all error handling when desired.
    """
    pass


class UnitIdConflictError(GenieToolsError):
    """
    Raised when attempting to create/move a unit to an ID that already exists.
    
    This occurs when:
    - create() or clone_into() targets an occupied ID with on_conflict="error"
    - move() destination is occupied with on_conflict="error"
    """
    pass


class GapNotAllowedError(GenieToolsError):
    """
    Raised when an operation would create illegal None gaps in a table.
    
    This occurs when:
    - Creating/cloning beyond current max ID with fill_gaps="error"
    - The "no gaps" policy prevents None values in unit tables
    """
    pass


class InvalidIdError(GenieToolsError):
    """
    Raised when an ID is invalid.
    
    This occurs when:
    - ID is negative
    - ID doesn't exist when expected (e.g., get() on non-existent unit)
    - ID is out of valid range for the table
    """
    pass


class ValidationError(GenieToolsError):
    """
    Raised when workspace validation fails.
    
    This occurs when:
    - Unit list lengths don't match across civs
    - None gaps detected in tables
    - Invalid references (graphic/sound IDs out of range)
    """
    pass


class TemplateNotFoundError(GenieToolsError):
    """
    Raised when no valid template can be found for cloning.
    
    This occurs when:
    - DAT file has no valid units to use as template
    - Specified base_unit_id doesn't exist
    """
    pass
