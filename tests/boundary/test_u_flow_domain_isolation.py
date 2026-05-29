"""Track A — U-FLOW-02 flow isolation Full RED (BR-05)."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from src.boundary.contracts import (
    INVALID_DUPLICATE_CODE,
    INVALID_RANGE_CODE,
    INVALID_SIZE_CODE,
)
from src.control.solve_use_case import SolveUseCase

AC_ID = "AC-FR-01-01"
DOC = f"{AC_ID}, BR-05 Domain isolation"


class TestUFlowDomainIsolation:
    """Invalid input must not invoke Domain resolver (extended beyond SIZE)."""

    def test_u_flow_02_null_grid_resolver_call_count_zero(
        self,
        null_grid: None,
        solve_use_case: SolveUseCase,
        domain_resolver_mock: MagicMock,
    ) -> None:
        """U-FLOW-02a — matrix=null → resolve 0 calls."""
        # Given
        grid = null_grid

        # When
        result = solve_use_case.execute(grid)

        # Then
        assert result.code == INVALID_SIZE_CODE
        assert domain_resolver_mock.resolve.call_count == 0

    def test_u_flow_02_invalid_size_resolver_call_count_zero(
        self,
        three_by_four_grid: list[list[int]],
        solve_use_case: SolveUseCase,
        domain_resolver_mock: MagicMock,
    ) -> None:
        """U-FLOW-02b — 3x4 → Domain 0 calls (SIZE short-circuit)."""
        # Given
        grid = three_by_four_grid

        # When
        solve_use_case.execute(grid)

        # Then
        assert domain_resolver_mock.resolve.call_count == 0

    def test_u_flow_02_invalid_range_resolver_call_count_zero(
        self,
        range_seventeen_grid: list[list[int]],
        solve_use_case: SolveUseCase,
        domain_resolver_mock: MagicMock,
    ) -> None:
        """U-FLOW-02c — value 17 → Domain 0 calls (RANGE violation)."""
        # Given
        grid = range_seventeen_grid

        # When
        result = solve_use_case.execute(grid)

        # Then
        assert result.code == INVALID_RANGE_CODE
        assert domain_resolver_mock.resolve.call_count == 0

    def test_u_flow_02_duplicate_resolver_call_count_zero(
        self,
        duplicate_nonzero_grid: list[list[int]],
        solve_use_case: SolveUseCase,
        domain_resolver_mock: MagicMock,
    ) -> None:
        """U-FLOW-02d — duplicate non-zero → Domain 0 calls."""
        # Given
        grid = duplicate_nonzero_grid

        # When
        result = solve_use_case.execute(grid)

        # Then
        assert result.code == INVALID_DUPLICATE_CODE
        assert domain_resolver_mock.resolve.call_count == 0
