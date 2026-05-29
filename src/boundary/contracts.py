"""Boundary re-exports of shared validation contracts (backward compatibility)."""

from __future__ import annotations

from src.contracts.validation_errors import (
    INVALID_BLANK_COUNT_CODE,
    INVALID_BLANK_COUNT_MESSAGE,
    INVALID_DUPLICATE_CODE,
    INVALID_DUPLICATE_MESSAGE,
    INVALID_RANGE_CODE,
    INVALID_RANGE_MESSAGE,
    INVALID_SIZE_CODE,
    INVALID_SIZE_MESSAGE,
    ValidationErrorCode,
    ValidationErrorResponse,
)

__all__ = [
    "INVALID_BLANK_COUNT_CODE",
    "INVALID_BLANK_COUNT_MESSAGE",
    "INVALID_DUPLICATE_CODE",
    "INVALID_DUPLICATE_MESSAGE",
    "INVALID_RANGE_CODE",
    "INVALID_RANGE_MESSAGE",
    "INVALID_SIZE_CODE",
    "INVALID_SIZE_MESSAGE",
    "ValidationErrorCode",
    "ValidationErrorResponse",
]
