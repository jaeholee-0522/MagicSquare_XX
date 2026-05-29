"""Track B — D-VAL-01~06 magic square validation Full RED (FR-04)."""

from __future__ import annotations

import pytest

# Domain Mock forbidden. G0~G3: tests/conftest.py.


class TestDValMagicSquare:
    """is_magic_square / MagicSquareValidator — I1~I5."""

    def test_d_val_01_g0_complete_grid_returns_true(
        self,
        g0_matrix: list[list[int]],
    ) -> None:
        """D-VAL-01 — G0 complete magic square → True."""
        from src.entity.magic_square_validator import MagicSquareValidator

        # Given
        grid = g0_matrix
        validator = MagicSquareValidator()

        # When
        result = validator.is_magic_square(grid)

        # Then
        assert result is True

    def test_d_val_02_row_sum_mismatch_returns_false(
        self,
        g0_row_sum_broken: list[list[int]],
    ) -> None:
        """D-VAL-02 — one row sum ≠ 34 → False (I1)."""
        from src.entity.magic_square_validator import MagicSquareValidator

        # Given
        grid = g0_row_sum_broken
        validator = MagicSquareValidator()

        # When
        result = validator.is_magic_square(grid)

        # Then
        assert result is False

    def test_d_val_03_col_sum_mismatch_returns_false(
        self,
        g0_col_sum_broken: list[list[int]],
    ) -> None:
        """D-VAL-03 — one column sum ≠ 34 → False (I2)."""
        from src.entity.magic_square_validator import MagicSquareValidator

        # Given
        grid = g0_col_sum_broken
        validator = MagicSquareValidator()

        # When
        result = validator.is_magic_square(grid)

        # Then
        assert result is False

    def test_d_val_04_diagonal_sum_mismatch_returns_false(
        self,
        g0_diagonal_broken: list[list[int]],
    ) -> None:
        """D-VAL-04 — diagonal sum ≠ 34 → False (I3)."""
        from src.entity.magic_square_validator import MagicSquareValidator

        # Given
        grid = g0_diagonal_broken
        validator = MagicSquareValidator()

        # When
        result = validator.is_magic_square(grid)

        # Then
        assert result is False

    def test_d_val_05_duplicate_in_one_to_sixteen_returns_false(
        self,
        g0_with_duplicate: list[list[int]],
    ) -> None:
        """D-VAL-05 — duplicate 1~16 → False (I4)."""
        from src.entity.magic_square_validator import MagicSquareValidator

        # Given
        grid = g0_with_duplicate
        validator = MagicSquareValidator()

        # When
        result = validator.is_magic_square(grid)

        # Then
        assert result is False

    def test_d_val_06_contains_zero_returns_false(
        self,
        g0_with_zero_cell: list[list[int]],
    ) -> None:
        """D-VAL-06 — complete grid containing 0 → False (I4)."""
        from src.entity.magic_square_validator import MagicSquareValidator

        # Given
        grid = g0_with_zero_cell
        validator = MagicSquareValidator()

        # When
        result = validator.is_magic_square(grid)

        # Then
        assert result is False
