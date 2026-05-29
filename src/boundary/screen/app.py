"""PyQt application entry point for Magic Square GUI."""

from __future__ import annotations

import sys

from PyQt6.QtWidgets import QApplication

from src.boundary.screen.main_window import MainWindow


def main() -> int:
    """Launch the Magic Square 4x4 GUI.

    Returns:
        Process exit code from the Qt event loop.
    """
    app = QApplication(sys.argv)
    app.setApplicationName("Magic Square 4x4")
    app.setOrganizationName("MagicSquare")
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
