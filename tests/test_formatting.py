"""Test that verifies all project files conform to black formatting."""

import subprocess
from pathlib import Path


def test_black_formatting():
    """Run black --check and verify all files are formatted correctly."""
    project_root = Path(__file__).parent.parent
    result = subprocess.run(
        ["black", "--check", "."], cwd=project_root, capture_output=True, text=True
    )
    if result.returncode != 0:
        raise AssertionError(f"Black check failed:\n{result.stdout}\n{result.stderr}")
