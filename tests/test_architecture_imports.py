"""Architecture import guard — ECB dependency direction."""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"


def _module_paths(layer: str) -> list[Path]:
    """List Python files under src/<layer>/."""
    layer_root = SRC_ROOT / layer
    return sorted(path for path in layer_root.rglob("*.py") if path.name != "__init__.py")


def test_entity_does_not_import_boundary_or_control() -> None:
    """Entity layer must remain independent of outer layers."""
    forbidden = ("from src.boundary", "import src.boundary", "from src.control", "import src.control")
    for path in _module_paths("entity"):
        source = path.read_text(encoding="utf-8")
        for token in forbidden:
            assert token not in source, f"{path.relative_to(PROJECT_ROOT)} imports outer layer via {token}"


def test_control_does_not_import_boundary() -> None:
    """Control layer must not depend on Boundary implementations."""
    forbidden = ("from src.boundary", "import src.boundary")
    for path in _module_paths("control"):
        source = path.read_text(encoding="utf-8")
        for token in forbidden:
            assert token not in source, f"{path.relative_to(PROJECT_ROOT)} must not import boundary"


def test_boundary_does_not_import_entity() -> None:
    """Boundary layer must not depend on Entity internals."""
    forbidden = ("from src.entity", "import src.entity")
    for path in _module_paths("boundary"):
        source = path.read_text(encoding="utf-8")
        for token in forbidden:
            assert token not in source, f"{path.relative_to(PROJECT_ROOT)} must not import entity"
