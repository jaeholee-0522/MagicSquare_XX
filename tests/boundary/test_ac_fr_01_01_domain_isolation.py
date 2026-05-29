"""AC-FR-01-01 Domain resolver isolation tests — PRD §8.1 INVALID_SIZE."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from src.boundary.contracts import INVALID_SIZE_CODE
from src.control.solve_use_case import SolveUseCase

AC_ID = "AC-FR-01-01"
DOC = f"{AC_ID}, PRD §8.1 INVALID_SIZE"


class TestAcFr0101DomainIsolation:
    """SIZE failure must not invoke Domain resolve()."""

    def test_null_grid_resolve_call_count_is_zero(
        self,
        null_grid: None,
        solve_use_case: SolveUseCase,
        domain_resolver_mock: MagicMock,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — None grid never calls resolve()."""
        # Given
        grid = null_grid

        # When
        solve_use_case.execute(grid)

        # Then
        assert domain_resolver_mock.resolve.call_count == 0  # AC-FR-01-01

    def test_null_grid_resolve_assert_not_called(
        self,
        null_grid: None,
        solve_use_case: SolveUseCase,
        domain_resolver_mock: MagicMock,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — spy: resolve not invoked."""
        # Given
        grid = null_grid

        # When
        solve_use_case.execute(grid)

        # Then
        domain_resolver_mock.resolve.assert_not_called()  # AC-FR-01-01

    def test_empty_list_resolve_call_count_is_zero(
        self,
        empty_grid: list,
        solve_use_case: SolveUseCase,
        domain_resolver_mock: MagicMock,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — empty grid blocks Domain."""
        # Given
        grid = empty_grid

        # When
        solve_use_case.execute(grid)

        # Then
        assert domain_resolver_mock.resolve.call_count == 0  # AC-FR-01-01

    def test_four_empty_rows_resolve_call_count_is_zero(
        self,
        four_rows_zero_columns_grid: list,
        solve_use_case: SolveUseCase,
        domain_resolver_mock: MagicMock,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — [[]]*4 blocks Domain."""
        # Given
        grid = four_rows_zero_columns_grid

        # When
        solve_use_case.execute(grid)

        # Then
        assert domain_resolver_mock.resolve.call_count == 0  # AC-FR-01-01

    def test_three_by_four_resolve_call_count_is_zero(
        self,
        three_by_four_grid: list[list[int]],
        solve_use_case: SolveUseCase,
        domain_resolver_mock: MagicMock,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — 3x4 blocks Domain."""
        # Given
        grid = three_by_four_grid

        # When
        solve_use_case.execute(grid)

        # Then
        assert domain_resolver_mock.resolve.call_count == 0  # AC-FR-01-01

    def test_null_grid_returns_invalid_size_before_any_resolve(
        self,
        null_grid: None,
        solve_use_case: SolveUseCase,
        domain_resolver_mock: MagicMock,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — error returned with zero Domain calls."""
        # Given
        grid = null_grid

        # When
        result = solve_use_case.execute(grid)

        # Then
        assert result.code == INVALID_SIZE_CODE  # AC-FR-01-01
        assert domain_resolver_mock.resolve.call_count == 0
