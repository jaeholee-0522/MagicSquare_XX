"""Approve-pattern utilities for Golden Master regression tests."""

from __future__ import annotations

import difflib
from pathlib import Path

from tests.golden_master.scenarios import SECTION_SEPARATOR


def unified_diff(
    expected: str,
    actual: str,
    *,
    fromfile: str,
    tofile: str,
) -> str:
    """Return a unified diff between expected and actual Golden Master text."""
    expected_lines = expected.splitlines(keepends=True)
    actual_lines = actual.splitlines(keepends=True)
    diff_lines = difflib.unified_diff(
        expected_lines,
        actual_lines,
        fromfile=fromfile,
        tofile=tofile,
        lineterm="",
    )
    return "".join(f"{line}\n" for line in diff_lines)


def read_expected(path: Path) -> str:
    """Read baseline text using ``open(expected).read()`` semantics."""
    with path.open(encoding="utf-8") as expected_file:
        return expected_file.read()


def extract_section(document: str, section_id: str) -> str:
    """Return one ``[section_id]`` block from a Golden Master document."""
    marker = f"[{section_id}]"
    if marker not in document:
        raise KeyError(f"Section not found in Golden Master baseline: {section_id}")

    start = document.index(marker)
    separator = document.find(SECTION_SEPARATOR, start)
    if separator == -1:
        return document[start:].rstrip("\n")
    return document[start:separator].rstrip("\n")


def compare_text(
    expected: str,
    actual: str,
    *,
    context: str,
) -> None:
    """Compare expected vs actual and fail with unified diff on mismatch."""
    if expected == actual:
        return

    diff = unified_diff(
        expected,
        actual,
        fromfile="expected",
        tofile="actual",
    )
    raise AssertionError(
        f"Golden Master snapshot mismatch ({context}).\n"
        "Re-run with --approve-golden-master to update the baseline.\n\n"
        f"{diff}"
    )


def approve_snapshot(
    expected_path: Path,
    actual: str,
    *,
    approve: bool = False,
) -> str:
    """Apply approve pattern: create, compare, or overwrite Golden Master file.

    Args:
        expected_path: Path to the version-controlled baseline file.
        actual: Newly captured Golden Master document.
        approve: When True, overwrite the baseline with ``actual``.

    Returns:
        ``"created"`` when the baseline was written because it was missing,
        ``"approved"`` when ``approve=True`` overwrote an existing baseline,
        ``"matched"`` when actual equals the existing baseline.

    Raises:
        AssertionError: When the baseline exists, ``approve`` is False, and
            ``actual`` differs from the stored content. The error message
            includes a unified diff.
    """
    if approve or not expected_path.is_file():
        action = "approved" if expected_path.is_file() and approve else "created"
        expected_path.parent.mkdir(parents=True, exist_ok=True)
        expected_path.write_text(actual, encoding="utf-8")
        return action

    expected = read_expected(expected_path)
    if expected == actual:
        return "matched"

    compare_text(expected, actual, context=str(expected_path))
    raise AssertionError("compare_text must raise on mismatch")


def approve_section(
    expected_path: Path,
    section_id: str,
    actual_section: str,
    *,
    full_document: str,
    approve: bool = False,
) -> None:
    """Approve or compare one scenario section against the baseline file."""
    if approve or not expected_path.is_file():
        expected_path.parent.mkdir(parents=True, exist_ok=True)
        expected_path.write_text(full_document, encoding="utf-8")
        return

    expected_document = read_expected(expected_path)
    expected_section = extract_section(expected_document, section_id)
    compare_text(
        expected_section,
        actual_section,
        context=f"[{section_id}]",
    )

