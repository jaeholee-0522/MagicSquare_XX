"""GUI smoke tests — verify screen layer imports without launching a display."""

from __future__ import annotations

import pytest

pytest.importorskip("PyQt6")


def test_main_window_imports() -> None:
    """MainWindow module is importable after GUI source restore."""
    from src.boundary.screen.main_window import MainWindow

    assert MainWindow is not None


def test_solve_presenter_imports() -> None:
    """SolvePresenter is importable and accepts an injected use case."""
    from src.bootstrap import build_solve_presenter
    from src.boundary.screen.solve_presenter import SolvePresenter

    presenter = build_solve_presenter()
    assert isinstance(presenter, SolvePresenter)
