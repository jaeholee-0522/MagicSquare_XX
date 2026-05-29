# PRD — Magic Square 4x4 TDD Practice

| Field | Value |
|---|---|
| Document ID | PRD-MSQ-4X4-001 |
| Version | 1.0 (Draft) |
| Status | Implementation-Ready with Open Decisions (§22) |
| Primary Sources | Report/01, Report/02, Report/03, Report/06 (Level 1~5), `.cursorrules`, `.cursor/rules/*.mdc` |

---

## 1. Executive Summary

Magic Square 4x4 TDD Practice는 4×4 마방진 **정답 산출**이 아니라, **불변식(Invariant)과 입출력 계약(Contract)을 고정한 뒤 Dual-Track TDD로 검증·구현·리팩토링하는 학습형 프로젝트이다. 학습자는 Track A(Boundary/UI Contract)와 Track B(Domain/Logic Invariant)를 분리하여 RED→GREEN→REFACTOR 사이클을 운영하고, Concept→Rule→Use Case→Contract→Test→Component 추적성을 유지한다. 본 PRD는 UI·DB·Web 없이 **콘솔/pytest 실행 가능한 순수 로직** 범위에서 구현 전 기준을 정의한다.

**훈련 핵심 역량**

- 불변식 사고: 규칙을 “항상 참” 조건으로 명문화
- 입력/출력 계약: `int[][]` 입력, `int[6]` 출력, 오류 코드 고정
- Dual-Track TDD: Boundary 실패와 Domain 실패를 분리 검증
- 설계→테스트→구현→리팩토링: 계약 변경 없이 구조만 개선

---

## 2. Background

4×4 마방진은 정수 1~16을 4×4 격자에 배치할 때 행·열·대각선 합이 모두 동일해야 하는 **강한 제약 문제**이다. 임의 배치의 대부분은 실패하며, 유효 상태만 식별 가능하다.

본 프로젝트는 이 문제를 **알고리즘 경쟁**이 아닌 **TDD 훈련 사례**로 사용한다 (Report/01).

- 3×3보다 상태 공간이 커서 검증·테스트 구조 차이가 드러난다.
- 문제 크기는 TDD 점진 검증에 적합하다.
- 핵심은 “정답 출력” 이전에 **조건 명세 가능성·검증 가능성·실패 패턴 식별 가능성**이다.

