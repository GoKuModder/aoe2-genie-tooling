import zlib
import os

DAT_FILE = r""

def inspect_at(offset, length=100):
    with open(DAT_FILE, "rb") as f:
        data = f.read()
    decompressed = zlib.decompress(data, -15)
    snippet = decompressed[offset : offset+length]
    print(f"Bytes at {offset}: {snippet.hex(' ')}")

if __name__ == "__main__":
    # Start of Player Colours count?
    inspect_at(133022, 100)
