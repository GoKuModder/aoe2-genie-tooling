"""
Base class for specific domain managers (Units, Graphics, etc.),
providing access to the shared DatFile and common helper methods
for list management, ID allocation, placeholder creation, and auto-tracking.
"""
from __future__ import annotations

import copy
from functools import wraps
from typing import TYPE_CHECKING, Any, Callable, List, Optional, TypeVar

from Actual_Tools.Shared.logger import logger
from Actual_Tools.Shared.registry import registry
from Actual_Tools.exceptions import (
    GapNotAllowedError,
    InvalidIdError,
    TemplateNotFoundError,
)

if TYPE_CHECKING:
    from genieutils.datfile import DatFile
    from genieutils.unit import Unit

__all__ = ["ToolBase", "tracks_creation"]

T = TypeVar("T")


def tracks_creation(item_type: str, name_param: str = "name"):
    """
    Decorator that auto-logs and registers created items.
    
    Apply to manager methods that create new items (units, graphics, sounds, techs).
    The decorated method must return an object with `.id` attribute.
    
    Args:
        item_type: Type of item ("unit", "graphic", "sound", "tech")
        name_param: Parameter name containing the item's name (default: "name")
    
    Example:
        @tracks_creation("graphic", name_param="file_name")
        def add_graphic(self, file_name: str, ...) -> Graphic:
            ...
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(self, *args, **kwargs) -> T:
            # Call the actual method
            result = func(self, *args, **kwargs)
            
            # Extract name from args/kwargs
            # Try kwargs first, then positional
            sig_params = list(func.__code__.co_varnames[1:])  # Skip 'self'
            name = kwargs.get(name_param)
            if name is None and name_param in sig_params:
                idx = sig_params.index(name_param)
                if idx < len(args):
                    name = args[idx]
            
            if name is None:
                name = getattr(result, "name", str(result.id))
            
            item_id = result.id
            
            # Auto-log and register
            _log_creation(self, item_type, name, item_id)
            _register_creation(item_type, name, item_id)
            
            return result
        return wrapper
    return decorator


def _log_creation(manager, item_type: str, name: str, item_id: int) -> None:
    """Internal: log item creation based on type."""
    component = {
        "unit": "units",
        "graphic": "graphics", 
        "sound": "sounds",
        "tech": "techs",
    }.get(item_type, "workspace")
    
    if item_type == "unit":
        logger.unit_created(name, item_id)
    elif item_type == "graphic":
        logger.graphic_created(name, item_id)
    elif item_type == "sound":
        logger.sound_created(name, item_id)
    elif item_type == "tech":
        logger.tech_created(name, item_id)


def _register_creation(item_type: str, name: str, item_id: int, **extra) -> None:
    """Internal: register item based on type."""
    if item_type == "unit":
        registry.register_unit(name, item_id, **extra)
    elif item_type == "graphic":
        registry.register_graphic(name, item_id, **extra)
    elif item_type == "sound":
        registry.register_sound(name, item_id, **extra)
    elif item_type == "tech":
        registry.register_tech(name, item_id, **extra)


class ToolBase:
    """
    Base class for domain managers providing shared utilities.
    
    Key responsibilities:
    - List capacity management with placeholder support
    - ID allocation utilities
    - Validation helpers
    - Auto-tracking (logging and registry) via decorator or manual call
    """
    
    # Subclasses can override for logging
    COMPONENT_NAME: str = "manager"

    def __init__(self, dat_file: DatFile) -> None:
        self.dat_file = dat_file

    # -------------------------
    # Auto-tracking (manual call when decorator not suitable)
    # -------------------------
    
    def _track_unit(self, name: str, unit_id: int, src_unit_id: Optional[int] = None) -> None:
        """Log and register a unit creation."""
        logger.unit_created(name, unit_id)
        registry.register_unit(name, unit_id, base_unit_id=src_unit_id)
    
    def _track_unit_clone(self, name: str, unit_id: int, source_id: int) -> None:
        """Log and register a unit clone."""
        logger.unit_cloned(name, unit_id, source_id)
        registry.register_unit(name, unit_id, base_unit_id=source_id)
    
    def _track_unit_move(self, src_id: int, dst_id: int) -> None:
        """Log a unit move (no registry needed)."""
        logger.unit_moved(src_id, dst_id)

    # -------------------------
    # ID Allocation
    # -------------------------

    def next_append_index(self, item_list: List[Any]) -> int:
        """
        Returns the index that would be used if an item were appended to the list.
        This is effectively `len(item_list)`.
        """
        return len(item_list)

    def allocate_next_unit_id(self) -> int:
        """Allocates the next unit ID based on civ[0]'s unit list length."""
        if not self.dat_file.civs:
            return 0
        return len(self.dat_file.civs[0].units)

    def allocate_next_graphic_id(self) -> int:
        """Returns the next available graphic ID (append position)."""
        return len(self.dat_file.graphics)

    def allocate_next_sound_id(self) -> int:
        """Returns the next available sound ID (append position)."""
        return len(self.dat_file.sounds)

    def allocate_next_tech_id(self) -> int:
        """Returns the next available tech ID (append position)."""
        return len(self.dat_file.techs)

    # -------------------------
    # List Capacity Management
    # -------------------------

    def ensure_capacity(
        self,
        target_list: List[Any],
        required_index: int,
        default_value: Any = None,
    ) -> None:
        """
        Extends the list with `default_value` to ensure `required_index` is valid.
        
        WARNING: Using None may violate "no gaps" policy for units.
        """
        if required_index < 0:
            raise InvalidIdError(f"Index {required_index} cannot be negative.")
        if required_index >= len(target_list):
            extend_count = required_index - len(target_list) + 1
            target_list.extend([default_value] * extend_count)

    def ensure_capacity_with_placeholders(
        self,
        target_list: List[Any],
        required_index: int,
        placeholder_factory: Callable[[], Any],
    ) -> None:
        """
        Extends the list with placeholder objects to ensure `required_index` is valid.
        Creates distinct placeholder objects for each new slot.
        """
        if required_index < 0:
            raise InvalidIdError(f"Index {required_index} cannot be negative.")
        while len(target_list) <= required_index:
            target_list.append(placeholder_factory())

    # -------------------------
    # Unit Placeholder Factory
    # -------------------------

    def find_first_valid_unit(self) -> Optional[Unit]:
        """Finds the first non-None unit across all civs to use as a template."""
        for civ in self.dat_file.civs:
            if civ and civ.units:
                for unit in civ.units:
                    if unit is not None:
                        return unit
        return None

    def create_placeholder_unit(self, template: Optional[Unit] = None) -> Unit:
        """
        Creates a disabled but serializable placeholder unit.
        
        Placeholder: enabled=0, name="", hit_points=1
        """
        if template is None:
            template = self.find_first_valid_unit()
        
        if template is None:
            raise TemplateNotFoundError(
                "Cannot create placeholder unit: no valid template unit found."
            )
        
        placeholder = copy.deepcopy(template)
        placeholder.name = ""
        placeholder.enabled = 0
        placeholder.hit_points = 1
        return placeholder

    def create_unit_placeholder_factory(self, template: Optional[Unit] = None) -> Callable[[], Unit]:
        """Returns a factory function that creates placeholder units."""
        if template is None:
            template = self.find_first_valid_unit()
        
        if template is None:
            raise TemplateNotFoundError(
                "Cannot create placeholder factory: no valid template unit found."
            )
        
        def factory() -> Unit:
            placeholder = copy.deepcopy(template)
            placeholder.name = ""
            placeholder.enabled = 0
            placeholder.hit_points = 1
            return placeholder
        
        return factory

    # -------------------------
    # Validation Utilities
    # -------------------------

    def validate_index_free(self, target_list: List[Any], index: int) -> None:
        """Raises ValueError if the index is already occupied (not None)."""
        if 0 <= index < len(target_list):
            if target_list[index] is not None:
                raise ValueError(f"Index {index} is already occupied.")

    def validate_range(self, value: int, min_val: int, max_val: int, name: str) -> None:
        """Validates that a value is within [min_val, max_val]."""
        if not (min_val <= value <= max_val):
            raise ValueError(f"{name} {value} must be between {min_val} and {max_val}.")

    def validate_id_positive(self, id_value: int, name: str = "ID") -> None:
        """Validates that an ID is non-negative."""
        if id_value < 0:
            raise InvalidIdError(f"{name} {id_value} cannot be negative.")

    def is_slot_occupied(self, target_list: List[Any], index: int) -> bool:
        """Returns True if the index exists in the list and is not None."""
        return 0 <= index < len(target_list) and target_list[index] is not None
