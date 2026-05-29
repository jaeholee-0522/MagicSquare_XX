"""Track A — U-OUT-01~03 output contract RED skeletons (FR-05)."""

from __future__ import annotations

import pytest

from src.control.solve_use_case import SolveUseCase

# from src.boundary.result_formatter import ResultFormatter


class TestUOutContract:
    """Boundary success output schema (valid input — G1)."""

    def test_u_out_01_success_result_length_is_six(
        self,
    ) -> None:
        """U-OUT-01 — success path returns int[6]."""
        # Given: G1 valid matrix (tests/conftest.py)
        # When: SolveUseCase.execute(matrix) or ResultFormatter.format(domain_result)
        pytest.fail("RED: U-OUT-01 — success result length must be 6")

    def test_u_out_02_success_coords_are_one_indexed_in_one_to_four(
        self,
    ) -> None:
        """U-OUT-02 — r1,c1,r2,c2 each in [1,4] (1-index)."""
        # Given: G1
        # When: execute(matrix) → result[0], result[1], result[3], result[4]
        pytest.fail("RED: U-OUT-02 — coordinates must be 1-index in [1,4]")

    def test_u_out_03_success_result_sequence_r1_c1_n1_r2_c2_n2(
        self,
    ) -> None:
        """U-OUT-03 — output order [r1,c1,n1,r2,c2,n2] per PRD §12.2."""
        # Given: G1; expected [1,1,1,4,4,16] at GREEN
        # When: execute(matrix)
        pytest.fail("RED: U-OUT-03 — result must follow [r1,c1,n1,r2,c2,n2] sequence")
