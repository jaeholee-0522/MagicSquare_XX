"""AC-FR-01-01 message identity tests — PRD §8.1 INVALID_SIZE."""

from __future__ import annotations

import pytest

from src.boundary.boundary_validator import BoundaryValidator
from src.boundary.contracts import INVALID_SIZE_CODE, INVALID_SIZE_MESSAGE
from src.control.solve_use_case import SolveUseCase

AC_ID = "AC-FR-01-01"
# Canonical SIZE message (test_plan anchor; PRD §13 UI-ERR-001 template maps at integration).
PRD_SIZE_MESSAGE = "Grid must be 4x4."
DOC = f"{AC_ID}, PRD §8.1 INVALID_SIZE"


class TestAcFr0101MessageIdentity:
    """Exact string equality for INVALID_SIZE message."""

    def test_null_grid_message_equals_prd_size_literal(
        self,
        null_grid: None,
        boundary_validator: BoundaryValidator,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — character-level message match."""
        # Given
        grid = null_grid
        expected = PRD_SIZE_MESSAGE

        # When
        result = boundary_validator.validate(grid)

        # Then
        assert result is not None
        assert result.message == expected  # AC-FR-01-01
        assert result.message == INVALID_SIZE_MESSAGE

    def test_null_grid_message_length_matches_literal(
        self,
        null_grid: None,
        boundary_validator: BoundaryValidator,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — no truncated or padded message."""
        # Given
        grid = null_grid

        # When
        result = boundary_validator.validate(grid)

        # Then
        assert result is not None
        assert len(result.message) == len(PRD_SIZE_MESSAGE)  # AC-FR-01-01

    def test_empty_list_message_is_byte_identical_to_constant(
        self,
        empty_grid: list,
        boundary_validator: BoundaryValidator,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — empty grid uses same message."""
        # Given
        grid = empty_grid

        # When
        result = boundary_validator.validate(grid)

        # Then
        assert result is not None
        assert list(result.message) == list(PRD_SIZE_MESSAGE)  # AC-FR-01-01

    def test_three_by_four_message_does_not_differ_by_case(
        self,
        three_by_four_grid: list[list[int]],
        boundary_validator: BoundaryValidator,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — case-sensitive equality."""
        # Given
        grid = three_by_four_grid

        # When
        result = boundary_validator.validate(grid)

        # Then
        assert result is not None
        assert result.message == PRD_SIZE_MESSAGE  # AC-FR-01-01
        assert result.message != PRD_SIZE_MESSAGE.upper()

    def test_null_grid_repeated_runs_same_message(
        self,
        null_grid: None,
        boundary_validator: BoundaryValidator,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — deterministic message (NFR-03)."""
        # Given
        grid = null_grid

        # When
        first = boundary_validator.validate(grid)
        second = boundary_validator.validate(grid)

        # Then
        assert first is not None and second is not None
        assert first.message == second.message == PRD_SIZE_MESSAGE  # AC-FR-01-01

    def test_null_grid_code_and_message_pair_is_fixed(
        self,
        null_grid: None,
        solve_use_case: SolveUseCase,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — code/message tuple invariant."""
        # Given
        grid = null_grid

        # When
        result = solve_use_case.execute(grid)

        # Then
        assert (result.code, result.message) == (
            INVALID_SIZE_CODE,
            PRD_SIZE_MESSAGE,
        )  # AC-FR-01-01
