"""Magic square validation (FR-04)."""

from __future__ import annotations

from src.entity.constants import (
    BLANK_VALUE,
    GRID_SIZE,
    MAGIC_CONSTANT,
    MAX_VALUE,
    MIN_VALUE,
)


class MagicSquareValidator:
    """Validates whether a complete 4x4 grid satisfies magic square invariants."""

    def is_magic_square(self, grid: list[list[int]]) -> bool:
        """Return True when all row, column, and diagonal sums equal MAGIC_CONSTANT.

        Args:
            grid: Complete 4x4 matrix with no blank cells.

        Returns:
            True if the grid is a valid magic square; False otherwise.
        """
        if self._contains_blank_or_out_of_range(grid):
            return False
        if self._has_duplicate_non_zero(grid):
            return False
        if not self._all_rows_sum_to_magic_constant(grid):
            return False
        if not self._all_columns_sum_to_magic_constant(grid):
            return False
        if not self._diagonals_sum_to_magic_constant(grid):
            return False
        return True

    def _contains_blank_or_out_of_range(self, grid: list[list[int]]) -> bool:
        for row in grid:
            for value in row:
                if value == BLANK_VALUE:
                    return True
                if value < MIN_VALUE or value > MAX_VALUE:
                    return True
        return False

    def _has_duplicate_non_zero(self, grid: list[list[int]]) -> bool:
        seen: set[int] = set()
        for row in grid:
            for value in row:
                if value in seen:
                    return True
                seen.add(value)
        return False

    def _all_rows_sum_to_magic_constant(self, grid: list[list[int]]) -> bool:
        return all(sum(row) == MAGIC_CONSTANT for row in grid)

    def _all_columns_sum_to_magic_constant(self, grid: list[list[int]]) -> bool:
        for col_index in range(GRID_SIZE):
            if sum(grid[row_index][col_index] for row_index in range(GRID_SIZE)) != MAGIC_CONSTANT:
                return False
        return True

    def _diagonals_sum_to_magic_constant(self, grid: list[list[int]]) -> bool:
        main_diagonal = sum(grid[index][index] for index in range(GRID_SIZE))
        anti_diagonal = sum(
            grid[index][GRID_SIZE - 1 - index] for index in range(GRID_SIZE)
        )
        return main_diagonal == MAGIC_CONSTANT and anti_diagonal == MAGIC_CONSTANT
