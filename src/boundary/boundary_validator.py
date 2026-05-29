"""Boundary input validation (FR-01)."""

from __future__ import annotations

from typing import Any

from src.boundary.contracts import ValidationErrorResponse
from src.entity.constants import GRID_SIZE


class BoundaryValidator:
    """Validates input contract before Domain invocation (FR-01).

    Validation order: SIZE → RANGE → ZERO COUNT → DUPLICATE (SIZE only in this slice).
    """

    def validate(self, grid: Any) -> ValidationErrorResponse | None:
        """Return SIZE failure response or None when SIZE contract passes.

        Args:
            grid: Candidate 4x4 int matrix.

        Returns:
            ValidationErrorResponse when SIZE is violated; None otherwise.
        """
        if self._is_size_invalid(grid):
            return ValidationErrorResponse.invalid_size()
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
