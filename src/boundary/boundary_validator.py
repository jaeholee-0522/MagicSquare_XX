"""Boundary input validation (FR-01)."""

from __future__ import annotations

from typing import Any

from src.boundary.contracts import ValidationErrorResponse
from src.entity.constants import (
    BLANK_VALUE,
    GRID_SIZE,
    MAX_VALUE,
    MIN_VALUE,
    REQUIRED_BLANK_COUNT,
)


class BoundaryValidator:
    """Validates input contract before Domain invocation (FR-01).

    Validation order: SIZE → RANGE → ZERO COUNT → DUPLICATE.
    """

    def validate(self, grid: Any) -> ValidationErrorResponse | None:
        """Return validation failure response or None when FR-01 contract passes.

        Args:
            grid: Candidate 4x4 int matrix.

        Returns:
            ValidationErrorResponse when a contract is violated; None otherwise.
        """
        if self._is_size_invalid(grid):
            return ValidationErrorResponse.invalid_size()
        if self._is_range_invalid(grid):
            return ValidationErrorResponse.invalid_range()
        if self._is_blank_count_invalid(grid):
            return ValidationErrorResponse.invalid_blank_count()
        if self._is_duplicate_invalid(grid):
            return ValidationErrorResponse.invalid_duplicate()
        return None

    def _is_size_invalid(self, grid: Any) -> bool:
        """Return True when matrix is not 4 rows x 4 columns."""
        if grid is None:
            return True
        if not isinstance(grid, list):
            return True
        if len(grid) != GRID_SIZE:
            return True
        for row in grid:
            if not isinstance(row, list):
                return True
            if len(row) != GRID_SIZE:
                return True
        return False

    def _is_range_invalid(self, grid: list) -> bool:
        """Return True when any cell is outside {0} union [MIN_VALUE, MAX_VALUE]."""
        for row in grid:
            for value in row:
                if value == BLANK_VALUE:
                    continue
                if value < MIN_VALUE or value > MAX_VALUE:
                    return True
        return False

    def _is_blank_count_invalid(self, grid: list) -> bool:
        """Return True when zero-cell count is not exactly REQUIRED_BLANK_COUNT."""
        blank_count = 0
        for row in grid:
            for value in row:
                if value == BLANK_VALUE:
                    blank_count += 1
        return blank_count != REQUIRED_BLANK_COUNT

    def _is_duplicate_invalid(self, grid: list) -> bool:
        """Return True when any non-zero value appears more than once."""
        seen: set[int] = set()
        for row in grid:
            for value in row:
                if value == BLANK_VALUE:
                    continue
                if value in seen:
                    return True
                seen.add(value)
        return False
