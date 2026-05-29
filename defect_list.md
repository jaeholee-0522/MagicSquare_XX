# Defect List — Magic Square 4×4 (AC-FR-01-01)

| Field | Value |
|---|---|
| Document ID | DEF-MSQ-001 |
| Version | 1.0 |
| Last Updated | 2026-05-29 |
| Scope | AC-FR-01-01 SIZE validation (Track A) |
| Test Reference | `tests/boundary/test_ac_fr_01_01_*.py`, `docs/test_plan.md` |
| Regression | `pytest tests/boundary/ tests/entity/test_user.py` → **35 passed** |

---

## Summary

| Status | Count |
|---|---|
| **Resolved** | 4 |
| **Open** | 0 |
| **Deferred** | 0 |

---

## Defect Register

| ID | Severity | AC ID | 재현 절차 | 기대값 | 실제값 | 근본 원인 | 수정 요약 | Status |
|---|---|---|---|---|---|---|---|---|
| DEF-001 | Critical | AC-FR-01-01 | 프로젝트 루트에서 `pytest tests/boundary/` 실행 (구현 전) | 테스트 수집 후 RED assertion 실패 | `ModuleNotFoundError: No module named 'src.boundary'` (`conftest.py:9`) | `src/boundary/` 패키지·`BoundaryValidator` 미구현 | `src/boundary/contracts.py`, `boundary_validator.py`, `control/solve_use_case.py`, `entity/domain_resolver.py` 추가 | **Resolved** |
| DEF-002 | Critical | AC-FR-01-01 | `grid=None`으로 `BoundaryValidator.validate()` 또는 `SolveUseCase.execute()` 호출 (SIZE 분기 없을 때) | `{ code: "INVALID_SIZE", message: "Grid must be 4x4." }` | `AttributeError: 'NoneType' object has no attribute ...` 또는 `TypeError: object of type 'NoneType' has no len()` | `grid is None` 선차단 없이 `len(grid)`/행 순회 수행 | `boundary_validator.py` `_is_size_invalid()`에 `if grid is None: return True` 및 `ValidationErrorResponse.invalid_size()` 반환 | **Resolved** |
| DEF-003 | Major | AC-FR-01-01 | `grid=None` 입력 후 `SolveUseCase.execute()` | Domain `resolve()` 호출 **0회** | (잠재) `resolve()` 1회 호출 → Domain 오염 또는 `NotImplementedError` | Control层에서 검증 실패 시 Domain 위임 누락 | `solve_use_case.py`: `validation_error is not None`이면 즉시 반환, `resolve()` 미호출 | **Resolved** |
| DEF-004 | Info | — | `.\.venv\Scripts\Activate.ps1` 실행 (`.venv` 미생성 상태) | 가상환경 활성화 | `지정된 경로를 찾을 수 없습니다.` | `python -m venv .venv` 미실행 | `C:\Users\usejen_id\AppData\Local\Python\bin\python.exe -m venv .venv`로 생성; `pytest.ini`에 `pythonpath = .` 설정 | **Resolved** |
| DEF-005 | Info | — | CMD에서 `$env:PYTHONPATH = (Get-Location).Path` 실행 | `PYTHONPATH` 설정 | `파일 이름, 디렉터리 이름 또는 볼륨 레이블 구문이 잘못되었습니다.` | PowerShell 문법을 CMD에서 실행 | CMD: `set PYTHONPATH=%CD%` / 또는 `pytest.ini`로 `PYTHONPATH` 불필요 | **Resolved** |

---

## 상세 재현 — DEF-001 (Resolved)

```text
ImportError while loading conftest '...\tests\boundary\conftest.py'.
tests\boundary\conftest.py:9: in <module>
    from src.boundary.boundary_validator import BoundaryValidator
E   ModuleNotFoundError: No module named 'src.boundary'
```

**수정 파일:** `src/boundary/__init__.py`, `contracts.py`, `boundary_validator.py`, `src/control/solve_use_case.py`, `src/entity/domain_resolver.py`

---

## 상세 재현 — DEF-002 (Resolved)

**시나리오:** SIZE 검증 없이 `validate(None)` 호출 시.

| | |
|---|---|
| **기대** | `ValidationErrorResponse(code="INVALID_SIZE", message="Grid must be 4x4.")` |
| **실제 (수정 전 패턴)** | `AttributeError` / `TypeError` on `None` |

**수정 위치:** `src/boundary/boundary_validator.py` — `_is_size_invalid()` L33-35

---

## 회귀 테스트 확인 (Green)

```powershell
cd C:\Users\usejen_id\Documents\CursorAI-main\Dev\MagicSquare_XX
.\.venv\Scripts\Activate.ps1
pytest tests/boundary/ tests/entity/test_user.py -v
```

| Suite | Result |
|---|---|
| `tests/boundary/` (AC-FR-01-01) | 30 passed |
| `tests/entity/test_user.py` | 5 passed |
| **Total** | **35 passed** |

---

## Open / Deferred

현재 **Open 결함 없음**. AC-FR-01-02~05, FR-02~05는 별도 RED 사이클에서 추적 예정.

---

## Traceability

| Defect ID | Test IDs | PRD / AC |
|---|---|---|
| DEF-001 | TC-A-01~07, TC-B-01~03 | AC-FR-01-01, FR-01 |
| DEF-002 | TC-A-01, TC-A-02, TC-A-03 | AC-FR-01-01, PRD §8.1 `INVALID_SIZE` |
| DEF-003 | TC-A-04, TC-B-01~03 | AC-FR-01-01, BR-05 |
| DEF-004 | — | 환경 설정 |
| DEF-005 | — | 환경 설정 |

---

*End of Defect List*
