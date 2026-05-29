"""Application composition root — wires Boundary, Control, and Entity."""

from __future__ import annotations

from src.boundary.boundary_validator import BoundaryValidator
from src.boundary.screen.solve_presenter import SolvePresenter
from src.control.solve_use_case import SolveUseCase
from src.entity.domain_resolver import DomainResolverImpl


def build_solve_use_case() -> SolveUseCase:
    """Create the default SolveUseCase with Boundary validation and Domain resolver."""
    return SolveUseCase(
        validator=BoundaryValidator(),
        domain_resolver=DomainResolverImpl(),
    )


def build_solve_presenter() -> SolvePresenter:
    """Create the GUI presenter backed by the default SolveUseCase."""
    return SolvePresenter(use_case=build_solve_use_case())
