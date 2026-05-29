"""Track B — D-SOL-01~04 two-cell solver Full RED (FR-05)."""

from __future__ import annotations

import pytest

from tests.conftest import G1_EXPECTED_SOLUTION, G2_EXPECTED_SOLUTION

# Domain Mock forbidden.


class TestDSolSolution:
    """solution / TwoCellSolver — Attempt 1/2, I8~I10."""

    def test_d_sol_01_g1_step_a_small_first_success(
        self,
        g1_matrix: list[list[int]],
    ) -> None:
        """D-SOL-01 — G1 Attempt 1 → [1,1,1,4,4,16] (1-index)."""
        from src.entity.solver import TwoCellSolver

        # Given
        grid = g1_matrix
        solver = TwoCellSolver()
        expected = G1_EXPECTED_SOLUTION

        # When
        result = solver.solve(grid)

        # Then
        assert result == expected

    def test_d_sol_02_g2_reverse_success(
        self,
        g2_matrix: list[list[int]],
    ) -> None:
        """D-SOL-02 — G2 Attempt 2 success (PRD Matrix B)."""
        from src.entity.solver import TwoCellSolver

        # Given
        grid = g2_matrix
        solver = TwoCellSolver()
        expected = G2_EXPECTED_SOLUTION

        # When
        result = solver.solve(grid)

        # Then
        assert result == expected

    def test_d_sol_03_g3_both_attempts_fail(
        self,
        g3_matrix: list[list[int]],
    ) -> None:
        """D-SOL-03 — G3 both fail → DOMAIN-ERR-NO_VALID_PLACEMENT."""
        from src.entity.domain_errors import DomainErrorResponse, NO_VALID_PLACEMENT_CODE
        from src.entity.solver import TwoCellSolver

        # Given
        grid = g3_matrix
        solver = TwoCellSolver()

        # When
        result = solver.solve(grid)

        # Then
        assert isinstance(result, DomainErrorResponse)
        assert result.code == NO_VALID_PLACEMENT_CODE

    def test_d_sol_04_output_length_six_and_coords_one_index(
        self,
        g1_matrix: list[list[int]],
    ) -> None:
        """D-SOL-04 — solution output len 6, coords ∈ [1,4]."""
        from src.entity.solver import TwoCellSolver

        # Given
        grid = g1_matrix
        solver = TwoCellSolver()

        # When
        result = solver.solve(grid)

        # Then
        assert isinstance(result, list)
        assert len(result) == 6
        r1, c1, _n1, r2, c2, _n2 = result
        for coord in (r1, c1, r2, c2):
            assert 1 <= coord <= 4
