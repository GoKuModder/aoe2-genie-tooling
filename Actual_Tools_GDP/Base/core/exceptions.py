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

import traceback
from typing import Any, List, Optional

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
    
    Features rich error messages with:
    - Decorated borders for visibility
    - Actual source code line
    - Context (what object was involved)
    - Current items listing
    - Helpful hints
    """
    
    def __init__(
        self,
        message: str,
        *,
        context: Optional[str] = None,
        current_items: Optional[List[str]] = None,
        hints: Optional[List[str]] = None,
        action_description: Optional[str] = None,
    ) -> None:
        """
        Initialize with rich error information.
        
        Args:
            message: Main error message
            context: Context string (e.g., "Graphic 'ARCHER' (ID: 100)")
            current_items: List of current items (e.g., ["Delta 0: → Graphic 50"])
            hints: List of helpful hints
            action_description: Human-readable description of what was attempted
        """
        self.base_message = message
        self.context = context
        self.current_items = current_items or []
        self.hints = hints or []
        self.action_description = action_description or "Invalid ID operation"
        
        # Get source location and code
        self._source_info = self._get_source_info()
        
        super().__init__(self._format())
    
    def _get_source_info(self) -> dict:
        """Extract the user's source line that triggered the error."""
        info = {"file": None, "lineno": None, "code": None}
        try:
            stack = traceback.extract_stack()
            for frame in reversed(stack):
                if "Actual_Tools_GDP" not in frame.filename and "validator" not in frame.filename:
                    info["file"] = frame.filename
                    info["lineno"] = frame.lineno
                    # Try to read actual source line
                    try:
                        with open(frame.filename, 'r', encoding='utf-8') as f:
                            lines = f.readlines()
                            if 0 <= frame.lineno - 1 < len(lines):
                                info["code"] = lines[frame.lineno - 1].rstrip()
                    except:
                        pass
                    break
        except:
            pass
        return info
    
    def _format(self) -> str:
        """Format the error message with decorated borders."""
        width = 90
        border = "_" * width
        
        lines = []
        lines.append("")
        lines.append(border)
        lines.append("")
        
        # Source code display
        if self._source_info.get("code"):
            lines.append(f"📍 {self._source_info['file']}:{self._source_info['lineno']}")
            lines.append("")
            lines.append(f"    {self._source_info['code']}")
            lines.append("")
        
        # Action description
        lines.append(f"❌ {self.action_description}")
        lines.append(f"   {self.base_message}")
        
        # Context
        if self.context:
            lines.append("")
            lines.append(f"📦 Context: {self.context}")
        
        # Current items
        if self.current_items:
            lines.append("")
            lines.append(f"📋 Available items:")
            for item in self.current_items[:5]:
                lines.append(f"   • {item}")
            if len(self.current_items) > 5:
                lines.append(f"   ... and {len(self.current_items) - 5} more")
        
        # Hints
        if self.hints:
            lines.append("")
            lines.append(f"💡 What to do:")
            for hint in self.hints:
                lines.append(f"   • {hint}")
        
        lines.append("")
        lines.append(border)
        lines.append("")
        
        return "\n".join(lines)


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
