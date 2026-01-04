"""
Logger - Colored console output for Actual_Tools.

Provides AoE2ScenarioParser-style colored logging to track library operations.
Users can see what the library is doing without adding print statements.

Usage:
<<<<<<< HEAD
    from Actual_Tools_GDP.Shared.logger import logger
=======
    from Actual_Tools.Shared.logger import logger
    
>>>>>>> origin/refactor-port-managers-to-gdp-783808832176151754
    logger.info("Loading DAT file...")
    logger.success("Created unit 'My Unit' at ID 2800")
"""
from __future__ import annotations

import sys
import time
from dataclasses import dataclass, field
from typing import ClassVar, Optional

__all__ = ["logger", "Logger"]


# ANSI color codes
class Colors:
    """ANSI escape codes for terminal colors."""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
<<<<<<< HEAD

=======
    
>>>>>>> origin/refactor-port-managers-to-gdp-783808832176151754
    # Foreground colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
<<<<<<< HEAD

=======
    
>>>>>>> origin/refactor-port-managers-to-gdp-783808832176151754
    # Bright colors
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"


def _supports_color() -> bool:
    """Check if the terminal supports ANSI colors."""
    # Windows 10+ supports ANSI, older might not
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
    Colored console logger for Actual_Tools.
<<<<<<< HEAD
    Provides consistent, colored output to track library operations.
    Automatically tracks elapsed time from creation.
=======
    
    Provides consistent, colored output to track library operations.
    Automatically tracks elapsed time from creation.
    
>>>>>>> origin/refactor-port-managers-to-gdp-783808832176151754
    Attributes:
        enabled: Whether logging is enabled (default: True)
        use_colors: Whether to use ANSI colors (auto-detected)
        start_time: When logging started (for elapsed time tracking)
    """
<<<<<<< HEAD
    enabled: bool = True
    use_colors: bool = field(default_factory=_supports_color)
    start_time: float = field(default_factory=time.time)
=======
    
    enabled: bool = True
    use_colors: bool = field(default_factory=_supports_color)
    start_time: float = field(default_factory=time.time)
    
>>>>>>> origin/refactor-port-managers-to-gdp-783808832176151754
    # Component prefixes with colors
    PREFIXES: ClassVar[dict] = {
        "workspace": (Colors.BRIGHT_CYAN, "Workspace"),
        "units": (Colors.BRIGHT_GREEN, "UnitManager"),
        "graphics": (Colors.BRIGHT_MAGENTA, "GraphicManager"),
        "sounds": (Colors.BRIGHT_YELLOW, "SoundManager"),
        "techs": (Colors.BRIGHT_BLUE, "TechManager"),
        "civs": (Colors.CYAN, "CivManager"),
    }
<<<<<<< HEAD

=======
    
>>>>>>> origin/refactor-port-managers-to-gdp-783808832176151754
    def _colorize(self, text: str, color: str) -> str:
        """Apply color to text if colors enabled."""
        if not self.use_colors:
            return text
        return f"{color}{text}{Colors.RESET}"
<<<<<<< HEAD

=======
    
>>>>>>> origin/refactor-port-managers-to-gdp-783808832176151754
    def _format_prefix(self, component: str) -> str:
        """Format a component prefix with color."""
        if component in self.PREFIXES:
            color, name = self.PREFIXES[component]
            prefix = f"[{name}]"
            return self._colorize(prefix, color)
        return f"[{component}]"
<<<<<<< HEAD

=======
    
>>>>>>> origin/refactor-port-managers-to-gdp-783808832176151754
    def _print(self, message: str) -> None:
        """Print if logging is enabled."""
        if self.enabled:
            print(message)
<<<<<<< HEAD
=======
    
>>>>>>> origin/refactor-port-managers-to-gdp-783808832176151754
    # -------------------------
    # Public Logging Methods
    # -------------------------
    
    def info(self, component: str, message: str) -> None:
        """
        Log an info message.
