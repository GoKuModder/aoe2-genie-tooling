"""
Actual_Tools - Production-quality tools layer for editing AoE2 DAT files.

This package provides an AoE2ScenarioParser-style API with GUI-like tabs
and intuitive managers for editing Genie Engine DAT files. It wraps
genieutils-py with a user-friendly, consistent interface.

Quick Start:
    from Actual_Tools import GenieWorkspace

    workspace = GenieWorkspace.load("empires2_x2_p1.dat")
    
    # Create a new unit based on Archer (ID 4)
    handle = workspace.units.create("My Custom Unit", base_unit_id=4)
    handle.stats.hit_points = 50
    handle.cost.food = 100
    
    workspace.save("output.dat")
    
    # Export created items for use with AoE2ScenarioParser
    workspace.save_registry("genie_edits.json")

Public API:
    - GenieWorkspace: Root entry point for DAT file editing
    - UnitHandle: Multi-civ unit accessor with tab-style properties
    - logger: Colored console output (can be disabled with logger.disable())
    - registry: JSON export for created items
    - Exceptions: GenieToolsError, UnitIdConflictError, GapNotAllowedError,
                  InvalidIdError, ValidationError, TemplateNotFoundError
"""

from Actual_Tools_GDP.Base.workspace import GenieWorkspace
# TEMPORARILY COMMENTED - rebuilding managers
# from Actual_Tools_GDP.Units.unit_handle_OLD import UnitHandle
from Actual_Tools_GDP.Base.core.logger import Logger
from Actual_Tools_GDP.Base.core.registry import Registry
from Actual_Tools_GDP.Base.core.exceptions import (
    GenieToolsError,
    GapNotAllowedError,
    InvalidIdError,
    TemplateNotFoundError,
    UnitIdConflictError,
    ValidationError,
)

# Create singleton instances for backward compatibility
logger = Logger()
registry = Registry()

__all__ = [
    # Core
    "GenieWorkspace",
    # "UnitHandle",  # TEMPORARILY COMMENTED
    # Logging/Registry
    "logger",
    "registry",
    # Exceptions
    "GenieToolsError",
    "GapNotAllowedError",
    "InvalidIdError",
    "TemplateNotFoundError",
    "UnitIdConflictError",
    "ValidationError",
]

__version__ = "1.2.0"
