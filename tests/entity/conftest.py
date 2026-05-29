"""Entity-layer fixtures (Track B — Domain Mock forbidden)."""

from __future__ import annotations

import pytest


@pytest.fixture
def g0_row_sum_broken(g0_matrix: list[list[int]]) -> list[list[int]]:
    """G0 with one row sum altered — not a magic square."""
    matrix = [row[:] for row in g0_matrix]
    matrix[0][0] = 1
    return matrix


@pytest.fixture
def g0_col_sum_broken(g0_matrix: list[list[int]]) -> list[list[int]]:
    """G0 with one column sum altered."""
    matrix = [row[:] for row in g0_matrix]
    matrix[0][0] = 1
    matrix[1][0] = 20
    return matrix


@pytest.fixture
def g0_diagonal_broken(g0_matrix: list[list[int]]) -> list[list[int]]:
    """G0 with main diagonal sum broken."""
    matrix = [row[:] for row in g0_matrix]
    matrix[0][0] = 1
    return matrix


@pytest.fixture
def g0_with_duplicate(g0_matrix: list[list[int]]) -> list[list[int]]:
    """G0 with duplicate non-zero values."""
    matrix = [row[:] for row in g0_matrix]
    matrix[1][1] = matrix[0][0]
    return matrix


@pytest.fixture
def g0_with_zero_cell(g0_matrix: list[list[int]]) -> list[list[int]]:
    """Complete G0 grid with one cell set to 0."""
    matrix = [row[:] for row in g0_matrix]
    matrix[2][2] = 0
    return matrix