단순 마방진 풀이 접근의 한계 (Report/01 Why #1):

- 정답 산출 편향 → 검증·재현·실패 처리 기준 약화
- “완성” 정의가 암묵적 → 요구사항 누락
- 실패 중심 테스트 구성 약화 → TDD 효과 감소
- 입력 검증·규칙 판정·결과 표현 책임 경계 흐림

---

## 3. Problem Statement

### 3.1 표면 문제 (비목표)

> 4×4 마방진의 정답 하나를 완성하는 문제

### 3.2 정식 문제 정의 (목표)

> 4×4 숫자 배치 상황에서 **규칙이 항상 일관되게 성립하는지 판단 가능**하도록 문제를 명세하고, 그 명세를 **반복 검증 가능한 형태**로 관리하는 문제

### 3.3 입력/출력 계약이 핵심인 이유

- 테스트 기대 결과를 고정하기 위해 필요 (Report/01 STEP 4)
- 오류 처리 정책 일관성 확보
- Boundary와 Domain 책임 분리
- 리팩토링 후에도 외부 계약 불변 보장

---

## 4. Why Now / Why Chain

| Why | 질문 | 핵심 답 | 학습자 Pain Point |
|---|---|---|---|
| Why #1 | 왜 마방진을 완성해야 하는가? | 정답 출력만 목표로 하면 검증·실패 처리·책임 분리가 약해진다 | 구현부터 시작하여 규칙·테스트 기준을 건너뜀 |
| Why #2 | 왜 프로그램으로 구현하는가? | 반복 실행, 검증 자동화, 오류 방지, 규칙 기반 사고 훈련 | 수기 계산·개인 숙련에 의존 |
| Why #3 | 왜 TDD로 설계하는가? | 규칙 해석 일관성, 변경 영향 격리, 실패 가시성, 회귀 감시 | 테스트 기준 불명확, 리팩토링 후 계약 깨짐 |

**지금 닫아야 하는 Gap**

- Boundary와 Domain 책임 혼합
- 불변식 없는 구현·하드코딩
- 입력 검증 실패 시 Domain 호출
- 두 조합 실패·출력 형식 등 **미정 실패 정책**
- Concept→Test 추적 단절

---

## 5. Target Users

| User | 목적 | 사용 환경 |
|---|---|---|
| TDD 학습자 | RED-GREEN-REFACTOR, Dual-Track TDD 훈련 | pytest 실행, 콘솔/CLI 호출 |
| 코드 리뷰어 | 계약·불변식·레이어 경계 준수 검토 | PR, 테스트 결과, Traceability Matrix |
| Clean Architecture / ECB 학습자 | Boundary→Control→Domain 의존 방향 훈련 | `src/boundary`, `src/control`, `src/entity` |

**범위 밖 환경:** UI 화면, DB, Web/API 서버, 외부 서비스

---

## 6. Vision & Epic Goal

### 6.1 Epic Title

**불변식 기반 사고 훈련 시스템 구축**

### 6.2 Business Goal

Magic Square 4×4를 통해 “작동하는 코드”가 아니라 **불변식과 계약으로 설명 가능한 코드**를 만드는 학습 체계를 구축한다.

### 6.3 Learning Goal

- 불변식 중심 설계 사고
- Dual-Track(UI + Logic) TDD
- 입력/출력 계약 정의 및 유지
- 설계→테스트→구현→리팩토링 규율
- Concept→Invariant→Contract→Test 추적성

### 6.4 Epic Success Criteria (검증 가능)

| ID | 기준 | 검증 방법 |
|---|---|---|
| ESC-01 | Domain Logic 테스트 커버리지 ≥ 95% | pytest-cov 리포트 |
| ESC-02 | Boundary 입력 검증 **계약 테스트** 전건 통과 (100%) | Boundary contract test suite GREEN |
| ESC-03 | 설명 없는 매직 넘버 0건 | 코드 리뷰 + 정적 검사 |
| ESC-04 | `GRID_SIZE`, `MIN_VALUE`, `MAX_VALUE`, `MAGIC_CONSTANT`, `BLANK_VALUE` 등 명명 상수 사용 | 코드 리뷰 |
| ESC-05 | 정답 하드코딩 0건 | 코드 리뷰 + Solver 테스트 |
| ESC-06 | §21 Traceability Matrix의 Concept/Invariant 각각 ≥ 1 Test Case Candidate 연결 | Matrix 점검 |
| ESC-07 | REFACTOR 후 외부 I/O 계약(형식·제약·오류 의미) 불변 | 회귀 테스트 GREEN |

### 6.5 User Story Index (Level 3)

| Story ID | Name | Layer | Protected Contract / Invariant |
|---|---|---|---|
| US-01 | 입력 검증 | Boundary | Input Contract, Error Contract, Boundary-Domain 호출 경계 |
| US-02 | 빈칸 좌표 탐색 | Domain | Blank Cell Invariant |
| US-03 | 누락 숫자 탐색 | Domain | Missing Number Invariant |
| US-04 | 마방진 검증 | Domain | Magic Constant Invariant (합=34) |
| US-05 | 두 가지 조합 시도 | Domain + Boundary Output | Combination Order + Output Contract |

---

## 7. Persona

**Primary Persona: TDD 학습 중인 소프트웨어 개발자**

- Clean Architecture / ECB 계층 분리를 이해하려 함
- 알고리즘 정답보다 **설계·계약·테스트·리팩토링 흐름**을 훈련하려 함
- 실패 원인을 레이어 단위로 분리해 진단하려 함

---

## 8. User Journey Summary

| Stage | Pain Point | Learning Outcome |
|---|---|---|
| **1. 문제 인식** | “정답부터” 구현하려는 습관 | 문제를 불변식·명세 중심으로 재정의 |
| **2. 계약 정의** | 유효성 실패와 계산 실패 혼동 | Input/Output/Error Contract를 테스트 가능 문장으로 고정 |
| **3. 도메인 분리** | Solver에 검증·탐색·포맷 혼재 | BlankFinder / MissingNumberFinder / MagicSquareValidator / Solver 분리 |
| **4. Dual-Track TDD** | 실패 원인 추적 어려움 | Track A(UI RED)와 Track B(Logic RED) 분리 운영 |
| **5. 회귀 보호** | 리팩토링 후 예외·형식 재발 | 정상/오류/조합실패/출력형식 회귀 대상 카탈로그화 |

---

## 9. Scope

### 9.1 In-Scope

- FR-01~FR-05 (§10) 전 기능
- Boundary 입력 검증 및 오류 응답
- Domain: 빈칸·누락 숫자·마방진 판정·두 조합 Solver·결과 포맷
- Dual-Track TDD 및 Traceability Matrix (§21)
- pytest 기반 계약·불변식 테스트
- 콘솔/CLI 또는 테스트 하네스를 통한 실행

### 9.2 Out-of-Scope

- UI 화면 개발
- DB 저장/검색
- Web/API 서버
- N×N 일반화
- 완전한 마방진 **생성** 알고리즘 (주어진 2빈칸 퍼즐 해결만)
- 사용자 인증/권한
- 네트워크 오류 처리
- QR 스캔, 외부 서비스 연동
- Report/02 Data Layer(File Repository) — 본 PRD 범위 **제외**

---

## 10. Functional Requirements

### FR-01 Input Verification (Boundary)

- **Description:** Boundary가 Domain 호출 전 입력 계약을 검증한다.
- **Layer:** Boundary (`BoundaryValidator`)
- **Input:** `int[][] matrix`
- **Processing Rules:**
  1. 검증 순서 고정: **SIZE → RANGE → ZERO COUNT → DUPLICATE** (Report/02 REG-02)
  2. 첫 위반 규칙 1건만 반환 (다중 오류 병합 금지)
  3. 검증 실패 시 Domain resolver **호출 0회**
  4. 검증 성공 시 Domain resolver **호출 1회**
- **Output:**
  - 성공: 검증 통과 신호 → Control/Domain 파이프라인 진행
  - 실패: §13 정의 구조화 실패 응답
- **Acceptance Criteria:**
  - AC-FR01-01: 행 개수 ≠ 4이면 `UI-ERR-001` 반환, Domain 호출 0회
  - AC-FR01-02: 임의 행 길이 ≠ 4이면 `UI-ERR-001` 반환, Domain 호출 0회
  - AC-FR01-03: 0 또는 1~16 범위 밖 값 존재 시 `UI-ERR-002` 반환, Domain 호출 0회
  - AC-FR01-04: `0` 개수 ≠ 2이면 `UI-ERR-003` 반환, Domain 호출 0회
  - AC-FR01-05: 0 제외 중복 존재 시 `UI-ERR-004` 반환, Domain 호출 0회
  - AC-FR01-06: 동일 위반 입력은 항상 동일 Error Code·Message 반환
- **Error / Exception Policy:** 구조화 실패 응답 (§13); uncaught exception 금지
- **Related Business Rules:** BR-01, BR-02, BR-03, BR-04, BR-05
- **Related Test Direction:** Track A — RED-BND-VAL-001~004, UT-01~04
- **Component Candidate:** `BoundaryValidator`

---

### FR-02 Blank Coordinate Discovery

- **Description:** 값 `0`인 셀 2개의 좌표를 row-major 순서로 식별한다.
- **Layer:** Domain (`BlankFinder`)
- **Input:** Boundary 검증 통과 `int[][] matrix`
- **Processing Rules:**
  1. `0`만 빈칸으로 판정
  2. row-major(행 우선, 열 증가) 스캔
  3. **첫 번째 빈칸:** row-major에서 최초 `0`
  4. **두 번째 빈칸:** row-major에서 두 번째 `0`
  5. Domain 내부 좌표: **0-index** `(row, col)` 사용
  6. 입력 행렬 **변경 금지** (§14 NFR)
- **Output:** 2개 좌표 `(r0,c0)`, `(r1,c1)` — 0-index, row-major 순
- **Acceptance Criteria:**
  - AC-FR02-01: `0` 셀만 결과에 포함
  - AC-FR02-02: 정확히 2개 좌표 반환
  - AC-FR02-03: row-major 순서 보장
  - AC-FR02-04: SC-DOM-SOL-001 행렬에서 `(2,2)`, `(3,3)` (0-index) 반환
- **Error / Exception Policy:** FR-01 통과 입력만 수신; 빈칸 규칙 위반은 FR-01에서 차단
- **Related Business Rules:** BR-02, BR-06, BR-07
- **Related Test Direction:** Track B — RED-DOM-BLK-001
- **Component Candidate:** `BlankFinder`

---

### FR-03 Missing Number Discovery

- **Description:** 1~16 중 입력에 없는 숫자 2개를 오름차순으로 도출한다.
- **Layer:** Domain (`MissingNumberFinder`)
- **Input:** Boundary 검증 통과 `int[][] matrix`
- **Processing Rules:**
  1. `0`은 계산 대상에서 제외
  2. 1~16 집합과 입력 non-zero 값의 차집합
  3. 결과 오름차순 정렬
  4. 입력 행렬 변경 금지
- **Output:** `[smaller, larger]` — 길이 2, 오름차순
- **Acceptance Criteria:**
  - AC-FR03-01: `0`은 누락 숫자 계산에서 제외
  - AC-FR03-02: 정확히 2개 숫자 반환
  - AC-FR03-03: 오름차순 반환
  - AC-FR03-04: SC-DOM-SOL-001 행렬에서 `[1, 6]` 반환
  - AC-FR03-05: 각 값 ∈ [1, 16]
- **Error / Exception Policy:** FR-01 통과 입력만 수신
- **Related Business Rules:** BR-03, BR-08, BR-09
- **Related Test Direction:** Track B — RED-DOM-MIS-001, RED-DOM-MIS-002
- **Component Candidate:** `MissingNumberFinder`

---

### FR-04 Magic Square Validation

- **Description:** 완성된 4×4 격자가 마방진 불변식(합=34)을 만족하는지 판정한다.
- **Layer:** Domain (`MagicSquareValidator`)
- **Input:** 4×4 `int[][]` (빈칸 없음, FR-01 통과)
- **Processing Rules:**
  1. 4개 행 합 = `MAGIC_CONSTANT` (34)
  2. 4개 열 합 = 34
  3. 주대각선 합 = 34
  4. 부대각선 합 = 34
  5. 전 조건 충족 시 `true`, 하나라도 불충족 시 `false`
- **Output:** `boolean`
- **Acceptance Criteria:**
  - AC-FR04-01: 4행 모두 34 → 행 조건 true
  - AC-FR04-02: 4열 모두 34 → 열 조건 true
  - AC-FR04-03: 두 대각선 모두 34 → 대각선 조건 true
  - AC-FR04-04: 행·열·대각선 전부 34 → `true`
  - AC-FR04-05: 하나라도 ≠ 34 → `false`
- **Error / Exception Policy:** 판정 결과만 반환; 예외로 성공/실패 대체 금지
- **Related Business Rules:** BR-10, BR-11
- **Related Test Direction:** Track B — RED-DOM-VAL-001~004
- **Component Candidate:** `MagicSquareValidator`

---

### FR-05 Two-Combination Solver and Result Formatting

- **Description:** 두 누락 숫자를 두 빈칸에 배치하는 Attempt 1·2를 수행하고, 성공 시 `int[6]`을 반환한다.
- **Layer:** Domain (`Solver`) + Boundary/Control (`ResultFormatter`)
- **Input:** FR-01 통과 matrix, FR-02 blank coords, FR-03 missing numbers
- **Processing Rules:**

  **Attempt 1 (small-first):**

  - `n1` = smaller missing → first blank (row-major 1st)
  - `n2` = larger missing → second blank (row-major 2nd)
  - 후보 행렬에 배치 후 FR-04 검증
  - `true`이면 Attempt 1 결과 채택

  **Attempt 2 (reverse, Attempt 1 실패 시):**

  - larger → first blank
  - smaller → second blank
  - FR-04 검증
  - `true`이면 Attempt 2 결과 채택

  **Both fail:**

  - §13 `DOMAIN-ERR-NO_VALID_PLACEMENT` 구조화 실패 응답 반환
  - `int[6]` 성공 출력 없음

  **Output formatting (성공 시):**

  - `[r1, c1, n1, r2, c2, n2]`
  - `r*, c*`: **1-index**, BlankFinder 좌표 + 1
  - `n1, n2`: 해당 빈칸에 배치된 숫자 (Attempt 채택 결과)
  - 길이 = 6

- **Output:** `int[6]` (성공) 또는 §13 Domain 실패 응답
- **Acceptance Criteria:**
  - AC-FR05-01: Attempt 1 성공 시 Attempt 1 배치 순서로 `int[6]` 반환
  - AC-FR05-02: Attempt 1 실패·Attempt 2 성공 시 Attempt 2 배치로 `int[6]` 반환 (SC-DOM-SOL-001: `[3,3,6,4,4,1]`)
  - AC-FR05-03: Attempt 1 성공 시 Attempt 2 미시도
  - AC-FR05-04: 두 Attempt 모두 실패 시 `DOMAIN-ERR-NO_VALID_PLACEMENT` 반환
  - AC-FR05-05: 좌표 1-index, 각 좌표 ∈ [1,4]
  - AC-FR05-06: 정답 하드코딩 없이 규칙 기반 산출
  - AC-FR05-07: 원본 입력 행렬 불변 (deep equality 유지)
- **Error / Exception Policy:** Domain 실패 = 구조화 응답 (Report/02 IT-04); uncaught exception 금지
- **Related Business Rules:** BR-06~BR-13
- **Related Test Direction:** Track B — RED-DOM-SOL-001, RED-DOM-SOL-002, RED-DOM-SOL-003; Track A — output schema tests
- **Component Candidate:** `Solver`, `ResultFormatter`

---

## 11. Business Rules / Domain Rules

| ID | Rule (항상 참) | 검증 |
|---|---|---|
| BR-01 | 입력은 4행 × 4열 `int[][]`이다 | AC-FR01-01, AC-FR01-02 |
| BR-02 | `0`(BLANK)은 정확히 2개이다 | AC-FR01-04 |
| BR-03 | 각 셀 값 ∈ {0} ∪ [1, 16] | AC-FR01-03 |
| BR-04 | 0 제외 값은 중복되지 않는다 | AC-FR01-05 |
| BR-05 | Boundary 검증 실패 시 Domain resolver 호출 0회 | AC-FR01-* |
| BR-06 | 첫 번째 빈칸 = row-major 최초 `0` | AC-FR02-03 |
| BR-07 | 두 번째 빈칸 = row-major 두 번째 `0` | AC-FR02-02 |
| BR-08 | 누락 숫자 = {1..16} \ {입력 non-zero 값}, 정확히 2개 | AC-FR03-02 |
| BR-09 | 누락 숫자 반환 순서 = 오름차순 | AC-FR03-03 |
| BR-10 | `MAGIC_CONSTANT = 34` (n=4) | AC-FR04-* |
| BR-11 | 유효 마방진 ⟺ 4행·4열·2대각선 합 모두 34 | AC-FR04-04, AC-FR04-05 |
| BR-12 | Attempt 1: smaller→1st blank, larger→2nd blank | AC-FR05-01 |
| BR-13 | Attempt 2: larger→1st blank, smaller→2nd blank (Attempt 1 실패 시) | AC-FR05-02 |
| BR-14 | 성공 출력 = `int[6]` `[r1,c1,n1,r2,c2,n2]`, 1-index | AC-FR05-05 |
| BR-15 | 처리 전후 입력 행렬 deep equality 유지 | AC-FR05-07, NFR-03 |

---

## 12. Input / Output Contract

### 12.1 Input Contract

| Field / Item | Type | Rule | Valid Example | Invalid Example | Error Code |
|---|---|---|---|---|---|
| `matrix` | `int[][]` | row count = 4 | 4×4 array | 3×4 array | UI-ERR-001 |
| `matrix[i]` | `int[]` | length = 4 for all i | `[4 ints]` | `[3 ints]` | UI-ERR-001 |
| `matrix[i][j]` | `int` | 0 or 1~16 | `0`, `7`, `16` | `-1`, `17` | UI-ERR-002 |
| zero cells | count | exactly 2 | two `0`s | one or three `0`s | UI-ERR-003 |
| non-zero values | uniqueness | no duplicate | `{1..16}` subset | two `5`s | UI-ERR-004 |

**검증 순서:** SIZE → RANGE → ZERO → DUPLICATE

### 12.2 Output Contract (Success)

| Field / Item | Type | Rule | Valid Example | Invalid Example | Failure Policy |
|---|---|---|---|---|---|
| result | `int[6]` | length = 6 | `[3,3,6,4,4,1]` | length 5 or 7 | UI-ERR-005 |
| r1, c1, r2, c2 | `int` | 1-index, each ∈ [1,4] | `3,3,4,4` | `0,5` | UI-ERR-006 |
| n1, n2 | `int` | missing numbers placed | `6, 1` | out of 1~16 | DOMAIN validation |
| format | sequence | `[r1,c1,n1,r2,c2,n2]` | `[1,1,1,4,4,16]` | reorder fields | contract test fail |

### 12.3 Output Contract (Failure)

| Case | Error Code | Layer | Domain Resolver Called |
|---|---|---|---|
| Size invalid | UI-ERR-001 | Boundary | No |
| Range invalid | UI-ERR-002 | Boundary | No |
| Zero count invalid | UI-ERR-003 | Boundary | No |
| Duplicate | UI-ERR-004 | Boundary | No |
| No valid placement | DOMAIN-ERR-NO_VALID_PLACEMENT | Domain | Yes (invoked; solver returns failure) |

---

## 13. Error / Failure Policy

**메시지 형식 (Report/02):** `[ErrorCode] cause:action`  
**예:** `[UI-ERR-001] matrix size invalid:provide 4x4 matrix`

| Condition | Error Code | Message Template | Layer | Domain Resolver Called | Related AC |
|---|---|---|---|---|---|
| Not 4×4 | UI-ERR-001 | `[UI-ERR-001] matrix size invalid:provide 4x4 matrix` | Boundary | **No** | AC-FR01-01, AC-FR01-02 |
| Zero count ≠ 2 | UI-ERR-003 | `[UI-ERR-003] blank count invalid:provide exactly 2 zeros` | Boundary | **No** | AC-FR01-04 |
| Value out of range | UI-ERR-002 | `[UI-ERR-002] value out of range:use 0 or 1-16` | Boundary | **No** | AC-FR01-03 |
| Duplicate non-zero | UI-ERR-004 | `[UI-ERR-004] duplicate value:remove duplicate non-zero` | Boundary | **No** | AC-FR01-05 |
| Both attempts fail | DOMAIN-ERR-NO_VALID_PLACEMENT | `[DOMAIN-ERR-NO_VALID_PLACEMENT] no valid placement:verify puzzle is solvable` | Domain | **Yes** | AC-FR05-04 |

**정책 확정 (본 PRD):**

- Boundary 실패: **구조화 실패 응답** 반환; Domain resolver **미호출**
- Domain 실패(두 조합 모두 불성립): **구조화 실패 응답** `DOMAIN-ERR-NO_VALID_PLACEMENT` 반환; uncaught exception **사용하지 않음** (Report/02 IT-04)
- 다중 입력 위반: **첫 번째 위반 1건만** 반환 (REG-02)

---

## 14. Non-Functional Requirements

| ID | Requirement | Verification |
|---|---|---|
| NFR-01 | Domain Logic line+branch coverage ≥ **95%** | pytest-cov gate |
| NFR-02 | Boundary validation contract coverage ≥ **85%** | pytest-cov gate |
| NFR-03 | **Deterministic:** 동일 입력 → 동일 출력/동일 Error Code | repeated run test |
| NFR-04 | **No input mutation:** 처리 전후 입력 `int[][]` deep equality | before/after equality test |
| NFR-05 | **Performance:** 4×4 단일 실행 wall-clock ≤ **50ms** (로컬 dev machine) | timed pytest |
| NFR-06 | Boundary·Domain 책임 분리; Domain은 Boundary/UI/DB/Web/파일시스템 비의존 | architecture test / import rule |
| NFR-07 | 설명 없는 매직 넘버 금지; §6.4 명명 상수 사용 | code review |
| NFR-08 | 정답 하드코딩 금지 | code review + Solver tests |
| NFR-09 | 전역 coverage minimum ≥ **80%** (`.cursorrules`) | pytest-cov |
| NFR-10 | Boundary 계약 테스트 suite **100% pass** (ESC-02) | CI GREEN |

---

## 15. Dual-Track TDD Strategy

### 15.1 Track A — Boundary / UI Contract TDD

| Focus | RED Examples | GREEN Scope |
|---|---|---|
| 입력 SIZE/RANGE/ZERO/DUPLICATE | RED-BND-VAL-001~004 | `BoundaryValidator` 최소 구현 |
| Domain 미호출 | mock/spy: resolver call count = 0 | 검증 실패 분기만 |
| 출력 `int[6]` schema | length, 1-index range | `ResultFormatter` |
| 오류 메시지 형식 | regex `[UI-ERR-*] ...:...` | template mapping |

### 15.2 Track B — Domain / Logic TDD

| Focus | RED Examples | GREEN Scope |
|---|---|---|
| BlankFinder row-major | RED-DOM-BLK-001 | blank scan only |
| MissingNumberFinder | RED-DOM-MIS-001/002 | set difference + sort |
| MagicSquareValidator | RED-DOM-VAL-001~004 | row/col/diag sums |
| small-first success | RED-DOM-SOL-002 | Attempt 1 path |
| reverse success | RED-DOM-SOL-001 | Attempt 2 path |
| both fail | RED-DOM-SOL-003 | failure response |

### 15.3 Parallel Progression Rules

1. UI RED와 Logic RED **테스트 파일·실패 원인 분리**
2. UI GREEN / Logic GREEN 각각 **해당 RED 통과 최소 코드**만 작성
3. REFACTOR는 GREEN 이후에만; **외부 I/O 계약 변경 금지**
4. Domain 전체 구현 후 Boundary 연결 **금지** — Track A·B **교차 진행**
5. 테스트 삭제·완화·과도 mock으로 GREEN **금지**
6. Contract-first: **테스트/계약 먼저**, 구현은 RED 확인 후

---

## 16. Test Plan / QA

### 16.1 Normal Scenarios

| ID | Scenario | Given | Expected |
|---|---|---|---|
| TP-N-01 | small-first success | §16.4 valid matrix A | Attempt 1 pass → `int[6]` Attempt 1 order |
| TP-N-02 | reverse success | §16.4 matrix B (SC-DOM-SOL-001) | Attempt 1 fail, Attempt 2 pass → `[3,3,6,4,4,1]` |

### 16.2 Exception Scenarios

| ID | Scenario | Expected |
|---|---|---|
| TP-E-01 | Not 4×4 | UI-ERR-001, Domain 0 calls |
| TP-E-02 | Blank count ≠ 2 | UI-ERR-003, Domain 0 calls |
| TP-E-03 | Value 17 present | UI-ERR-002, Domain 0 calls |
| TP-E-04 | Duplicate non-zero | UI-ERR-004, Domain 0 calls |
| TP-E-05 | Both attempts fail | DOMAIN-ERR-NO_VALID_PLACEMENT |

### 16.3 Boundary Scenarios

| ID | Check | Expected |
|---|---|---|
| TP-B-01 | Value `1` present | passes FR-01 |
| TP-B-02 | Value `16` present | passes FR-01 |
| TP-B-03 | `0` only as blank | blank detection correct |
| TP-B-04 | Output coords 1-index | all ∈ [1,4] |
| TP-B-05 | Output length | exactly 6 |

### 16.4 Representative Test Data

**Matrix B — reverse success (SC-DOM-SOL-001):**

```
16  2   3  13
 5 11  10   8
 9  7   0  12
 4 14  15   0
```

- Missing: `[1, 6]`; blanks 0-index `(2,2)`, `(3,3)`; 1-index `(3,3)`, `(4,4)`
- Expected: `[3, 3, 6, 4, 4, 1]`

**Matrix A — small-first success:**

```
 0 15 14  4
12  6  7  9
 8 10 11  5
13  3  2  0
```

- Missing: `[1, 16]`; Attempt 1 expected success
- Expected: `[1, 1, 1, 4, 4, 16]`

**Invalid size (3×4):**

```
[[1,2,3,4],[5,6,7,8],[9,10,11,12]]
```

→ UI-ERR-001

**Invalid blank count (1 zero):**

```
16  2   3  13
 5 11  10   8
 9  7   6  12
 4 14  15   0
```

→ UI-ERR-003

**Duplicate:**

```
16  2   3  13
 5  5  10   8
 9  7   6  12
 4 14  15   1
```

→ UI-ERR-004

**Invalid range (17):**

```
16  2   3  13
 5 11  10   8
 9  7  17  12
 4 14  15   0
```

→ UI-ERR-002

**Both attempts fail:** FR-01 통과 행렬 중 Attempt 1·2 모두 FR-04 `false`. Fixture는 RED-DOM-SOL-003에서 확정·고정한다.

---

## 17. Architecture Overview (High-Level)

```
[Caller / pytest / CLI]
        │
        ▼
┌───────────────────┐
│  Boundary Layer   │  BoundaryValidator, ResultFormatter
│  (Track A)        │  Input validation, error mapping, output schema
└─────────┬─────────┘
          │ boundary → control (only)
          ▼
┌───────────────────┐
│  Control Layer    │  Use-case orchestration (optional but recommended)
│  (Application)    │  Validates-then-solve pipeline
└─────────┬─────────┘
          │ control → entity (only)
          ▼
┌───────────────────┐
│  Domain Layer     │  BlankFinder, MissingNumberFinder,
│  (Entity / Track B)│ MagicSquareValidator, Solver
└───────────────────┘
```

**의존 방향 (ECB + Clean Architecture):**

- Boundary → Control → Domain(Entity)
- Domain은 Boundary/Control/UI/DB/Web/파일시스템 **import 금지**
- Boundary가 Domain 내부 직접 조작 **금지**

**용어 매핑:** Report/02 Screen Layer = Boundary; Logic/Domain Layer = Entity (+ Control orchestration)

---

## 18. Component Candidates

| Component | Layer | Responsibility | Input | Output | Related FR | Related Test |
|---|---|---|---|---|---|---|
| `BoundaryValidator` | Boundary | FR-01 input contract | `int[][]` | pass / UI-ERR-* | FR-01 | RED-BND-VAL-* |
| `BlankFinder` | Domain | FR-02 blank coords | validated matrix | 2×(row,col) 0-index | FR-02 | RED-DOM-BLK-001 |
| `MissingNumberFinder` | Domain | FR-03 missing nums | validated matrix | `[sm,lr]` sorted | FR-03 | RED-DOM-MIS-* |
| `MagicSquareValidator` | Domain | FR-04 magic check | 4×4 complete grid | boolean | FR-04 | RED-DOM-VAL-* |
| `Solver` | Domain | FR-05 Attempt 1/2 | matrix, blanks, missing | candidate grid / success flag | FR-05 | RED-DOM-SOL-* |
| `ResultFormatter` | Boundary | FR-05 output contract | 0-index placement | `int[6]` 1-index | FR-05 | UT-05, output schema |

---

## 19. Risks & Ambiguities

| Risk | Impact | Mitigation / Decision |
|---|---|---|
| 1-index vs 0-index 혼동 | Wrong output coords | Domain 0-index 내부, Boundary 1-index 외부 (§FR-02, FR-05) |
| row-major 첫 빈칸 정의 누락 | Wrong Attempt order | BR-06, BR-07 명시 |
| small-first vs reverse fixture 혼동 | False GREEN | Matrix A/B 분리 (§16.4) |
| Input mutation | Flaky tests | NFR-04 deep equality |
| Both-fail policy omitted | Untestable failure | §13 DOMAIN-ERR-NO_VALID_PLACEMENT 확정 |
| MAGIC_CONSTANT 34 hardcoded | Magic number violation | `MAGIC_CONSTANT` named constant (ESC-04) |
| Boundary+Domain mixed | Untestable layers | Dual-Track + FR-01 call count AC |
| Both-fail fixture 미확정 | RED-DOM-SOL-003 blocked | RED 단계에서 fixture 고정 (§16.4) |

---

## 20. Engineering Principles

| Principle | Source | Requirement |
|---|---|---|
| PEP 8, max line 88 | `.cursorrules`, `magicsquare-python-code-style.mdc` | All Python code |
| Type hints (params + return) | same | All functions |
| Google docstrings | same | Public methods |
| pytest + AAA | `magicsquare-tdd-testing.mdc` | All tests; `test_` prefix |
| RED → GREEN → REFACTOR | `.cursorrules` tdd_rules | No impl before RED; no refactor in GREEN |
| ECB layers | `magicsquare-ecb-architecture.mdc` | boundary / control / entity |
| `print()` debugging forbidden | `magicsquare-forbidden.mdc` | Use `logging` |
| bare `except:` forbidden | same | Explicit exceptions |
| Test weakening forbidden | same | No delete/bypass to force GREEN |
| Magic numbers forbidden | same | Named constants in entity |
| Coverage | Report/02 + `.cursorrules` | Domain ≥95%, Boundary ≥85%, global ≥80% |

**Repository layout:** `src/{boundary,control,entity}/`, `tests/{boundary,control,entity}/`

---

## 21. Traceability Matrix

| Concept / Invariant | Business Rule | Feature ID | Acceptance Criteria | Test Case Candidate | Component |
|---|---|---|---|---|---|
| 4×4 입력 | BR-01 | FR-01 | AC-FR01-01, AC-FR01-02 | RED-BND-VAL-004, UT-01 | BoundaryValidator |
| 빈칸 2개 | BR-02 | FR-01 | AC-FR01-04 | RED-BND-VAL-001 | BoundaryValidator |
| 값 0 또는 1~16 | BR-03 | FR-01 | AC-FR01-03 | RED-BND-VAL-003 | BoundaryValidator |
| 중복 금지 | BR-04 | FR-01 | AC-FR01-05 | RED-BND-VAL-002 | BoundaryValidator |
| row-major 첫 빈칸 | BR-06 | FR-02 | AC-FR02-03 | RED-DOM-BLK-001 | BlankFinder |
| 누락 숫자 2개 | BR-08 | FR-03 | AC-FR03-02 | RED-DOM-MIS-001 | MissingNumberFinder |
| 누락 숫자 오름차순 | BR-09 | FR-03 | AC-FR03-03 | RED-DOM-MIS-002 | MissingNumberFinder |
| 마방진 상수 34 | BR-10 | FR-04 | AC-FR04-04 | RED-DOM-VAL-* | MagicSquareValidator |
| 행/열/대각선 합 | BR-11 | FR-04 | AC-FR04-01~05 | RED-DOM-VAL-001~004 | MagicSquareValidator |
| small-first 시도 | BR-12 | FR-05 | AC-FR05-01 | RED-DOM-SOL-002 | Solver |
| reverse 시도 | BR-13 | FR-05 | AC-FR05-02 | RED-DOM-SOL-001 | Solver |
| int[6] 반환 | BR-14 | FR-05 | AC-FR05-05 | UT-05, TP-B-05 | ResultFormatter |
| 1-index 좌표 | BR-14 | FR-05 | AC-FR05-05 | UT-05, TP-B-04 | ResultFormatter |
| Domain 미호출(입력 실패) | BR-05 | FR-01 | AC-FR01-* | UT-01~04 | BoundaryValidator |
| 두 조합 모두 실패 | §13 | FR-05 | AC-FR05-04 | RED-DOM-SOL-003 | Solver |
| 입력 불변 | BR-15 | FR-02~05 | AC-FR05-07 | NFR-04 test | All Domain |

---

## 22. Open Questions / Decision Needed

| ID | Topic | Conflict | Options | PRD Impact |
|---|---|---|---|---|
| **DN-01** | 성공 응답 래퍼 | Report/02: `RESULT_OK + int[6]` vs 본 PRD 고정 계약: `int[6]` | (A) bare `int[6]` (B) `{status: OK, result: int[6]}` (C) `RESULT_OK` prefix string | Boundary success schema |
| **DN-02** | Control Layer 필수 여부 | Report/02 Application Service “선택” vs ECB control 권장 | (A) Boundary→Domain 직접 (B) Control 필수 | §17 구조, import rules |
| **DN-03** | Both-fail fixture | §16.4 미확정 행렬 | RED-DOM-SOL-003에서 확정 | TP-E-05 executable |
| **DN-04** | Boundary coverage vs pass rate | ESC-02 100% pass vs NFR-02 85% coverage | 둘 다 유지: **pass 100%** + **coverage ≥85%** | CI gate definition |
| **DN-05** | Report/4 파일명 | 사용자 지정 `Report/4.UserJourney_*` vs 저장소 `Report/06` | Report/06 + Level 1~5 세션 산출물을 Report/4 역할로 사용 | 문서 traceability only |

**본 PRD에서 확정한 항목 (충돌 해결):**

- 두 조합 모두 실패 → `DOMAIN-ERR-NO_VALID_PLACEMENT` **구조화 실패 응답** (Report/02 IT-04)
- 입력 검증 실패 → Domain resolver **0회 호출** (US-01)
- 입력 행렬 **변경 금지** (NFR-04)
- Data Layer **Out-of-Scope** (프로젝트 개요 vs Report/02 §3)

---

## 23. Appendix

### 23.1 Reference Documents

| Alias | Repository Path | PRD Usage |
|---|---|---|
| Report/1 | `Report/01.4x4_MagicSquare_Problem_Definition_Report.md` | §2~4 |
| Report/2 | `Report/02.4x4_MagicSquare_TDD_Design_Report.md` | §10~14, §13 errors |
| Report/3 | `Report/03.4x4_MagicSquare_CursorRules_UserEntity_Implementation_Report.md` | §20 |
| Report/4 | `Report/06.MagicSquare_Level1-5_Scenario_Verification_Report.md` + Level 1~5 artifacts | §6~8, §16, §21 |
| Cursor Rules | `.cursorrules`, `.cursor/rules/*.mdc` | §20 |

### 23.2 Cursor Rules Summary

| File | Scope |
|---|---|
| `magicsquare-project.mdc` | Baseline, layout, workflow |
| `magicsquare-ecb-architecture.mdc` | Layer boundaries |
| `magicsquare-python-code-style.mdc` | PEP8, types, docstrings |
| `magicsquare-tdd-testing.mdc` | RED/GREEN/REFACTOR, pytest AAA |
| `magicsquare-forbidden.mdc` | print, bare except, magic numbers, test weakening |

### 23.3 Gherkin Scenario Summary

| Scenario ID | Layer | Summary |
|---|---|---|
| SC-BND-VAL-001 | Boundary | blank count ≠ 2 → fail, Domain not run |
| SC-BND-VAL-002 | Boundary | duplicate → fail, Domain not run |
| SC-BND-VAL-003 | Boundary | range violation → fail, Domain not run |
| SC-BND-VAL-004 | Boundary | not 4×4 → fail, Domain not run |
| SC-DOM-SOL-001 | Domain | small-first fail → reverse success → `[3,3,6,4,4,1]` |
| SC-DOM-SOL-002 | Domain | small-first immediate success |
| SC-DOM-BLK-001 | Domain | 2 blanks row-major |
| SC-DOM-MIS-001/002 | Domain | missing count + ascending order |
| SC-DOM-VAL-001~004 | Domain | row/col/diag fail branches + full pass |

### 23.4 RED Test ID Backlog

| RED ID | Track | Related FR |
|---|---|---|
| RED-BND-VAL-001~004 | A | FR-01 |
| RED-DOM-BLK-001 | B | FR-02 |
| RED-DOM-MIS-001, 002 | B | FR-03 |
| RED-DOM-VAL-001~004 | B | FR-04 |
| RED-DOM-SOL-001, 002, 003 | B | FR-05 |

---

*End of PRD — ready for implementation after DN-01~DN-03 resolution.*
