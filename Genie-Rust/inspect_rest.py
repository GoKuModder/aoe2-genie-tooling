import zlib
import os

DAT_FILE = r""

def inspect_rest():
    with open(DAT_FILE, "rb") as f:
        data = f.read()
    decompressed = zlib.decompress(data, -15)
    
    # 8 (header) + 2 (size) + 2 (used) + 408 (pointers) = 420
    offset = 420
    print(f"Bytes at {offset} (Start of Rest 0): {decompressed[offset:offset+40].hex(' ')}")
    
    # Let's check if the 6 bytes are actually BEFORE the restrictions or inside them.
    # Restriction 0: 130 * (4 + 16) = 2600 bytes.
    # If it starts at 420, it ends at 3020.
    offset2 = 420 + 2600
    print(f"Bytes at {offset2} (Start of Rest 1?): {decompressed[offset2:offset2+40].hex(' ')}")

if __name__ == "__main__":
    inspect_rest()
