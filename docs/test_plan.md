# Test Plan — AC-FR-01-01: SIZE 입력 검증 (grid=None → INVALID_SIZE)

| Field | Value |
|---|---|
| Document ID | TP-MSQ-FR01-01 |
| Version | 1.0 |
| Author Role | Senior QA Lead |
| Status | Draft — RED Phase Ready |
| Primary AC | **AC-FR-01-01** |
| Related FR | **FR-01** Input Verification (Boundary) |
| PRD Reference | `docs/PRD_MagicSquare.md` §10, §12.1, §13, §14, §16.2, §21 |
| Design Reference | `Report/02.4x4_MagicSquare_TDD_Design_Report.md` §2.3 (UT-01) |
| Tech Stack | Python 3.11+, pytest, pydantic, unittest.mock |
| Target Component | `BoundaryValidator` (`src/boundary/`) |
| Test Track | **Track A — Boundary / UI Contract TDD** |

---

## 1. Executive Summary

본 테스트 계획서는 FR-01 Acceptance Criteria 중 **가장 선행**되는 **AC-FR-01-01**(SIZE 검증)을 대상으로 한다.  
검증 순서 **SIZE → RANGE → ZERO COUNT → DUPLICATE** (PRD §12.1)에 따라, 크기 위반 입력은 Domain resolver **호출 0회**로 즉시 차단되어야 한다 (BR-05, AC-FR-01-01).

**Anchor Sample (선택 예제)**

| 항목 | 값 |
|---|---|
| AC ID | AC-FR-01-01 |
| 입력 | `grid = None` |
| 기대 출력 | `{ "code": "INVALID_SIZE", "message": "Grid must be 4x4." }` |
| Domain 호출 | **0회** |

> **PRD 매핑 참고:** PRD §13은 동일 SIZE 위반을 `UI-ERR-001` / `[UI-ERR-001] matrix size invalid:provide 4x4 matrix`로 정의한다.  
> 본 계획서는 Anchor Sample 기준으로 **`INVALID_SIZE`** 코드를 사용하며, 구현 시 pydantic Error Contract 모델에서 PRD 코드와 1:1 매핑 테이블을 유지한다.

---

## 2. Test Objectives

| ID | Objective | Verification |
|---|---|---|
| OBJ-01 | `None` 및 비-4×4 입력에 대해 `INVALID_SIZE` 구조화 실패 응답 반환 | Assert `code`, `message` |
| OBJ-02 | SIZE 위반 시 Domain resolver **미호출** (Boundary–Domain 격리) | mock/spy `call_count == 0` |
| OBJ-03 | 동일 위반 입력 → 동일 Error Code·Message (결정론, NFR-03) | 반복 실행 equality |
| OBJ-04 | SIZE 검증 분기만 최소 구현하여 Boundary 커버리지 85%+ 기여 | pytest-cov gate |
| OBJ-05 | AC-FR-01-01 범위 외 정상 4×4 입력은 **본 Suite에서 테스트하지 않음** | Suite exclusion rule |

---

## 3. Scope

### 3.1 In-Scope

- `BoundaryValidator` SIZE 검증 로직 (행 개수, 열 개수)
- Control/Boundary 파이프라인 진입점에서의 SIZE 선차단
- 구조화 실패 응답 스키마 (`code`, `message`) — pydantic 모델 검증
- Domain resolver mock/spy 호출 횟수 검증
- 경계값·예외·특이 입력 (§5, §6)

### 3.2 Out-of-Scope (본 Suite)

| Item | Reason | Covered By |
|---|---|---|
| `grid = 4×4` 정상 입력 | AC-FR-01-01 범위 외 | FR-02~FR-05 Suite, UT-05 |
| RANGE 위반 (`UI-ERR-002` / `INVALID_RANGE`) | SIZE 이후 순서 | AC-FR-01-03 Suite |
| ZERO COUNT 위반 | SIZE 이후 순서 | AC-FR-01-04 Suite (RED-BND-VAL-001) |
| DUPLICATE 위반 | SIZE 이후 순서 | AC-FR-01-05 Suite (RED-BND-VAL-002) |
| Solver / BlankFinder / Validator Domain 로직 | Track B | `tests/entity/` |
| 출력 `int[6]` schema | FR-05 | `ResultFormatter` Suite |

---

## 4. pytest 기반 단위 테스트 범위 및 우선순위

### 4.1 테스트 파일 구조 (예정)

