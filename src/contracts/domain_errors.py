"""Domain structured failure contracts (solver / placement errors)."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict

NO_VALID_PLACEMENT_CODE: Literal["DOMAIN-ERR-NO_VALID_PLACEMENT"] = (
    "DOMAIN-ERR-NO_VALID_PLACEMENT"
)
NO_VALID_PLACEMENT_MESSAGE: str = (
    "No valid placement for the two missing numbers."
)

DomainErrorCode = Literal["DOMAIN-ERR-NO_VALID_PLACEMENT"]


class DomainErrorResponse(BaseModel):
    """Structured failure returned when Domain logic cannot produce a solution."""

    model_config = ConfigDict(frozen=True)

    code: DomainErrorCode
    message: str

    @classmethod
    def no_valid_placement(cls) -> DomainErrorResponse:
        """Build the canonical both-attempts-failed response."""
        return cls(code=NO_VALID_PLACEMENT_CODE, message=NO_VALID_PLACEMENT_MESSAGE)
