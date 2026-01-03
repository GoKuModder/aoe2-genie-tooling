import zlib
import os

DAT_FILE = r""

def inspect_gap():
    with open(DAT_FILE, "rb") as f:
        data = f.read()
    decompressed = zlib.decompress(data, -15)
    
    # End of restrictions: 133,020
    offset = 133010
    snippet = decompressed[offset : offset+30]
    print(f"Bytes around end of restrictions ({offset}): {snippet.hex(' ')}")

if __name__ == "__main__":
    inspect_gap()