<<<<<<< HEAD
=======
        
>>>>>>> origin/refactor-port-managers-to-gdp-783808832176151754
        Args:
            component: The component name (workspace, units, graphics, etc.)
            message: The message to log
        """
        prefix = self._format_prefix(component)
        self._print(f"{prefix} {message}")
<<<<<<< HEAD
    def success(self, component: str, message: str) -> None:
        """
        Log a success message (green checkmark).
=======
    
    def success(self, component: str, message: str) -> None:
        """
        Log a success message (green checkmark).
        
>>>>>>> origin/refactor-port-managers-to-gdp-783808832176151754
        Args:
            component: The component name
            message: The message to log
        """
        prefix = self._format_prefix(component)
        check = self._colorize("✓", Colors.BRIGHT_GREEN)
        self._print(f"{prefix} {check} {message}")
<<<<<<< HEAD
    def warning(self, component: str, message: str) -> None:
        """
        Log a warning message (yellow).
=======
    
    def warning(self, component: str, message: str) -> None:
        """
        Log a warning message (yellow).
        
>>>>>>> origin/refactor-port-managers-to-gdp-783808832176151754
        Args:
            component: The component name
            message: The message to log
        """
        prefix = self._format_prefix(component)
        warn = self._colorize("⚠", Colors.BRIGHT_YELLOW)
        msg = self._colorize(message, Colors.YELLOW)
        self._print(f"{prefix} {warn} {msg}")
<<<<<<< HEAD
    def error(self, component: str, message: str) -> None:
        """
        Log an error message (red).
=======
    
    def error(self, component: str, message: str) -> None:
        """
        Log an error message (red).
        
>>>>>>> origin/refactor-port-managers-to-gdp-783808832176151754
        Args:
            component: The component name
            message: The message to log
        """
        prefix = self._format_prefix(component)
        err = self._colorize("✗", Colors.BRIGHT_RED)
        msg = self._colorize(message, Colors.RED)
        self._print(f"{prefix} {err} {msg}")
<<<<<<< HEAD
    # -------------------------
    # Specialized Logging
    # -------------------------
=======
    
    # -------------------------
    # Specialized Logging
    # -------------------------
    
>>>>>>> origin/refactor-port-managers-to-gdp-783808832176151754
    def load_start(self, filename: str) -> None:
        """Log DAT file load start."""
        name = self._colorize(filename, Colors.BOLD + Colors.WHITE)
        self.info("workspace", f"Loading {name}...")
<<<<<<< HEAD

=======
    
>>>>>>> origin/refactor-port-managers-to-gdp-783808832176151754
    def load_complete(self, num_civs: int, num_units: int) -> None:
        """Log DAT file load complete."""
        civs = self._colorize(str(num_civs), Colors.BRIGHT_CYAN)
        units = self._colorize(str(num_units), Colors.BRIGHT_GREEN)
        self.success("workspace", f"Loaded {civs} civilizations, {units} units")
<<<<<<< HEAD

=======
    
>>>>>>> origin/refactor-port-managers-to-gdp-783808832176151754
    def save_start(self, filename: str) -> None:
        """Log DAT file save start."""
        name = self._colorize(filename, Colors.BOLD + Colors.WHITE)
        self.info("workspace", f"Saving to {name}...")
<<<<<<< HEAD

=======
    
>>>>>>> origin/refactor-port-managers-to-gdp-783808832176151754
    def save_complete(self, filename: str) -> None:
        """Log DAT file save complete."""
        name = self._colorize(filename, Colors.BOLD + Colors.WHITE)
        self.success("workspace", f"Saved: {name}")
<<<<<<< HEAD

=======
    
