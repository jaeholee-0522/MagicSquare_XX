# Magic Square 4×4 — TDD Practice

**바로가기:** [RED 단계 To-Do 리스트](#red-단계-to-do-리스트) · [RED 커밋 배치 계획](#red-커밋-배치-계획-dual-track-full-red) · [RED Start Checklist](#7-red-start-checklist)

## 1. Project Start Declaration

본 프로젝트는 **PRD 기반 Dual-Track TDD**로 Magic Square 4×4를 구현하는 학습형 연습이다.  
현재 단계는 **RED 단계 완료** — Track A/B Full RED 54건 + R0 GREEN 30건 작성·실패 확인 완료. **다음: GREEN (R1부터 순차 구현)**.

| 용어 | 정의 |
|---|---|
| **RED** | 테스트 실패 상태를 **확인**하는 단계 (미구현으로 인한 기대 실패) |
| **GREEN** | RED 실패를 통과시키기 위한 **최소 구현 작업 후보**만 기술 (본 README에서는 실행하지 않음) |
| **REFACTOR** | GREEN 이후 **구조 개선 후보**만 기술 (실제 수행 없음) |

**고정 TDD 흐름**

```
Scenario → Acceptance Criteria → RED Test ID → Test Skeleton
→ Run Test → Confirm Failure (RED) → GREEN Task Candidate → REFACTOR Candidate
```

> 상세 개발 보드(Task ID 포함)는 Turn 1 To-Do List에 정의되어 있다. 본 README는 Scenario 중심 온보딩 가이드이다.  
> 준비 작업 보고서: [`Report/08.MagicSquare_TDD_Startup_ToDo_README_Report.md`](Report/08.MagicSquare_TDD_Startup_ToDo_README_Report.md)

---

## 2. PRD Summary

### 2.1 목적

4×4 마방진 **정답 산출**이 아니라, **불변식(Invariant)과 입출력 계약(Contract)을 고정한 뒤** Dual-Track TDD로 검증·구현·리팩토링하는 것이 목적이다.

### 2.2 학습 목표

- 불변식 중심 설계 사고
- Dual-Track(UI Contract + Logic Invariant) TDD
- 입력/출력 계약 정의 및 유지
- 설계 → 테스트 → 구현 → 리팩토링 규율
- Concept → Invariant → Contract → Test 추적성

### 2.3 도메인 규칙 (요약)

| 구분 | 규칙 |
|---|---|
| 격자 | 4행 × 4열 `int[][]` |
| 빈칸 | `0` 정확히 2개 |
| 값 범위 | `0` 또는 1~16 |
| 중복 | 0 제외 값 중복 금지 |
| 마방진 | 4행·4열·2대각선 합 = **34** (`MAGIC_CONSTANT`) |
| Solver | Attempt 1 (small-first) → 실패 시 Attempt 2 (reverse) |
| 입력 불변 | 처리 전후 입력 행렬 deep equality 유지 |

**검증 순서 (Boundary):** SIZE → RANGE → ZERO COUNT → DUPLICATE  
**Boundary 실패 시:** Domain resolver **호출 0회**

### 2.4 I/O 계약 (요약)

| 항목 | 계약 |
|---|---|
| 입력 | `int[][] matrix` (4×4, 빈칸 2개, 값 규칙 준수) |
| 성공 출력 | `int[6]` = `[r1, c1, n1, r2, c2, n2]` (좌표 **1-index**) |
| Boundary 오류 | `UI-ERR-001` ~ `UI-ERR-004` (구조화 메시지) |
| Domain 오류 | `DOMAIN-ERR-NO_VALID_PLACEMENT` (두 조합 모두 실패) |

> **Open Question (DN-01):** 성공 응답 envelope — 현재 bare `int[6]` 기준으로 진행. PRD §22 확정 후 v1.1 반영.

### 2.5 Epic Success Criteria

| ID | 기준 |
|---|---|
| ESC-01 | Domain Logic 테스트 커버리지 ≥ 95% |
| ESC-02 | Boundary 입력 검증 계약 테스트 **100%** 통과 |
| ESC-03 | 설명 없는 매직 넘버 0건 |
| ESC-04 | `GRID_SIZE`, `MAGIC_CONSTANT`, `BLANK_VALUE` 등 명명 상수 사용 |
| ESC-05 | 정답 하드코딩 0건 |
| ESC-06 | Traceability Matrix — Concept/Invariant 각 ≥ 1 Test Case |
| ESC-07 | REFACTOR 후 외부 I/O 계약 불변 |

**PRD:** [`docs/PRD_MagicSquare.md`](docs/PRD_MagicSquare.md) (v1.0 Draft, Implementation-Ready)

---

## 3. TDD Development Flow

| 단계 | 설명 |
|---|---|
| 1. Scenario | Level 1~5 시나리오를 RED 대상으로 선정 |
| 2. Acceptance Criteria | FR/BR 기반으로 통과 조건을 테스트 가능 문장으로 고정 |
| 3. RED Test ID | `RED-BND-*`, `RED-DOM-*` 등 추적 ID 부여 |
| 4. Test Skeleton | pytest AAA 스켈레톤 작성 (구현 없이 실패 유도) |
| 5. Run Test | `pytest` 실행 |
| 6. Confirm Failure (RED) | **미구현**으로 인한 실패인지 확인 (깨진 테스트 아님) |
| 7. GREEN Task Candidate | 해당 RED를 통과시킬 **최소 구현** 후보만 기록 |
| 8. REFACTOR Candidate | GREEN 이후 구조 개선 후보만 기록 (계약 변경 금지) |

---

## 4. Development Methodology

### 4.1 Dual-Track TDD

| Track | 초점 | RED 예시 |
|---|---|---|
| **Track A (Boundary)** | 입력 계약, 오류 응답, Domain 미호출, 출력 스키마 | `RED-BND-001` ~ `007` |
| **Track B (Domain/Logic)** | 빈칸·누락 숫자·마방진 검증·Solver | `RED-DOM-001` ~ `010` |

- UI( Boundary ) RED와 Logic RED는 **테스트 파일·실패 원인을 분리**한다.
- Track A·B를 **교차 진행**한다 (Domain 전체 구현 후 Boundary 연결 금지).

### 4.2 ECB Architecture

- **Entity:** 도메인 규칙·불변식 (`BlankFinder`, `MagicSquareValidator`, `Solver` 등)
- **Control:** 유스케이스 오케스트레이션 (DN-02: 필수 여부 미확정)
- **Boundary:** 외부 I/O, 입력 검증, 결과 포맷 (`BoundaryValidator`, `ResultFormatter`)

**의존 방향:** `boundary → control → entity` (역방향 금지)

### 4.3 Traceability

Concept → Rule (BR) → Functional Requirement (FR) → Acceptance Criteria → RED Test ID → Component Candidate

### 4.4 RED → GREEN → REFACTOR

1. **RED:** 실패 상태 확인  
2. **GREEN:** 최소 구현으로 해당 RED만 통과  
3. **REFACTOR:** GREEN 유지하며 구조만 개선 (외부 계약 불변)

---

## 5. ECB Role Separation

| Layer | 책임 | Magic Square 컴포넌트 후보 |
|---|---|---|
| **Boundary** | 입력 검증, 오류 매핑, 성공 `int[6]` 포맷, 외부 I/O | `BoundaryValidator`, `ResultFormatter` |
| **Control** | 검증 통과 후 Domain 파이프라인 조율 | (DN-02 확정 후) |
| **Entity (Domain)** | 빈칸·누락 숫자·마방진 판정·두 조합 Solver | `BlankFinder`, `MissingNumberFinder`, `MagicSquareValidator`, `Solver` |

| 규칙 | 내용 |
|---|---|
| BR-05 | Boundary 검증 실패 시 Domain resolver **0회** 호출 |
| NFR-06 | Domain은 Boundary/UI/DB/Web에 **비의존** |

---

## 6. Scenario → AC → RED Tracking Board

필수 Scenario **15건** + 통합 관련 **2건** = **17행** (Task ID 없음, Scenario 중심).

| # | Scenario ID | 설명 | Acceptance Criteria (요약) | RED Test ID | ECB Layer | Status |
|---|---|---|---|---|---|---|
| 1 | SC-BND-001 | `None` 입력 | Domain 미호출, 구조화 오류 | RED-BND-001 | Boundary | ✅ RED |
| 2 | SC-BND-002 | 4×4가 아닌 입력 | `UI-ERR-001`, Domain 0회 | RED-BND-002 | Boundary | ✅ RED |
| 3 | SC-BND-003 | 빈칸 개수 오류 | `UI-ERR-003`, Domain 0회 | RED-BND-003 | Boundary | ✅ RED |
| 4 | SC-BND-004 | 값 범위 오류 | `UI-ERR-002`, Domain 0회 | RED-BND-004 | Boundary | ✅ RED |
| 5 | SC-BND-005 | 중복 숫자 오류 | `UI-ERR-004`, Domain 0회 | RED-BND-005 | Boundary | ✅ RED |
| 6 | SC-DOM-001 | 빈칸 row-major 탐색 | 2개 좌표, 0-index, row-major | RED-DOM-001 | Entity | ✅ RED |
| 7 | SC-DOM-003 | 누락 숫자 오름차순 | `[smaller, larger]`, `0` 제외 | RED-DOM-003 | Entity | ✅ RED |
| 8 | SC-DOM-004 | 모든 행 합 34 | 행 조건 true/false | RED-DOM-004 | Entity | ✅ RED |
| 9 | SC-DOM-005 | 모든 열 합 34 | 열 조건 true/false | RED-DOM-005 | Entity | ✅ RED |
| 10 | SC-DOM-006 | 두 대각선 합 34 | 대각선 조건 true/false | RED-DOM-006 | Entity | ✅ RED |
| 11 | SC-DOM-008 | small-first 성공 | Attempt 1만으로 `int[6]` | RED-DOM-008 | Entity | ✅ RED |
| 12 | SC-DOM-009 | reverse 성공 | Attempt 2로 `[3,3,6,4,4,1]` 등 | RED-DOM-009 | Entity | ✅ RED |
| 13 | SC-DOM-010 | 두 조합 모두 실패 | `DOMAIN-ERR-NO_VALID_PLACEMENT` | RED-DOM-010 | Entity | ✅ RED |
| 14 | SC-BND-006 | 결과 배열 길이 6 | `len(result) == 6` | RED-BND-006 | Boundary | ✅ RED |
| 15 | SC-BND-007 | 반환 좌표 1-index | 각 좌표 ∈ [1, 4] | RED-BND-007 | Boundary | ✅ RED |
| 16 | SC-INT-001 | Boundary 실패 시 Domain 미호출 | resolver call count = 0 | RED-INT-001 | Integration | ✅ RED |
| 17 | SC-INT-002 | End-to-end (검증 통과 → Solver) | FR-01~05 파이프라인 | RED-INT-002 | Integration | ✅ RED |

> PRD·Report/06는 `RED-BND-VAL-*`, `RED-DOM-BLK-*` 등 **상세 RED ID**를 병행 사용한다. 본 보드 ID는 TDD 시작 보드(Report/08) 기준이다.

---

## 7. RED Start Checklist

RED 사이클 시작 전 아래 **11항목**을 확인한다.

- [x] **1.** [`docs/PRD_MagicSquare.md`](docs/PRD_MagicSquare.md) 검토 (FR-01~05, BR-01~15, §12~13, §15 Dual-Track, §16 Test Plan, §21 Traceability)
- [x] **2.** Report/02 (Invariant·I/O Contract), Report/03 (ECB·pytest), Report/06 (Scenario ID) 확인
- [x] **3.** `.cursor/rules/*.mdc` — TDD·ECB·forbidden 규칙 숙지
- [x] **4.** RED = **미구현으로 인한 실패 확인** (테스트 자체 오류 아님)
- [x] **5.** Dual-Track 분리: Boundary RED / Logic RED **파일·실패 원인 분리**
- [x] **6.** ECB 의존 방향 `boundary → control → entity` 준수
- [x] **7.** §6 Tracking Board — 필수 Scenario ↔ RED Test ID 매핑 완료
- [x] **8.** `tests/` · `src/` 레이어 병렬 구조 (`boundary`, `control`, `entity`) 준비
- [ ] **9.** `pyproject.toml` — **미작성** (GREEN 단계에서 pytest·coverage gate 추가 예정)
- [x] **10.** Open Questions **DN-01~03** 인지 (envelope, Control 필수 여부, both-fail fixture)
- [x] **11.** Full RED 대상 작성 완료 — R0~R6 배치 (`test_ac_fr_01_01_*`, `test_u_*`, `test_d_*`) → pytest **25 failed, 37 passed** 확인

**다음 단계:** [RED 커밋 배치 계획](#red-커밋-배치-계획-dual-track-full-red)에 따라 **R1 GREEN**부터 순차 구현.

---

## RED 단계 To-Do 리스트

<!-- GitHub Task List: 저장소 README를 GitHub에서 열면 체크박스를 클릭해 [x]로 바꿀 수 있습니다. -->

이 체크리스트는 [`docs/test_plan.md`](docs/test_plan.md) · Report/10 기반입니다. **RED**(실패 테스트 작성) 완료 시 항목을 체크합니다.

| 사용 환경 | 체크 방법 |
|---|---|
| **GitHub** (권장) | 저장소에서 `README.md` 열기 → 체크박스 클릭 → 변경 사항 커밋 |
| **Cursor / VS Code** | 미리보기 또는 편집기에서 `- [ ]`를 `- [x]`로 직접 수정 후 저장 |

### Track A — UI / Boundary 테스트 (AC-FR-01-01 SIZE — R0)
- [x] TC-A-01: grid=None 입력 → 실패 결과 반환 (Happy Path of Failure)
- [x] TC-A-02: code가 정확히 "INVALID_SIZE" 문자열인지 검증
- [x] TC-A-03: message가 "Grid must be 4x4." 와 문자 단위 동일한지 검증
- [x] TC-A-04: grid=None 시 Domain 진입점 0회 호출 (mock/spy 검증)
- [x] TC-A-05: grid=[] 빈 리스트 → 실패 결과 반환
- [x] TC-A-06: grid=3×4 크기 불일치 → 실패 결과 반환
- [x] TC-A-07: 반환 객체 타입이 지정 실패 결과 구조체인지 검증

### Track A — UI / Boundary 테스트 (FR-01 확장 — R1~R3, R6)
- [x] TC-A-08: U-IN-04~05 빈칸 개수 위반 → `INVALID_BLANK_COUNT` (Full RED)
- [x] TC-A-09: U-IN-06~07 값 범위 위반 → `INVALID_RANGE` (Full RED)
- [x] TC-A-10: U-IN-08 중복 non-zero → `INVALID_DUPLICATE` (Full RED)
- [x] TC-A-11: U-FLOW-02a~d invalid 입력 시 Domain resolver 0회 (Full RED)
- [x] TC-A-12: U-OUT-01~03 성공 출력 `int[6]` 계약 (Full RED)

### Track B — Domain / Logic 격리 (AC-FR-01-01)
- [x] TC-B-01: resolve()가 None grid를 직접 받지 않음을 격리 검증
- [x] TC-B-02: Boundary가 None 분기를 처리 후 resolve() 미호출 확인
- [x] TC-B-03: resolve() mock이 호출됐을 경우 테스트 실패 처리
- [x] TC-B-04: AC-FR-01-02~05 범위의 케이스는 이 커밋에 포함하지 않음 확인

### Track B — Domain / Logic (FR-02~05 — R4, R5)
- [x] TC-B-05: D-LOC-01 G1 빈칸 좌표 row-major (Full RED)
- [x] TC-B-06: D-MIS-01 G1 누락 숫자 `[1, 16]` 오름차순 (Full RED)
- [x] TC-B-07: D-VAL-01~06 마방진 검증 true/false (Full RED)
- [x] TC-B-08: D-SOL-01~04 Solver Attempt 1/2/both-fail (Full RED)

### Fixture SSOT
- [x] G0~G3 및 PRD §16.4 invalid matrix fixture (`tests/conftest.py`)

### 커버리지 목표 *(GREEN 단계 gate — RED 범위 외)*
- [ ] Domain Logic: 95%+ (pip install pytest-cov)
- [ ] Boundary Layer: 85%+
- [ ] 전체 TOTAL: 90%+

### 결함 목록 연결
- [x] defect_list.md 생성 및 발견 결함 기록
- [x] 모든 결함 수정 후 회귀 테스트 통과 확인

---

## RED 커밋 배치 계획 (Dual-Track Full RED)

Report/10 기준으로 RED 테스트를 **배치(R0~R6)** 단위로 커밋하고, 각 배치 GREEN 후 다음 배치로 진행한다.

| 배치 | 커밋 메시지 예시 | Test ID | 건수 | 파일 | RED 상태 |
|:---:|---|---:|---:|---|:---:|
| **R0** | `test(red): AC-FR-01-01 SIZE validation suite` | U-IN-01~03 | 30 | `test_ac_fr_01_01_*.py` | ✅ GREEN |
| **R1** | `test(red): U-IN-04~05 blank count validation` | U-IN-04, U-IN-05 | 2 | `test_u_in_validation.py` | ✅ RED |
| **R2** | `test(red): U-IN-06~07 range validation` | U-IN-06, U-IN-07 | 2 | `test_u_in_validation.py` | ✅ RED |
| **R3** | `test(red): U-IN-08 duplicate validation` | U-IN-08 | 1 | `test_u_in_validation.py` | ✅ RED |
| **R4** | `test(red): Track B entity FR-02~04` | D-LOC-01, D-MIS-01, D-VAL-01~06 | 8 | `test_d_loc/mis/val_*.py` | ✅ RED |
| **R5** | `test(red): Track B solver FR-05` | D-SOL-01~04 | 4 | `test_d_sol_solution.py` | ✅ RED |
| **R6** | `test(red): U-OUT + U-FLOW extended` | U-OUT-01~03, U-FLOW-02a~d | 7 | `test_u_out_*.py`, `test_u_flow_*.py` | ✅ RED |

> **RED 단계 완료 확인:** `pytest tests/boundary/ tests/entity/` → **62 collected, 37 passed, 25 failed**. 실패 원인 = 미구현(요구사항 부재), 테스트 오류 아님. U-FLOW-02a/b는 R0 GREEN.

**권장 GREEN 순서:** R1 → R2 → R3 → R4 → R5 → R6

### RED 완료 회귀 명령

```bash
pytest tests/boundary/ tests/entity/ -q
# 기대: 37 passed, 25 failed (R1~R6 미구현)
```

---

## 8. Quality Gates

| Gate | 기준 | 검증 |
|---|---|---|
| Domain coverage | line+branch **≥ 95%** | pytest-cov (NFR-01, ESC-01) |
| Boundary coverage | contract **≥ 85%** | pytest-cov (NFR-02) |
| Global coverage | **≥ 80%** | `.cursorrules` (NFR-09) |
| Boundary pass rate | 계약 테스트 **100%** | ESC-02 |
| Test style | pytest, **Arrange–Act–Assert** | `.cursor/rules/magicsquare-tdd-testing.mdc` |
| Forbidden | `print()` 디버깅, bare `except`, 매직 넘버, 테스트 약화, TDD RED 생략 | `.cursor/rules/magicsquare-forbidden.mdc` |

---

## 9. Reference Documents

| 문서 | 경로 | 역할 |
|---|---|---|
| PRD | [`docs/PRD_MagicSquare.md`](docs/PRD_MagicSquare.md) | FR/BR, 계약, Dual-Track, Test Plan, Traceability |
| Test Plan (RED) | [`docs/test_plan.md`](docs/test_plan.md) | AC-FR-01-01, 경계값·mock 전략, 커버리지 gate |
| 문제 정의 | [`Report/01.4x4_MagicSquare_Problem_Definition_Report.md`](Report/01.4x4_MagicSquare_Problem_Definition_Report.md) | 문제 인식·불변식 프레이밍 |
| TDD 설계 | [`Report/02.4x4_MagicSquare_TDD_Design_Report.md`](Report/02.4x4_MagicSquare_TDD_Design_Report.md) | Invariant, I/O Contract, RED 우선 테스트 설계 |
| Cursor Rules 구현 | [`Report/03.4x4_MagicSquare_CursorRules_UserEntity_Implementation_Report.md`](Report/03.4x4_MagicSquare_CursorRules_UserEntity_Implementation_Report.md) | ECB 샘플, pytest/AAA, coverage |
| Scenario 검증 | [`Report/06.MagicSquare_Level1-5_Scenario_Verification_Report.md`](Report/06.MagicSquare_Level1-5_Scenario_Verification_Report.md) | Level 1~5 Scenario ID 백로그 |
| TDD 시작 준비 | [`Report/08.MagicSquare_TDD_Startup_ToDo_README_Report.md`](Report/08.MagicSquare_TDD_Startup_ToDo_README_Report.md) | To-Do List·README 준비 보고서 |
| AC-FR-01-01 RED→GREEN | [`Report/09.MagicSquare_AC_FR_01_01_RED_GREEN_Report.md`](Report/09.MagicSquare_AC_FR_01_01_RED_GREEN_Report.md) | SIZE 검증 테스트·구현·결함 보고서 |
| Dual-Track RED Skeleton | [`Report/10.MagicSquare_DualTrack_RED_Design_And_Skeleton_Report.md`](Report/10.MagicSquare_DualTrack_RED_Design_And_Skeleton_Report.md) | RED 설계표·스켈레톤 24건·Prompt 통합 |
| 결함 목록 | [`docs/defect_list.md`](docs/defect_list.md) | DEF-001~005 (Resolved) |
| Cursor Rules | [`.cursor/rules/`](.cursor/rules/) | Quality Gates, ECB, TDD, forbidden |
| Transcript (시작 준비) | [`Prompt/08.MagicSquare_TDD_Startup_Transcript.md`](Prompt/08.MagicSquare_TDD_Startup_Transcript.md) | TDD 시작 준비 세션 기록 |
| Transcript (AC-FR-01-01) | [`Prompt/09.MagicSquare_AC_FR_01_01_Transcript.md`](Prompt/09.MagicSquare_AC_FR_01_01_Transcript.md) | AC-FR-01-01 RED→GREEN 세션 기록 |
| Transcript (Dual-Track RED) | [`Prompt/10.MagicSquare_DualTrack_RED_Design_And_Skeleton_Transcript.md`](Prompt/10.MagicSquare_DualTrack_RED_Design_And_Skeleton_Transcript.md) | RED 설계·스켈레톤·Prompt 통합 세션 |

### 문서 간 관계

```
Report/01 (문제 정의)
    ↓
Report/02 (TDD 설계·계약) ──→ docs/PRD_MagicSquare.md
    ↓                              ↓
Report/06 (Scenario 검증)    Report/08 (TDD 시작 준비)
    ↓                              ↓
Report/03 (ECB·pytest 규칙) ──→ README.md (본 문서)
    ↓
src/ + tests/  ←── RED → GREEN → REFACTOR
```

---

## 10. Current Project Status

| 항목 | 상태 |
|---|---|
| PRD | `docs/PRD_MagicSquare.md` v1.0 Draft — Implementation-Ready |
| 개발 To-Do List | Turn 1 작성 완료 — **파일 미저장** (선택: `docs/TDD_Development_ToDo_List.md`) |
| MagicSquare 구현 | **진행 중** — R0 SIZE GREEN; R1~R6 GREEN 대기 |
| MagicSquare 테스트 | **RED 완료** — 62 collected (R0 GREEN 30 + Full RED 25 failed + sample 7) |
| `docs/defect_list.md` | DEF-001~005 기록, Open 0건 |
| `pyproject.toml` | **미작성** — GREEN 단계 coverage gate 추가 예정 |
| 현재 단계 | **RED 완료 → GREEN 시작 (R1: U-IN-04~05 blank count)** |

### 권장 GREEN 순서

1. **R1 GREEN** — `BoundaryValidator` ZERO COUNT 분기 (`U-IN-04~05`)
2. **R2 GREEN** — RANGE 분기 (`U-IN-06~07`)
3. **R3 GREEN** — DUPLICATE 분기 (`U-IN-08`)
4. **R4 GREEN** — Entity FR-02~04 (`BlankFinder`, `MissingNumberFinder`, `MagicSquareValidator`)
5. **R5 GREEN** — Entity FR-05 (`TwoCellSolver`)
6. **R6 GREEN** — U-OUT + U-FLOW-02c/d 통합
7. **`pyproject.toml`** — pytest-cov gate 설정
8. **DN-01~03** 확정 후 PRD v1.1 개정

### Open Questions (PRD §22)

| ID | Topic | 현재 기준 |
|---|---|---|
| DN-01 | 성공 응답 envelope | bare `int[6]` |
| DN-02 | Control Layer 필수 여부 | To-Do에 Control Integration 포함, README는 Scenario 중심 |
| DN-03 | Both-fail fixture | G3 placeholder in `tests/conftest.py` — GREEN 시 검증·확정 |

---

## 한 줄 결론

이 프로젝트의 본질은 **정답 1개 산출**이 아니라, **불변식과 계약으로 설명 가능한 코드**를 Dual-Track TDD로 만드는 것이다.  
**RED 단계 완료** — 다음: **R1 GREEN** (`BoundaryValidator` blank count 분기 최소 구현).
