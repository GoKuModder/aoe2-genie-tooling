"""Type stubs for GenieWorkspace - enables IDE autocomplete"""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Actual_Tools_GDP.Graphics.graphic_manager import GraphicManager
    from Actual_Tools_GDP.Sounds.sound_manager import SoundManager
    from Actual_Tools_GDP.Techs.tech_manager import TechManager

class GenieWorkspace:
    """
    Root entrypoint for editing a Genie `.dat` file.
    
    Provides managers for units, graphics, sounds, techs, effects, and civilizations.
    """
    
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
    
    @staticmethod
    def load(path: str) -> GenieWorkspace:
        """
        Load a DAT file from disk.
        
        Args:
            path: Path to the .dat file
            
        Returns:
            GenieWorkspace instance with loaded data
        """
        ...
    
    def save(self, path: str, validate: bool = True) -> None:
        """
        Save the DAT file to disk.
        
        Args:
            path: Output path for the .dat file
            validate: Whether to validate before saving
        """
        ...
