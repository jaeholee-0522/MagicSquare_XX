"""Solve use case — validates input then delegates to Domain."""

from __future__ import annotations

from typing import Any

from src.control.ports import InputValidator, SolveResult
from src.entity.domain_resolver import DomainResolver


class SolveUseCase:
    """Orchestrates FR-01 validation and Domain resolution (Control layer)."""

    def __init__(
        self,
        validator: InputValidator,
        domain_resolver: DomainResolver,
    ) -> None:
        """Wire input validator port and Domain resolver."""
        self._validator = validator
        self._domain_resolver = domain_resolver

    def execute(self, grid: Any) -> SolveResult:
        """Validate input; on Boundary failure return error without calling Domain.

        Args:
            grid: Raw matrix input from caller.

        Returns:
            ValidationErrorResponse on Boundary failure; Domain result on success.
        """
        validation_error = self._validator.validate(grid)
        if validation_error is not None:
            return validation_error
        return self._domain_resolver.resolve(grid)
