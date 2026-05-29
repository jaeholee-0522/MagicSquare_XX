# Golden Master Execution Example — GM-2 Magic Square

Command:

```bash
pytest -m golden_master -v
```

Output (2026-05-29):

```text
============================= test session starts =============================
platform win32 -- Python 3.14.0, pytest-8.4.2, pluggy-1.6.0
rootdir: MagicSquare_XX
configfile: pytest.ini
collected 68 items / 62 deselected / 6 selected

tests/test_golden_master_magic_square.py::TestGoldenMasterMagicSquare::test_gm2_full_document_matches_baseline PASSED
tests/test_golden_master_magic_square.py::TestGoldenMasterMagicSquare::test_gm_tc_01_normal_success PASSED
tests/test_golden_master_magic_square.py::TestGoldenMasterMagicSquare::test_gm_tc_02_reverse_success PASSED
tests/test_golden_master_magic_square.py::TestGoldenMasterMagicSquare::test_gm_tc_03_invalid_blank_count PASSED
tests/test_golden_master_magic_square.py::TestGoldenMasterMagicSquare::test_gm_tc_04_duplicate_number PASSED
tests/test_golden_master_magic_square.py::TestGoldenMasterMagicSquare::test_gm_tc_05_no_valid_magic_square PASSED

====================== 6 passed, 62 deselected in 0.11s =======================
```

## Failure diff example

When solver output drifts from `tests/golden_master_expected.txt`:

```text
AssertionError: Golden Master snapshot mismatch ([normal_success]).
Re-run with --approve-golden-master to update the baseline.

--- expected
+++ actual
@@ -5,4 +5,4 @@
 13 3 2 0
 Output:
-[1, 1, 1, 4, 4, 16]
+[1, 1, 1, 4, 4, 15]
```

Approve updated baseline:

```bash
pytest -m golden_master -v --approve-golden-master
```
