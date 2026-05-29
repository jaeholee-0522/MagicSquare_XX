"""Missing number discovery (FR-03)."""

from __future__ import annotations

from src.entity.constants import BLANK_VALUE, GRID_SIZE, MAX_VALUE, MIN_VALUE


class MissingNumberFinder:
    """Finds numbers from MIN_VALUE..MAX_VALUE absent from the grid."""

    def find_missing(self, grid: list[list[int]]) -> list[int]:
        """Return missing values in ascending order.

        Args:
            grid: 4x4 matrix with blank cells marked as BLANK_VALUE.

        Returns:
            Sorted list of values in [MIN_VALUE, MAX_VALUE] not present as non-zero.
        """
        present = {
            grid[row_index][col_index]
            for row_index in range(GRID_SIZE)
            for col_index in range(GRID_SIZE)
            if grid[row_index][col_index] != BLANK_VALUE
        }
        return [
            value
            for value in range(MIN_VALUE, MAX_VALUE + 1)
            if value not in present
        ]
