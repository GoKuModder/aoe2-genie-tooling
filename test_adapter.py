"""Test the adapter layer."""
import sys
sys.path.insert(0, "Actual_Tools-GDP")

from Shared.dat_adapter import DatFile

DAT_FILE = r"F:\Games\AOE II DE Scirpting Python Projects\1 GenieUtils Python Tools  Library\empires2_x2_p1.dat"

def main():
    print("Loading via adapter...")
    dat = DatFile.parse(DAT_FILE)
    
    print(f"Version: {dat.version}")
    print(f"Civs: {len(dat.civs)}")
    print(f"Graphics: {len(dat.graphics)}")
    print(f"Sounds: {len(dat.sounds)}")
    print(f"Effects: {len(dat.effects)}")
    print(f"Techs: {len(dat.techs)}")
    
    if len(dat.civs) > 0:
        civ = dat.civs[0]
        print(f"First Civ Name: {civ.name}")
        if hasattr(civ, 'units') and len(civ.units) > 0:
            unit = next((u for u in civ.units if u is not None), None)
            if unit:
                print(f"First Unit Name: {unit.name}")
                print(f"First Unit HP: {unit.hit_points}")
    
    # Test save
    print("\nTesting save...")
    dat.save(r"F:\Games\AOE II DE Scirpting Python Projects\1 GenieUtils Python Tools  Library\Actual_Tools-GDP\test_output.dat")
    print("Save successful!")

if __name__ == "__main__":
    main()
