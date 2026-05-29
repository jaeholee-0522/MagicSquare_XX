#!/usr/bin/env python3
"""Generate tests/golden_master_expected.txt from live Magic Square Solver output."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tests.golden_master.approval import approve_snapshot
from tests.golden_master.scenarios import build_golden_master_document

DEFAULT_OUTPUT = PROJECT_ROOT / "tests" / "golden_master_expected.txt"


def main() -> int:
    """Capture solver output and write or approve the Golden Master baseline."""
    parser = argparse.ArgumentParser(
        description="Generate GM-1 Golden Master baseline from solver output.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Baseline file path (default: {DEFAULT_OUTPUT.as_posix()})",
    )
    parser.add_argument(
        "--approve",
        action="store_true",
        help="Overwrite an existing baseline with current solver output.",
    )
    args = parser.parse_args()

    actual = build_golden_master_document()
    action = approve_snapshot(args.output, actual, approve=args.approve)
    print(f"Golden Master baseline {action}: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
