"""
GenieWorkspace - Root entrypoint for editing Genie DAT files.

This module provides a single workspace that owns the DatFile and exposes
domain managers for units, graphics, sounds, techs, and civilizations.

Example:
    workspace = GenieWorkspace.load("empires2_x2_p1.dat")
    handle = workspace.units.create("My Unit", base_unit_id=4)
    handle.stats.hit_points = 50
    workspace.save("output.dat")
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Union

from Actual_Tools_GDP.Shared.dat_adapter import DatFile

from Actual_Tools_GDP.Units.unit_manager import GenieUnitManager
from Actual_Tools_GDP.Graphics.graphic_manager import GraphicManager
from Actual_Tools_GDP.Sounds.sound_manager import SoundManager
from Actual_Tools_GDP.Techs.tech_manager import TechManager
from Actual_Tools_GDP.Effects.effect_manager import EffectManager
from Actual_Tools_GDP.Civilizations.civ_manager import CivilizationsManager
from Actual_Tools_GDP.Shared.logger import logger
from Actual_Tools_GDP.Shared.registry import registry
from Actual_Tools_GDP.exceptions import ValidationError

__all__ = ["GenieWorkspace"]

PathLike = Union[str, Path]


@dataclass(slots=True)
class GenieWorkspace:
    """
    Root entrypoint for editing a Genie `.dat` file.

    Design goals:
    - One authoritative owner of the DatFile instance (IO lives here)
    - Composition: exposes domain managers (units/graphics/sounds/techs/civs)
    - No explicit apply() step - changes go directly to the DatFile
    
    Attributes:
        dat: The underlying DatFile object
        source_path: Path from which the DAT was loaded (if any)
        units: Manager for unit operations
        graphics: Manager for graphic operations
        sounds: Manager for sound operations
        techs: Manager for technology operations
        civs: Manager for civilization operations
    """
    dat: DatFile
    source_path: Optional[Path] = None

    units: GenieUnitManager = field(init=False)
    graphics: GraphicManager = field(init=False)
    sounds: SoundManager = field(init=False)
    techs: TechManager = field(init=False)
    effects: EffectManager = field(init=False)
    civs: CivilizationsManager = field(init=False)

    def __post_init__(self) -> None:
        """Initialize managers after dataclass construction."""
        self.units = GenieUnitManager(self.dat)
        self.graphics = GraphicManager(self.dat)
        self.sounds = SoundManager(self.dat)
        self.techs = TechManager(self.dat)
        self.effects = EffectManager(self.dat)
        self.civs = CivilizationsManager(self.dat)

    # -------------------------
    # Construction / IO
    # -------------------------

    @classmethod
    def load(cls, path: PathLike) -> "GenieWorkspace":
        """
        Load a DatFile from disk and return a workspace.
        
        Args:
            path: Path to the .dat file
        
        Returns:
            A new GenieWorkspace with the loaded data
        """
        p = Path(path)
        
        # Log start
        logger.load_start(p.name)
        logger.reset_timer()

        # Try different loader methods (genieutils compatibility)
        loader = getattr(DatFile, "parse", None) or getattr(DatFile, "from_file", None)
        if loader is None:
            raise RuntimeError(
                "DatFile loader not found. Expected DatFile.parse(...) or DatFile.from_file(...)."
            )

        dat = loader(str(p))
        workspace = cls(dat=dat, source_path=p)
        
        # Log completion
        num_civs = len(dat.civs)
        num_units = len(dat.civs[0].units) if dat.civs else 0
        logger.load_complete(num_civs, num_units)
        
        return workspace

    def save(self, target_path: PathLike, validate: bool = True) -> None:
        """
        Save the current DAT state to disk.
        
        Performs two-pass validation:
        1. Validates all deferred references (UUIDs, graphics, sounds, etc.)
        2. Writes the DAT file
        
        Args:
            target_path: Path to save the .dat file to
            validate: If True, run validation before save (default True)
        
        Raises:
            ValidationError: If deferred references are invalid
        """
        from Actual_Tools_GDP.Shared.manifest_loader import serializer, ReferenceNotFoundError
        
        out = Path(target_path)
        
        # Log start
        logger.save_start(out.name)
        
        # Pass 2: Validate all deferred references
        if validate:
            errors = serializer.validate_all(self.dat)
            if errors:
                # Log all errors
                for err in errors:
                    logger.error("workspace", str(err))
                
                # Clear serializer for next attempt
                serializer.clear()
                
                # Raise first error
                raise errors[0]
            
            # Clear after successful validation
            serializer.clear()

        # Try different saver methods
        saver = getattr(self.dat, "save", None) or getattr(self.dat, "write", None)
        if saver is None:
            raise RuntimeError(
                "DatFile save method not found. Expected dat.save(...) or dat.write(...)."
            )

        saver(str(out))
        
        # Log completion
        logger.save_complete(out.name)
    
    def save_registry(self, path: PathLike) -> None:
        """
        Save the registry of created items to a JSON file.
        
        This JSON file can be used by AoE2ScenarioParser to reference
        the units, graphics, and sounds created during this session.
        
        Args:
            path: Path to save the JSON file
        """
        registry.save(path)
        logger.success("workspace", f"Registry saved: {Path(path).name} ({registry.summary()})")
    
    def print_summary(self) -> None:
        """Print a summary and total elapsed time."""
        logger.print_elapsed()

    # -------------------------
    # Manager Factory Methods
    # -------------------------

    def genie_unit_manager(self) -> GenieUnitManager:
        """
        Get the GenieUnitManager instance.
        
        Returns:
            GenieUnitManager for unit operations
        
        Example:
            >>> um = workspace.genie_unit_manager()
            >>> unit = um.create("New Unit", base_unit_id=4)
        """
        return self.units
    
    def graphic_manager(self) -> GraphicManager:
        """
        Get the GraphicManager instance.
        
        Returns:
            GraphicManager for graphic operations
        """
        return self.graphics
    
    def sound_manager(self) -> SoundManager:
        """
        Get the SoundManager instance.
        
        Returns:
            SoundManager for sound operations
        """
        return self.sounds
    
    def tech_manager(self) -> TechManager:
        """
        Get the TechManager instance.
        
        Returns:
            TechManager for technology operations
        """
        return self.techs
    
    def civ_manager(self) -> CivilizationsManager:
        """
        Get the CivilizationsManager instance.
        
        Returns:
            CivilizationsManager for civilization operations
        """
        return self.civs
    
    def effect_manager(self) -> EffectManager:
        """
        Get the EffectManager instance.
        
        Returns:
            EffectManager for effect operations
        
        Example:
            >>> em = workspace.effect_manager()
            >>> effect = em.create("My Effect")
            >>> effect.add_command(type_=5, a=4, d=2.0)
        """
        return self.effects

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
        if self.dat.civs:
            expected_len = len(self.dat.civs[0].units)
            for civ_id, civ in enumerate(self.dat.civs):
                if len(civ.units) != expected_len:
                    add_issue(
                        f"Civ {civ_id} has {len(civ.units)} units, "
                        f"expected {expected_len} (civ 0 length)"
                    )
        
        # Check for None gaps in unit tables
        for civ_id, civ in enumerate(self.dat.civs):
            for unit_id, unit in enumerate(civ.units):
                if unit is None:
                    add_issue(f"Civ {civ_id} unit[{unit_id}] is None (gap detected)")
        
        # Check graphic references (spot check using sampled units)
        num_graphics = len(self.dat.graphics)
        if self.dat.civs and self.dat.civs[0].units:
            for unit in self.dat.civs[0].units[:100]:  # Sample first 100
                if unit is None:
                    continue
                gfx1, gfx2 = unit.standing_graphic
                if gfx1 >= 0 and gfx1 >= num_graphics:
                    add_issue(f"Unit {unit.id} references invalid graphic {gfx1}")
                if gfx2 >= 0 and gfx2 >= num_graphics:
                    add_issue(f"Unit {unit.id} references invalid graphic {gfx2}")
        
        # Check sound references (spot check)
        num_sounds = len(self.dat.sounds)
        if self.dat.civs and self.dat.civs[0].units:
            for unit in self.dat.civs[0].units[:100]:  # Sample first 100
                if unit is None:
                    continue
                if unit.selection_sound >= 0 and unit.selection_sound >= num_sounds:
                    add_issue(f"Unit {unit.id} references invalid sound {unit.selection_sound}")
        
        # Check tech effect_id references
        num_effects = len(self.dat.effects)
        for tech_id, tech in enumerate(self.dat.techs):
            if tech is None:
                continue
            if hasattr(tech, 'effect_id') and tech.effect_id >= 0:
                if tech.effect_id >= num_effects:
                    add_issue(f"Tech {tech_id} references invalid effect {tech.effect_id}")
                elif self.dat.effects[tech.effect_id] is None:
                    add_issue(f"Tech {tech_id} references deleted effect {tech.effect_id}")
        
        # Check effect command targets (sample first 100 effects)
        num_units = len(self.dat.civs[0].units) if self.dat.civs else 0
        for effect_id, effect in enumerate(self.dat.effects[:100]):
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
