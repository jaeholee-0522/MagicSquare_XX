# Golden Master Approval Pattern — GM-1 / GM-2 Magic Square Solver

| Field | Value |
|---|---|
| Document ID | GM-MSQ-01 |
| Version | 2.0 |
| Test ID | **GM-1** (baseline), **GM-2** (test code) |
| Baseline File | `tests/golden_master_expected.txt` |
| Test Module | `tests/test_golden_master_magic_square.py` |
| Generator | `scripts/generate_golden_master.py` |

---

## 1. Purpose

GM-1 captures **end-to-end SolveUseCase output** for five representative scenarios and stores the result as a version-controlled Golden Master baseline. Future solver or contract changes that alter observable output fail with a unified diff instead of silently drifting.

Capture strategy: **Result DTO serialize** (not stdout). The test runs `SolveUseCase.execute(grid)` and serializes:

- success → `Output:\n[r1, c1, n1, r2, c2, n2]`
- Boundary failure → `Error:\n<ValidationErrorCode>`
- Domain failure → `Error:\n<DomainErrorCode>`

---

## 2. Scenarios (GM-1)

| Section ID | Scenario | Input Source |
|---|---|---|
| `normal_success` | Attempt 1 (small-first) success | PRD §16.4 Matrix A (`G1`) |
| `reverse_success` | Attempt 2 (reverse) success | PRD §16.4 Matrix B (`G2`) |
| `invalid_blank_count` | Blank count ≠ 2 | PRD §16.4 one-zero grid |
| `duplicate_number` | Duplicate non-zero values | PRD §16.4 duplicate grid |
| `no_valid_solution` | Both attempts fail | `G3` |

---

## 3. Baseline File Structure

Each section uses this block format:

```text
[section_id]
Input:
<4 rows, space-separated integers>
Output:
[int list]
```

or, for failures:

```text
[section_id]
Input:
<grid>
Error:
ERROR_CODE
```

Sections are separated by a fixed delimiter:

```text
________________________________________
```

Example (`normal_success`):

```text
[normal_success]
Input:
0 15 14 4
12 6 7 9
8 10 11 5
13 3 2 0
Output:
[1, 1, 1, 4, 4, 16]
```

---

## 4. Approve Pattern

Implementation: `tests/golden_master/approval.py` → `approve_snapshot()`.

| Condition | Behavior |
|---|---|
| Baseline file **missing** | Write current output → pass (`created`) |
| Baseline exists, output **matches** | Pass (`matched`) |
| Baseline exists, output **differs** | Emit unified diff → **FAIL** |
| Explicit approve flag set | Overwrite baseline → pass (`approved`) |

### Approve flags

**pytest**

```bash
pytest tests/test_golden_master.py --approve-golden-master
```

**Generator script**

```bash
python scripts/generate_golden_master.py
python scripts/generate_golden_master.py --approve
```

- First run (no baseline): both paths create `tests/golden_master_expected.txt`.
- Intentional output change: re-run with `--approve-golden-master` or `--approve`, review diff, commit updated baseline.

---

## 5. Workflow

### Initial baseline creation

```bash
python scripts/generate_golden_master.py
git add tests/golden_master_expected.txt
git commit -m "Add GM-1 Golden Master baseline for Magic Square Solver output."
```

### Regression check (CI / local)

```bash
pytest tests/test_golden_master.py
```

### Updating baseline after approved change

```bash
pytest tests/test_golden_master.py --approve-golden-master
git add tests/golden_master_expected.txt
git commit -m "Approve GM-1 Golden Master baseline after solver output change."
```

---

## 6. Architecture Notes

| Layer | Role in GM-1 |
|---|---|
| `tests/golden_master/scenarios.py` | Scenario catalog, grid formatting, DTO serialization |
| `tests/golden_master/approval.py` | Approve / compare / unified diff |
| `tests/test_golden_master.py` | pytest entry point |
| `scripts/generate_golden_master.py` | Standalone baseline generator |

GM-1 exercises the full **Boundary → Control → Entity** path via `SolveUseCase` with real `BoundaryValidator` and `DomainResolverImpl`. It complements unit tests in `tests/entity/` and `tests/boundary/` by locking the integrated observable contract.

---

## 7. Failure Example

When output drifts, pytest fails with:

```text
AssertionError: Golden Master snapshot mismatch.
Re-run with --approve-golden-master to update the baseline.

--- tests/golden_master_expected.txt
+++ tests/golden_master_expected.txt (actual)
@@ ...
```

---

## 8. GM-2 Test Code

| Test Case | Method | Verification |
|---|---|---|
| GM-TC-01 | `test_gm_tc_01_normal_success` | int[6], row-major, 1-index, small-first |
| GM-TC-02 | `test_gm_tc_02_reverse_success` | int[6], row-major, 1-index, reverse fallback |
| GM-TC-03 | `test_gm_tc_03_invalid_blank_count` | Boundary Error Contract `INVALID_BLANK_COUNT` |
| GM-TC-04 | `test_gm_tc_04_duplicate_number` | Boundary Error Contract `INVALID_DUPLICATE` |
| GM-TC-05 | `test_gm_tc_05_no_valid_magic_square` | Domain Error Contract `DOMAIN-ERR-NO_VALID_PLACEMENT` |

### Marking and execution

```python
@pytest.mark.golden_master
def test_gm_tc_01_normal_success(...):
    """[TAG][GoldenMaster] GM-TC-01 정상 조합 성공."""
```

```bash
pytest -m golden_master -v
```

### Per-test flow

1. **API result serialization** — `SolveUseCase.execute(grid)` captures DTO output.
2. **Contract assertions** — `tests/golden_master/contracts.py`.
3. **Section compare** — `open(expected).read()` vs actual section; unified diff on mismatch.
4. **Approve pattern** — missing baseline auto-created; `--approve-golden-master` overwrites.

Execution sample: [`docs/golden_master_execution_example.md`](golden_master_execution_example.md)

