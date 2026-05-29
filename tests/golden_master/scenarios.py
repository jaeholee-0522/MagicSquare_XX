"""GM-2 scenario definitions and SolveUseCase output serialization."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from src.boundary.boundary_validator import BoundaryValidator
from src.boundary.contracts import (
    INVALID_BLANK_COUNT_CODE,
    INVALID_DUPLICATE_CODE,
    ValidationErrorResponse,
)
from src.control.solve_use_case import SolveUseCase
from src.entity.domain_errors import (
    NO_VALID_PLACEMENT_CODE,
    DomainErrorResponse,
)
from src.entity.domain_resolver import DomainResolverImpl
from tests.conftest import (
    DUPLICATE_GRID,
    G1,
    G2,
    G3,
    ONE_ZERO_GRID,
)

SECTION_SEPARATOR = "________________________________________"


@dataclass(frozen=True)
class GoldenMasterScenario:
    """One GM-2 input scenario with traceable test-case and section identifiers."""

    test_case_id: str
    section_id: str
    grid: list[list[int]]
    expects_success: bool = False
    uses_small_first: bool = False
    uses_reverse_fallback: bool = False
    expected_error_code: str | None = None


GM2_SCENARIOS: tuple[GoldenMasterScenario, ...] = (
    GoldenMasterScenario(
        test_case_id="GM-TC-01",
        section_id="normal_success",
        grid=G1,
        expects_success=True,
        uses_small_first=True,
    ),
    GoldenMasterScenario(
        test_case_id="GM-TC-02",
        section_id="reverse_success",
        grid=G2,
        expects_success=True,
        uses_reverse_fallback=True,
    ),
    GoldenMasterScenario(
        test_case_id="GM-TC-03",
        section_id="invalid_blank_count",
        grid=ONE_ZERO_GRID,
        expected_error_code=INVALID_BLANK_COUNT_CODE,
    ),
    GoldenMasterScenario(
        test_case_id="GM-TC-04",
        section_id="duplicate_number",
        grid=DUPLICATE_GRID,
        expected_error_code=INVALID_DUPLICATE_CODE,
    ),
    GoldenMasterScenario(
        test_case_id="GM-TC-05",
        section_id="no_valid_solution",
        grid=G3,
        expected_error_code=NO_VALID_PLACEMENT_CODE,
    ),
)

# Backward-compatible alias used by the baseline generator.
GM1_SCENARIOS = GM2_SCENARIOS


def format_grid(grid: list[list[int]]) -> str:
    """Render a 4x4 matrix as four space-separated rows."""
    return "\n".join(" ".join(str(value) for value in row) for row in grid)


def serialize_result(result: Any) -> str:
    """Serialize SolveUseCase result to Golden Master Output/Error block."""
    if isinstance(result, ValidationErrorResponse | DomainErrorResponse):
        return f"Error:\n{result.code}"
    if isinstance(result, list):
        return f"Output:\n{result}"
    raise TypeError(f"Unsupported result type for Golden Master: {type(result)!r}")


def format_section(scenario: GoldenMasterScenario, result: Any) -> str:
    """Format one scenario block for the expected snapshot file."""
    return (
        f"[{scenario.section_id}]\n"
        f"Input:\n{format_grid(scenario.grid)}\n"
        f"{serialize_result(result)}"
    )


def capture_api_result(
    scenario: GoldenMasterScenario,
    use_case: SolveUseCase | None = None,
) -> Any:
    """Capture raw SolveUseCase result for contract assertions."""
    solver = use_case or SolveUseCase(
        validator=BoundaryValidator(),
        domain_resolver=DomainResolverImpl(),
    )
    return solver.execute(scenario.grid)


def capture_scenario(
    scenario: GoldenMasterScenario,
    use_case: SolveUseCase | None = None,
) -> str:
    """Run one scenario through SolveUseCase and return its formatted block."""
    solver = use_case or SolveUseCase(
        validator=BoundaryValidator(),
        domain_resolver=DomainResolverImpl(),
    )
    result = solver.execute(scenario.grid)
    return format_section(scenario, result)


def build_golden_master_document(
    scenarios: tuple[GoldenMasterScenario, ...] = GM2_SCENARIOS,
    use_case: SolveUseCase | None = None,
) -> str:
    """Build the full GM-2 baseline document from live solver output."""
    sections = [capture_scenario(scenario, use_case) for scenario in scenarios]
    return f"\n{SECTION_SEPARATOR}\n".join(sections) + "\n"
