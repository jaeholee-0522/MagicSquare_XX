"""Boundary error and validation response contracts."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict

INVALID_SIZE_CODE: Literal["INVALID_SIZE"] = "INVALID_SIZE"
INVALID_SIZE_MESSAGE: str = "Grid must be 4x4."


class ValidationErrorResponse(BaseModel):
    """Structured failure returned when input contract validation fails.

    AC-FR-01-01, PRD §8.1 INVALID_SIZE (maps to PRD §13 UI-ERR-001 at integration).
    """

    model_config = ConfigDict(frozen=True)

    code: Literal["INVALID_SIZE"]
    message: str

    @classmethod
    def invalid_size(cls) -> ValidationErrorResponse:
        """Build the canonical SIZE violation response."""
        return cls(code=INVALID_SIZE_CODE, message=INVALID_SIZE_MESSAGE)
