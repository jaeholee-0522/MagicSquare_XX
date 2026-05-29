"""Shared fixtures for AC-FR-01-01 Boundary SIZE validation tests."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from src.boundary.boundary_validator import BoundaryValidator
from src.boundary.contracts import INVALID_SIZE_CODE, INVALID_SIZE_MESSAGE
from src.control.solve_use_case import SolveUseCase
from src.entity.domain_resolver import DomainResolver

# PRD §12.1 SIZE contract; anchor message per test_plan / README (maps to PRD §13 UI-ERR-001).
PRD_SECTION = "§8.1"
AC_ID = "AC-FR-01-01"


@pytest.fixture
def null_grid() -> None:
    """Explicit None matrix input."""
    return None


@pytest.fixture
def empty_grid() -> list:
    """Zero-row matrix."""
    return []


@pytest.fixture
def four_rows_zero_columns_grid() -> list:
    """Four rows with empty column lists."""
    return [[]] * 4


@pytest.fixture
def three_by_four_grid() -> list[list[int]]:
    """Three rows by four columns — row count violation."""
    return [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
    ]


@pytest.fixture
def domain_resolver_mock() -> MagicMock:
    """Stand-in for Domain resolver; must not be called on SIZE failure."""
    resolver = MagicMock(spec=DomainResolver)
    resolver.resolve = MagicMock(name="resolve")
    return resolver


@pytest.fixture
def boundary_validator() -> BoundaryValidator:
    """Boundary validator under test."""
    return BoundaryValidator()


@pytest.fixture
def solve_use_case(
    boundary_validator: BoundaryValidator,
    domain_resolver_mock: MagicMock,
) -> SolveUseCase:
    """Control orchestrator wiring Boundary validation to Domain resolver."""
    return SolveUseCase(
        validator=boundary_validator,
        domain_resolver=domain_resolver_mock,
    )
