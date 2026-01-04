from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Union

from .backend import DatFile
from .Terrains.terrain_manager import TerrainManager

PathLike = Union[str, Path]

@dataclass(slots=True)
class GenieWorkspace:
    """
    Root entrypoint for editing a Genie `.dat` file.
    """
    dat: DatFile
    source_path: Optional[Path] = None
    terrains: TerrainManager = field(init=False)

    def __post_init__(self) -> None:
        """Initialize managers after dataclass construction."""
        self.terrains = TerrainManager(self.dat)

    @classmethod
    def load(cls, path: PathLike) -> "GenieWorkspace":
        """
        Load a DatFile from disk and return a workspace.
        """
        p = Path(path)
        loader = getattr(DatFile, "parse", None) or getattr(DatFile, "from_file", None)
        if loader is None:
            raise RuntimeError(
                "DatFile loader not found. Expected DatFile.parse(...) or DatFile.from_file(...)."
            )

        dat = loader(str(p))
        workspace = cls(dat=dat, source_path=p)

        return workspace

    def save(self, target_path: PathLike) -> None:
        """
        Save the current DAT state to disk.
        """
        out = Path(target_path)
        saver = getattr(self.dat, "save", None) or getattr(self.dat, "write", None)
        if saver is None:
            raise RuntimeError(
                "DatFile save method not found. Expected dat.save(...) or dat.write(...)."
            )
        saver(str(out))

    def terrain_manager(self) -> TerrainManager:
        """
        Get the TerrainManager instance.
        """
        return self.terrains
