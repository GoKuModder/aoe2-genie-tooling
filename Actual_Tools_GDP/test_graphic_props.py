"""
Test: Verify graphic properties frame_count, frame_duration, sequence_type are saved correctly.
"""
import sys
import tempfile
from pathlib import Path

lib_path = Path(r"c:\AoE2DE Modding\Code\1 GenieUtils Python Tools  Library")
sys.path.insert(0, str(lib_path))
sys.path.insert(0, str(lib_path / "GenieDatParser" / "src"))

from Actual_Tools_GDP.Base.workspace import GenieWorkspace

SOURCE_DAT = Path(r"C:\Program Files (x86)\Steam\steamapps\common\AoE2DE\resources\_common\dat\empires2_x2_p1.dat")

print("=" * 60)
print("TEST: Graphic Properties Save/Load")
print("=" * 60)

ws = GenieWorkspace.load(str(SOURCE_DAT))

# Create a new graphic with specific values
print("\n1. Creating graphic with specific values...")
g = ws.graphic_manager.add_graphic("test_graphic")
print(f"   Created graphic ID: {g.id}")

# Set properties
g.frame_count = 20
g.frame_duration = 2.5
g.sequence_type = 9

print(f"   Set: frame_count=20, frame_duration=2.5, sequence_type=9")

# Read back immediately
print(f"\n2. Reading back BEFORE save:")
print(f"   frame_count: {g.frame_count}")
print(f"   frame_duration: {g.frame_duration}")
print(f"   sequence_type: {g.sequence_type}")

# Check underlying sprite directly
sprite = ws.dat.sprites[g.id]
print(f"\n3. Checking underlying sprite directly:")
print(f"   num_frames: {sprite.num_frames}")
print(f"   frame_rate: {sprite.frame_rate}")
print(f"   sequence_type: {sprite.sequence_type}")

# Save
temp_path = Path(tempfile.gettempdir()) / "test_graphic.dat"
ws.save(str(temp_path))
print(f"\n4. Saved to: {temp_path}")

# Reload
ws2 = GenieWorkspace.load(str(temp_path))
print(f"\n5. Reloaded. Checking graphic ID {g.id}...")

sprite2 = ws2.dat.sprites[g.id]
print(f"   num_frames: {sprite2.num_frames}")
print(f"   frame_rate: {sprite2.frame_rate}")
print(f"   sequence_type: {sprite2.sequence_type}")

# Verify
ok = (sprite2.num_frames == 20 and sprite2.frame_rate == 2.5 and sprite2.sequence_type == 9)
print("\n" + "=" * 60)
if ok:
    print("SUCCESS: All values preserved correctly!")
else:
    print("FAILURE: Values NOT preserved!")
print("=" * 60)
