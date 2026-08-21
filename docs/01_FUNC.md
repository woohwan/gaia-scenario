# 1. 기능 검증 (TC-FUNC-01, 03~07)

Dataset 생성부터 대화형 질의응답까지 기본 워크플로우가 정상 동작하는지 확인합니다.
**TC-FUNC-02(NAS 외 Object Type Dataset 생성)는 이번 범위에서 제외**했습니다(NAS만
다루는 나머지 6개는 API/RAGAS 없이 UI만으로 수행 가능하므로 포함).

## 공통 사전 준비

### 사용 데이터
- **`finance-core` Dataset** — 이 문서의 모든 TC(01, 03~07)의 기본 대상. 삼양식품/
  현대자동차/삼성전자/교보증권 4개사, `$GAIA_DATASET_DIR` 기준 6.5GB. Dataset 정의는
  [00_COMMON_SETUP.md](00_COMMON_SETUP.md) 0.4 레지스트리 #1과 동일합니다.
- 소규모로 빠르게 반복 확인하고 싶다면 이 저장소의 `poc_dataset/TC-FUNC/sample_dataset/`
  폴더(삼양식품 1개사, 123MB, 233개 DART 공시 PDF/XLS/XML 파일, 이미 준비되어 있음)를
  별도 NAS 경로에 올려 사용해도 됩니다.

### Dataset 등록값

| Dataset 이름 | Object Type | 포함 경로 | Authorized User |
|---|---|---|---|
| `finance-core` | NAS | `$GAIA_DATASET_DIR/003230_삼양식품/`, `$GAIA_DATASET_DIR/005380_현대자동차/`, `$GAIA_DATASET_DIR/005930_삼성전자/`, `$GAIA_DATASET_DIR/030610_교보증권/` | User A |

---

## TC-FUNC-01 — Dataset 생성 - 기본 흐름 `[P1]`

**목적**: Gaia Dataset 생성 워크플로우 자체가 오류 없이 동작하는지 확인.

### 데이터 준비
1. 위 4개 회사 경로를 [00_COMMON_SETUP.md](00_COMMON_SETUP.md) 0.2절 절차대로 NAS 소스로
   Cohesity에 백업합니다(Helios 로그인 → Protection > Sources에 NAS 등록 → 해당 4개 경로로
   Protection Group 생성 → 백업 1회 성공까지 대기).
2. 백업이 최소 1회 성공해 "보호된 데이터 소스"로 노출되는지 Data Insights에서 확인합니다.

### 테스트 수행 절차
[00_COMMON_SETUP.md](00_COMMON_SETUP.md) 0.3절의 Dataset 생성 공통 절차를 아래 값으로
수행합니다:
1. Gaia Admin 역할 사용자로 Helios(Self-Managed) 로그인.
2. **Insights > Data Insights > Create Dataset** 이동.
3. Dataset 이름 `finance-core` 입력, Object Type `NAS` 선택.
4. 1단계에서 백업한 4개 회사 경로를 소스 목록에서 체크.
5. **Authorized Users**에 User A 지정.
6. **Create** 클릭.
7. Index Status가 `Running` → `Succeeded`로 바뀔 때까지 대기(수 분~수십 분, 6.5GB 기준).

### 예상 결과 / 합격 기준
- Dataset이 생성되고 Indexing이 자동 시작되며 Datasets 목록에 `finance-core`가 표시됨.
- 생성 완료까지 오류 메시지 없음, Index Status가 최종적으로 `Succeeded`.

### 결과 기록
| 항목 | 결과 | 비고 |
|---|---|---|
| Dataset 생성 오류 여부 | PASS/FAIL | |
| Index Status 최종값 | Succeeded/Warning/Failed | |
| Indexing 소요 시간 | ___분 | |

---

## TC-FUNC-03 — 단일 질문-답변 기본 동작 `[P1]`

**사전조건**: TC-FUNC-01의 `finance-core` Dataset이 Index Status `Succeeded`.

### 테스트 수행 절차
1. Gaia - AI Assistant 화면 진입, Dataset으로 `finance-core` 선택.
2. [QA_finance_core.md](QA_finance_core.md)에서 질문 1개를 골라(예: 1번) 그대로 입력합니다.
3. 답변과 함께 Citation이 표시되는지 확인하고, QA 문서의 "정답"·"근거"와 대조합니다.

