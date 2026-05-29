"""AC-FR-01-01 boundary-value SIZE tests — PRD §8.1 INVALID_SIZE."""

from __future__ import annotations

import pytest

from src.boundary.boundary_validator import BoundaryValidator
from src.boundary.contracts import INVALID_SIZE_CODE, INVALID_SIZE_MESSAGE
from src.control.solve_use_case import SolveUseCase

AC_ID = "AC-FR-01-01"
DOC = f"{AC_ID}, PRD §8.1 INVALID_SIZE"


class TestAcFr0101BoundaryValues:
    """Non-4x4 and degenerate matrix shapes fail SIZE check first."""

    def test_empty_list_returns_invalid_size_code(
        self,
        empty_grid: list,
        boundary_validator: BoundaryValidator,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — zero rows → INVALID_SIZE."""
        # Given
        grid = empty_grid

        # When
        result = boundary_validator.validate(grid)

        # Then
        assert result is not None
        assert result.code == INVALID_SIZE_CODE  # AC-FR-01-01

    def test_empty_list_returns_grid_must_be_4x4_message(
        self,
        empty_grid: list,
        boundary_validator: BoundaryValidator,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — empty list message contract."""
        # Given
        grid = empty_grid

        # When
        result = boundary_validator.validate(grid)

        # Then
        assert result is not None
        assert result.message == INVALID_SIZE_MESSAGE  # AC-FR-01-01

    def test_four_empty_rows_returns_invalid_size_code(
        self,
        four_rows_zero_columns_grid: list,
        boundary_validator: BoundaryValidator,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — four rows with zero columns."""
        # Given
        grid = four_rows_zero_columns_grid

        # When
        result = boundary_validator.validate(grid)

        # Then
        assert result is not None
        assert result.code == INVALID_SIZE_CODE  # AC-FR-01-01

    def test_three_by_four_grid_returns_invalid_size_code(
        self,
        three_by_four_grid: list[list[int]],
        boundary_validator: BoundaryValidator,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — three rows is not 4x4."""
        # Given
        grid = three_by_four_grid

        # When
        result = boundary_validator.validate(grid)

        # Then
        assert result is not None
        assert result.code == INVALID_SIZE_CODE  # AC-FR-01-01

    def test_three_by_four_grid_via_use_case_returns_failure(
        self,
        three_by_four_grid: list[list[int]],
        solve_use_case: SolveUseCase,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — 3x4 blocked at Boundary."""
        # Given
        grid = three_by_four_grid

        # When
        result = solve_use_case.execute(grid)

        # Then
        assert result is not None
        assert result.code == INVALID_SIZE_CODE  # AC-FR-01-01
        assert result.message == INVALID_SIZE_MESSAGE

    def test_single_row_grid_returns_invalid_size_code(
        self,
        boundary_validator: BoundaryValidator,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — one row is not 4x4."""
        # Given
        grid = [[1, 2, 3, 4]]

        # When
        result = boundary_validator.validate(grid)

        # Then
        assert result is not None
        assert result.code == INVALID_SIZE_CODE  # AC-FR-01-01
