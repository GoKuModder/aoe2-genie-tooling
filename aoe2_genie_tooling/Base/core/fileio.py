"""
FileIO - Handles reading and writing DAT files.

Responsibilities:
- Load DAT files from disk using GenieDatParser backend
- Save modified DAT files to disk
- Handle backend method variations (parse/from_file, save/write)
"""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from aoe2_genie_tooling.Base.workspace import GenieWorkspace

# Import DatFile from vendored GenieDatParser
import aoe2_genie_tooling._vendor  # Initialize vendored path
from sections.datfile_sections import DatFile

PathLike = Union[str, Path]

__all__ = ["FileIO"]


class FileIO:
    """
    Handles file I/O operations for DAT files.
    
    Pattern: Instance bound to workspace for saving, static method for loading.
    """
    
    def __init__(self, workspace: GenieWorkspace) -> None:
        """
        Initialize FileIO with workspace reference.
        
        Args:
            workspace: The GenieWorkspace instance owning this FileIO
        """
        self.workspace = workspace
    
    @staticmethod
    def load_dat_file(path: PathLike) -> DatFile:
        """
        Load a DatFile from disk using GenieDatParser backend.
        
        Tries multiple loader methods for compatibility:
        - DatFile.parse(path)
        - DatFile.from_file(path)
        
        Args:
            path: Path to the .dat file
        
        Returns:
            Loaded DatFile instance
        
        Raises:
            RuntimeError: If no compatible loader method found
        """
        p = Path(path)
        
        # Try different loader methods (backend compatibility)
        loader = getattr(DatFile, "parse", None) or getattr(DatFile, "from_file", None)
        if loader is None:
            raise RuntimeError(
                "DatFile loader not found. "
                "Expected DatFile.parse(...) or DatFile.from_file(...)."
            )
        
        return loader(str(p))
    
    def save(self, path: PathLike) -> None:
        """
        Save the workspace's DAT file to disk.
        
        Uses DatFile.to_file() method from GenieDatParser.
        
        Args:
            path: Output path for the .dat file
        """
        p = Path(path)
        
        # Use to_file method from GenieDatParser
        self.workspace.dat.to_file(str(p))
