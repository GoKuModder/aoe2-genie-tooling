"""
Shared utilities module for Actual_Tools.

This module provides:
- ToolBase: Base class with common utilities
- logger: Colored console output
- registry: JSON export for created items
- manifest: Attribute manifest loader
- serializer: TwoPassSerializer for deferred validation
"""

<<<<<<< HEAD
from Actual_Tools_GDP.Shared.tool_base import ToolBase, tracks_creation
from Actual_Tools_GDP.Shared.logger import logger, Logger
from Actual_Tools_GDP.Shared.registry import registry, Registry
from Actual_Tools_GDP.Shared.manifest_loader import (
    manifest, 
    serializer, 
=======
from .tool_base import ToolBase, tracks_creation
from .logger import logger, Logger
from .registry import registry, Registry
from .manifest_loader import (
    manifest,
    serializer,
>>>>>>> origin/refactor-port-managers-to-gdp-783808832176151754
    DeferredReference,
    ValidationError,
    ReferenceNotFoundError,
    EnumValueError,
    CircularReferenceError,
    DuplicateIdError,
)

__all__ = [
<<<<<<< HEAD
    "ToolBase", 
    "tracks_creation",
    "logger", 
    "Logger", 
    "registry", 
=======
    "ToolBase",
    "tracks_creation",
    "logger",
    "Logger",
    "registry",
>>>>>>> origin/refactor-port-managers-to-gdp-783808832176151754
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
<<<<<<< HEAD

=======
>>>>>>> origin/refactor-port-managers-to-gdp-783808832176151754
