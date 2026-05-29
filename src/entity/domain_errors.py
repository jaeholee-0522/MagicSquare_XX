"""Domain-layer structured failure responses (re-exported from shared contracts)."""

from __future__ import annotations

from src.contracts.domain_errors import (
    NO_VALID_PLACEMENT_CODE,
    NO_VALID_PLACEMENT_MESSAGE,
    DomainErrorCode,
    DomainErrorResponse,
)

__all__ = [
    "NO_VALID_PLACEMENT_CODE",
    "NO_VALID_PLACEMENT_MESSAGE",
    "DomainErrorCode",
    "DomainErrorResponse",
]
