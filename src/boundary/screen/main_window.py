"""Main application window for the Magic Square 4x4 solver."""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.bootstrap import build_solve_presenter
from src.boundary.screen.grid_input_widget import GridInputWidget
from src.boundary.screen.sample_puzzles import SAMPLE_PUZZLES
from src.boundary.screen.solve_presenter import (
    ErrorOutcome,
    SolvePresenter,
    SolveResultKind,
    SuccessOutcome,
)
from src.contracts.grid_constants import MAGIC_CONSTANT, REQUIRED_BLANK_COUNT


class MainWindow(QMainWindow):
    """Primary GUI: grid editor, sample loader, and solve action."""

    def __init__(self, presenter: SolvePresenter | None = None) -> None:
        """Initialize window with optional presenter injection."""
        super().__init__()
        self._presenter = presenter or build_solve_presenter()
        self._grid = GridInputWidget()
        self._result_label = QLabel()
        self._result_label.setWordWrap(True)
        self._result_label.setTextFormat(Qt.TextFormat.RichText)
        self._result_label.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft,
        )
        self._build_ui()
        self._set_idle_message()

    def _build_ui(self) -> None:
        """Assemble title, instructions, grid, controls, and result panel."""
        self.setWindowTitle("Magic Square 4×4 Solver")
        self.setMinimumSize(480, 520)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("4×4 Magic Square Solver")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        hint = QLabel(
            f"Enter values 1–16 with exactly {REQUIRED_BLANK_COUNT} blanks (0). "
            f"All rows, columns, and diagonals must sum to {MAGIC_CONSTANT}."
        )
        hint.setWordWrap(True)
        hint.setStyleSheet("color: #444;")
        layout.addWidget(hint)

        layout.addWidget(self._grid, alignment=Qt.AlignmentFlag.AlignCenter)

        controls = QHBoxLayout()
        self._sample_combo = QComboBox()
        self._sample_combo.addItem("Load sample…")
        for name in SAMPLE_PUZZLES:
            self._sample_combo.addItem(name)
        self._sample_combo.currentIndexChanged.connect(self._on_sample_selected)

        solve_btn = QPushButton("Solve")
        solve_btn.setDefault(True)
        solve_btn.clicked.connect(self._on_solve)

        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(self._on_clear)

        controls.addWidget(self._sample_combo)
        controls.addStretch()
        controls.addWidget(clear_btn)
        controls.addWidget(solve_btn)
        layout.addLayout(controls)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(separator)

        result_title = QLabel("Result")
        result_title.setStyleSheet("font-weight: bold;")
        layout.addWidget(result_title)
        layout.addWidget(self._result_label)

    def _set_idle_message(self) -> None:
        """Show neutral prompt before the user runs solve."""
        self._result_label.setStyleSheet("color: #666; padding: 8px;")
        self._result_label.setText("Enter a puzzle and click <b>Solve</b>.")

    def _on_sample_selected(self, index: int) -> None:
        """Load a demo puzzle when the user picks from the combo box."""
        if index <= 0:
            return
        name = self._sample_combo.itemText(index)
        puzzle = SAMPLE_PUZZLES.get(name)
        if puzzle is not None:
            self._grid.set_grid([row[:] for row in puzzle])
            self._set_idle_message()
        self._sample_combo.setCurrentIndex(0)

    def _on_clear(self) -> None:
        """Reset grid and result panel."""
        self._grid.clear_all()
        self._set_idle_message()

    def _on_solve(self) -> None:
        """Collect grid, invoke use case, and render outcome."""
        grid = self._grid.get_grid()
        outcome = self._presenter.solve(grid)
        if isinstance(outcome, SuccessOutcome):
            self._show_success(outcome)
        elif isinstance(outcome, ErrorOutcome):
            self._show_error(outcome)

    def _show_success(self, outcome: SuccessOutcome) -> None:
        """Display placement details and update the grid."""
        placement = outcome.placement
        r1, c1, n1, r2, c2, n2 = placement
        self._grid.apply_solution(placement)
        self._result_label.setStyleSheet(
            "background-color: #d4edda; color: #155724; "
            "border: 1px solid #c3e6cb; border-radius: 4px; padding: 10px;"
        )
        self._result_label.setText(
            "<b>Solution found</b><br>"
            f"Cell ({r1}, {c1}) ← <b>{n1}</b><br>"
            f"Cell ({r2}, {c2}) ← <b>{n2}</b><br>"
            f"<span style='color:#555;'>Output: [{', '.join(map(str, placement))}]</span>"
        )

    def _show_error(self, outcome: ErrorOutcome) -> None:
        """Display boundary or domain error without mutating solved cells."""
        self._grid.clear_highlight()
        if outcome.kind == SolveResultKind.VALIDATION_ERROR:
            title = "Input validation failed"
            bg = "#fff3cd"
            fg = "#856404"
            border = "#ffeeba"
        else:
            title = "No valid solution"
            bg = "#f8d7da"
            fg = "#721c24"
            border = "#f5c6cb"

        self._result_label.setStyleSheet(
            f"background-color: {bg}; color: {fg}; "
            f"border: 1px solid {border}; border-radius: 4px; padding: 10px;"
        )
        self._result_label.setText(
            f"<b>{title}</b><br>"
            f"Code: <code>{outcome.code}</code><br>"
            f"{outcome.message}"
        )

        if outcome.kind == SolveResultKind.VALIDATION_ERROR:
            QMessageBox.warning(
                self,
                title,
                f"{outcome.code}\n\n{outcome.message}",
            )
