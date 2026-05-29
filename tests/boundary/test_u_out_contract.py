"""Track A — U-OUT-01~03 output contract Full RED (FR-05)."""

from __future__ import annotations

import pytest

from src.control.solve_use_case import SolveUseCase
from tests.conftest import G1_EXPECTED_SOLUTION

AC_ID = "FR-05"
DOC = f"{AC_ID}, PRD §12.2 success int[6]"


class TestUOutContract:
    """Boundary success output schema (valid input — G1)."""

    def test_u_out_01_success_result_length_is_six(
        self,
        g1_matrix: list[list[int]],
        solve_use_case: SolveUseCase,
    ) -> None:
        """U-OUT-01 — success path returns int[6]."""
        # Given
        grid = g1_matrix

        # When
        result = solve_use_case.execute(grid)

        # Then
        assert isinstance(result, list)
        assert len(result) == 6

    def test_u_out_02_success_coords_are_one_indexed_in_one_to_four(
        self,
        g1_matrix: list[list[int]],
        solve_use_case: SolveUseCase,
    ) -> None:
        """U-OUT-02 — r1,c1,r2,c2 each in [1,4] (1-index)."""
        # Given
        grid = g1_matrix

        # When
        result = solve_use_case.execute(grid)

        # Then
        assert isinstance(result, list)
        r1, c1, _n1, r2, c2, _n2 = result
        for coord in (r1, c1, r2, c2):
            assert 1 <= coord <= 4

    def test_u_out_03_success_result_sequence_r1_c1_n1_r2_c2_n2(
        self,
        g1_matrix: list[list[int]],
        solve_use_case: SolveUseCase,
    ) -> None:
        """U-OUT-03 — output order [r1,c1,n1,r2,c2,n2] per PRD §12.2."""
        # Given
        grid = g1_matrix
        expected = G1_EXPECTED_SOLUTION

        # When
        result = solve_use_case.execute(grid)

        # Then
        assert result == expected
