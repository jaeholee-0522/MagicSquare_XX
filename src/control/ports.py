"""Control-layer ports (protocols) for dependency inversion."""

from __future__ import annotations

from typing import Any, Protocol

from src.contracts.domain_errors import DomainErrorResponse
from src.contracts.validation_errors import ValidationErrorResponse

SolveResult = ValidationErrorResponse | DomainErrorResponse | list[int]


class InputValidator(Protocol):
    """Port for FR-01 input validation invoked before Domain resolution."""

    def validate(self, grid: Any) -> ValidationErrorResponse | None:
        """Return validation failure response or None when FR-01 contract passes."""
        ...