```
tests/
└── boundary/
    ├── conftest.py                          # 공통 fixture, mock resolver
    ├── test_boundary_validator_size.py      # AC-FR-01-01 (본 계획)
    └── test_boundary_validator_size_edges.py # 예외/특이 케이스 (P2)
```

### 4.2 단위 테스트 범위

| Layer | Module Under Test | Test Type | Scope |
|---|---|---|---|
| Boundary | `BoundaryValidator.validate_size()` | Unit | 행/열 개수 판정, `INVALID_SIZE` 반환 |
| Boundary | `BoundaryValidator.validate()` | Unit | SIZE 분기 최우선 실행 확인 |
| Control | `SolveUseCase.execute()` (또는 동등 orchestrator) | Unit + mock | SIZE 실패 시 resolver 미위임 |
| Contract | `ValidationErrorResponse` (pydantic) | Schema | `code`, `message` 필드 강제 |

### 4.3 우선순위 매트릭스

| Priority | Test ID | Scenario | Input | Expected | Rationale |
|---|---|---|---|---|---|
| **P0 — RED First** | TP-FR01-01-001 | Anchor: null grid | `None` | `INVALID_SIZE`, Domain 0 | 선택 Anchor Sample; 최소 선행 AC |
| **P0** | TP-FR01-01-002 | Empty grid | `[]` | `INVALID_SIZE`, Domain 0 | 행 개수 0; SIZE 최우선 차단 |
| **P0** | TP-FR01-01-003 | Row count mismatch | `3×4` matrix | `INVALID_SIZE`, Domain 0 | PRD §16.4 Invalid size; UT-01 |
| **P1** | TP-FR01-01-004 | Column count mismatch | `4×3` matrix | `INVALID_SIZE`, Domain 0 | AC-FR-01-02 (열 길이 ≠ 4) |
| **P1** | TP-FR01-01-005 | Oversized grid | `5×5` matrix | `INVALID_SIZE`, Domain 0 | 양방향 크기 초과 |
| **P1** | TP-FR01-01-006 | Rows exist, no columns | `[[]] * 4` | `INVALID_SIZE`, Domain 0 | 행=4, 열=0; SIZE/열 계약 위반 |
| **P2** | TP-FR01-01-007~ | §6 예외/특이 케이스 | various | `INVALID_SIZE` or TypeError policy | 방어적 입력 처리 |

### 4.4 RED → GREEN → REFACTOR 운영 규칙

1. **RED:** P0 케이스(`None`, `[]`, `3×4`) 테스트 먼저 작성 → 실패 확인 (missing behavior, not broken test)
2. **GREEN:** `BoundaryValidator` SIZE 분기 최소 구현 → P0 GREEN
3. **GREEN 확장:** P1 경계값 GREEN
4. **REFACTOR:** GREEN 이후 상수 추출 (`GRID_SIZE = 4`), 중복 제거; **외부 I/O 계약 불변**
5. **금지:** 테스트 삭제·skip·assertion 완화로 GREEN 강제 (`.cursor/rules/magicsquare-forbidden.mdc`)

### 4.5 pytest Convention

- **AAA 패턴:** Arrange (입력·mock) → Act (validate/execute) → Assert (응답·call_count)
- **함수명:** `test_<scenario>_<expected_outcome>` (예: `test_null_grid_returns_invalid_size`)
- **Fixture scope:** `function` (기본)
- **Parametrize:** `3×4`, `4×3`, `5×5`는 `@pytest.mark.parametrize`로 통합 가능

---

## 5. 경계값 케이스 목록

검증 순서상 SIZE가 최우선이므로, 아래 모든 케이스는 **RANGE/ZERO/DUPLICATE 검사 이전**에 실패해야 한다.

| Case ID | Input | Size Diagnosis | Expected `code` | Expected `message` | Domain Calls | AC Mapping |
|---|---|---|---|---|---|---|
| **BV-01** | `grid = None` | matrix absent | `INVALID_SIZE` | `Grid must be 4x4.` | **0** | AC-FR-01-01 |
| **BV-02** | `grid = []` | row count = 0 | `INVALID_SIZE` | `Grid must be 4x4.` | **0** | AC-FR-01-01 |
| **BV-03** | `grid = [[]] * 4` | row count = 4, col count = 0 | `INVALID_SIZE` | `Grid must be 4x4.` | **0** | AC-FR-01-01 / AC-FR-01-02 |
| **BV-04** | `3×4` matrix | row count = 3 | `INVALID_SIZE` | `Grid must be 4x4.` | **0** | AC-FR-01-01 |
| **BV-05** | `4×3` matrix | col count = 3 | `INVALID_SIZE` | `Grid must be 4x4.` | **0** | AC-FR-01-02 |
| **BV-06** | `5×5` matrix | row count = 5 | `INVALID_SIZE` | `Grid must be 4x4.` | **0** | AC-FR-01-01 |