### 예상 결과 / 합격 기준
- 질문과 관련된 정확한 답변이 생성되고 Citation이 함께 표시됨.
- 답변 내용이 원문과 사실관계 일치, Citation 최소 1개 이상 표시.

### 결과 기록
| 질문 | 답변 정확성 | Citation 개수 | 비고 |
|---|---|---|---|
| | PASS/FAIL | | |

---

## TC-FUNC-04 — Citation 표시 및 원문 이동 `[P1]`

**사전조건**: TC-FUNC-03 완료(답변 및 Citation 존재).

### 테스트 수행 절차
1. TC-FUNC-03에서 얻은 답변의 Citation에 마우스를 올려(또는 클릭해) 원문 텍스트
   reference를 확인.
2. Citation이 가리키는 문서명·페이지/구간이 실제 근거와 일치하는지 원본 파일(NAS 경로
   또는 다운로드된 사본)과 직접 대조.

### 예상 결과 / 합격 기준
- Citation이 가리키는 문서의 관련 텍스트가 정확히 표시됨.
- Citation이 실제 근거 문서/구간과 100% 일치.

### 결과 기록
| Citation 대상 문서 | 원문 대조 결과 | 비고 |
|---|---|---|
| | 일치/불일치 | |

---

## TC-FUNC-05 — Source Reference 다운로드 `[P2]`

**사전조건**: TC-FUNC-03 완료.

### 테스트 수행 절차
1. 답변 화면에서 **Source References** 클릭.
2. 다운로드 아이콘 클릭해 원본 파일 다운로드.
3. 다운로드된 파일을 열어 손상 여부 확인, Citation 내용과 일치하는지 대조.

### 예상 결과 / 합격 기준
- 원본 파일이 정상적으로 다운로드됨.
- 다운로드된 파일이 손상 없이 열리고 Citation 내용과 일치.

### 결과 기록
| 다운로드 파일 | 정상 오픈 여부 | Citation 내용 일치 | 비고 |
|---|---|---|---|
| | | | |

---

## TC-FUNC-06 — Multi-turn 대화 (맥락 유지) `[P2]`

**사전조건**: TC-FUNC-03 완료.

### 테스트 수행 절차
1. 1차 질문 입력([QA_finance_core.md](QA_finance_core.md) 7번 재사용): "삼양식품(주)이
   제65기 사업보고서를 한국거래소에 제출한 날짜는 언제입니까?" → 정답 2026년 3월 18일.
2. 주어를 생략한 후속 질문을 연속 입력: "그 보고서의 대표이사는 누구야?" (QA 9번과 동일
   사실 — 정답 "김정수, 김동찬").
3. 이전 대화 맥락(주어="그 보고서"=2026-03-18 제출 삼양식품 사업보고서)을 이해하고 QA
   9번의 정답과 일치하는 답변을 제공하는지 확인.

### 예상 결과 / 합격 기준
- 이전 대화 맥락(주어, 시점, 대상)을 이해하고 일관된 답변 제공.
- 후속 질문에서 맥락 정보 재입력 없이도 정확한 답변 도출.

### 결과 기록
| 1차 질문 | 후속 질문 | 맥락 유지 여부 | 비고 |
|---|---|---|---|
| | | PASS/FAIL | |

---

## TC-FUNC-07 — Chat History 조회 및 비활성화 `[P3]`

**사전조건**: TC-FUNC-03/06 등으로 이전 대화 이력이 존재.

### 테스트 수행 절차
1. **Settings > Preferences**에서 Chat History 조회, 기존 대화 이력이 남아있는지 확인.
2. Chat History 토글을 Off로 변경.
3. Off 상태에서 신규 질문을 1건 입력.
4. Chat History 목록을 다시 열어 방금 입력한 신규 대화가 저장되지 않았는지 확인.

### 예상 결과 / 합격 기준
- 이력 조회 가능하며, Off 설정 후 신규 대화가 저장되지 않음.
- 토글 Off 이후 신규 대화 미저장 확인.

### 결과 기록
| 단계 | 결과 | 비고 |
|---|---|---|
| Off 이전 이력 조회 | PASS/FAIL | |
| Off 이후 신규 대화 미저장 | PASS/FAIL | |
