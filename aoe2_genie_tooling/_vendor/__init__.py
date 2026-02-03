# Vendored from GenieDatParser
# This module makes the vendored code available for import as 'sections'

import sys
from pathlib import Path

# Add the _vendor directory to sys.path so 'from sections.xxx' works
_vendor_path = str(Path(__file__).parent)
if _vendor_path not in sys.path:
    sys.path.insert(0, _vendor_path)