### 5.1 대표 입력 데이터

**BV-04 — 3×4 (PRD §16.4):**

```python
[
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
]
```

**BV-05 — 4×3:**

```python
[
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    [10, 11, 12],
]
```

**BV-06 — 5×5:**

```python
[[1, 2, 3, 4, 5] for _ in range(5)]
```

### 5.2 명시적 제외 케이스

| Input | Exclusion Reason |
|---|---|
| `grid = 4×4` 정상 행렬 (0 두 개 포함) | AC-FR-01-01 범위 외; FR-02~05 및 UT-05 Suite에서 검증 |
| 값 범위/빈칸/중복 위반 4×4 | SIZE 통과 후 후속 AC 담당 (AC-FR-01-03~05) |

---

## 6. 예외 / 특이 케이스 목록

SIZE 검증 Robustness 및 Boundary 방어 로직 확인용 (Priority P2).

| Case ID | Input | Expected Behavior | Domain Calls | Notes |
|---|---|---|---|---|
| **EX-01** | `grid = ""` (str) | `INVALID_SIZE` 또는 명시적 TypeError → `INVALID_SIZE` 매핑 | **0** | 타입 계약 위반; uncaught exception 금지 (FR-01 Error Policy) |
| **EX-02** | `grid = 123` (int) | `INVALID_SIZE` (non-iterable) | **0** | |
| **EX-03** | `grid = {}` (dict) | `INVALID_SIZE` | **0** | |
| **EX-04** | `grid = [[1,2,3,4], None, [5,6,7,8], [9,10,11,12]]` | `INVALID_SIZE` | **0** | 행 원소가 list가 아님 |
| **EX-05** | Ragged/jagged: `[[1,2,3,4], [5,6], [7,8,9,10], [11,12,13,14]]` | `INVALID_SIZE` (첫 열 길이 ≠ 4 행) | **0** | AC-FR-01-02; SIZE 단계에서 열 검사 |
| **EX-06** | `grid = [[]] * 4` 후 한 행 mutation | `INVALID_SIZE` (열 길이 불일치 가능) | **0** | Python `[[]]*4` 참조 공유 함정; SIZE/열 검증 독립성 확인 |
| **EX-07** | Nested depth 오류: `[1, 2, 3, 4]` (1D list) | `INVALID_SIZE` | **0** | row count = 1 |
| **EX-08** | `grid = [[1,2,3,4]] * 3` (3 rows, valid cols) | `INVALID_SIZE` | **0** | BV-04와 동형 |
| **EX-09** | 동일 BV-01 입력 100회 반복 | 매회 동일 `code`/`message` | **0** | NFR-03 Deterministic |

### 6.1 예외 처리 정책 (테스트 관점)

- FR-01 Error Policy: **uncaught exception 금지** → 모든 EX 케이스는 구조화 실패 응답으로 수렴해야 함
- Python 내장 `TypeError`/`AttributeError` 발생 시 Boundary에서 catch하여 `INVALID_SIZE`로 매핑할지, 사전 타입 가드로 처리할지 **구현 전 팀 합의** 필요 (Open Decision)
- 본 Suite는 **어떤 경로든** 최종 응답 `{ code: "INVALID_SIZE", ... }` + Domain 0회를 assert

---

## 7. Domain resolver 진입점 호출 횟수 검증 전략 (mock / spy)

### 7.1 격리 대상

| Entry Point | Layer | Mock Target | When to Verify |
|---|---|---|---|
| `DomainResolver.solve()` | Control → Entity | Primary spy | Control orchestration 테스트 |
| `Solver.solve()` | Entity | Secondary spy | Boundary 통합 경로 |
| `SolveUseCase.execute()` | Control | System under test | End-to-end Boundary 진입 |

**원칙 (BR-05, AC-FR-01-01):** SIZE 위반 시 Domain resolver **call_count == 0**

### 7.2 Mock / Spy 패턴

