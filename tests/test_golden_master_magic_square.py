"""GM-2 Golden Master regression tests for Magic Square Solver output."""

from __future__ import annotations

from pathlib import Path

import pytest

from src.control.solve_use_case import SolveUseCase
from tests.golden_master.approval import approve_section, approve_snapshot
from tests.golden_master.contracts import assert_scenario_contract
from tests.golden_master.scenarios import (
    GM2_SCENARIOS,
    GoldenMasterScenario,
    build_golden_master_document,
    capture_api_result,
    format_section,
)

EXPECTED_PATH = Path(__file__).resolve().parent / "golden_master_expected.txt"
pytestmark = pytest.mark.golden_master


def _run_golden_master_case(
    scenario: GoldenMasterScenario,
    integrated_solve_use_case: SolveUseCase,
    approve_golden_master: bool,
) -> None:
    """Execute one GM-2 case: API capture, contract checks, section approval."""
    result = capture_api_result(scenario, integrated_solve_use_case)
    assert_scenario_contract(scenario, result)

    actual_section = format_section(scenario, result)
    full_document = build_golden_master_document(use_case=integrated_solve_use_case)
    approve_section(
        EXPECTED_PATH,
        scenario.section_id,
        actual_section,
        full_document=full_document,
        approve=approve_golden_master,
    )


class TestGoldenMasterMagicSquare:
    """[TAG][GoldenMaster] GM-2 end-to-end approval tests."""

    @pytest.mark.golden_master
    def test_gm2_full_document_matches_baseline(
        self,
        integrated_solve_use_case: SolveUseCase,
        approve_golden_master: bool,
    ) -> None:
        """[TAG][GoldenMaster] Full baseline compare via open(expected).read()."""
        actual = build_golden_master_document(use_case=integrated_solve_use_case)
        action = approve_snapshot(
            EXPECTED_PATH,
            actual,
            approve=approve_golden_master,
        )
        assert action in {"matched", "created", "approved"}

    @pytest.mark.golden_master
    def test_gm_tc_01_normal_success(
        self,
        integrated_solve_use_case: SolveUseCase,
        approve_golden_master: bool,
    ) -> None:
        """[TAG][GoldenMaster] GM-TC-01 정상 조합 성공 — int[6], row-major, 1-index, small-first."""
        _run_golden_master_case(
            GM2_SCENARIOS[0],
            integrated_solve_use_case,
            approve_golden_master,
        )

    @pytest.mark.golden_master
    def test_gm_tc_02_reverse_success(
        self,
        integrated_solve_use_case: SolveUseCase,
        approve_golden_master: bool,
    ) -> None:
        """[TAG][GoldenMaster] GM-TC-02 reverse 조합 성공 — reverse fallback rule."""
        _run_golden_master_case(
            GM2_SCENARIOS[1],
            integrated_solve_use_case,
            approve_golden_master,
        )

    @pytest.mark.golden_master
    def test_gm_tc_03_invalid_blank_count(
        self,
        integrated_solve_use_case: SolveUseCase,
        approve_golden_master: bool,
    ) -> None:
        """[TAG][GoldenMaster] GM-TC-03 INVALID_BLANK_COUNT — Boundary Error Contract."""
        _run_golden_master_case(
            GM2_SCENARIOS[2],
            integrated_solve_use_case,
            approve_golden_master,
        )

    @pytest.mark.golden_master
    def test_gm_tc_04_duplicate_number(
        self,
        integrated_solve_use_case: SolveUseCase,
        approve_golden_master: bool,
    ) -> None:
        """[TAG][GoldenMaster] GM-TC-04 DUPLICATE_NUMBER — Boundary Error Contract."""
        _run_golden_master_case(
            GM2_SCENARIOS[3],
            integrated_solve_use_case,
            approve_golden_master,
        )

    @pytest.mark.golden_master
    def test_gm_tc_05_no_valid_magic_square(
        self,
        integrated_solve_use_case: SolveUseCase,
        approve_golden_master: bool,
    ) -> None:
        """[TAG][GoldenMaster] GM-TC-05 NO_VALID_MAGIC_SQUARE — Domain Error Contract."""
        _run_golden_master_case(
            GM2_SCENARIOS[4],
            integrated_solve_use_case,
            approve_golden_master,
        )
