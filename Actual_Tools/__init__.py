"""
Actual_Tools - High-level Python toolkit for editing Age of Empires II Definitive Edition DAT files.
"""

# Public API
from .Base.base_manager import GenieWorkspace
from .Units.unit_handle import UnitHandle
from .exceptions import (
    UnitIdConflictError,
    GapNotAllowedError,
    InvalidIdError,
    TemplateNotFoundError,
    ValidationError,
)
from .Shared.logger import logger

__all__ = [
    "GenieWorkspace",
    "UnitHandle",
    "UnitIdConflictError",
    "GapNotAllowedError",
    "InvalidIdError",
    "TemplateNotFoundError",
    "ValidationError",
    "logger",
]
