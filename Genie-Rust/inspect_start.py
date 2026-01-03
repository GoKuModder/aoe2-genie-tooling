import zlib
import os

DAT_FILE = r""

def inspect_start():
    with open(DAT_FILE, "rb") as f:
        data = f.read()
    decompressed = zlib.decompress(data, -15)
    print(f"Header: {decompressed[:8].hex(' ')}")
    print(f"TerrRest Size & Used: {decompressed[8:12].hex(' ')}")
    print(f"Next 40 bytes: {decompressed[12:52].hex(' ')}")

if __name__ == "__main__":
    inspect_start()
