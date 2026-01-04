# Agent Instructions for the Datasets/ Directory

This directory contains the core game data definitions, manifests, and raw data extracts that drive the `Actual_Tools` library. It is considered the "source of truth" for game mechanics and object attributes.

When working with files in this directory, please adhere to the following guidelines:

1.  **Maintain Data Integrity:** The data in this directory is critical for the correct functioning of the entire toolkit. Before making any changes, ensure you understand their full impact. Any modifications to data schemas, such as adding a new attribute or changing a data type, must be reflected across all relevant files and tested thoroughly.

2.  **Follow Established Formats:** All data files, whether CSV, Python scripts, or Markdown, follow a specific schema. Do not alter the structure of these files (e.g., change column order in `manifest.csv` or modify function signatures in `.py` files) without a compelling reason and updating the code that consumes them.

3.  **Source of Truth:** The data here is the ground truth. Do not hardcode values in other parts of the codebase that should be defined here. When you need to reference game data, it should be loaded from the files in this directory.

4.  **Differential Testing:** The `.dat` file in the root of the repository (`empires2_x2_p1_RUST_TEST.dat`) is a truncated test file. Any changes to data structures should be tested against this file to ensure that both the Rust and Python backends can still parse it correctly.

By following these instructions, you help ensure that the project's data remains consistent, reliable, and easy to maintain.
