# Magic Square 4×4 — TDD Practice

## 1. Project Start Declaration

본 프로젝트는 **PRD 기반 Dual-Track TDD**로 Magic Square 4×4를 구현하는 학습형 연습이다.  
현재 단계는 **TDD 시작 준비 완료**이며, 구현·테스트 코드 작성 전에 본 README를 기준으로 RED 사이클을 시작한다.

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
| 1 | SC-BND-001 | `None` 입력 | Domain 미호출, 구조화 오류 | RED-BND-001 | Boundary | ⬜ RED |
| 2 | SC-BND-002 | 4×4가 아닌 입력 | `UI-ERR-001`, Domain 0회 | RED-BND-002 | Boundary | ⬜ RED |
| 3 | SC-BND-003 | 빈칸 개수 오류 | `UI-ERR-003`, Domain 0회 | RED-BND-003 | Boundary | ⬜ RED |
| 4 | SC-BND-004 | 값 범위 오류 | `UI-ERR-002`, Domain 0회 | RED-BND-004 | Boundary | ⬜ RED |
| 5 | SC-BND-005 | 중복 숫자 오류 | `UI-ERR-004`, Domain 0회 | RED-BND-005 | Boundary | ⬜ RED |
| 6 | SC-DOM-001 | 빈칸 row-major 탐색 | 2개 좌표, 0-index, row-major | RED-DOM-001 | Entity | ⬜ RED |
| 7 | SC-DOM-003 | 누락 숫자 오름차순 | `[smaller, larger]`, `0` 제외 | RED-DOM-003 | Entity | ⬜ RED |
| 8 | SC-DOM-004 | 모든 행 합 34 | 행 조건 true/false | RED-DOM-004 | Entity | ⬜ RED |
| 9 | SC-DOM-005 | 모든 열 합 34 | 열 조건 true/false | RED-DOM-005 | Entity | ⬜ RED |
| 10 | SC-DOM-006 | 두 대각선 합 34 | 대각선 조건 true/false | RED-DOM-006 | Entity | ⬜ RED |
| 11 | SC-DOM-008 | small-first 성공 | Attempt 1만으로 `int[6]` | RED-DOM-008 | Entity | ⬜ RED |
| 12 | SC-DOM-009 | reverse 성공 | Attempt 2로 `[3,3,6,4,4,1]` 등 | RED-DOM-009 | Entity | ⬜ RED |
| 13 | SC-DOM-010 | 두 조합 모두 실패 | `DOMAIN-ERR-NO_VALID_PLACEMENT` | RED-DOM-010 | Entity | ⬜ RED |
| 14 | SC-BND-006 | 결과 배열 길이 6 | `len(result) == 6` | RED-BND-006 | Boundary | ⬜ RED |
| 15 | SC-BND-007 | 반환 좌표 1-index | 각 좌표 ∈ [1, 4] | RED-BND-007 | Boundary | ⬜ RED |
| 16 | SC-INT-001 | Boundary 실패 시 Domain 미호출 | resolver call count = 0 | RED-INT-001 | Integration | ⬜ RED |
| 17 | SC-INT-002 | End-to-end (검증 통과 → Solver) | FR-01~05 파이프라인 | RED-INT-002 | Integration | ⬜ RED |

> PRD·Report/06는 `RED-BND-VAL-*`, `RED-DOM-BLK-*` 등 **상세 RED ID**를 병행 사용한다. 본 보드 ID는 TDD 시작 보드(Report/08) 기준이다.

---

## 7. RED Start Checklist

RED 사이클 시작 전 아래 **11항목**을 확인한다.

