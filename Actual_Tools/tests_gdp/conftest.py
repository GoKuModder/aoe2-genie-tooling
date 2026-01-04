"""
Pytest fixtures for Actual_Tools GDP (Genie-Rust) backend tests.

This conftest.py provides fixtures that load a real, truncated DAT file
using the Genie-Rust backend. This allows for testing against actual
game data structures.
"""
import os
import pytest
from Actual_Tools import GenieWorkspace

@pytest.fixture(scope="function")
def dat_file() -> GenieWorkspace:
    """
    Loads the test DAT file using the Genie-Rust backend.

    This fixture is function-scoped to ensure test isolation. It provides
    a fresh, fully-parsed workspace object for each test function.
    """
    # The test runner is executed from the root of the repository.
    dat_path = "empires2_x2_p1_RUST_TEST.dat"

    if not os.path.exists(dat_path):
        pytest.fail(f"Test DAT file not found at: {os.path.abspath(dat_path)}")

    # The GenieWorkspace will automatically use the high-performance backend
    # if it's available, which is what we want for these tests.
    workspace = GenieWorkspace.load(dat_path)

    return workspace