>>>>>>> origin/refactor-port-managers-to-gdp-783808832176151754
    def unit_created(self, name: str, unit_id: int) -> None:
        """Log unit creation."""
        unit_name = self._colorize(f"'{name}'", Colors.BRIGHT_GREEN)
        uid = self._colorize(str(unit_id), Colors.BRIGHT_CYAN)
        self.success("units", f"Created {unit_name} at ID {uid}")
<<<<<<< HEAD

=======
    
>>>>>>> origin/refactor-port-managers-to-gdp-783808832176151754
    def unit_cloned(self, name: str, unit_id: int, source_id: int) -> None:
        """Log unit cloning."""
        unit_name = self._colorize(f"'{name}'", Colors.BRIGHT_GREEN)
        uid = self._colorize(str(unit_id), Colors.BRIGHT_CYAN)
        src = self._colorize(str(source_id), Colors.DIM)
        self.success("units", f"Cloned {unit_name} to ID {uid} (from {src})")
<<<<<<< HEAD

=======
    
>>>>>>> origin/refactor-port-managers-to-gdp-783808832176151754
    def unit_moved(self, src_id: int, dst_id: int) -> None:
        """Log unit move."""
        src = self._colorize(str(src_id), Colors.DIM)
        dst = self._colorize(str(dst_id), Colors.BRIGHT_CYAN)
        self.success("units", f"Moved unit {src} → {dst}")
<<<<<<< HEAD

=======
    
>>>>>>> origin/refactor-port-managers-to-gdp-783808832176151754
    def graphic_created(self, name: str, graphic_id: int) -> None:
        """Log graphic creation."""
        gname = self._colorize(f"'{name}'", Colors.BRIGHT_MAGENTA)
        gid = self._colorize(str(graphic_id), Colors.BRIGHT_CYAN)
        self.success("graphics", f"Created {gname} at ID {gid}")
<<<<<<< HEAD

=======
    
>>>>>>> origin/refactor-port-managers-to-gdp-783808832176151754
    def sound_created(self, name: str, sound_id: int) -> None:
        """Log sound creation."""
        sname = self._colorize(f"'{name}'", Colors.BRIGHT_YELLOW)
        sid = self._colorize(str(sound_id), Colors.BRIGHT_CYAN)
        self.success("sounds", f"Created {sname} at ID {sid}")
<<<<<<< HEAD

=======
    
>>>>>>> origin/refactor-port-managers-to-gdp-783808832176151754
    def tech_created(self, name: str, tech_id: int) -> None:
        """Log tech creation."""
        tname = self._colorize(f"'{name}'", Colors.BRIGHT_BLUE)
        tid = self._colorize(str(tech_id), Colors.BRIGHT_CYAN)
        self.success("techs", f"Created {tname} at ID {tid}")
<<<<<<< HEAD

=======
    
    # -------------------------
    # Timing
    # -------------------------
    
    def reset_timer(self) -> None:
        """Reset the start time for elapsed tracking."""
        self.start_time = time.time()
    
    def elapsed(self) -> float:
        """Get elapsed time since start (or last reset)."""
        return time.time() - self.start_time
    
>>>>>>> origin/refactor-port-managers-to-gdp-783808832176151754
    def print_elapsed(self) -> None:
        """Print the total elapsed time."""
        elapsed = self.elapsed()
        time_str = self._colorize(f"{elapsed:.2f}s", Colors.BRIGHT_CYAN)
        self._print("")
        self._print(f"{'─' * 50}")
        self._print(f"Total time: {time_str}")
        self._print(f"{'─' * 50}")
<<<<<<< HEAD
=======
    
>>>>>>> origin/refactor-port-managers-to-gdp-783808832176151754
    # -------------------------
    # Control
    # -------------------------
    
    def disable(self) -> None:
        """Disable all logging output."""
        self.enabled = False
<<<<<<< HEAD
=======
    
>>>>>>> origin/refactor-port-managers-to-gdp-783808832176151754
    def enable(self) -> None:
        """Enable logging output."""
        self.enabled = True


# Global logger instance
logger = Logger()
