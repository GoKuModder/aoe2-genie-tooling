import zlib
import os

DAT_FILE = r""

def inspect_data():
    with open(DAT_FILE, "rb") as f:
        data = f.read()
    
    decompressed = zlib.decompress(data, -15)
    print(f"Decompressed size: {len(decompressed)}")
    
    # Check around offset 133598
    offset = 133598
    snippet = decompressed[offset-20 : offset+20]
    print(f"Bytes around {offset}: {snippet.hex(' ')}")
    
    # Search for the string "VER 1.1" or similar to confirm start
    print(f"Start: {decompressed[:10].hex(' ')}")

if __name__ == "__main__":
    inspect_data()
