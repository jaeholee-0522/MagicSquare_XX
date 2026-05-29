"""Shared fixtures for Dual-Track RED/GREEN (G0~G3, PRD §16.4)."""

from __future__ import annotations

import pytest

# G0 — complete 4x4 magic square (all rows/cols/diags sum 34, no zeros)
G0: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]

# G1 — PRD §16.4 Matrix A (small-first success); blanks 0-index (0,0), (3,3)
G1: list[list[int]] = [
    [0, 15, 14, 4],
    [12, 6, 7, 9],
    [8, 10, 11, 5],
    [13, 3, 2, 0],
]
G1_EXPECTED_SOLUTION: list[int] = [1, 1, 1, 4, 4, 16]

# G2 — PRD §16.4 Matrix B (reverse success); blanks 0-index (2,2), (3,3)
G2: list[list[int]] = [
    [16, 2, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 0, 12],
    [4, 14, 15, 0],
]
G2_EXPECTED_SOLUTION: list[int] = [3, 3, 6, 4, 4, 1]

# G3 — both Attempt 1/2 fail (DN-03 placeholder; verify at GREEN)
G3: list[list[int]] = [
    [0, 2, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 6, 12],
    [4, 14, 0, 1],
]

# PRD §16.4 invalid blank count (one zero)
ONE_ZERO_GRID: list[list[int]] = [
    [16, 2, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 6, 12],
    [4, 14, 15, 0],
]

# PRD §16.4 invalid blank count (three zeros)
THREE_ZERO_GRID: list[list[int]] = [
    [0, 15, 14, 4],
    [12, 6, 7, 9],
    [8, 10, 11, 5],
    [13, 3, 0, 0],
]

# PRD §16.4 invalid range (17)
RANGE_SEVENTEEN_GRID: list[list[int]] = [
    [16, 2, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 17, 12],
    [4, 14, 15, 0],
]

# PRD §16.4 duplicate non-zero
DUPLICATE_GRID: list[list[int]] = [
    [16, 2, 3, 13],
    [5, 5, 10, 8],
    [9, 7, 6, 12],
    [4, 14, 15, 1],
]

# Valid 4x4 with one out-of-range value (-1)
RANGE_MINUS_ONE_GRID: list[list[int]] = [
    [0, 15, 14, 4],
    [12, 6, 7, 9],
    [8, 10, 11, 5],
    [13, 3, -1, 2],
]


def _deep_copy(matrix: list[list[int]]) -> list[list[int]]:
    return [row[:] for row in matrix]


@pytest.fixture
def g0_matrix() -> list[list[int]]:
    """G0 — complete magic square."""
    return _deep_copy(G0)


@pytest.fixture
def g1_matrix() -> list[list[int]]:
    """G1 — Matrix A (PRD §16.4)."""
    return _deep_copy(G1)


@pytest.fixture
def g2_matrix() -> list[list[int]]:
    """G2 — Matrix B (PRD §16.4)."""
    return _deep_copy(G2)


@pytest.fixture
def g3_matrix() -> list[list[int]]:
    """G3 — both-fail placeholder (DN-03)."""
    return _deep_copy(G3)


@pytest.fixture
def zero_blank_count_grid(g0_matrix: list[list[int]]) -> list[list[int]]:
    """4x4 with zero blanks (G0 — no zeros)."""
    return g0_matrix


@pytest.fixture
def three_blank_grid() -> list[list[int]]:
    """4x4 with three zeros."""
    return _deep_copy(THREE_ZERO_GRID)


@pytest.fixture
def one_zero_grid() -> list[list[int]]:
    """4x4 with one zero (PRD §16.4)."""
    return _deep_copy(ONE_ZERO_GRID)


@pytest.fixture
def range_seventeen_grid() -> list[list[int]]:
    """4x4 with value 17 (PRD §16.4)."""
    return _deep_copy(RANGE_SEVENTEEN_GRID)


@pytest.fixture
def range_minus_one_grid() -> list[list[int]]:
    """4x4 with value -1."""
    return _deep_copy(RANGE_MINUS_ONE_GRID)


@pytest.fixture
def duplicate_nonzero_grid() -> list[list[int]]:
    """4x4 with duplicate non-zero (PRD §16.4)."""
    return _deep_copy(DUPLICATE_GRID)