- [ ] **1.** [`docs/PRD_MagicSquare.md`](docs/PRD_MagicSquare.md) 검토 (FR-01~05, BR-01~15, §12~13, §15 Dual-Track, §16 Test Plan, §21 Traceability)
- [ ] **2.** Report/02 (Invariant·I/O Contract), Report/03 (ECB·pytest), Report/06 (Scenario ID) 확인
- [ ] **3.** `.cursor/rules/*.mdc` — TDD·ECB·forbidden 규칙 숙지
- [ ] **4.** RED = **미구현으로 인한 실패 확인** (테스트 자체 오류 아님)
- [ ] **5.** Dual-Track 분리: Boundary RED / Logic RED **파일·실패 원인 분리**
- [ ] **6.** ECB 의존 방향 `boundary → control → entity` 준수
- [ ] **7.** §6 Tracking Board — 필수 Scenario ↔ RED Test ID 매핑 완료
- [ ] **8.** `tests/` · `src/` 레이어 병렬 구조 (`boundary`, `control`, `entity`) 준비
- [ ] **9.** `pyproject.toml` — **미작성** (후속 RED 단계에서 pytest·coverage gate 추가)
- [ ] **10.** Open Questions **DN-01~03** 인지 (envelope, Control 필수 여부, both-fail fixture)
- [ ] **11.** 첫 RED 대상 선정 — 권장: **`RED-BND-002`** (4×4 아님) Test Skeleton → pytest → RED 실패 확인

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
| 문제 정의 | [`Report/01.4x4_MagicSquare_Problem_Definition_Report.md`](Report/01.4x4_MagicSquare_Problem_Definition_Report.md) | 문제 인식·불변식 프레이밍 |
| TDD 설계 | [`Report/02.4x4_MagicSquare_TDD_Design_Report.md`](Report/02.4x4_MagicSquare_TDD_Design_Report.md) | Invariant, I/O Contract, RED 우선 테스트 설계 |
| Cursor Rules 구현 | [`Report/03.4x4_MagicSquare_CursorRules_UserEntity_Implementation_Report.md`](Report/03.4x4_MagicSquare_CursorRules_UserEntity_Implementation_Report.md) | ECB 샘플, pytest/AAA, coverage |
| Scenario 검증 | [`Report/06.MagicSquare_Level1-5_Scenario_Verification_Report.md`](Report/06.MagicSquare_Level1-5_Scenario_Verification_Report.md) | Level 1~5 Scenario ID 백로그 |
| TDD 시작 준비 | [`Report/08.MagicSquare_TDD_Startup_ToDo_README_Report.md`](Report/08.MagicSquare_TDD_Startup_ToDo_README_Report.md) | To-Do List·README 준비 보고서 |
| Cursor Rules | [`.cursor/rules/`](.cursor/rules/) | Quality Gates, ECB, TDD, forbidden |
| Transcript | [`Prompting/08.MagicSquare_TDD_Startup_Transcript.md`](Prompting/08.MagicSquare_TDD_Startup_Transcript.md) | TDD 시작 준비 세션 기록 |

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
| MagicSquare 구현 | **미시작** (`src/entity/user.py` ECB 샘플만 존재) |
| MagicSquare 테스트 | **미시작** (`tests/entity/test_user.py` 샘플만 존재) |
| `pyproject.toml` | **미작성** — RED 단계에서 추가 예정 |
| 현재 단계 | **TDD RED 시작 직전** |

### 권장 RED 시작 순서

1. **`pyproject.toml`** — pytest, coverage gate 설정  
2. **`RED-BND-002`** — 4×4 아님 Test Skeleton → pytest → RED 실패 확인  
3. **Track A:** `RED-BND-001` ~ `005` (Boundary 입력 검증)  
4. **Track B:** `RED-DOM-001` ~ (Domain 로직) — Track A와 **교차 진행**  
5. **`RED-DOM-010`** — both-fail fixture 확정 (**DN-03**)  
6. **DN-01~03** 확정 후 PRD v1.1 개정

### Open Questions (PRD §22)

| ID | Topic | 현재 기준 |
|---|---|---|
| DN-01 | 성공 응답 envelope | bare `int[6]` |
| DN-02 | Control Layer 필수 여부 | To-Do에 Control Integration 포함, README는 Scenario 중심 |
| DN-03 | Both-fail fixture | `RED-DOM-010` / SC-DOM-010 — RED 단계에서 fixture 고정 필요 |

---

## 한 줄 결론

이 프로젝트의 본질은 **정답 1개 산출**이 아니라, **불변식과 계약으로 설명 가능한 코드**를 Dual-Track TDD로 만드는 것이다.  
다음 단계: **Test Skeleton 작성 → pytest 실행 → RED 실패 상태 확인**.
