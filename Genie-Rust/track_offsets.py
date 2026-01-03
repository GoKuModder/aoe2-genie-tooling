"""Get exact byte offsets for all sections up to Effects."""
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))

from genieutils.datfile import DatFile
from genieutils.common import ByteHandler
import zlib

DAT_FILE = r""

class TrackingByteHandler(ByteHandler):
    def consume_range(self, length):
        old_pos = self.pos
        result = super().consume_range(length)
        return result
    
    def log_pos(self, label):
        print(f"{label}: pos={self.pos}")

def main():
    with open(DAT_FILE, "rb") as f:
        compressed = f.read()
    data = zlib.decompress(compressed, -15)
    
    handler = ByteHandler(data)
    
    # Version
    handler.read_string(8)
    print(f"After version: pos={handler.pos}")
    
    # Terrain restrictions
    terr_rest_size = handler.read_int_16()
    terrains_used = handler.read_int_16()
    print(f"TerrRest size={terr_rest_size}, terrains_used={terrains_used}")
    
    # Skip pointer arrays
    handler.consume_range(terr_rest_size * 4 * 2)
    print(f"After pointers: pos={handler.pos}")
    
    # Skip terrain restrictions (each has terrains_used * 20 bytes)
    handler.consume_range(terr_rest_size * terrains_used * 20)
    print(f"After TerrainRestrictions: pos={handler.pos}")
    
    # Player colours
    player_count = handler.read_int_16()
    handler.consume_range(player_count * 36)
    print(f"After PlayerColours ({player_count}): pos={handler.pos}")
    
    # Sounds
    sound_count = handler.read_int_16()
    print(f"Sound count: {sound_count}, pos={handler.pos}")
    
    # We can't easily skip Sounds without knowing their exact size.
    # Instead, use the library to parse and report positions

if __name__ == "__main__":
    main()
