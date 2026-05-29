# Magic Square 4×4 — TDD Practice

**바로가기:** [RED 단계 To-Do 리스트](#red-단계-to-do-리스트) · [REFACTOR 단계 To-Do](#refactor-단계-to-do-리스트) · [REFACTOR 유형·우선순위](#refactor-유형별-분류--우선순위) · [ECB 레이어 분리](#ecb-레이어-분리-프롬프트--src-매핑) · [QA 코드 스멜 (Control/Boundary)](#p2--qa-코드-스멜-controlboundary) · [RED 커밋 배치 계획](#red-커밋-배치-계획-dual-track-full-red) · [RED Start Checklist](#7-red-start-checklist)

## 1. Project Start Declaration

본 프로젝트는 **PRD 기반 Dual-Track TDD**로 Magic Square 4×4를 구현하는 학습형 연습이다.  
현재 단계는 **GREEN 완료 (R0~R8)** — Dual-Track 62건 + Golden Master 6건 PASS. **다음: REFACTOR** (계약 불변, 구조 개선).

| 용어 | 정의 |
|---|---|
| **RED** | 테스트 실패 상태를 **확인**하는 단계 (미구현으로 인한 기대 실패) |
| **GREEN** | RED 실패를 통과시키기 위한 **최소 구현 작업 후보**만 기술 (본 README에서는 실행하지 않음) |
| **REFACTOR** | GREEN 이후 **구조 개선** (외부 I/O 계약·Golden Master 불변) |

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
- **Control:** 유스케이스 오케스트레이션 (`SolveUseCase`, `src/control/ports.py`)
- **Boundary:** 외부 I/O, 입력 검증, 결과 포맷 (`BoundaryValidator`, PyQt `screen/`)
- **Contracts:** 레이어 공유 상수·오류 DTO (`src/contracts/`)
- **Bootstrap:** composition root (`src/bootstrap.py`)

**의존 방향:** `boundary → control → entity` (역방향 금지; 공유는 `contracts`만)

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
- [x] **9.** `pyproject.toml` — pytest·coverage gate (≥80%) 작성 완료
- [x] **10.** Open Questions **DN-01~03** 확정 (envelope, Control, G3 both-fail)
- [x] **11.** Full RED 대상 작성 완료 — R0~R6 배치 (`test_ac_fr_01_01_*`, `test_u_*`, `test_d_*`) → pytest **25 failed, 37 passed** 확인

**다음 단계:** **REFACTOR** — § [REFACTOR 단계 To-Do](#refactor-단계-to-do-리스트) P1 테스트 보강 후 레이어별 구조 개선 (계약·Golden Master 불변).

---

## RED 단계 To-Do 리스트

### Golden Master 회귀 안전장치

Refactoring 시작 전 구축.  
GREEN 완료 후 즉시 적용.

#### 기준 파일 생성
- [x] GM-01: `golden_master_expected.txt` 생성
- [x] GM-02: 정상/역순/오류 시나리오 추가
- [x] GM-03: `git add tests/golden_master_expected.txt`

#### 테스트 코드
- [x] GM-04: `test_golden_master_magic_square` 작성
- [x] GM-05: approve 패턴 적용
- [x] GM-06: Golden Master 테스트 PASS 확인

#### 회귀 보호
- [x] GM-07: row-major 규칙 보호
- [x] GM-08: 1-index 출력 보호
- [x] GM-09: reverse 조합 fallback 보호
- [x] GM-10: Error Contract 보호

### REFACTOR 단계 To-Do 리스트

`.cursorrules` **refactor_phase** 기준: 외부 동작 불변 · 리팩터링 후 전체 pytest · coverage 유지(≥80%).  
**RED 스켈레톤(`pytest.fail`) 0건** — 리팩토링 전 추가 GREEN 불필요.

#### P0 — REFACTOR 전제 (구조·GUI)

- [x] RF-P0-01: `src/contracts/` 공유 상수·오류 DTO 분리 (`grid_constants`, `validation_errors`, `domain_errors`)
- [x] RF-P0-02: `src/control/ports.py` — `InputValidator` Protocol, `SolveResult` 타입
- [x] RF-P0-03: `SolveUseCase` — Boundary 직접 import 제거 (Protocol 주입)
- [x] RF-P0-04: `BoundaryValidator` — `entity.constants` 대신 `contracts` 사용
- [x] RF-P0-05: `src/bootstrap.py` composition root (GUI·테스트 wiring)
- [x] RF-P0-06: PyQt GUI 소스 복원 (`main_window`, `grid_input_widget`, `solve_presenter`, `sample_puzzles`)
- [x] RF-P0-07: `tests/test_architecture_imports.py` — ECB import guard
- [x] RF-P0-08: `tests/boundary/test_solve_presenter.py` — Presenter 5 시나리오
- [x] RF-P0-09: `tests/boundary/test_gui_smoke.py` — GUI import smoke (PyQt6 optional)

#### ECB 레이어 분리 (프롬프트 ↔ src 매핑)

`.cursorrules` ECB: **Boundary** = E001~E005·int[6]/Error 직렬화 · **Control** = locate→find→solve 오케스트레이션 · **Entity** = VO·Domain Service · **Screen** = 표시·입력·UIBoundary 호출.  
허용: `boundary→control`, `control→entity` / 금지: `entity→boundary|control`, `control→boundary`, Screen→Control/Entity 직접.

##### 프롬프트 파일 ↔ 실제 경로

| 프롬프트 (학습용) | 실제 경로 | ECB 역할 | 적합 |
|---|---|---|:---:|
| `domain.py` | `src/control/solve_use_case.py`, `ports.py` | Control | 적합 |
| `boundary.py` | `src/boundary/boundary_validator.py`, `contracts.py` | Boundary | 적합 |
| `ui_boundary.py` | `src/boundary/screen/solve_presenter.py` | Boundary (UI 어댑터) | 부분 |
| `gui/main_window.py` | `src/boundary/screen/main_window.py` | Screen | 부분 |
| (구) `input_validator.py` | `boundary_validator.py` | Boundary | — |
| (구) `two_cell_solver.py` | `entity/solver.py` `TwoCellSolver` | Entity | — |

> `solve_partial_magic_square.py` → **`SolveUseCase`(Control)**. locate/find/solve·Step A/B·int[6] 조립은 **Entity**에 분리됨.

##### ECB P0 — 레이어 위치·Screen 경계 (계약 E001~E007·int[6] 1순위)

- [ ] RF-ECB-P0-01: `entity/domain_resolver.py` → `src/control/` (`DomainResolverImpl` + Protocol → `ports.py`)
- [ ] RF-ECB-P0-02: `main_window` E006/E007 — 오류 타이틀·색·`QMessageBox` → `solve_presenter` 또는 Boundary UI mapper
- [ ] RF-ECB-P0-03: `main_window` — `bootstrap`/`SAMPLE_PUZZLES` 제거, `app.py` 단일 composition·Presenter 주입만

##### ECB P1 — 테스트 갭 연동 (REFACTOR 전 안전망)

| ECB 항목 | 연결 README | 내용 |
|---|---|---|
| RF-ECB-P1-01 | RF-P1-01 | Control `SolveUseCase` mock 단위 테스트 |
| RF-ECB-P1-02 | RF-P1-02 | Boundary 비정수 셀 → `INVALID_RANGE` (TypeError 방지) |
| RF-ECB-P1-03 | RF-P1-04 | Golden Master `INVALID_SIZE` / `INVALID_RANGE` |
| RF-ECB-P1-04 | RF-P1-03 | 입력 grid 불변성 (NFR-04) |
| RF-ECB-P1-05 | RF-P1-05 | GUI headless 동작 (Solve/Clear/샘플/오류) |
| RF-ECB-P1-06 | RF-P2-H01~H03 | int[6]·`GridInputWidget` 스키마 가드 (U-OUT·UI) |

**REFACTOR 1순위 (한 줄):** E001~E007·int[6] 유지 — `DomainResolver` Control 이전 + Screen↔UIBoundary(`solve_presenter`) 경계 정리.

**테스트 없이 ECB 분리 금지 (한 줄):** refactor_phase는 동작·coverage 불변 전제인데, Screen·Control 경계는 P1/ECB-P1 테스트 없이 구조만 바꾸면 회귀를 pytest가 잡지 못함.

#### P1 — 테스트 보강 (REFACTOR 안전망)

- [ ] RF-P1-01: `tests/control/test_solve_use_case.py` — mock validator/resolver 단위 테스트
- [ ] RF-P1-02: Boundary 비정수 셀 검증 + 테스트 (`"5"`, `1.5` → `INVALID_RANGE`, `TypeError` 방지)
- [ ] RF-P1-03: 입력 grid 불변성 테스트 (PRD NFR-04 — `execute` 전후 deep equality)
- [ ] RF-P1-04: Golden Master — `INVALID_SIZE`, `INVALID_RANGE` 시나리오 추가
- [ ] RF-P1-05: GUI 동작 테스트 (headless Qt) — Solve/Clear/샘플 로드/오류 표시
- [ ] RF-P1-06: `integrated_solve_use_case` fixture 중복 제거 (`conftest.py` 단일 SSOT)

#### P2 — 구조 REFACTOR (GREEN·GM 유지)

- [ ] RF-P2-01: `DomainResolver` Protocol → `control/ports.py` 이동 검토
- [ ] RF-P2-02: `SolveUseCase.execute` / resolver 반환 타입 `Any` → `SolveResult` 정리
- [ ] RF-P2-03: `boundary/contracts.py` re-export → import 경로 일원화 후 deprecate
- [ ] RF-P2-04: `entity/user.py` 스캐폴드 정리 (Magic Square 범위 외)

#### P2 — QA 코드 스멜 (Control/Boundary)

QA 엔지니어 점검 기준: `src/control/*`, `src/boundary/*` (Screen UI 포함).  
참조 결합만 기록: 구 `input_validator.py` → `boundary_validator.py`, 구 `two_cell_solver.py` → `entity/solver.py` `TwoCellSolver`.

##### P2-H — High (계약 E001~E005 · int[6] 회귀 위험)

- [ ] RF-P2-H01: **`ResultFormatter` 역할** — `SolvePresenter` 성공 분기에서 int[6] length=6·coords∈[1,4] 검증 (U-OUT Boundary enforcement; PRD §12.2)
- [ ] RF-P2-H02: **`GridInputWidget.set_grid`** — `GRID_SIZE` 검증 추가 (비4×4 입력 시 IndexError 방지)
- [ ] RF-P2-H03: **`GridInputWidget.apply_solution` / `highlight_placements`** — placement 스키마 가드 (malformed int[6] → UI 오류 표시)
- [ ] RF-P2-H04: **`SolveUseCase.execute`** — `grid: Any` → `list[list[int]]` (FR-01 입력 계약 타입 복원)

##### P2-M — Medium (DRY · SSOT · 가독성)

- [ ] RF-P2-M01: int[6] `[r1,c1,n1,r2,c2,n2]` 언팩·1-index 변환 단일 helper (`SOLUTION_LENGTH=6` SSOT 공유)
- [ ] RF-P2-M02: `BoundaryValidator` — `_is_range_invalid` / `_is_blank_count_invalid` / `_is_duplicate_invalid` 단일 순회 통합
- [ ] RF-P2-M03: Screen→`bootstrap` 직접 import 제거 — `app.py` 단일 composition root, `MainWindow(presenter=…)` 필수 주입
- [ ] RF-P2-M04: `main_window` 힌트 `"1–16"` → `MIN_VALUE`/`MAX_VALUE` SSOT 사용
- [ ] RF-P2-M05: `main_window._build_ui` / `_show_error`, `grid_input_widget._build_ui` 분리 (본문 ≤20줄)
- [ ] RF-P2-M06: `DomainResolver` Protocol → `control/ports.py` 이동 (Control inversion 대칭)
- [ ] RF-P2-M07: `validation_errors` 메시지 `"4x4"`, `"2"`, `"1-16"` ↔ `grid_constants` 문자열 SSOT 연동

##### P2-L — Low (스타일 · Dead code)

- [ ] RF-P2-L01: 미사용 `_ERROR_STYLE` / `highlight_placements(is_error=True)` 제거 또는 domain-error 하이라이트 연결
- [ ] RF-P2-L02: `SolveResult` union type alias 명명 개선 (Result 객체와 혼동 방지)

##### QA 코드 스멜 요약표

| 파일 | 줄 | 스멜 | 우선순위 |
|---|---|---|---|
| `boundary/screen/solve_presenter.py` | 71–74 | int[6] 검증 없이 SuccessOutcome 통과 | **High** |
| `boundary/screen/grid_input_widget.py` | 83–88, 117–126 | set_grid/apply_solution 스키마 미검증 | **High** |
| `boundary/screen/main_window.py` | 135–136 | int[6] 3중 소비·검증 없음 | **High** |
| `control/solve_use_case.py` | 23, 32 | `execute(grid: Any)` 타입 소실 | **High** |
| `boundary/boundary_validator.py` | 57–86 | full-grid 순회 3회 중복 | Medium |
| `boundary/screen/main_window.py` | 47–100, 148–177 | `_build_ui`·`_show_error` 장함수 | Medium |
| `entity/solver.py` (참조) | 10, 65–72 | `SOLUTION_LENGTH` 미사용·int[6] 형식 Boundary 중복 | Medium |

> **점검 제외(해당 없음):** 예외 제어 흐름 오용, 불필요한 주석, 긴 매개변수 목록(>3) — 대상 파일 전체.

#### 레이어별 REFACTOR 준비도

| 레이어 | REFACTOR | 비고 |
|---|---|---|
| `src/entity/*` | **가능** | `test_d_*` + Golden Master |
| `src/control/*` | **가능** | boundary/Golden Master 간접 보호; P1-01 권장 |
| `src/boundary/*` (core) | **가능** | `test_u_*`, `test_ac_fr_*`, presenter |
| `src/boundary/screen/*` | **P2-H 후** | smoke만 있음; P2-H01~H03(int[6]·UI 가드) 선행 권장 |

#### REFACTOR 회귀 명령

```bash
pytest tests/ -q --cov=src --cov-fail-under=80
pytest -m golden_master -v
pytest tests/test_architecture_imports.py -q
```

#### REFACTOR 유형별 분류 · 우선순위

미완료 REFACTOR 항목을 **유형별**로 묶고, 실행 **우선순위** 순으로 정렬한다.  
상세 분석: [`Report/16.MagicSquare_REFACTOR_Classification_Priority_Report.md`](Report/16.MagicSquare_REFACTOR_Classification_Priority_Report.md)

##### 전체 우선순위 요약

| 순위 | 단계 | 유형 | 핵심 목적 |
|:---:|---|---|---|
| 1 | **P1** | 테스트/회귀 보호 | REFACTOR 전 안전망 — ECB·Screen 분리 전 필수 |
| 2 | **P2-H** | 계약·타입 강화 | E001~E005·int[6] 회귀 위험 제거 |
| 3 | **ECB P0** | ECB 레이어 분리 | `DomainResolver` Control 이전 + Screen↔Presenter 경계 |
| 4 | **P2** | 구조 개선 | 타입·import·dead scaffold 정리 |
| 5 | **P2-M** | DRY·SSOT·가독성 | 중복 제거, composition root, 함수 분리 |
| 6 | **P2-L** | 스타일·Dead code | 미사용 코드·명명 개선 |
| 7 | *(부가)* | 품질 게이트 | 커버리지 목표 (RED 체크리스트 잔여) |

> **P0 (RF-P0-01~09)** · Golden Master(GM-01~10) **완료**.

##### 1. 테스트 / 회귀 보호 (P1 — 최우선)

*테스트 없이 ECB 분리 금지* — 구조 리팩토링 **전** 반드시 선행.

| # | ID | 항목 |
|---|---|---|
| 1 | RF-P1-01 | `tests/control/test_solve_use_case.py` — mock validator/resolver 단위 테스트 |
| 2 | RF-P1-02 | Boundary 비정수 셀 검증 (`"5"`, `1.5` → `INVALID_RANGE`, TypeError 방지) |
| 3 | RF-P1-03 | 입력 grid 불변성 테스트 (PRD NFR-04 — execute 전후 deep equality) |
| 4 | RF-P1-04 | Golden Master — `INVALID_SIZE`, `INVALID_RANGE` 시나리오 추가 |
| 5 | RF-P1-05 | GUI headless 동작 테스트 (Solve/Clear/샘플/오류 표시) |
| 6 | RF-P1-06 | `integrated_solve_use_case` fixture 중복 제거 (`conftest.py` SSOT) |

**ECB P1 매핑** (P1과 1:1 연동, 동일 우선순위):

| ECB ID | 연결 P1 | 내용 |
|---|---|---|
| RF-ECB-P1-01 | RF-P1-01 | Control `SolveUseCase` mock 단위 테스트 |
| RF-ECB-P1-02 | RF-P1-02 | Boundary 비정수 → `INVALID_RANGE` |
| RF-ECB-P1-03 | RF-P1-04 | Golden Master 오류 시나리오 |
| RF-ECB-P1-04 | RF-P1-03 | grid 불변성 (NFR-04) |
| RF-ECB-P1-05 | RF-P1-05 | GUI headless 동작 |
| RF-ECB-P1-06 | RF-P2-H01~H03 | int[6]·GridInputWidget 스키마 가드 (P2-H 연계) |

##### 2. 계약·타입 강화 (P2-H — QA High)

`src/boundary/screen/*`는 smoke만 있음 — **P2-H 선행 권장** (§레이어별 REFACTOR 준비도).

| # | ID | 항목 | 대상 |
|---|---|---|---|
| 1 | RF-P2-H01 | `SolvePresenter` 성공 분기 int[6] 검증 (length=6, coords∈[1,4]) | U-OUT Boundary enforcement |
| 2 | RF-P2-H02 | `GridInputWidget.set_grid` — `GRID_SIZE` 검증 | UI 입력 가드 |
| 3 | RF-P2-H03 | `apply_solution` / `highlight_placements` — malformed int[6] UI 오류 | UI 출력 가드 |
| 4 | RF-P2-H04 | `SolveUseCase.execute` — `grid: Any` → `list[list[int]]` | FR-01 입력 계약 복원 |

##### 3. ECB 레이어 분리 (ECB P0 — 구조 1순위)

**REFACTOR 1순위:** E001~E007·int[6] 유지 — `DomainResolver` Control 이전 + Screen↔UIBoundary(`solve_presenter`) 경계 정리.

| # | ID | 항목 |
|---|---|---|
| 1 | RF-ECB-P0-01 | `entity/domain_resolver.py` → `src/control/` (`DomainResolverImpl` + Protocol → `ports.py`) |
| 2 | RF-ECB-P0-02 | `main_window` E006/E007 — 오류 타이틀·색·`QMessageBox` → `solve_presenter` 또는 Boundary UI mapper |
| 3 | RF-ECB-P0-03 | `main_window` — `bootstrap`/`SAMPLE_PUZZLES` 제거, `app.py` 단일 composition·Presenter 주입 |

> RF-ECB-P0-03 ↔ RF-P2-M03 동일 방향(composition root).

##### 4. 구조 개선 (P2)

| # | ID | 항목 |
|---|---|---|
| 1 | RF-P2-02 | `SolveUseCase.execute` / resolver 반환 `Any` → `SolveResult` *(H04 연계)* |
| 2 | RF-P2-01 / RF-P2-M06 | `DomainResolver` Protocol → `control/ports.py` *(ECB-P0-01 연계)* |
| 3 | RF-P2-03 | `boundary/contracts.py` re-export → import 경로 일원화 후 deprecate |
| 4 | RF-P2-04 | `entity/user.py` 스캐폴드 정리 (Magic Square 범위 외) |

##### 5. DRY · SSOT · 가독성 (P2-M)

| # | ID | 항목 |
|---|---|---|
| 1 | RF-P2-M01 | int[6] 언팩·1-index 변환 단일 helper (`SOLUTION_LENGTH=6` SSOT) |
| 2 | RF-P2-M02 | `BoundaryValidator` — 3회 full-grid 순회 → 단일 순회 |
| 3 | RF-P2-M03 | Screen→`bootstrap` 직접 import 제거 — `app.py` composition root |
| 4 | RF-P2-M04 | `main_window` 힌트 `"1–16"` → `MIN_VALUE`/`MAX_VALUE` SSOT |
| 5 | RF-P2-M05 | `main_window._build_ui` / `_show_error`, `grid_input_widget._build_ui` 분리 (≤20줄) |
| 6 | RF-P2-M07 | `validation_errors` 메시지 ↔ `grid_constants` 문자열 SSOT 연동 |

##### 6. 스타일 · Dead code (P2-L)

| # | ID | 항목 |
|---|---|---|
| 1 | RF-P2-L01 | 미사용 `_ERROR_STYLE` / `highlight_placements(is_error=True)` 제거 또는 domain-error 연결 |
| 2 | RF-P2-L02 | `SolveResult` union type alias 명명 개선 |

##### 7. 품질 게이트 (부가 — RED 체크리스트 잔여)

| # | 항목 | 목표 |
|---|---|---|
| 1 | Domain Logic coverage | 95%+ |
| 2 | Boundary Layer coverage | 85%+ |
| 3 | 전체 TOTAL coverage | 90%+ |

##### 권장 실행 Wave

| Wave | 범위 | 항목 |
|:---:|---|---|
| **1** | 안전망 | RF-P1-01~06 전체 |
| **2** | 계약 | RF-P2-H01~H04 (+ RF-ECB-P1-06 연계 테스트) |
| **3** | 아키텍처 | RF-ECB-P0-01~03 |
| **4** | 정리 | RF-P2-01~04 → RF-P2-M01~M07 → RF-P2-L01~L02 |

##### QA 코드 스멜 ↔ REFACTOR 매핑

| 파일 | 스멜 | 대응 REFACTOR |
|---|---|---|
| `solve_presenter.py` 71–74 | int[6] 미검증 | **RF-P2-H01** |
| `grid_input_widget.py` 83–88, 117–126 | set_grid/apply_solution 미검증 | **RF-P2-H02, H03** |
| `main_window.py` 135–136 | int[6] 3중 소비·미검증 | **RF-P2-H01, M01** |
| `solve_use_case.py` 23, 32 | `grid: Any` | **RF-P2-H04, P2-02** |
| `boundary_validator.py` 57–86 | 3회 순회 | **RF-P2-M02** |
| `main_window.py` 47–100, 148–177 | 장함수 | **RF-P2-M05** |
| `entity/solver.py` (참조) | int[6] Boundary 중복 | **RF-P2-M01** |

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
| Dual-Track Full GREEN R1~R8 | [`Report/12.MagicSquare_DualTrack_Full_GREEN_R1_R8_Report.md`](Report/12.MagicSquare_DualTrack_Full_GREEN_R1_R8_Report.md) | R1~R8 GREEN·PRD v1.1·coverage gate |
| Golden Master GM-1~GM-3 | [`Report/13.MagicSquare_Golden_Master_GM1_GM3_Report.md`](Report/13.MagicSquare_Golden_Master_GM1_GM3_Report.md) | Golden Master baseline·approve·회귀 보호 |
| REFACTOR P0 ECB·QA | [`Report/14.MagicSquare_REFACTOR_P0_ECB_QA_Report.md`](Report/14.MagicSquare_REFACTOR_P0_ECB_QA_Report.md) | contracts·bootstrap·QA 스멜·ECB 매핑 README |
| QA Control/Boundary 스멜 | [`Report/15.MagicSquare_QA_Control_Boundary_Smell_Report.md`](Report/15.MagicSquare_QA_Control_Boundary_Smell_Report.md) | quality-assurance-engineer 점검·P2-H/M/L·회귀 버그 |
| REFACTOR 유형·우선순위 | [`Report/16.MagicSquare_REFACTOR_Classification_Priority_Report.md`](Report/16.MagicSquare_REFACTOR_Classification_Priority_Report.md) | 미완료 REFACTOR 7유형·Wave 1~4·QA 매핑 |
| AC-FR-01-01 단일 GREEN 검증 | [`Report/11.MagicSquare_AC_FR_01_01_Single_Test_GREEN_Verification_Report.md`](Report/11.MagicSquare_AC_FR_01_01_Single_Test_GREEN_Verification_Report.md) | 단일 pytest GREEN 검증 |
| 결함 목록 | [`docs/defect_list.md`](docs/defect_list.md) | DEF-001~005 (Resolved) |
| Cursor Rules | [`.cursor/rules/`](.cursor/rules/) | Quality Gates, ECB, TDD, forbidden |
| Transcript (시작 준비) | [`Prompt/08.MagicSquare_TDD_Startup_Transcript.md`](Prompt/08.MagicSquare_TDD_Startup_Transcript.md) | TDD 시작 준비 세션 기록 |
| Transcript (AC-FR-01-01) | [`Prompt/09.MagicSquare_AC_FR_01_01_Transcript.md`](Prompt/09.MagicSquare_AC_FR_01_01_Transcript.md) | AC-FR-01-01 RED→GREEN 세션 기록 |
| Transcript (Dual-Track RED) | [`Prompt/10.MagicSquare_DualTrack_RED_Design_And_Skeleton_Transcript.md`](Prompt/10.MagicSquare_DualTrack_RED_Design_And_Skeleton_Transcript.md) | RED 설계·스켈레톤·Prompt 통합 세션 |
| Transcript (Full GREEN R1~R8) | [`Prompt/12.MagicSquare_DualTrack_Full_GREEN_R1_R8_Transcript.md`](Prompt/12.MagicSquare_DualTrack_Full_GREEN_R1_R8_Transcript.md) | R1~R8 GREEN·PRD v1.1 세션 |
| Transcript (Golden Master GM-1~GM-3) | [`Prompt/13.MagicSquare_Golden_Master_GM1_GM3_Transcript.md`](Prompt/13.MagicSquare_Golden_Master_GM1_GM3_Transcript.md) | Golden Master baseline·테스트·README 세션 |
| Transcript (REFACTOR P0 ECB·QA) | [`Prompt/14.MagicSquare_REFACTOR_P0_ECB_QA_Transcript.md`](Prompt/14.MagicSquare_REFACTOR_P0_ECB_QA_Transcript.md) | ECB P0·code-review·QA·ECB README 세션 |
| Transcript (QA Control/Boundary) | [`Prompt/15.MagicSquare_QA_Control_Boundary_Smell_Transcript.md`](Prompt/15.MagicSquare_QA_Control_Boundary_Smell_Transcript.md) | QA engineer 스멜 점검·README P2·Export 세션 |
| Transcript (REFACTOR 유형·우선순위) | [`Prompt/16.MagicSquare_REFACTOR_Classification_Priority_Transcript.md`](Prompt/16.MagicSquare_REFACTOR_Classification_Priority_Transcript.md) | REFACTOR 분류·README·Report·Export 세션 |
| Transcript (AC-FR-01-01 단일 GREEN) | [`Prompt/11.MagicSquare_AC_FR_01_01_Single_Test_GREEN_Transcript.md`](Prompt/11.MagicSquare_AC_FR_01_01_Single_Test_GREEN_Transcript.md) | 단일 pytest GREEN 검증 세션 |

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
| PRD | `docs/PRD_MagicSquare.md` v1.1 — DN-01~DN-03 resolved |
| 개발 To-Do List | Turn 1 작성 완료 — **파일 미저장** (선택: `docs/TDD_Development_ToDo_List.md`) |
| MagicSquare 구현 | **R0~R8 GREEN 완료** + ECB P0 (`contracts`, `ports`, `bootstrap`) |
| MagicSquare 테스트 | **~76 PASS** — Dual-Track + Golden Master + architecture guard |
| `docs/defect_list.md` | DEF-001~005 기록, Open 0건 |
| `pyproject.toml` | pytest-cov gate (≥80%); GUI optional omit |
| 현재 단계 | **REFACTOR** — Golden Master 구축 완료, P0 ECB·GUI 복원 완료 |

### GREEN 순서 (완료)

1. ~~**R1 GREEN** — `BoundaryValidator` ZERO COUNT 분기 (`U-IN-04~05`)~~ ✅
2. ~~**R2 GREEN** — RANGE 분기 (`U-IN-06~07`)~~ ✅
3. ~~**R3 GREEN** — DUPLICATE 분기 (`U-IN-08`)~~ ✅
4. ~~**R4 GREEN** — Entity FR-02~04~~ ✅
5. ~~**R5 GREEN** — Entity FR-05 (`TwoCellSolver`)~~ ✅
6. ~~**R6 GREEN** — U-OUT + U-FLOW-02c/d 통합~~ ✅
7. ~~**`pyproject.toml`** — pytest-cov gate 설정~~ ✅
8. ~~**DN-01~03** 확정 후 PRD v1.1 개정~~ ✅

### Open Questions (PRD §22)

| ID | Topic | 현재 기준 |
|---|---|---|
| DN-01 | 성공 응답 envelope | **확정:** bare `int[6]` |
| DN-02 | Control Layer 필수 여부 | **확정:** `SolveUseCase` 필수 |
| DN-03 | Both-fail fixture | **확정:** G3 in `tests/conftest.py` |
| DN-04 | Boundary coverage vs pass rate | pass 100% + coverage ≥85% (gate ≥80% global) |
| DN-05 | Report/4 파일명 | Report/06 사용 |

---

## 한 줄 결론

이 프로젝트의 본질은 **정답 1개 산출**이 아니라, **불변식과 계약으로 설명 가능한 코드**를 Dual-Track TDD로 만드는 것이다.  
**R0~R8 GREEN 완료** — Dual-Track PASS, Golden Master 회귀 안전장치, REFACTOR P0(ECB·GUI) 적용. 다음: P1 테스트 보강 → **P2-H QA High**(int[6]·UI 가드) → 구조 REFACTOR.
