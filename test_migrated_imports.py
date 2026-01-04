"""Test imports for migrated Actual_Tools-GDP."""
import sys
import os

# Set up path
sys.path.insert(0, os.path.dirname(__file__))

print("Testing imports...")

try:
    from Actual_Tools_GDP.Shared.dat_adapter import DatFile, Unit, Civ
    print("  ✓ dat_adapter imports OK")
except Exception as e:
    print(f"  ✗ dat_adapter import failed: {e}")

try:
    from Actual_Tools_GDP.Units.unit_manager import GenieUnitManager
    print("  ✓ GenieUnitManager import OK")
except Exception as e:
    print(f"  ✗ GenieUnitManager import failed: {e}")

try:
    from Actual_Tools_GDP.Sounds.sound_manager import SoundManager
    print("  ✓ SoundManager import OK")
except Exception as e:
    print(f"  ✗ SoundManager import failed: {e}")

try:
    from Actual_Tools_GDP.Graphics.graphic_manager import GraphicManager
    print("  ✓ GraphicManager import OK")
except Exception as e:
    print(f"  ✗ GraphicManager import failed: {e}")

print("\nDone.")
