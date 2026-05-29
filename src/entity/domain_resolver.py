"""Domain resolver entry point (invoked only after Boundary validation passes)."""

from __future__ import annotations

from typing import Any, Protocol


class DomainResolver(Protocol):
    """Resolves a validated puzzle matrix through the Domain pipeline."""

    def resolve(self, grid: list[list[int]]) -> Any:
        """Run Domain logic for a SIZE-validated matrix."""
        ...


class DomainResolverImpl:
    """Default Domain resolver stub for GREEN expansion beyond AC-FR-01-01."""

    def resolve(self, grid: list[list[int]]) -> Any:
        """Placeholder until FR-02~FR-05 Domain pipeline is implemented."""
        raise NotImplementedError("Domain pipeline not implemented")
