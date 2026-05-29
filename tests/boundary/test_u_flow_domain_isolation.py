"""Track A — U-FLOW-02 flow isolation RED skeletons (BR-05, U-FLOW-02)."""

from __future__ import annotations

import pytest

from src.boundary.boundary_validator import BoundaryValidator
from src.control.solve_use_case import SolveUseCase

# Control mock/spy: DomainResolver.resolve — call_count == 0 on any FR-01 failure.


class TestUFlowDomainIsolation:
    """Invalid input must not invoke Domain resolver (extended beyond SIZE)."""

    def test_u_flow_02_null_grid_resolver_call_count_zero(
        self,
    ) -> None:
        """U-FLOW-02a — matrix=null → resolve/execute 0 calls."""
        # Given: grid = None; SolveUseCase(validator, domain_resolver_mock)
        # When: solve_use_case.execute(None)
        # Then: domain_resolver_mock.resolve.call_count == 0
        pytest.fail("RED: U-FLOW-02 — null input must not call Domain resolver")

    def test_u_flow_02_invalid_size_resolver_call_count_zero(
        self,
    ) -> None:
        """U-FLOW-02b — 3x4 → Domain 0 calls (SIZE short-circuit)."""
        # Given: 3x4 matrix; mock DomainResolver
        # When: SolveUseCase.execute(matrix)
        pytest.fail("RED: U-FLOW-02 — invalid SIZE must not call Domain resolver")

    def test_u_flow_02_invalid_range_resolver_call_count_zero(
        self,
    ) -> None:
        """U-FLOW-02c — value 17 → Domain 0 calls (RANGE violation)."""
        # Given: PRD §16.4 range-invalid matrix
        # When: SolveUseCase.execute(matrix)
        pytest.fail("RED: U-FLOW-02 — UI-ERR-002 path must not call Domain resolver")

    def test_u_flow_02_duplicate_resolver_call_count_zero(
        self,
    ) -> None:
        """U-FLOW-02d — duplicate non-zero → Domain 0 calls."""
        # Given: PRD §16.4 duplicate matrix
        # When: SolveUseCase.execute(matrix)
        pytest.fail("RED: U-FLOW-02 — UI-ERR-004 path must not call Domain resolver")
