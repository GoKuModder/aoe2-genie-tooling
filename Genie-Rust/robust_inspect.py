import zlib
import sys

DAT_FILE = r""

def inspect(offset, length):
    with open(DAT_FILE, "rb") as f:
        data = f.read()
    decompressed = zlib.decompress(data, -15)
    snippet = decompressed[offset : offset+length]
    print(f"OFFSET {offset}: {snippet.hex(' ')}")
    sys.stdout.flush()

if __name__ == "__main__":
    # Check end of restrictions and start of player colors
    inspect(133010, 50)
