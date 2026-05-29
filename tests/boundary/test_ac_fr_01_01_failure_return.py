"""AC-FR-01-01 failure-return contract tests — PRD §8.1 INVALID_SIZE."""

from __future__ import annotations

import pytest

from src.boundary.boundary_validator import BoundaryValidator
from src.boundary.contracts import (
    INVALID_SIZE_CODE,
    INVALID_SIZE_MESSAGE,
    ValidationErrorResponse,
)
from src.control.solve_use_case import SolveUseCase

AC_ID = "AC-FR-01-01"
DOC = f"{AC_ID}, PRD §8.1 INVALID_SIZE"


class TestAcFr0101FailureReturn:
    """Structured failure when SIZE contract is violated."""

    def test_null_grid_returns_validation_error_response(
        self,
        null_grid: None,
        boundary_validator: BoundaryValidator,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — null grid returns failure envelope."""
        # Given
        grid = null_grid

        # When
        result = boundary_validator.validate(grid)

        # Then
        assert isinstance(result, ValidationErrorResponse)

    def test_null_grid_returns_invalid_size_code(
        self,
        null_grid: None,
        boundary_validator: BoundaryValidator,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — failure code is INVALID_SIZE."""
        # Given
        grid = null_grid

        # When
        result = boundary_validator.validate(grid)

        # Then
        assert result is not None
        assert result.code == INVALID_SIZE_CODE  # AC-FR-01-01

    def test_null_grid_returns_grid_must_be_4x4_message(
        self,
        null_grid: None,
        boundary_validator: BoundaryValidator,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — canonical SIZE message."""
        # Given
        grid = null_grid

        # When
        result = boundary_validator.validate(grid)

        # Then
        assert result is not None
        assert result.message == INVALID_SIZE_MESSAGE  # AC-FR-01-01

    def test_null_grid_via_use_case_returns_failure_not_success(
        self,
        null_grid: None,
        solve_use_case: SolveUseCase,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — orchestration returns error envelope."""
        # Given
        grid = null_grid

        # When
        result = solve_use_case.execute(grid)

        # Then
        assert isinstance(result, ValidationErrorResponse)  # AC-FR-01-01

    def test_null_grid_failure_has_exactly_code_and_message_fields(
        self,
        null_grid: None,
        boundary_validator: BoundaryValidator,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — failure schema exposes code and message."""
        # Given
        grid = null_grid

        # When
        result = boundary_validator.validate(grid)

        # Then
        assert result is not None
        assert result.model_dump() == {
            "code": INVALID_SIZE_CODE,
            "message": INVALID_SIZE_MESSAGE,
        }  # AC-FR-01-01

    def test_null_grid_validate_does_not_return_none(
        self,
        null_grid: None,
        boundary_validator: BoundaryValidator,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — SIZE violation is never silent pass."""
        # Given
        grid = null_grid

        # When
        result = boundary_validator.validate(grid)

        # Then
        assert result is not None  # AC-FR-01-01
