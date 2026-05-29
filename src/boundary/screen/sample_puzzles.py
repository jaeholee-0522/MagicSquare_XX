"""Sample puzzle grids for GUI demo (PRD §16.4 G1/G2)."""

from __future__ import annotations

G1: list[list[int]] = [
    [0, 15, 14, 4],
    [12, 6, 7, 9],
    [8, 10, 11, 5],
    [13, 3, 2, 0],
]

G2: list[list[int]] = [
    [16, 2, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 0, 12],
    [4, 14, 15, 0],
]

SAMPLE_PUZZLES: dict[str, list[list[int]]] = {
    "G1 (Attempt 1)": G1,
    "G2 (Attempt 2)": G2,
}
