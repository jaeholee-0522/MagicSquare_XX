"""Track A — U-IN-04~08 input validation Full RED (FR-01).

U-IN-01~03 covered by tests/boundary/test_ac_fr_01_01_*.py (Report/09).
PRD §12.1 order: SIZE → RANGE → ZERO → DUPLICATE.
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from src.boundary.boundary_validator import BoundaryValidator
from src.boundary.contracts import (
    INVALID_BLANK_COUNT_CODE,
    INVALID_BLANK_COUNT_MESSAGE,
    INVALID_DUPLICATE_CODE,
    INVALID_DUPLICATE_MESSAGE,
    INVALID_RANGE_CODE,
    INVALID_RANGE_MESSAGE,
    ValidationErrorResponse,
)
from src.control.solve_use_case import SolveUseCase

AC_ID = "AC-FR-01-04"
DOC = f"{AC_ID}, PRD §8.1 UI-ERR-003"


class TestUInBlankCountValidation:
    """AC-FR-01-04 — zero count must be exactly 2."""

    def test_u_in_04_zero_blank_count_returns_invalid_blank_count_code(
        self,
        zero_blank_count_grid: list[list[int]],
        boundary_validator: BoundaryValidator,
    ) -> None:
        """U-IN-04 — 4x4 with zero blanks → INVALID_BLANK_COUNT."""
        # Given
        grid = zero_blank_count_grid

        # When
        result = boundary_validator.validate(grid)

        # Then
        assert result is not None
        assert result.code == INVALID_BLANK_COUNT_CODE

    def test_u_in_04_zero_blank_count_domain_not_called(
        self,
        zero_blank_count_grid: list[list[int]],
        solve_use_case: SolveUseCase,
        domain_resolver_mock: MagicMock,
    ) -> None:
        """U-IN-04 — zero blanks blocks Domain resolver."""
        # Given
        grid = zero_blank_count_grid

        # When
        result = solve_use_case.execute(grid)

        # Then
        assert isinstance(result, ValidationErrorResponse)
        assert result.code == INVALID_BLANK_COUNT_CODE
        assert domain_resolver_mock.resolve.call_count == 0

    def test_u_in_05_three_blanks_returns_invalid_blank_count_code(
        self,
        three_blank_grid: list[list[int]],
        boundary_validator: BoundaryValidator,
    ) -> None:
        """U-IN-05 — three zeros → INVALID_BLANK_COUNT."""
        # Given
        grid = three_blank_grid

        # When
        result = boundary_validator.validate(grid)

        # Then
        assert result is not None
        assert result.code == INVALID_BLANK_COUNT_CODE
        assert result.message == INVALID_BLANK_COUNT_MESSAGE

    def test_u_in_05_one_zero_grid_returns_invalid_blank_count_code(
        self,
        one_zero_grid: list[list[int]],
        boundary_validator: BoundaryValidator,
    ) -> None:
        """U-IN-05 — PRD §16.4 one-zero matrix → INVALID_BLANK_COUNT."""
        # Given
        grid = one_zero_grid

        # When
        result = boundary_validator.validate(grid)

        # Then
        assert result is not None
        assert result.code == INVALID_BLANK_COUNT_CODE


class TestUInRangeValidation:
    """AC-FR-01-03 — values must be 0 or 1~16."""

    def test_u_in_06_value_minus_one_returns_invalid_range_code(
        self,
        range_minus_one_grid: list[list[int]],
        boundary_validator: BoundaryValidator,
    ) -> None:
        """U-IN-06 — value -1 → INVALID_RANGE."""
        # Given
        grid = range_minus_one_grid

        # When
        result = boundary_validator.validate(grid)

        # Then
        assert result is not None
        assert result.code == INVALID_RANGE_CODE
        assert result.message == INVALID_RANGE_MESSAGE

    def test_u_in_07_value_seventeen_returns_invalid_range_code(
        self,
        range_seventeen_grid: list[list[int]],
        boundary_validator: BoundaryValidator,
    ) -> None:
        """U-IN-07 — PRD §16.4 grid with 17 → INVALID_RANGE."""
        # Given
        grid = range_seventeen_grid

        # When
        result = boundary_validator.validate(grid)

        # Then
        assert result is not None
        assert result.code == INVALID_RANGE_CODE


class TestUInDuplicateValidation:
    """AC-FR-01-05 — duplicate non-zero values forbidden."""

    def test_u_in_08_duplicate_nonzero_returns_invalid_duplicate_code(
        self,
        duplicate_nonzero_grid: list[list[int]],
        boundary_validator: BoundaryValidator,
    ) -> None:
        """U-IN-08 — duplicate non-zero → INVALID_DUPLICATE."""
        # Given
        grid = duplicate_nonzero_grid

        # When
        result = boundary_validator.validate(grid)

        # Then
        assert result is not None
        assert result.code == INVALID_DUPLICATE_CODE
        assert result.message == INVALID_DUPLICATE_MESSAGE

    def test_u_in_08_duplicate_nonzero_domain_not_called(
        self,
        duplicate_nonzero_grid: list[list[int]],
        solve_use_case: SolveUseCase,
        domain_resolver_mock: MagicMock,
    ) -> None:
        """U-IN-08 — duplicate blocks Domain resolver."""
        # Given
        grid = duplicate_nonzero_grid

        # When
        result = solve_use_case.execute(grid)

        # Then
        assert result.code == INVALID_DUPLICATE_CODE
        assert domain_resolver_mock.resolve.call_count == 0
