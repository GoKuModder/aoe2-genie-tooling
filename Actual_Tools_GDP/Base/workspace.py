"""
GenieWorkspace - Root entrypoint for editing Genie DAT files.

Top-to-bottom architecture: Workspace owns DatFile and all support systems.
Managers receive workspace reference for cross-manager access and shared state.

Example:
    workspace = GenieWorkspace.load("empires2_x2_p1.dat")
    unit_manager = workspace.unit_manager
    unit = unit_manager.create("Hero", base_unit_id=4)
    unit.hit_points = 100
    workspace.save("output.dat")
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Union

# Core data access - GenieDatParser is local, not installed
import sys
from pathlib import Path
_genie_parser_path = Path(__file__).parent.parent.parent / "GenieDatParser" / "src"
if str(_genie_parser_path) not in sys.path:
    sys.path.insert(0, str(_genie_parser_path))
from sections.datfile_sections import DatFile
from Actual_Tools_GDP.Base.config import Config, ValidationLevel
from bfp_rs import Version

# Support systems
from Actual_Tools_GDP.Base.core.fileio import FileIO
from Actual_Tools_GDP.Base.core.registry import Registry
from Actual_Tools_GDP.Base.core.logger import Logger
from Actual_Tools_GDP.Base.core.validator import Validator
from Actual_Tools_GDP.Base.core.id_tracker import IDTracker
from Actual_Tools_GDP.Base.core.exceptions import ValidationError

# Managers (TEMPORARILY COMMENTED - need to be rebuilt)
from Actual_Tools_GDP.Units.unit_manager import UnitManager
from Actual_Tools_GDP.Graphics.graphic_manager import GraphicManager
from Actual_Tools_GDP.Sounds.sound_manager import SoundManager
from Actual_Tools_GDP.Techs.tech_manager import TechManager
from Actual_Tools_GDP.Effects.effect_manager import EffectManager
from Actual_Tools_GDP.Civilizations.civ_manager import CivManager

__all__ = ["GenieWorkspace"]

PathLike = Union[str, Path]


@dataclass
class GenieWorkspace:
    """
    Root entrypoint for editing a Genie `.dat` file.

    Architecture: Top-to-Bottom with Dependency Injection
    - Owns the DatFile instance
    - Instantiates all support systems (FileIO, Registry, Logger, etc.)
    - Creates managers and passes self (workspace) for cross-manager access
    - Provides property-based access to managers
    
    Attributes:
        dat: The underlying DatFile object (from GenieDatParser)
        source_path: Path from which the DAT was loaded (if any)
        file_io: Handles read/write operations
        registry: Tracks created items for ASP integration
        logger: Colored console output
        validator: Validates attributes and references
        id_tracker: Tracks ID movements and ensures uniqueness
    """
    dat: DatFile
    source_path: Optional[Path] = None
    target_version: Version = field(default_factory=lambda: Config.DEFAULT_VERSION)
    validation_level: ValidationLevel = field(default_factory=lambda: Config.DEFAULT_VALIDATION)

    def __post_init__(self) -> None:
        """
        Initialize workspace support systems and managers.
        
        Order:
        1. Support systems (FileIO, Registry, Logger, Validator, IDTracker)
        2. Managers (receive workspace for cross-manager access)
        """
        # Support systems
        self.file_io = FileIO(self)
        self.registry = Registry()
        self.logger = Logger()
        self.validator = Validator()
        self.id_tracker = IDTracker()
        
        # Managers (private, accessed via properties)
        self._unit_manager = UnitManager(self)
        self._graphic_manager = GraphicManager(self)
        self._sound_manager = SoundManager(self)
        # self._terrain_manager = TerrainManager(self)
        self._tech_manager = TechManager(self)
        self._effect_manager = EffectManager(self)
        self._civ_manager = CivManager(self)
    
    # Manager Properties
    @property
    def unit_manager(self) -> UnitManager:
        """Access the unit manager."""
        return self._unit_manager
    
    @property
    def graphic_manager(self) -> GraphicManager:
        """Access the graphic manager."""
        return self._graphic_manager
    
    @property
    def sound_manager(self) -> SoundManager:
        """Access the sound manager."""
        return self._sound_manager
    
    @property
    def terrain_manager(self) -> TerrainManager:
        """Access the terrain manager."""
        return self._terrain_manager
    
    @property
    def tech_manager(self) -> TechManager:
        """Access the tech manager."""
        return self._tech_manager
    
    @property
    def effect_manager(self) -> EffectManager:
        """Access the effect manager."""
        return self._effect_manager
    
    @property
    def civ_manager(self) -> CivManager:
        """Access the civilization manager."""
        return self._civ_manager

    # Alias for backward compatibility
    @property
    def civilization_manager(self) -> CivManager:
        """Access the civilization manager (alias for civ_manager)."""
        return self._civ_manager

    # -------------------------
    # Construction / IO
    # -------------------------

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
        p = Path(path)
        
        # Load DAT file via FileIO
        dat = FileIO.load_dat_file(p)
        workspace = cls(dat=dat, source_path=p, validation_level=validation)
        
        # If validate_all, register all existing objects
        if validation == ValidationLevel.VALIDATE_ALL:
            workspace.registry.register_all_at_load(workspace)
            workspace.logger.info(f"Loaded with validation=VALIDATE_ALL ({workspace.registry.summary()})")
        else:
            workspace.logger.info(f"Loaded {p.name} (validation={validation.value})")
        
        return workspace

    def save(
        self,
        target_path: PathLike,
        validate: Union[ValidationLevel, bool] = None,
    ) -> None:
        """
        Save the current DAT state to disk.
        
        Performs optional validation before writing based on validation level:
        - NO_VALIDATION: Skip all checks
        - VALIDATE_NEW: Check session-created objects only
        - VALIDATE_ALL: Full validation of all references
        
        Args:
            target_path: Path to save the .dat file to
            validate: Override validation level. If None, uses workspace default.
                      True = VALIDATE_NEW, False = NO_VALIDATION for backward compat.
        
        Raises:
            ValidationError: If validation fails
        """
        out = Path(target_path)
        
        # Determine validation level
        if validate is None:
            level = self.validation_level
        elif validate is True:
            level = ValidationLevel.VALIDATE_NEW
        elif validate is False:
            level = ValidationLevel.NO_VALIDATION
        else:
            level = validate
        
        # Perform validation based on level
        if level != ValidationLevel.NO_VALIDATION:
            validate_existing = (level == ValidationLevel.VALIDATE_ALL)
            issues = self.validator.validate_all_references(self, validate_existing)
            if issues:
                self.logger.error(f"Validation failed with {len(issues)} issues")
                raise ValidationError(f"Validation failed: {issues[0]}")
        
        # Save via FileIO
        self.file_io.save(str(out))
        self.logger.info(f"Saved to {out.name}")
    
    def save_registry(self, path: PathLike) -> None:
        """
        Save the registry of created items to a JSON file.
        
        This JSON file can be used by AoE2ScenarioParser to reference
        the units, graphics, and sounds created during this session.
        
        Args:
            path: Path to save the JSON file
        """
        self.registry.export_json(str(path))
        self.logger.info(f"Registry saved: {Path(path).name}")
    
    def upgrade_validation(self, level: ValidationLevel) -> None:
        """
        Upgrade validation level mid-session.
        
        If upgrading to VALIDATE_ALL, registers all existing objects that
        haven't been registered yet.
        
        Args:
            level: Target validation level
            
        Example:
            workspace = GenieWorkspace.load("file.dat")  # Default: VALIDATE_NEW
            workspace.upgrade_validation(ValidationLevel.VALIDATE_ALL)
        """
        if level == ValidationLevel.VALIDATE_ALL and self.validation_level != ValidationLevel.VALIDATE_ALL:
            # Register existing objects if not already done
            self.registry.register_all_at_load(self)
            self.logger.info(f"Upgraded to VALIDATE_ALL ({self.registry.summary()})")
        
        self.validation_level = level
    
    # -------------------------
    # Validation
    # -------------------------

    def validate(self, raise_on_error: bool = False) -> List[str]:
        """
        Run integrity checks on the workspace.
        
        Checks performed:
        - Unit list length consistency across civs
        - No None gaps in unit tables
        - Referenced graphic IDs exist
        - Referenced sound IDs exist
        - Tech effect_id references exist
        - Effect command target IDs are valid
        
        Args:
            raise_on_error: If True, raises ValidationError on first issue
        
        Returns:
            List of issue descriptions (empty if valid)
        """
        issues: List[str] = []
        
        def add_issue(msg: str) -> None:
            issues.append(msg)
            if raise_on_error:
                raise ValidationError(msg)
        
        # Check unit list lengths match across civs
        if self.dat.civilizations:
            expected_len = len(self.dat.civilizations[0].units)
            for civ_id, civ in enumerate(self.dat.civilizations):
                if len(civ.units) != expected_len:
                    add_issue(
                        f"Civ {civ_id} has {len(civ.units)} units, "
                        f"expected {expected_len} (civ 0 length)"
                    )
        
        # Check for None gaps in unit tables
        for civ_id, civ in enumerate(self.dat.civilizations):
            for unit_id, unit in enumerate(civ.units):
                if unit is None:
                    add_issue(f"Civ {civ_id} unit[{unit_id}] is None (gap detected)")
        
        # Check graphic references (spot check using sampled units)
        num_graphics = len(self.dat.sprites)
        if self.dat.civilizations and self.dat.civilizations[0].units:
            for unit in self.dat.civilizations[0].units[:100]:  # Sample first 100
                if unit is None:
                    continue
                gfx1, gfx2 = unit.standing_graphic
                if gfx1 >= 0 and gfx1 >= num_graphics:
                    add_issue(f"Unit {unit.id} references invalid graphic {gfx1}")
                if gfx2 >= 0 and gfx2 >= num_graphics:
                    add_issue(f"Unit {unit.id} references invalid graphic {gfx2}")
        
        # Check sound references (spot check)
        num_sounds = len(self.dat.sounds)
        if self.dat.civilizations and self.dat.civilizations[0].units:
            for unit in self.dat.civilizations[0].units[:100]:  # Sample first 100
                if unit is None:
                    continue
                if unit.selection_sound >= 0 and unit.selection_sound >= num_sounds:
                    add_issue(f"Unit {unit.id} references invalid sound {unit.selection_sound}")
        
        # Check tech effect_id references
        num_effects = len(self.dat.tech_effects)
        for tech_id, tech in enumerate(self.dat.techs):
            if tech is None:
                continue
            if hasattr(tech, 'effect_id') and tech.effect_id >= 0:
                if tech.effect_id >= num_effects:
                    add_issue(f"Tech {tech_id} references invalid effect {tech.effect_id}")
                elif self.dat.effects[tech.effect_id] is None:
                    add_issue(f"Tech {tech_id} references deleted effect {tech.effect_id}")
        
        # Check effect command targets (sample first 100 effects)
        num_units = len(self.dat.civilizations[0].units) if self.dat.civilizations else 0
        for effect_id, effect in enumerate(self.dat.tech_effects[:100]):
            if effect is None:
                continue
            for cmd_id, cmd in enumerate(effect.effect_commands):
                # Type 0, 4, 5 = unit attribute modifiers (parameter A = unit/class)
                # Check if references look like unit IDs (positive, reasonable range)
                if cmd.type_ in (0, 4, 5) and cmd.a >= 0:
                    if cmd.c == -1 and cmd.a >= num_units:  # -1 = all civs, A = unit ID
                        add_issue(
                            f"Effect {effect_id} cmd {cmd_id}: "
                            f"type {cmd.type_} references invalid unit {cmd.a}"
                        )
        
        return issues

    def is_valid(self) -> bool:
        """
        Quick check if the workspace passes all validation checks.
        
        Returns:
            True if valid, False otherwise
        """
        return len(self.validate()) == 0
