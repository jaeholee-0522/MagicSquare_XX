"""Track B — D-MIS-01 missing number discovery Full RED (FR-03)."""

from __future__ import annotations

import pytest

# Domain Mock forbidden.


class TestDMisMissingNumbers:
    """find_not_exist_nums / MissingNumberFinder — ascending pair."""

    def test_d_mis_01_g1_missing_numbers_ascending(
        self,
        g1_matrix: list[list[int]],
    ) -> None:
        """D-MIS-01 — G1 → [1, 16] ascending."""
        from src.entity.missing_number_finder import MissingNumberFinder

        # Given
        grid = g1_matrix
        finder = MissingNumberFinder()
        expected = [1, 16]

        # When
        result = finder.find_missing(grid)

        # Then
        assert result == expected
