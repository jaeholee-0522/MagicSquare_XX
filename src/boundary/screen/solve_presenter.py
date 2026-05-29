"""Thin adapter between PyQt screen and SolveUseCase (Control layer)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Literal

from src.boundary.boundary_validator import BoundaryValidator
from src.boundary.contracts import ValidationErrorResponse
from src.control.solve_use_case import SolveUseCase
from src.entity.domain_errors import DomainErrorResponse
from src.entity.domain_resolver import DomainResolverImpl


class SolveResultKind(str, Enum):
    """Discriminator for solve outcomes presented to the UI."""

    SUCCESS = "success"
    VALIDATION_ERROR = "validation_error"
    DOMAIN_ERROR = "domain_error"


@dataclass(frozen=True)
class SuccessOutcome:
    """Successful placement returned as int[6] = [r1, c1, n1, r2, c2, n2]."""

    kind: Literal[SolveResultKind.SUCCESS]
    placement: list[int]


@dataclass(frozen=True)
class ErrorOutcome:
    """Structured boundary or domain failure for display."""

    kind: Literal[SolveResultKind.VALIDATION_ERROR, SolveResultKind.DOMAIN_ERROR]
    code: str
    message: str


SolveOutcome = SuccessOutcome | ErrorOutcome


class SolvePresenter:
    """Wires SolveUseCase and maps responses to UI-friendly outcomes."""

    def __init__(self, use_case: SolveUseCase | None = None) -> None:
        """Create presenter with optional injected use case (for testing)."""
        if use_case is None:
            use_case = SolveUseCase(
                validator=BoundaryValidator(),
                domain_resolver=DomainResolverImpl(),
            )
        self._use_case = use_case

    def solve(self, grid: list[list[int]]) -> SolveOutcome:
        """Run solve flow and normalize Control/Domain responses.

        Args:
            grid: 4x4 matrix from the UI grid editor.

        Returns:
            SuccessOutcome with placement, or ErrorOutcome with code/message.
        """
        result = self._use_case.execute(grid)
        if isinstance(result, ValidationErrorResponse):
            return ErrorOutcome(
                kind=SolveResultKind.VALIDATION_ERROR,
                code=result.code,
                message=result.message,
            )
        if isinstance(result, DomainErrorResponse):
            return ErrorOutcome(
                kind=SolveResultKind.DOMAIN_ERROR,
                code=result.code,
                message=result.message,
            )
        return SuccessOutcome(
            kind=SolveResultKind.SUCCESS,
            placement=list(result),
        )
