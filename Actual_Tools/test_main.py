#!/usr/bin/env python3
"""
Actual_Tools Round-Trip Demo

This script demonstrates the Actual_Tools API with round-trip verification:
1. Load a DAT file
2. Apply changes using the public API
3. Save to a temp output file
4. Reload the output file
5. Verify changes persisted

NOT a pytest file - run directly with: python test_main.py

Requirements:
    - empires2_x2_p1.dat must be in the same directory as this script
    - The genieutils-py library must be installed/available
"""
from __future__ import annotations

import os
import sys
import zlib
from pathlib import Path

# Add paths for development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).parent.parent))

from genieutils.datfile import DatFile

# --- Monkeypatch DatFile.save to fix zlib issue ---
def patched_save(self, target_file: str) -> None:
    """Patched save method to fix zlib wbits issue."""
    uncompressed = self.to_bytes()
    compressobj = zlib.compressobj(level=-1, wbits=-15)
    compressed = compressobj.compress(uncompressed) + compressobj.flush()
    Path(target_file).write_bytes(compressed)

DatFile.save = patched_save
# --------------------------------------------------------


def main() -> int:
    """
    Run the round-trip demonstration.
    
    Returns:
        0 if all tests pass, 1 otherwise
    """
    from Actual_Tools import GenieWorkspace
    
    print("=" * 70)
    print("Actual_Tools Round-Trip Demo")
    print("=" * 70)
    
    # Paths
    script_dir = Path(__file__).parent
    input_dat = script_dir / "empires2_x2_p1.dat"
    output_dat = script_dir / "empires2_x2_p1_test_output.dat"
    
    if not input_dat.exists():
        print(f"ERROR: Input DAT file not found: {input_dat}")
        print("Please copy empires2_x2_p1.dat to the Actual_Tools directory.")
        return 1
    
    # -------------------------
    # Step 1: Load
    # -------------------------
    print(f"\n1. Loading {input_dat.name}...")
    workspace = GenieWorkspace.load(input_dat)
    
    num_civs = len(workspace.dat.civs)
    num_units = len(workspace.dat.civs[0].units)
    print(f"   Loaded: {num_civs} civilizations, {num_units} units")
    
    # -------------------------
    # Step 2: Apply Changes
    # -------------------------
    print("\n2. Applying changes...")
    
    # Test values and expected results
    TEST_UNIT_ID = 2850
    TEST_UNIT_NAME = "RoundTripTestUnit"
    TEST_UNIT_HP = 999
    TEST_ICON_ID = 123
    
    CLONE_UNIT_ID = 2851
    CLONE_UNIT_NAME = "ClonedTestUnit"
    
    TEST_GRAPHIC_ID = None  # Will be assigned
    TEST_GRAPHIC_NAME = "round_trip_test.slp"
    
    # Create a unit
    print(f"   Creating unit at ID {TEST_UNIT_ID}...")
    unit_handle = workspace.units.create(
        name=TEST_UNIT_NAME,
        base_unit_id=4,  # Clone from Archer
        unit_id=TEST_UNIT_ID,
        on_conflict="overwrite",
    )
    unit_handle.stats.hit_points = TEST_UNIT_HP
    unit_handle.icon_id = TEST_ICON_ID
    print(f"   - Name: {unit_handle.name}")
    print(f"   - HP: {unit_handle.stats.hit_points}")
    print(f"   - Icon: {unit_handle.icon_id}")
    
    # Clone a unit
    print(f"\n   Cloning unit 4 to ID {CLONE_UNIT_ID}...")
    clone_handle = workspace.units.clone_into(
        dest_unit_id=CLONE_UNIT_ID,
        base_unit_id=4,
        name=CLONE_UNIT_NAME,
        on_conflict="overwrite",
    )
    print(f"   - Name: {clone_handle.name}")
    
    # Create a graphic
    print("\n   Creating graphic...")
    new_graphic = workspace.graphics.add_graphic(
        file_name=TEST_GRAPHIC_NAME,
        template_id=0,
    )
    TEST_GRAPHIC_ID = new_graphic.id
    print(f"   - ID: {TEST_GRAPHIC_ID}")
    print(f"   - File: {new_graphic.file_name}")
    
    # Assign graphic to unit's attack
    unit_handle.graphics.attack = new_graphic
    print(f"   - Assigned to unit attack graphic")
    
    # -------------------------
    # Step 3: Save
    # -------------------------
    print(f"\n3. Saving to {output_dat.name}...")
    try:
        workspace.save(output_dat)
        print("   Save complete!")
    except Exception as e:
        print(f"   ERROR: Save failed: {e}")
        print("")
        print("   This may be due to genieutils-py limitations.")
        print("   The patched_save function attempts to fix zlib issues.")
        return 1
    
    # -------------------------
    # Step 4: Reload
    # -------------------------
    print(f"\n4. Reloading {output_dat.name} for verification...")
    workspace2 = GenieWorkspace.load(output_dat)
    print("   Reload complete!")
    
    # -------------------------
    # Step 5: Verify
    # -------------------------
    print("\n5. Verifying changes persisted...")
    
    all_pass = True
    
    # Verify created unit
    unit = workspace2.dat.civs[0].units[TEST_UNIT_ID]
    
    def check(description: str, expected, actual) -> bool:
        nonlocal all_pass
        if expected == actual:
            print(f"   ✓ {description}: {actual}")
            return True
        else:
            print(f"   ✗ {description}: expected {expected!r}, got {actual!r}")
            all_pass = False
            return False
    
    print("\n   Unit checks:")
    check("Unit name", TEST_UNIT_NAME, unit.name)
    check("Unit HP", TEST_UNIT_HP, unit.hit_points)
    check("Unit icon_id", TEST_ICON_ID, unit.icon_id)
    if unit.type_50:
        check("Unit attack_graphic", TEST_GRAPHIC_ID, unit.type_50.attack_graphic)
    
    # Verify cloned unit
    clone = workspace2.dat.civs[0].units[CLONE_UNIT_ID]
    print("\n   Clone checks:")
    check("Clone name", CLONE_UNIT_NAME, clone.name)
    
    # Verify graphic
    graphic = workspace2.dat.graphics[TEST_GRAPHIC_ID]
    print("\n   Graphic checks:")
    check("Graphic file_name", TEST_GRAPHIC_NAME, graphic.file_name)
    
    # -------------------------
    # Summary
    # -------------------------
    print("\n" + "=" * 70)
    if all_pass:
        print("ALL TESTS PASSED!")
        print("")
        print("The round-trip test verified:")
        print("  - Unit creation with custom properties")
        print("  - Unit cloning")
        print("  - Graphic creation and assignment")
        print("  - Save/reload data integrity")
        return 0
    else:
        print("SOME TESTS FAILED!")
        print("")
        print("Check the output above for details.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
