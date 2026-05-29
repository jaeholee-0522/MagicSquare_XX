"""Two-cell solver with Attempt 1/2 placement (FR-05)."""

from __future__ import annotations

from src.entity.blank_finder import BlankFinder
from src.entity.domain_errors import DomainErrorResponse
from src.entity.magic_square_validator import MagicSquareValidator
from src.entity.missing_number_finder import MissingNumberFinder

SOLUTION_LENGTH: int = 6


class TwoCellSolver:
    """Places two missing numbers into two blanks using small-first then reverse."""

    def __init__(self) -> None:
        """Wire Domain helpers for blank, missing, and validation steps."""
        self._blank_finder = BlankFinder()
        self._missing_finder = MissingNumberFinder()
        self._validator = MagicSquareValidator()

    def solve(
        self,
        grid: list[list[int]],
    ) -> list[int] | DomainErrorResponse:
        """Run Attempt 1 then Attempt 2; return int[6] or domain failure.

        Args:
            grid: Validated 4x4 matrix with exactly two blank cells.

        Returns:
            One-indexed placement `[r1,c1,n1,r2,c2,n2]` or DomainErrorResponse.
        """
        blank_coords = self._blank_finder.find_blank_coords(grid)
        missing_numbers = self._missing_finder.find_missing(grid)
        smaller, larger = sorted(missing_numbers)

        attempt_one = self._try_placement(grid, blank_coords, smaller, larger)
        if attempt_one is not None:
            return attempt_one

        attempt_two = self._try_placement(grid, blank_coords, larger, smaller)
        if attempt_two is not None:
            return attempt_two

        return DomainErrorResponse.no_valid_placement()

    def _try_placement(
        self,
        grid: list[list[int]],
        blank_coords: list[tuple[int, int]],
        first_number: int,
        second_number: int,
    ) -> list[int] | None:
        """Return formatted success when candidate grid is a magic square."""
        candidate = [row[:] for row in grid]
        first_row, first_col = blank_coords[0]
        second_row, second_col = blank_coords[1]
        candidate[first_row][first_col] = first_number
        candidate[second_row][second_col] = second_number

        if not self._validator.is_magic_square(candidate):
            return None

        return [
            first_row + 1,
            first_col + 1,
            first_number,
            second_row + 1,
            second_col + 1,
            second_number,
        ]
