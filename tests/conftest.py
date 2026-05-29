"""Shared fixture placeholders for Dual-Track RED (G0~G3).

Report/09 — matrices are fixed in RED phase; uncomment when implementing GREEN.
"""

from __future__ import annotations

# G0 — complete 4x4 magic square (all rows/cols/diags sum 34, no zeros)
# G0 = [
#     [16, 3, 2, 13],
#     [5, 10, 11, 8],
#     [9, 6, 7, 12],
#     [4, 15, 14, 1],
# ]

# G1 — PRD §16.4 Matrix A (small-first success); blanks 0-index (0,0), (3,3)
# G1 = [
#     [0, 15, 14, 4],
#     [12, 6, 7, 9],
#     [8, 10, 11, 5],
#     [13, 3, 2, 0],
# ]
# Expected solution (1-index): [1, 1, 1, 4, 4, 16]

# G2 — PRD §16.4 Matrix B (reverse success); blanks 0-index (2,2), (3,3) — TBD for D-SOL-02
# G2 = [
#     [16, 2, 3, 13],
#     [5, 11, 10, 8],
#     [9, 7, 0, 12],
#     [4, 14, 15, 0],
# ]
# Expected solution (1-index): [3, 3, 6, 4, 4, 1]

# G3 — both Attempt 1/2 fail; fixture to be fixed at RED-DOM-SOL-003 / DN-03
# G3 = None  # placeholder
