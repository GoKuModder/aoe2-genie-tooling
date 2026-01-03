import zlib
import os

DAT_FILE = r""

def test_decompression():
    with open(DAT_FILE, "rb") as f:
        data = f.read()
    
    # Try standard zlib
    try:
        d = zlib.decompress(data)
        print(f"Success: standard zlib, size: {len(d)}")
        return
    except Exception as e:
        print(f"Failed: standard zlib: {e}")

    # Try raw deflate
    try:
        d = zlib.decompress(data, -15)
        print(f"Success: raw deflate, size: {len(d)}")
        return
    except Exception as e:
        print(f"Failed: raw deflate: {e}")

    # Try uncompressed (check version string)
    if b"VER" in data[:10] or b"1.1" in data[:10]:
        print("Success: appears to be uncompressed")
        return

if __name__ == "__main__":
    test_decompression()
