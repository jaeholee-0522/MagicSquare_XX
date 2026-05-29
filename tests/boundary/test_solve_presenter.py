"""SolvePresenter adapter tests (no PyQt display required)."""

from __future__ import annotations

from src.bootstrap import build_solve_presenter
from src.boundary.screen.solve_presenter import ErrorOutcome, SuccessOutcome, SolveResultKind
from tests.conftest import DUPLICATE_GRID, G1, G2, G3, ONE_ZERO_GRID


class TestSolvePresenter:
    """Maps SolveUseCase results to UI outcomes via composition root."""

    def test_presenter_g1_success(self) -> None:
        """G1 returns SuccessOutcome with int[6] placement."""
        presenter = build_solve_presenter()
        outcome = presenter.solve(G1)
        assert isinstance(outcome, SuccessOutcome)
        assert outcome.placement == [1, 1, 1, 4, 4, 16]

    def test_presenter_g2_reverse_success(self) -> None:
        """G2 returns SuccessOutcome from reverse attempt."""
        presenter = build_solve_presenter()
        outcome = presenter.solve(G2)
        assert isinstance(outcome, SuccessOutcome)
        assert outcome.placement == [3, 3, 6, 4, 4, 1]

    def test_presenter_invalid_blank_count(self) -> None:
        """Blank count violation maps to validation ErrorOutcome."""
        presenter = build_solve_presenter()
        outcome = presenter.solve(ONE_ZERO_GRID)
        assert isinstance(outcome, ErrorOutcome)
        assert outcome.kind == SolveResultKind.VALIDATION_ERROR
        assert outcome.code == "INVALID_BLANK_COUNT"

    def test_presenter_duplicate_number(self) -> None:
        """Duplicate non-zero maps to validation ErrorOutcome."""
        presenter = build_solve_presenter()
        outcome = presenter.solve(DUPLICATE_GRID)
        assert isinstance(outcome, ErrorOutcome)
        assert outcome.code == "INVALID_DUPLICATE"

    def test_presenter_no_valid_solution(self) -> None:
        """G3 maps to domain ErrorOutcome."""
        presenter = build_solve_presenter()
        outcome = presenter.solve(G3)
        assert isinstance(outcome, ErrorOutcome)
        assert outcome.kind == SolveResultKind.DOMAIN_ERROR
        assert outcome.code == "DOMAIN-ERR-NO_VALID_PLACEMENT"
