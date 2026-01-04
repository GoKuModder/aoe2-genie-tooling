"""
Migration helper script for Actual_Tools-GDP.

This script updates imports from genieutils to the new adapter.
Run this script from the library root directory.
"""
import os
import re

ROOT = "Actual_Tools-GDP"

# Mappings for genieutils imports to adapter imports
IMPORT_MAPPINGS = {
    # DatFile
    r"from genieutils\.datfile import DatFile": "from Actual_Tools_GDP.Shared.dat_adapter import DatFile",
    r"from genieutils\.datfile import ": "from Actual_Tools_GDP.Shared.dat_adapter import ",
    
    # Unit types
    r"from genieutils\.unit import Unit": "from Actual_Tools_GDP.Shared.dat_adapter import Unit",
    r"from genieutils\.unit import AttackOrArmor": "from Actual_Tools_GDP.Shared.dat_adapter import AttackOrArmor",
    r"from genieutils\.unit import DamageGraphic": "from Actual_Tools_GDP.Shared.dat_adapter import DamageGraphic",
    r"from genieutils\.unit import TrainLocation": "from Actual_Tools_GDP.Shared.dat_adapter import TrainLocation",
    r"from genieutils\.unit import ResourceStorage": "from Actual_Tools_GDP.Shared.dat_adapter import ResourceStorage",
    r"from genieutils\.unit import ": "from Actual_Tools_GDP.Shared.dat_adapter import ",
    
    # Task
    r"from genieutils\.task import Task": "from Actual_Tools_GDP.Shared.dat_adapter import Task",
    r"from genieutils\.task import ": "from Actual_Tools_GDP.Shared.dat_adapter import ",
    
    # Sound
    r"from genieutils\.sound import Sound, SoundItem": "from Actual_Tools_GDP.Shared.dat_adapter import Sound, SoundItem",
    r"from genieutils\.sound import Sound": "from Actual_Tools_GDP.Shared.dat_adapter import Sound",
    r"from genieutils\.sound import SoundItem": "from Actual_Tools_GDP.Shared.dat_adapter import SoundItem",
    r"from genieutils\.sound import ": "from Actual_Tools_GDP.Shared.dat_adapter import ",
    
    # Graphic
    r"from genieutils\.graphic import Graphic": "from Actual_Tools_GDP.Shared.dat_adapter import Graphic",
    r"from genieutils\.graphic import ": "from Actual_Tools_GDP.Shared.dat_adapter import ",
    
    # Tech
    r"from genieutils\.tech import Tech": "from Actual_Tools_GDP.Shared.dat_adapter import Tech",
    r"from genieutils\.tech import ": "from Actual_Tools_GDP.Shared.dat_adapter import ",
    
    # Civ
    r"from genieutils\.civ import Civ": "from Actual_Tools_GDP.Shared.dat_adapter import Civ",
    r"from genieutils\.civ import ": "from Actual_Tools_GDP.Shared.dat_adapter import ",
    
    # Module reference updates
    r"from Actual_Tools\.": "from Actual_Tools_GDP.",
    r"import Actual_Tools\.": "import Actual_Tools_GDP.",
}

def migrate_file(filepath):
    """Migrate a single file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"  Error reading {filepath}: {e}")
        return False
    
    original = content
    for pattern, replacement in IMPORT_MAPPINGS.items():
        content = re.sub(pattern, replacement, content)
    
    if content != original:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  Updated: {filepath}")
            return True
        except Exception as e:
            print(f"  Error writing {filepath}: {e}")
            return False
    return False

def main():
    print(f"Migrating files in {ROOT}...")
    updated = 0
    total = 0
    
    for dirpath, dirnames, filenames in os.walk(ROOT):
        # Skip __pycache__
        dirnames[:] = [d for d in dirnames if d != '__pycache__']
        
        for filename in filenames:
            if filename.endswith('.py'):
                total += 1
                filepath = os.path.join(dirpath, filename)
                if migrate_file(filepath):
                    updated += 1
    
    print(f"\nMigration complete: {updated}/{total} files updated.")

if __name__ == "__main__":
    main()
