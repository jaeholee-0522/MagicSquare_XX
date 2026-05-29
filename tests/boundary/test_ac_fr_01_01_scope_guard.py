"""AC-FR-01-01 scope guard tests — PRD §8.1 INVALID_SIZE."""

from __future__ import annotations

from pathlib import Path

import pytest

AC_ID = "AC-FR-01-01"
DOC = f"{AC_ID}, PRD §8.1 INVALID_SIZE"

_BOUNDARY_TEST_DIR = Path(__file__).parent
_AC_FR_01_01_MODULES = (
    "test_ac_fr_01_01_failure_return.py",
    "test_ac_fr_01_01_boundary_values.py",
    "test_ac_fr_01_01_domain_isolation.py",
    "test_ac_fr_01_01_message_identity.py",
)

# Out of scope for this RED commit (AC-FR-01-02~05, FR-02~05).
_FORBIDDEN_ASSERT_CODES = (
    "UI-ERR-002",
    "UI-ERR-003",
    "UI-ERR-004",
    "INVALID_RANGE",
    "INVALID_BLANK_COUNT",
    "INVALID_DUPLICATE",
    "DOMAIN-ERR-NO_VALID_PLACEMENT",
)

_FORBIDDEN_DOMAIN_IMPORTS = (
    "BlankFinder",
    "MissingNumberFinder",
    "MagicSquareValidator",
    "Solver",
)

# Valid 4x4 with two blanks (FR-02~05 territory) — must not appear as test input.
_VALID_4X4_MARKER = "[0, 0,"


class TestAcFr0101ScopeGuard:
    """Ensure this RED slice stays within AC-FR-01-01 SIZE only."""

    def test_scope_module_names_target_ac_fr_01_01_only(self) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — suite files are AC-FR-01-01 prefixed."""
        # Given
        names = {p.name for p in _BOUNDARY_TEST_DIR.glob("test_ac_fr_01_01_*.py")}

        # When / Then
        assert "test_ac_fr_01_01_failure_return.py" in names  # AC-FR-01-01
        assert "test_ac_fr_01_01_boundary_values.py" in names

    def test_scope_no_out_of_scope_error_codes_in_ac_fr_01_01_sources(self) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — AC-FR-01-02~05 codes not asserted here."""
        # Given
        sources = "".join(
            (_BOUNDARY_TEST_DIR / name).read_text(encoding="utf-8")
            for name in _AC_FR_01_01_MODULES
        )

        # When / Then
        for forbidden in _FORBIDDEN_ASSERT_CODES:
            assert forbidden not in sources  # AC-FR-01-01

    def test_scope_no_domain_component_imports_in_ac_fr_01_01_sources(self) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — FR-02~05 Domain types not imported."""
        # Given
        sources = "".join(
            (_BOUNDARY_TEST_DIR / name).read_text(encoding="utf-8")
            for name in _AC_FR_01_01_MODULES
        )

        # When / Then
        for symbol in _FORBIDDEN_DOMAIN_IMPORTS:
            assert symbol not in sources  # AC-FR-01-01

    def test_scope_no_valid_4x4_two_blank_fixture_in_ac_fr_01_01_sources(self) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — valid 4x4 success path excluded."""
        # Given
        sources = "".join(
            (_BOUNDARY_TEST_DIR / name).read_text(encoding="utf-8")
            for name in _AC_FR_01_01_MODULES
        )

        # When / Then
        assert _VALID_4X4_MARKER not in sources  # AC-FR-01-01

    def test_scope_conftest_does_not_define_four_by_three_fixture(self) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — AC-FR-01-02 (4x3) deferred to later suite."""
        # Given
        conftest_source = (_BOUNDARY_TEST_DIR / "conftest.py").read_text(encoding="utf-8")

        # When / Then
        assert "four_by_three" not in conftest_source  # AC-FR-01-01

    def test_scope_boundary_values_exclude_range_violation_seventeen(self) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — value 17 (AC-FR-01-03) not in this slice."""
        # Given
        sources = "".join(
            (_BOUNDARY_TEST_DIR / name).read_text(encoding="utf-8")
            for name in _AC_FR_01_01_MODULES
        )

        # When / Then
        assert ", 17," not in sources  # AC-FR-01-01
        assert ", 17]" not in sources
