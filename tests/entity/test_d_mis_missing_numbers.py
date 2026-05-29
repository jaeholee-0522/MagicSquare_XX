"""Track B — D-MIS-01 missing number discovery RED skeleton (FR-03)."""

from __future__ import annotations

import pytest

# from src.entity.missing_number_finder import MissingNumberFinder

# Domain Mock forbidden.


class TestDMisMissingNumbers:
    """find_not_exist_nums / MissingNumberFinder — ascending pair."""

    def test_d_mis_01_g1_missing_numbers_ascending(
        self,
    ) -> None:
        """D-MIS-01 — G1 → [1, 16] ascending."""
        # Given: G1
        # When: MissingNumberFinder.find_missing(matrix)
        pytest.fail("RED: D-MIS-01 — G1 missing numbers [1, 16] ascending")
