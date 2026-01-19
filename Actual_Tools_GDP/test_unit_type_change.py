"""
Test: Safe unit type change from 70 (Creatable) to 80 (Building).
Verifies lazy validation system works correctly.
"""
import sys
from pathlib import Path
import tempfile

lib_path = Path(r"c:\AoE2DE Modding\Code\1 GenieUtils Python Tools  Library")
sys.path.insert(0, str(lib_path))
sys.path.insert(0, str(lib_path / "GenieDatParser" / "src"))

from Actual_Tools_GDP.Base.workspace import GenieWorkspace

SOURCE_DAT = Path(r"C:\Program Files (x86)\Steam\steamapps\common\AoE2DE\resources\_common\dat\empires2_x2_p1.dat")

print("=" * 60)
print("TEST: Unit Type Change (70 to 80)")
print("=" * 60)

# Load
print("\n1. Loading DAT...")
ws = GenieWorkspace.load(str(SOURCE_DAT))

# Use existing Villager (type 70 Creatable)
print("\n2. Getting Villager (type 70 Creatable)...")
TEST_UNIT_ID = 83  # Villager
building_unit = ws.unit_manager.get(TEST_UNIT_ID)

print(f"   Original type: {building_unit.type_}")
print(f"   Has creation_info: {building_unit._primary_unit.creation_info is not None}")
print(f"   Has building_info: {building_unit._primary_unit.building_info is not None}")

# Change to Building type
print("\n3. Converting to type 80 (Building)...")
building_unit.change_unit_type(80)
print(f"   New type: {building_unit.type_}")
print(f"   Dirty units tracked: {ws._type_changed_units}")

# Save (triggers validation)
temp_path = Path(tempfile.gettempdir()) / "test_type_change.dat"
print(f"\n4. Saving DAT (triggers validation)...")
ws.save(str(temp_path))
print(f"   Saved to: {temp_path}")
print(f"   Dirty units after save: {ws._type_changed_units}")

# Reload and verify
print(f"\n5. Reloading DAT...")
ws2 = GenieWorkspace.load(str(temp_path))
unit2 = ws2.unit_manager.get(TEST_UNIT_ID)

print(f"   Reloaded type: {unit2.type_}")
print(f"   Has creation_info: {unit2._primary_unit.creation_info is not None}")
print(f"   Has building_info: {unit2._primary_unit.building_info is not None}")

# Verify correctness
print("\n" + "=" * 60)
success = (
    unit2.type_ == 80 and
    unit2._primary_unit.creation_info is None and
    unit2._primary_unit.building_info is not None
)

if success:
    print("SUCCESS: Type change validated correctly!")
    print("  - Type is 80 (Building)")
    print("  - creation_info removed")
    print("  - building_info initialized")
else:
    print("FAILURE: Structures didn't sync correctly")
    print(f"  Type: {unit2.type_} (expected 80)")
    print(f"  creation_info: {unit2._primary_unit.creation_info} (expected None)")
    print(f"  building_info: {unit2._primary_unit.building_info} (expected not None)")
print("=" * 60)

# Cleanup
temp_path.unlink(missing_ok=True)