#### Pattern A — Control Layer Unit Test (권장)

```python
from unittest.mock import MagicMock, patch

def test_null_grid_blocks_domain_resolver(null_grid, boundary_validator, solve_use_case):
    # Arrange
    mock_resolver = MagicMock()
    solve_use_case = SolveUseCase(
        validator=boundary_validator,
        domain_resolver=mock_resolver,
    )

    # Act
    result = solve_use_case.execute(grid=null_grid)

    # Assert — response contract
    assert result.code == "INVALID_SIZE"
    assert result.message == "Grid must be 4x4."

    # Assert — Domain isolation
    mock_resolver.solve.assert_not_called()
    assert mock_resolver.solve.call_count == 0
```

#### Pattern B — pytest `mocker` fixture (pytest-mock)

```python
def test_empty_grid_domain_not_called(mocker, empty_grid, solve_use_case):
    spy = mocker.spy(solve_use_case._domain_resolver, "solve")

    result = solve_use_case.execute(grid=empty_grid)

    assert result.code == "INVALID_SIZE"
    spy.assert_not_called()
```

#### Pattern C — `unittest.mock.patch` on import path

```python
@patch("src.control.solve_use_case.DomainResolver.solve")
def test_3x4_grid_domain_never_invoked(mock_solve, three_by_four_grid, solve_use_case):
    result = solve_use_case.execute(grid=three_by_four_grid)

    assert result.code == "INVALID_SIZE"
    mock_solve.assert_not_called()
```

### 7.3 검증 체크리스트

- [ ] BV-01 ~ BV-06 **전 케이스**에서 `call_count == 0`
- [ ] EX-01 ~ EX-09 **전 케이스**에서 `call_count == 0`
- [ ] mock이 실제 Domain 로직을 대체하여 **Boundary 책임만** 검증 (Report/02 §2.3)
- [ ] mock 반환값 설정 없이도 테스트 통과 (Domain 미호출이므로 mock stub 불필요)
- [ ] `autospec=True` 사용 검토 → 실제 resolver 시그니처 drift 조기 감지

### 7.4 Dual-Track 분리 원칙

| Track | Mock Usage | Purpose |
|---|---|---|
| **Track A (본 Suite)** | Domain resolver = mock/spy | Boundary 계약 + 호출 격리 |
| **Track B** | Boundary = 직접 호출 없음 | Domain 불변식 단독 검증 |

Track A 테스트에서 Domain mock으로 GREEN을 만들지 않는다 — **SIZE 실패 assert가 primary**, mock은 call count 검증 전용.

---

## 8. 커버리지 목표

### 8.1 프로젝트 전역 Gate (PRD §14, §20)

| Metric | Target | Scope | Gate |
|---|---|---|---|
| Domain Logic | **≥ 95%** | `src/entity/` | pytest-cov fail-under |
| Boundary Validation | **≥ 85%** | `src/boundary/` | pytest-cov fail-under |
| Global | **≥ 80%** | `src/` | `.cursorrules` |

### 8.2 본 Suite (AC-FR-01-01) 기여 목표

| Module | Target Lines / Branches | Notes |
|---|---|---|
| `boundary_validator.py` — SIZE 분기 | **100%** branch on `validate_size` | 본 Suite 핵심 |
| `boundary_validator.py` — 전체 | ≥ 85% (누적) | RANGE/ZERO/DUP Suite와 합산 |
| `control/solve_use_case.py` — early return | SIZE fail path **100%** | mock spy 테스트 |
| `entity/*` | 본 Suite에서 **0% 호출** | Domain Suite에서 95%+ 달성 |

> Domain 95%+는 Track B (`tests/entity/`) Suite 책임.  
> 본 Track A Suite는 Boundary 85%+ gate에 **SIZE 분기 커버리지**를 우선 기여한다.

### 8.3 커버리지 제외 / 주의

- `if TYPE_CHECKING:` 블록 — 측정 제외 가능
- pydantic model 정의 라인 — schema 테스트로 간접 커버
- `[[]] * 4` mutation 케이스 (EX-06) — branch coverage 명시적 추가

---

## 9. pytest-cov 측정 전략

### 9.1 설치

```bash
pip install pytest-cov
```

### 9.2 실행 — 전체 프로젝트

```bash
pytest --cov=src --cov-report=term-missing
```

### 9.3 실행 — Boundary Suite (본 계획 범위)

