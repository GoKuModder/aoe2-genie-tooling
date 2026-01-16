"""
Test Reset-Append-Save strategy.
"""
import sys
from pathlib import Path
import tempfile

lib_path = Path(r"c:\AoE2DE Modding\Code\1 GenieUtils Python Tools  Library")
sys.path.insert(0, str(lib_path))
sys.path.insert(0, str(lib_path / "GenieDatParser" / "src"))

from Actual_Tools_GDP.Base.workspace import GenieWorkspace
from sections.sprite_data.sprite import Sprite
from sections.sprite_data.facet_attack_sound import FacetAttackSound

print("1: Load DAT", flush=True)
SOURCE_DAT = Path(r"C:\Program Files (x86)\Steam\steamapps\common\AoE2DE\resources\_common\dat\empires2_x2_p1.dat")
ws = GenieWorkspace.load(str(SOURCE_DAT))

print("2: Create sprite with Reset-Append", flush=True)
new_sprite = Sprite(ver=ws.dat.ver)

# Break sharing (safe for new sprite too)
new_sprite.facet_attack_sounds = []

# Populate via append
for i in range(16):
    s = FacetAttackSound(ver=ws.dat.ver)
    s.sound_id1 = i
    new_sprite.facet_attack_sounds.append(s)

# Update metadata
new_sprite.num_facets = 16
new_sprite.facets_have_attack_sounds = True

print(f"  List len: {len(new_sprite.facet_attack_sounds)}")
print(f"  Num facets: {new_sprite.num_facets}")

# Add to sprites
print("3: Add to sprites list", flush=True)
ws.dat.sprites.append(new_sprite) # using append here is fine for test

# Save
print("4: Save", flush=True)
TEST_DIR = Path(tempfile.mkdtemp())
output = TEST_DIR / "test_reset_append.dat"
ws.save(str(output), validate=False)
print(f"  Saved: {output.stat().st_size} bytes")

print("5: Reload", flush=True)
ws2 = GenieWorkspace.load(str(output))
print(f"  Reloaded sprites: {len(ws2.dat.sprites)}")

# Find our sprite (last one)
loaded_sprite = ws2.dat.sprites[-1]
print(f"  Loaded num_facets: {loaded_sprite.num_facets}")
print(f"  Loaded sounds len: {len(loaded_sprite.facet_attack_sounds)}")

print("\n=== SUCCESS ===")
