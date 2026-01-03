"""Capture byte offsets from genieutils-py parsing."""
import sys
import os
import zlib

sys.path.append(os.path.dirname(os.getcwd()))

DAT_FILE = r""

def get_offsets():
    with open(DAT_FILE, "rb") as f:
        compressed = f.read()
    data = zlib.decompress(compressed, -15)
    
    print(f"Total decompressed size: {len(data)}")
    
    # Manual offset calculation based on genieutils structure
    pos = 0
    
    # Header: 8 bytes
    version = data[pos:pos+8]
    pos += 8
    print(f"Version: {version.decode('utf-8', errors='ignore').strip()}")
    
    # TerrainRestrictions size (u16) and terrains_used (u16)
    terr_rest_size = int.from_bytes(data[pos:pos+2], 'little')
    pos += 2
    terrains_used = int.from_bytes(data[pos:pos+2], 'little')
    pos += 2
    print(f"TerrainRestrictions: size={terr_rest_size}, terrains_used={terrains_used}")
    
    # Two pointer arrays (i32 each)
    ptr_bytes = terr_rest_size * 4 * 2
    pos += ptr_bytes
    print(f"After pointers: pos={pos}")
    
    # TerrainRestrictions: each has (terrains_used * 4) floats + (terrains_used * 16) TerrainPassGraphics
    rest_size = terrains_used * (4 + 16)  # 20 bytes per terrain
    total_rest = terr_rest_size * rest_size
    pos += total_rest
    print(f"After TerrainRestrictions: pos={pos}")
    
    # PlayerColours size (u16)
    player_count = int.from_bytes(data[pos:pos+2], 'little')
    pos += 2
    print(f"PlayerColour count at pos={pos-2}: {player_count}")
    
    # PlayerColours: 36 bytes each (9 * i32)
    pos += player_count * 36
    print(f"After PlayerColours: pos={pos}")
    
    # Sounds size (u16)
    sound_count = int.from_bytes(data[pos:pos+2], 'little')
    print(f"Sound count at pos={pos}: {sound_count}")

if __name__ == "__main__":
    get_offsets()
