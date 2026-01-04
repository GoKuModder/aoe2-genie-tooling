"""Final integration test for Actual_Tools_GDP with GenieDatParser backend."""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from Actual_Tools_GDP.Shared.dat_adapter import DatFile

DAT_FILE = r"F:\Games\AOE II DE Scirpting Python Projects\1 GenieUtils Python Tools  Library\empires2_x2_p1.dat"
OUTPUT_FILE = r"F:\Games\AOE II DE Scirpting Python Projects\1 GenieUtils Python Tools  Library\Actual_Tools_GDP\final_test_output.dat"

def main():
    print("=== Final Integration Test ===\n")
    
    # Load
    print("1. Loading .dat file...")
    dat = DatFile.parse(DAT_FILE)
    print(f"   Version: {dat.version}")
    print(f"   Civs: {len(dat.civs)}")
    print(f"   Sounds: {len(dat.sounds)}")
    print(f"   Graphics: {len(dat.graphics)}")
    print(f"   Effects: {len(dat.effects)}")
    print(f"   Techs: {len(dat.techs)}")
    
    # Access data
    print("\n2. Accessing unit data...")
    civ = dat.civs[0]
    print(f"   First Civ: {civ.name}")
    unit = next((u for u in civ.units if u is not None), None)
    if unit:
        print(f"   First Unit: {unit.name} (HP: {unit.hit_points})")
    
    # Save
    print("\n3. Saving .dat file...")
    dat.save(OUTPUT_FILE)
    print(f"   Saved to: {OUTPUT_FILE}")
    
    # Verify by reloading
    print("\n4. Verifying by reloading...")
    dat2 = DatFile.parse(OUTPUT_FILE)
    print(f"   Reloaded Civs: {len(dat2.civs)}")
    print(f"   Reloaded Sounds: {len(dat2.sounds)}")
    
    if len(dat2.civs) == len(dat.civs) and len(dat2.sounds) == len(dat.sounds):
        print("\n✓ SUCCESS: Round-trip test passed!")
    else:
        print("\n✗ FAILURE: Data mismatch after round-trip!")

if __name__ == "__main__":
    main()
