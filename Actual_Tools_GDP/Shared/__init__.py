"""
Shared utilities module for Actual_Tools.

This module provides:
- ToolBase: Base class with common utilities
- logger: Colored console output
- registry: JSON export for created items
- manifest: Attribute manifest loader
- serializer: TwoPassSerializer for deferred validation
"""

from Actual_Tools_GDP.Shared.tool_base import ToolBase, tracks_creation
from Actual_Tools_GDP.Shared.logger import logger, Logger
from Actual_Tools_GDP.Shared.registry import registry, Registry
from Actual_Tools_GDP.Shared.manifest_loader import (
    manifest, 
    serializer, 
    DeferredReference,
    ValidationError,
    ReferenceNotFoundError,
    EnumValueError,
    CircularReferenceError,
    DuplicateIdError,
)

__all__ = [
    "ToolBase", 
    "tracks_creation",
    "logger", 
    "Logger", 
    "registry", 
    "Registry",
    "manifest",
    "serializer",
    "DeferredReference",
    "ValidationError",
    "ReferenceNotFoundError",
    "EnumValueError",
    "CircularReferenceError",
    "DuplicateIdError",
]

