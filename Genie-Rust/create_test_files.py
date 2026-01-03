"""Create minimal .dat test files for alignment isolation."""
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))

from genieutils.datfile import DatFile
from pathlib import Path
import zlib

SOURCE = r""
OUT_DIR = Path(r"")

def compress_raw_deflate(data):
    """Compress using raw deflate (no header)."""
    compressor = zlib.compressobj(level=6, wbits=-15)
    return compressor.compress(data) + compressor.flush()

def main():
    OUT_DIR.mkdir(exist_ok=True)
    
    print("Loading source file...")
    df = DatFile.parse(SOURCE)
    
    # File 1: 1 civ with 1 unit
    print("Creating file_1_unit.dat...")
    df1 = DatFile.parse(SOURCE)
    df1.civs = df1.civs[:1]
    df1.civs[0].units = df1.civs[0].units[:1]
    df1.sounds = []
    df1.graphics = []
    df1.graphic_pointers = []
    df1.effects = []
    df1.techs = []
    uncompressed = df1.to_bytes()
    Path(OUT_DIR / "file_1_unit.dat").write_bytes(compress_raw_deflate(uncompressed))
    print(f"  Civs: {len(df1.civs)}, Units: {len(df1.civs[0].units)}")
    
    # File 2: 1 sound only
    print("Creating file_1_sound.dat...")
    df2 = DatFile.parse(SOURCE)
    df2.sounds = df2.sounds[:1]
    df2.graphics = []
    df2.graphic_pointers = []
    df2.civs = []
    df2.effects = []
    df2.techs = []
    uncompressed = df2.to_bytes()
    Path(OUT_DIR / "file_1_sound.dat").write_bytes(compress_raw_deflate(uncompressed))
    print(f"  Sounds: {len(df2.sounds)}")
    
    # File 3: 1 graphic only
    print("Creating file_1_graphic.dat...")
    df3 = DatFile.parse(SOURCE)
    df3.graphics = df3.graphics[:1]
    df3.graphic_pointers = df3.graphic_pointers[:1]
    df3.sounds = []
    df3.civs = []
    df3.effects = []
    df3.techs = []
    uncompressed = df3.to_bytes()
    Path(OUT_DIR / "file_1_graphic.dat").write_bytes(compress_raw_deflate(uncompressed))
    print(f"  Graphics: {len(df3.graphics)}")
    
    print("Done!")

if __name__ == "__main__":
    main()

