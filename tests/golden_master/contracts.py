"""Golden Master contract assertions for Magic Square Solver output."""

from __future__ import annotations

from typing import Any

from src.boundary.contracts import (
    INVALID_BLANK_COUNT_CODE,
    INVALID_DUPLICATE_CODE,
    ValidationErrorResponse,
)
from src.entity.blank_finder import BlankFinder
from src.entity.domain_errors import (
    NO_VALID_PLACEMENT_CODE,
    DomainErrorResponse,
)
from src.entity.missing_number_finder import MissingNumberFinder
from src.entity.solver import SOLUTION_LENGTH
from tests.golden_master.scenarios import GoldenMasterScenario


def assert_int_six_output(result: list[int]) -> None:
    """Verify success output is int[6] with 1-index coordinates in [1, 4]."""
    assert isinstance(result, list)
    assert len(result) == SOLUTION_LENGTH
    assert all(isinstance(value, int) for value in result)

    row_one, col_one, number_one, row_two, col_two, number_two = result
    for coordinate in (row_one, col_one, row_two, col_two):
        assert 1 <= coordinate <= 4
    assert isinstance(number_one, int)
    assert isinstance(number_two, int)


def assert_row_major_and_one_index(
    grid: list[list[int]],
    result: list[int],
) -> None:
    """Verify blank placement follows row-major discovery with 1-index coords."""
    blank_coords = BlankFinder().find_blank_coords(grid)
    row_one, col_one, _, row_two, col_two, _ = result

    assert (row_one - 1, col_one - 1) == blank_coords[0]
    assert (row_two - 1, col_two - 1) == blank_coords[1]


def assert_small_first_placement(grid: list[list[int]], result: list[int]) -> None:
    """Verify Attempt 1 places the smaller missing number in the first blank."""
    missing_numbers = MissingNumberFinder().find_missing(grid)
    smaller, _larger = sorted(missing_numbers)
    _row_one, _col_one, number_one, _row_two, _col_two, _number_two = result
    assert number_one == smaller


def assert_reverse_fallback_placement(
    grid: list[list[int]],
    result: list[int],
) -> None:
    """Verify Attempt 2 places the larger missing number in the first blank."""
    missing_numbers = MissingNumberFinder().find_missing(grid)
    _smaller, larger = sorted(missing_numbers)
    _row_one, _col_one, number_one, _row_two, _col_two, _number_two = result
    assert number_one == larger


def assert_boundary_error_contract(
    result: Any,
    *,
    expected_code: str,
) -> None:
    """Verify Boundary Error Contract exposes code and message only."""
    assert isinstance(result, ValidationErrorResponse)
    assert result.code == expected_code
    assert result.model_dump().keys() == {"code", "message"}


def assert_domain_error_contract(result: Any) -> None:
    """Verify Domain Error Contract for no valid placement."""
    assert isinstance(result, DomainErrorResponse)
    assert result.code == NO_VALID_PLACEMENT_CODE
    assert result.model_dump().keys() == {"code", "message"}


def assert_scenario_contract(scenario: GoldenMasterScenario, result: Any) -> None:
    """Apply contract checks appropriate to the GM-2 scenario kind."""
    if scenario.expects_success:
        assert isinstance(result, list)
        assert_int_six_output(result)
        assert_row_major_and_one_index(scenario.grid, result)
        if scenario.uses_small_first:
            assert_small_first_placement(scenario.grid, result)
        if scenario.uses_reverse_fallback:
            assert_reverse_fallback_placement(scenario.grid, result)
        return

    if scenario.expected_error_code == INVALID_BLANK_COUNT_CODE:
        assert_boundary_error_contract(result, expected_code=INVALID_BLANK_COUNT_CODE)
        return

    if scenario.expected_error_code == INVALID_DUPLICATE_CODE:
        assert_boundary_error_contract(result, expected_code=INVALID_DUPLICATE_CODE)
        return

    if scenario.expected_error_code == NO_VALID_PLACEMENT_CODE:
        assert_domain_error_contract(result)
        return

    raise ValueError(f"Unhandled scenario contract: {scenario.test_case_id}")