```bash
pytest tests/boundary/test_boundary_validator_size.py \
       --cov=src/boundary \
       --cov=src/control \
       --cov-report=term-missing \
       --cov-fail-under=85
```

### 9.4 실행 — Domain Suite (Track B, 별도 Gate)

```bash
pytest tests/entity/ \
       --cov=src/entity \
       --cov-report=term-missing \
       --cov-fail-under=95
```

### 9.5 실행 — AC-FR-01-01 Slice Only (개발 중 빠른 피드백)

```bash
pytest tests/boundary/test_boundary_validator_size.py -k "invalid_size" \
       --cov=src/boundary/boundary_validator \
       --cov-report=term-missing
```

### 9.6 CI Gate 권장 설정 (`pyproject.toml` 또는 `pytest.ini` 예시)

```ini
[tool:pytest]
testpaths = tests
addopts =
    --cov=src
    --cov-report=term-missing
    --cov-report=html:htmlcov
    --cov-fail-under=80

[coverage:run]
source = src
branch = true

[coverage:report]
fail_under = 80
show_missing = true
```

### 9.7 측정 해석 가이드

| Report Column | Action if Missing |
|---|---|
| `boundary_validator.py` SIZE branch | BV-01~06, EX-05, EX-07 미작성 또는 미실행 |
| `solve_use_case.py` early-return | mock spy 테스트 누락 |
| `entity/solver.py` | 정상 — 본 Suite에서 호출 금지 |

---

## 10. Traceability Matrix (본 Suite)

| Business Rule | AC ID | Test Case ID | Input | Expected | Component |
|---|---|---|---|---|---|
| BR-01 (4×4 입력) | AC-FR-01-01 | TP-FR01-01-001 | `None` | `INVALID_SIZE` | BoundaryValidator |
| BR-01 | AC-FR-01-01 | TP-FR01-01-002 | `[]` | `INVALID_SIZE` | BoundaryValidator |
| BR-01 | AC-FR-01-01/02 | TP-FR01-01-006 | `[[]]*4` | `INVALID_SIZE` | BoundaryValidator |
| BR-01 | AC-FR-01-01 | TP-FR01-01-003 | `3×4` | `INVALID_SIZE` | BoundaryValidator |
| BR-01 | AC-FR-01-02 | TP-FR01-01-004 | `4×3` | `INVALID_SIZE` | BoundaryValidator |
| BR-01 | AC-FR-01-01 | TP-FR01-01-005 | `5×5` | `INVALID_SIZE` | BoundaryValidator |
| BR-05 (Domain 미호출) | AC-FR-01-01 | TP-FR01-01-* | all BV/EX | call_count = 0 | Control + mock |

**PRD Test Candidate Mapping:** RED-BND-VAL-004, UT-01, TP-E-01

---

## 11. Exit Criteria (본 Suite GREEN)

- [ ] P0 + P1 전건 GREEN (BV-01 ~ BV-06)
- [ ] 전 BV/EX 케이스 Domain resolver `call_count == 0` 확인
- [ ] `INVALID_SIZE` / `"Grid must be 4x4."` 응답 일관성 (NFR-03)
- [ ] `src/boundary/` 누적 커버리지 ≥ 85% (전체 Boundary Suite 합산 기준)
- [ ] uncaught exception 0건
- [ ] 4×4 정상 입력 테스트가 **본 Suite에 포함되지 않음** 확인

---

## 12. Appendix

### 12.1 Expected Response Schema (pydantic)

```python
class ValidationErrorResponse(BaseModel):
    code: Literal["INVALID_SIZE"]
    message: Literal["Grid must be 4x4."]
```

### 12.2 PRD Error Code Cross-Reference

| Test Plan Code | PRD §13 Code | PRD Message Template |
|---|---|---|
| `INVALID_SIZE` | `UI-ERR-001` | `[UI-ERR-001] matrix size invalid:provide 4x4 matrix` |

### 12.3 Related Documents

| Document | Path |
|---|---|
| PRD | `docs/PRD_MagicSquare.md` |
| TDD Design Report | `Report/02.4x4_MagicSquare_TDD_Design_Report.md` |
| TDD Testing Rules | `.cursor/rules/magicsquare-tdd-testing.mdc` |
| ECB Architecture | `.cursor/rules/magicsquare-ecb-architecture.mdc` |

---

*End of Test Plan — AC-FR-01-01 SIZE Validation (Track A)*
