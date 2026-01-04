"""
This module provides a backend abstraction layer for data parsing.

It attempts to import the high-performance Rust-based `genie_rust`
library. If it's not available, it falls back to the pure Python
`genieutils` library.

This allows the tools to function in different environments while
taking advantage of performance improvements when possible.
"""

# pylint: disable=unused-import

try:
    # Prioritize the high-performance Rust backend
    from genie_rust import DatFile, Effect, EffectCommand

except ImportError:
    # Fallback to the pure Python implementation
    from genieutils.datfile import DatFile
    from genieutils.effect import Effect, EffectCommand
