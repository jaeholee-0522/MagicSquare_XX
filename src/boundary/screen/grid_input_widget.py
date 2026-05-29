"""4x4 grid editor widget for Magic Square input."""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QGridLayout,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from src.contracts.grid_constants import BLANK_VALUE, GRID_SIZE, MAX_VALUE

_DEFAULT_STYLE = ""
_HIGHLIGHT_STYLE = (
    "QSpinBox { background-color: #d4edda; border: 2px solid #28a745; "
    "font-weight: bold; }"
)
_ERROR_STYLE = (
    "QSpinBox { background-color: #f8d7da; border: 2px solid #dc3545; }"
)


class GridInputWidget(QWidget):
    """Editable 4x4 integer grid; 0 denotes a blank cell."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """Build spin boxes for each cell in a GRID_SIZE x GRID_SIZE layout."""
        super().__init__(parent)
        self._cells: list[list[QSpinBox]] = []
        self._build_ui()

    def _build_ui(self) -> None:
        """Lay out spin boxes with row/column headers."""
        outer = QVBoxLayout(self)
        grid = QGridLayout()
        grid.setSpacing(6)

        for col in range(GRID_SIZE):
            grid.addWidget(
                self._make_header_label(str(col + 1)),
                0,
                col + 1,
                alignment=Qt.AlignmentFlag.AlignCenter,
            )

        for row in range(GRID_SIZE):
            grid.addWidget(
                self._make_header_label(str(row + 1)),
                row + 1,
                0,
                alignment=Qt.AlignmentFlag.AlignCenter,
            )
            row_cells: list[QSpinBox] = []
            for col in range(GRID_SIZE):
                spin = QSpinBox()
                spin.setRange(BLANK_VALUE, MAX_VALUE)
                spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
                spin.setMinimumWidth(52)
                spin.setSpecialValueText("·")
                spin.valueChanged.connect(self._on_cell_changed)
                grid.addWidget(spin, row + 1, col + 1)
                row_cells.append(spin)
            self._cells.append(row_cells)

        outer.addLayout(grid)

    @staticmethod
    def _make_header_label(text: str) -> QWidget:
        """Create a centered header label for row/column indices."""
        from PyQt6.QtWidgets import QLabel

        label = QLabel(text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-weight: bold; color: #555;")
        return label

    def get_grid(self) -> list[list[int]]:
        """Read current cell values as a 4x4 matrix."""
        return [[cell.value() for cell in row] for row in self._cells]

    def set_grid(self, matrix: list[list[int]]) -> None:
        """Populate cells from a matrix; resets highlight styling."""
        for row_idx, row in enumerate(matrix):
            for col_idx, value in enumerate(row):
                self._cells[row_idx][col_idx].setValue(value)
        self.clear_highlight()

    def clear_all(self) -> None:
        """Reset every cell to blank (0)."""
        for row in self._cells:
            for cell in row:
                cell.setValue(BLANK_VALUE)
        self.clear_highlight()

    def clear_highlight(self) -> None:
        """Remove success/error cell styling."""
        for row in self._cells:
            for cell in row:
                cell.setStyleSheet(_DEFAULT_STYLE)

    def highlight_placements(
        self,
        placement: list[int],
        *,
        is_error: bool = False,
    ) -> None:
        """Highlight cells referenced in [r1,c1,n1,r2,c2,n2] (1-indexed).

        Args:
            placement: Solver output coordinates and values.
            is_error: When True, apply error styling instead of success.
        """
        self.clear_highlight()
        style = _ERROR_STYLE if is_error else _HIGHLIGHT_STYLE
        r1, c1, _n1, r2, c2, _n2 = placement
        for row, col in ((r1 - 1, c1 - 1), (r2 - 1, c2 - 1)):
            self._cells[row][col].setStyleSheet(style)

    def apply_solution(self, placement: list[int]) -> None:
        """Write solved values into blank cells and highlight them."""
        r1, c1, n1, r2, c2, n2 = placement
        self._cells[r1 - 1][c1 - 1].setValue(n1)
        self._cells[r2 - 1][c2 - 1].setValue(n2)
        self.highlight_placements(placement)

    def _on_cell_changed(self, _value: int) -> None:
        """Clear highlight when the user edits a cell."""
        sender = self.sender()
        if isinstance(sender, QSpinBox) and sender.styleSheet():
            sender.setStyleSheet(_DEFAULT_STYLE)
