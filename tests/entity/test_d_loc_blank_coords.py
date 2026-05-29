"""Track B — D-LOC-01 blank coordinate discovery RED skeleton (FR-02)."""

from __future__ import annotations

import pytest

# from src.entity.blank_finder import BlankFinder

# Domain Mock forbidden — use real G1 matrix at GREEN.


class TestDLocBlankCoords:
    """find_blank_coords / BlankFinder — row-major two blanks."""

    def test_d_loc_01_g1_row_major_blank_coords(
        self,
    ) -> None:
        """D-LOC-01 — G1 → 0-index (0,0), (3,3) row-major."""
        # Given: G1 (tests/conftest.py)
        # When: BlankFinder.find_blank_coords(matrix)  # or find_blank_coords(matrix)
        pytest.fail("RED: D-LOC-01 — G1 blanks (0,0) and (3,3) row-major")
