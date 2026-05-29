"""Track A — U-IN-04~08 input validation RED skeletons (FR-01).

U-IN-01~03 covered by tests/boundary/test_ac_fr_01_01_*.py (Report/08).
PRD §12.1 order: SIZE → RANGE → ZERO → DUPLICATE.
"""

from __future__ import annotations

import pytest

from src.boundary.boundary_validator import BoundaryValidator

# Future contract name per Report/09; GREEN may alias InputValidator → BoundaryValidator.
# from src.boundary.input_validator import InputValidator


class TestUInValidation:
    """Boundary input validation beyond SIZE (AC-FR01-03~05)."""

    def test_u_in_04_zero_blank_count_returns_ui_err_003(
        self,
    ) -> None:
        """U-IN-04 — 4x4 with zero blanks → UI-ERR-003, Domain 0 calls."""
        # Given: G0-like full grid (no zeros) — see tests/conftest.py G0 comment
        # When: validator = BoundaryValidator(); validator.validate(matrix)
        pytest.fail("RED: U-IN-04 — zero blank count → UI-ERR-003, resolver not invoked")

    def test_u_in_05_three_blanks_returns_ui_err_003(
        self,
    ) -> None:
        """U-IN-05 — PRD §16.4 one-zero matrix (3 effective blanks policy) → UI-ERR-003."""
        # Given: 4x4 with single 0 (PRD invalid blank count example)
        # When: BoundaryValidator.validate(matrix)
        pytest.fail("RED: U-IN-05 — blank count ≠ 2 → UI-ERR-003, resolver not invoked")

    def test_u_in_06_value_minus_one_returns_ui_err_002(
        self,
    ) -> None:
        """U-IN-06 — value -1 → UI-ERR-002 (RANGE before ZERO when size valid)."""
        # Given: valid 4x4 with one cell -1
        # When: BoundaryValidator.validate(matrix)
        pytest.fail("RED: U-IN-06 — value out of range (-1) → UI-ERR-002")

    def test_u_in_07_value_seventeen_returns_ui_err_002(
        self,
    ) -> None:
        """U-IN-07 — PRD §16.4 grid with 17 → UI-ERR-002."""
        # Given: PRD §16.4 invalid range (17) matrix
        # When: BoundaryValidator.validate(matrix)
        pytest.fail("RED: U-IN-07 — value 17 → UI-ERR-002")

    def test_u_in_08_duplicate_nonzero_returns_ui_err_004(
        self,
    ) -> None:
        """U-IN-08 — duplicate non-zero → UI-ERR-004."""
        # Given: PRD §16.4 duplicate matrix (two 5s)
        # When: BoundaryValidator.validate(matrix)
        pytest.fail("RED: U-IN-08 — duplicate non-zero → UI-ERR-004")
