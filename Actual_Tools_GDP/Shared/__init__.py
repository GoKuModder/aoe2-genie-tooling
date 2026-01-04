"""
Shared utilities module for Actual_Tools_GDP.

This module provides:
- ToolBase: Base class with common utilities
- logger: Colored console output
- registry: JSON export for created items
- manifest: Attribute manifest loader
- serializer: TwoPassSerializer for deferred validation
"""

from .tool_base import ToolBase, tracks_creation
from .logger import logger, Logger
from .registry import registry, Registry
from .manifest_loader import (
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
