"""Structured validation failure contracts (FR-01 input verification)."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict

INVALID_SIZE_CODE: Literal["INVALID_SIZE"] = "INVALID_SIZE"
INVALID_SIZE_MESSAGE: str = "Grid must be 4x4."

INVALID_BLANK_COUNT_CODE: Literal["INVALID_BLANK_COUNT"] = "INVALID_BLANK_COUNT"
INVALID_BLANK_COUNT_MESSAGE: str = "Blank count must be exactly 2."

INVALID_RANGE_CODE: Literal["INVALID_RANGE"] = "INVALID_RANGE"
INVALID_RANGE_MESSAGE: str = "Value must be 0 or 1-16."

INVALID_DUPLICATE_CODE: Literal["INVALID_DUPLICATE"] = "INVALID_DUPLICATE"
INVALID_DUPLICATE_MESSAGE: str = "Duplicate non-zero values are not allowed."

ValidationErrorCode = Literal[
    "INVALID_SIZE",
    "INVALID_BLANK_COUNT",
    "INVALID_RANGE",
    "INVALID_DUPLICATE",
]


class ValidationErrorResponse(BaseModel):
    """Structured failure returned when input contract validation fails.

    AC-FR-01-01~05; implementation aliases map to PRD §13 UI-ERR-* at integration.
    """

    model_config = ConfigDict(frozen=True)

    code: ValidationErrorCode
    message: str

    @classmethod
    def invalid_size(cls) -> ValidationErrorResponse:
        """Build the canonical SIZE violation response."""
        return cls(code=INVALID_SIZE_CODE, message=INVALID_SIZE_MESSAGE)

    @classmethod
    def invalid_blank_count(cls) -> ValidationErrorResponse:
        """Build the canonical blank-count violation response."""
        return cls(code=INVALID_BLANK_COUNT_CODE, message=INVALID_BLANK_COUNT_MESSAGE)

    @classmethod
    def invalid_range(cls) -> ValidationErrorResponse:
        """Build the canonical value-range violation response."""
        return cls(code=INVALID_RANGE_CODE, message=INVALID_RANGE_MESSAGE)

    @classmethod
    def invalid_duplicate(cls) -> ValidationErrorResponse:
        """Build the canonical duplicate violation response."""
        return cls(code=INVALID_DUPLICATE_CODE, message=INVALID_DUPLICATE_MESSAGE)
