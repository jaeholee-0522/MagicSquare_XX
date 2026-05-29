"""Track B — D-LOC-01 blank coordinate discovery Full RED (FR-02)."""

from __future__ import annotations

import pytest

# Domain Mock forbidden — use real G1 matrix at GREEN.


class TestDLocBlankCoords:
    """find_blank_coords / BlankFinder — row-major two blanks."""

    def test_d_loc_01_g1_row_major_blank_coords(
        self,
        g1_matrix: list[list[int]],
    ) -> None:
        """D-LOC-01 — G1 → 0-index (0,0), (3,3) row-major."""
        from src.entity.blank_finder import BlankFinder

        # Given
        grid = g1_matrix
        finder = BlankFinder()
        expected = [(0, 0), (3, 3)]

        # When
        result = finder.find_blank_coords(grid)

        # Then
        assert result == expected
