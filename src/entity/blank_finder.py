"""Blank coordinate discovery (FR-02)."""

from __future__ import annotations

from src.entity.constants import BLANK_VALUE, GRID_SIZE


class BlankFinder:
    """Finds zero-cell coordinates in row-major order."""

    def find_blank_coords(self, grid: list[list[int]]) -> list[tuple[int, int]]:
        """Return 0-index coordinates of blank cells in row-major order.

        Args:
            grid: 4x4 matrix containing exactly two blank cells.

        Returns:
            List of (row, col) tuples for each blank cell.
        """
        coords: list[tuple[int, int]] = []
        for row_index in range(GRID_SIZE):
            for col_index in range(GRID_SIZE):
                if grid[row_index][col_index] == BLANK_VALUE:
                    coords.append((row_index, col_index))
        return coords
