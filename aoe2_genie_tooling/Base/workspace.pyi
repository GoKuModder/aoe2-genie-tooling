"""Type stubs for GenieWorkspace - enables IDE autocomplete"""
from pathlib import Path
from typing import List, Optional, Union

from bfp_rs import Version
from sections.datfile_sections import DatFile

from aoe2_genie_tooling.Base.config import ValidationLevel
from aoe2_genie_tooling.Base.core.fileio import FileIO
from aoe2_genie_tooling.Base.core.registry import Registry
from aoe2_genie_tooling.Base.core.logger import Logger
from aoe2_genie_tooling.Base.core.validator import Validator
from aoe2_genie_tooling.Base.core.id_tracker import IDTracker

from aoe2_genie_tooling.Units.unit_manager import UnitManager
from aoe2_genie_tooling.Graphics.graphic_manager import GraphicManager
from aoe2_genie_tooling.Sounds.sound_manager import SoundManager
from aoe2_genie_tooling.Techs.tech_manager import TechManager
from aoe2_genie_tooling.Effects.effect_manager import EffectManager
from aoe2_genie_tooling.Civilizations.civ_manager import CivManager

PathLike = Union[str, Path]


class GenieWorkspace:
    """
    Root entrypoint for editing a Genie `.dat` file.
    
    Architecture: Top-to-Bottom with Dependency Injection
    - Owns the DatFile instance
    - Instantiates all support systems (FileIO, Registry, Logger, etc.)
    - Creates managers and passes self (workspace) for cross-manager access
    - Provides property-based access to managers
    """
    
    # Core data
    dat: DatFile
    source_path: Optional[Path]
    target_version: Version
    validation_level: ValidationLevel
    
    # Support systems
    file_io: FileIO
    registry: Registry
    logger: Logger
    validator: Validator
    id_tracker: IDTracker
    
    # Manager properties
    @property
    def unit_manager(self) -> UnitManager:
        """Access the unit manager."""
        ...
    
    @property
    def graphic_manager(self) -> GraphicManager:
        """Access the graphic manager."""
        ...
    
    @property
    def sound_manager(self) -> SoundManager:
        """Access the sound manager."""
        ...
    
    @property
    def tech_manager(self) -> TechManager:
        """Access the tech manager."""
        ...
    
    @property
    def effect_manager(self) -> EffectManager:
        """Access the effect manager."""
        ...
    
    @property
    def civ_manager(self) -> CivManager:
        """Access the civilization manager."""
        ...
    
    @property
    def civilization_manager(self) -> CivManager:
        """Access the civilization manager (alias for civ_manager)."""
        ...
    
    # Construction / IO
    @classmethod
    def load(
        cls,
        path: PathLike,
        validation: ValidationLevel = ValidationLevel.VALIDATE_NEW,
    ) -> "GenieWorkspace":
        """
        Load a DatFile from disk and return a workspace.
        
        Args:
            path: Path to the .dat file
            validation: Validation level (default: VALIDATE_NEW)
        
        Returns:
            A new GenieWorkspace with the loaded data
        """
        ...
    
    def save(
        self,
        target_path: PathLike,
        validate: Union[ValidationLevel, bool] = None,
    ) -> None:
        """
        Save the current DAT state to disk.
        
        Args:
            target_path: Path to save the .dat file to
            validate: Override validation level. If None, uses workspace default.
                      True = VALIDATE_NEW, False = NO_VALIDATION for backward compat.
        
        Raises:
            ValidationError: If validation fails
        """
        ...
    
    def save_registry(self, path: PathLike) -> None:
        """
        Save the registry of created items to a JSON file.
        
        Args:
            path: Path to save the JSON file
        """
        ...
    
    def upgrade_validation(self, level: ValidationLevel) -> None:
        """
        Upgrade validation level mid-session.
        
        Args:
            level: Target validation level
        """
        ...
    
    # Validation
    def validate(self, raise_on_error: bool = False) -> List[str]:
        """
        Run integrity checks on the workspace.
        
        Args:
            raise_on_error: If True, raises ValidationError on first issue
        
        Returns:
            List of issue descriptions (empty if valid)
        """
        ...
    
    def is_valid(self) -> bool:
        """
        Quick check if the workspace passes all validation checks.
        
        Returns:
            True if valid, False otherwise
        """
        ...
