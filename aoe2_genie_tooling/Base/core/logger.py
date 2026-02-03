"""
Logger - Colored console output for aoe2_genie_tooling.

Provides colored logging to track library operations.
Users can see what the library is doing without adding print statements.

Usage:
    logger = Logger()
    logger.info("Loading DAT file...")
    logger.success("unit_manager", "Created unit 'My Unit' at ID 2800")
"""
from __future__ import annotations

import sys
import time
from dataclasses import dataclass, field
from typing import ClassVar

__all__ = ["Logger"]


# ANSI color codes
class Colors:
    """ANSI escape codes for terminal colors."""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"

    # Foreground colors
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    CYAN = "\033[36m"

    # Bright colors
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"


def _supports_color() -> bool:
    """Check if the terminal supports ANSI colors."""
    if sys.platform == "win32":
        try:
            import os
            return os.environ.get("TERM") != "dumb" or "WT_SESSION" in os.environ
        except Exception:
            return True  # Assume modern Windows
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()


@dataclass
class Logger:
    """
    Colored console logger for aoe2_genie_tooling.

    Provides consistent, colored output to track library operations.
    Automatically tracks elapsed time from creation.

    Attributes:
        enabled: Whether logging is enabled (default: True)
        use_colors: Whether to use ANSI colors (auto-detected)
        start_time: When logging started (for elapsed time tracking)
    """

    enabled: bool = True
    use_colors: bool = field(default_factory=_supports_color)
    start_time: float = field(default_factory=time.time)

    # Component prefixes with colors
    PREFIXES: ClassVar[dict] = {
        "workspace": (Colors.BRIGHT_CYAN, "Workspace"),
        "units": (Colors.BRIGHT_GREEN, "Unit"),
        "graphics": (Colors.BRIGHT_MAGENTA, "Graphic"),
        "sounds": (Colors.BRIGHT_YELLOW, "Sound"),
        "techs": (Colors.BRIGHT_BLUE, "Tech"),
        "effects": (Colors.BRIGHT_MAGENTA, "Effect"),
        "civs": (Colors.CYAN, "Civ"),
    }

    def _colorize(self, text: str, color: str) -> str:
        """Apply color to text if colors enabled."""
        if not self.use_colors:
            return text
        return f"{color}{text}{Colors.RESET}"

    def _format_prefix(self, component: str) -> str:
        """Format a component prefix with color."""
        if component in self.PREFIXES:
            color, name = self.PREFIXES[component]
            prefix = f"[{name}]"
            return self._colorize(prefix, color)
        return f"[{component}]"

    def _print(self, message: str) -> None:
        """Print if logging is enabled."""
        if self.enabled:
            print(message)

    # -------------------------
    # Public Logging Methods
    # -------------------------

    def info(self, message: str, component: str = "workspace") -> None:
        """
        Log an info message.

        Args:
            message: The message to log
            component: Optional component name (default: workspace)
        """
        prefix = self._format_prefix(component)
        self._print(f"{prefix} {message}")

    def success(self, message: str, component: str = "workspace") -> None:
        """
        Log a success message (green checkmark).

        Args:
            message: The message to log
            component: Optional component name
        """
        prefix = self._format_prefix(component)
        check = self._colorize("✓", Colors.BRIGHT_GREEN)
        self._print(f"{prefix} {check} {message}")

    def warning(self, message: str, component: str = "workspace") -> None:
        """
        Log a warning message (yellow).

        Args:
            message: The message to log
            component: Optional component name
        """
        prefix = self._format_prefix(component)
        warn = self._colorize("⚠", Colors.BRIGHT_YELLOW)
        msg = self._colorize(message, Colors.YELLOW)
        self._print(f"{prefix} {warn} {msg}")

    def error(self, message: str, component: str = "workspace") -> None:
        """
        Log an error message (red).

        Args:
            message: The message to log
            component: Optional component name
        """
        prefix = self._format_prefix(component)
        err = self._colorize("✗", Colors.BRIGHT_RED)
        msg = self._colorize(message, Colors.RED)
        self._print(f"{prefix} {err} {msg}")

    # -------------------------
    # Timing
    # -------------------------

    def reset_timer(self) -> None:
        """Reset the start time for elapsed tracking."""
        self.start_time = time.time()

    def elapsed(self) -> float:
        """Get elapsed time since start (or last reset)."""
        return time.time() - self.start_time

    # -------------------------
    # Control
    # -------------------------

    def disable(self) -> None:
        """Disable all logging output."""
        self.enabled = False

    def enable(self) -> None:
        """Enable logging output."""
        self.enabled = True
