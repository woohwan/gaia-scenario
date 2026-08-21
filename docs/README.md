# Gaia PoC 테스트 시나리오 — API/RAG 제외 버전

Cohesity Gaia가 아직 REST API(GAIA_VIEW 등)를 제공하지 않는 상태에서, **API 호출/RAGAS
자동 채점, RAG 품질(TC-RAG 전체) 관련 TC를 모두 제외**하고 사람이 Helios UI(Gaia AI
Assistant)로 직접 수행할 수 있는 테스트 시나리오만 정리한 문서입니다.

**이 `docs/` 폴더(00~06번 절차 문서 7개 + `QA_*.md` 5개, 총 12개 문서)만으로 테스트를
처음부터 끝까지 수행할 수 있습니다.**
Dataset을 어디에 어떻게 만드는지, 어떤 데이터를 올리는지, 어떤 질문을 어떻게 판정하는지
전부 각 문서 안에 직접 적혀 있으며, 이 저장소의 다른 위치(`poc_dataset/`의 각 하위
README, 루트의 `cohesity_gaia_poc_testcases.md`/`EXECUTION_ORDER.md`/`migration.md` 등)를
열어볼 필요가 없습니다. 다만 합성 문서(docx/xlsx/pdf 등)처럼 실제로 업로드해야 하는
**데이터 파일 자체**는 이 저장소의 `poc_dataset/` 아래에 이미 만들어져 있으므로, 각 절차에
그 파일 경로를 "업로드 대상"으로만 직접 명시했습니다(그 경로에 있는 설명 문서를 열어볼
필요는 없습니다).

## 처음 시작하기 (Quick Start)

Gaia는 **Dataset**(파일 묶음)을 만들고 인덱싱이 끝나야만 그 안에서 질문할 수 있습니다.
그래서 모든 테스트는 "① 필요한 Dataset이 있는지 확인 → ② 없으면 만들기 → ③ 해당 TC
문서를 열어 순서대로 클릭/질문"의 반복입니다. 아래 순서 그대로 따라가면 됩니다.

### 1단계 — 첫 Dataset 만들기

[00_COMMON_SETUP.md](00_COMMON_SETUP.md)를 처음부터 다 읽지 말고, 아래 3곳만 펼쳐서
순서대로 실행합니다.

1. **0.2절**을 열어, 삼양식품/현대자동차/삼성전자/교보증권 4개사 폴더를 Cohesity에
   백업합니다(NAS 소스 등록 — Gaia Dataset은 이미 백업된 데이터에서만 만들 수 있어서
   반드시 먼저 해야 하는 선행 작업입니다).
2. **0.4절 표의 1번째 줄**(`finance-core`)을 열어 입력할 값 3가지를 확인합니다 —
   Dataset 이름 `finance-core`, 포함 경로는 1번에서 백업한 4개사, Authorized User는
   User A.
3. **0.3절**을 열어 9단계(Helios 클릭 순서)를 그대로 따라가며, 입력이 필요한 곳마다
   2번에서 확인한 값을 넣습니다.
4. Index Status가 `Succeeded`로 바뀔 때까지 기다립니다.

### 2단계 — 첫 테스트 실행

[01_FUNC.md](01_FUNC.md)를 열어 TC-FUNC-01, 03~07을(파일에 있는 순서 그대로,
TC-FUNC-02는 이 문서 세트에 없음) 위에서 아래로 그냥 따라 합니다. Dataset은 1단계에서
이미 만들었으니 각 TC의 "테스트 수행 절차"부터 바로 시작하면 됩니다. 여기까지 끝내면
첫 카테고리(기능 검증)가 끝납니다.

### 3단계 — 나머지 반복

[03_DATA.md](03_DATA.md), [04_RBAC.md](04_RBAC.md), [05_SEC.md](05_SEC.md),
[06_PERF.md](06_PERF.md)도 똑같은 패턴입니다.

1. 각 TC 상단에 "이 TC는 어떤 Dataset이 필요하다"고 적혀 있습니다.
2. 그 Dataset이 00_COMMON_SETUP.md 0.4절 표에 몇 번인지 찾습니다.
3. 아직 안 만들었으면 1단계와 같은 방식(0.2절 백업 → 0.4절 표 값 확인 → 0.3절
   9단계 실행)으로 만들고, 이미 만들었으면 그냥 재사용합니다.
4. 그 TC의 절차를 따라갑니다.

FUNC 이후로는 어느 문서부터 봐도 상관없습니다(자세한 순서 팁은 아래 "실행 순서" 참고).

## 이 문서 세트가 다루는 범위

| 파일 | 내용 |
|---|---|
| [00_COMMON_SETUP.md](00_COMMON_SETUP.md) | 환경 변수, NAS 백업/Dataset 생성 공통 절차, 이 세트가 쓰는 전체 Dataset 목록·회사 목록, 테스트 계정, Continuous Indexing 활성화 절차 |
| [01_FUNC.md](01_FUNC.md) | 기능 검증 — TC-FUNC-01, 03~07 (6개) |
| [03_DATA.md](03_DATA.md) | 데이터/인덱싱 — TC-DATA-01~07 (7개) |
| [04_RBAC.md](04_RBAC.md) | 권한/RBAC — TC-RBAC-01~08 (8개, 전체) |
| [05_SEC.md](05_SEC.md) | AI Security — TC-SEC-01~06 (6개, 전체) |
| [06_PERF.md](06_PERF.md) | 운영/성능(API 비의존 항목만) — TC-PERF-01, 02, 03, 04, 05, 07 (6개) |
| **합계** | **33 / 50 TC** |

번호가 02(RAG)로 비어 보이는 것은 의도된 것입니다 — RAG 품질 대분류(TC-RAG-01~07) 전체가
이번 범위에서 빠졌기 때문에 `02_RAG.md` 파일 자체를 두지 않았습니다.

### QA(질문-정답-근거) 세트

여러 TC에서 "동일 질문셋"이 필요할 때 즉석에서 질문을 만들지 않도록, Dataset별 QA 문서를
따로 준비했습니다. 전부 실제 문서 내용에서 직접 추출한 사실 기반입니다(허구 데이터 없음).

| 파일 | 대상 Dataset | 개수 |
|---|---|---|
| [QA_finance_core.md](QA_finance_core.md) | `finance-core` | 50 |
| [QA_perf_common.md](QA_perf_common.md) | `perf-1gb`/`10gb`/`100gb`/`200gb` 공통 | 50 |
| [QA_format_fixture.md](QA_format_fixture.md) | `format-fixture` | 4 (+선택 100) |
| [QA_hr_synthetic.md](QA_hr_synthetic.md) | `hr-synthetic` | 25 (원본 분량 한계) |
| [QA_small_fixtures.md](QA_small_fixtures.md) | `freshness` + `corrupt-files` | 4 + 4 = 8 (원본 분량 한계) |

5개 파일 모두 `docs/` 안에 있으므로, `poc_dataset/`의 원본 json/md를 직접 열어볼 필요
없이 이 문서들만으로 질문·정답·근거를 확인할 수 있습니다.

## 이번 범위에서 제외한 17개 TC와 이유

### 1) API가 없어서 제외 (11개)

Cohesity Gaia REST API(`/ask`, `/ask/exhaustive`, `/datasets`, `/discovery` 등)가 아직
제공되지 않아, API 호출 자체가 전제조건인 TC와 API 응답을 자동 채점(RAGAS)하는 TC는
제외했습니다.

| TC | 제외 사유 |
|---|---|
| TC-RAG-01 (Faithfulness) | REST API 반복 호출 + RAGAS 자동 채점 필요 |
| TC-RAG-02 (Response Relevancy) | 상동 |
| TC-RAG-03 (Context Precision/Recall) | REST API(`/ask/exhaustive`) 호출 + RAGAS 자동 채점 필요 |
| TC-PERF-06 (API 오류율/Timeout) | REST API를 반복 호출하는 것이 테스트 방법 자체 |
| TC-API-01~07 (7개) | 전부 REST API 엔드포인트 직접 호출이 테스트 대상 |

### 2) 사용자 요청으로 제외 — RAG 품질 전체 + 기타 2개 (6개)

RAGAS 자동 채점과 무관하게 UI로 수동 수행이 가능했던 나머지 RAG 항목과, NAS 외 다른
소스 유형이 필요한 TC 2개도 이번 범위에서 함께 제외했습니다.

| TC | 대분류 | 제외 사유 |
|---|---|---|
| TC-RAG-04 (No-answer correctness) | RAG | RAG 품질 대분류 전체 제외 |
| TC-RAG-05 (수치 정확도) | RAG | 상동 |
| TC-RAG-06 (모호성에 따른 답변 품질) | RAG | 상동 |
| TC-RAG-07 (다국어 질의응답) | RAG | 상동 |
| TC-FUNC-02 (Object Type별 Dataset 생성) | FUNC | NAS 외 Object Type이 테스트 대상 |
| TC-DATA-08 (Include-Exclude 제약) | DATA | NAS 외 소스 유형이 테스트 대상 |

이 17개 TC는 이번 문서 세트에서 다루지 않으므로 별도의 데이터/Dataset 준비 안내도 포함하지
않았습니다. 범위를 넓힐 필요가 생기면 이 문서 세트와 동일한 구조(목적 → 데이터 준비 →
수행 절차 → 합격기준 → 결과 기록)로 새 문서를 추가하면 됩니다.

## 실행 순서 (위 Quick Start의 3단계를 진행할 때 참고할 세부 팁)

1. [01_FUNC.md](01_FUNC.md)를 가장 먼저 끝냅니다 — 기본 워크플로우(Dataset 생성,
   질의응답)가 안 되면 나머지는 의미가 없습니다.
2. [03_DATA.md](03_DATA.md), [04_RBAC.md](04_RBAC.md), [05_SEC.md](05_SEC.md) — 세
   문서는 순서와 무관하게 진행 가능합니다. 단, TC-DATA-03/04/05는 같은 `freshness`
   Dataset의 소스 파일을 직접 교체/삭제하는 절차이므로 세 TC를 묶어서 진행하세요.
3. [06_PERF.md](06_PERF.md) — 대부분 인프라 모니터링/측정이라 마지막에 진행해도 무방하나,
   TC-PERF-07은 `perf-100gb`(또는 200gb)와 `finance-core`가 동시에 등록되어 있어야
   하므로 이 둘의 등록 시점을 미리 맞춰 두세요.

## 각 TC 문서의 공통 구조

01~06번 문서는 TC별로 아래 5개 절을 동일한 순서로 담고 있습니다.

1. **목적 / 중요도** — TC가 검증하는 내용 + P1/P2/P3 등급
2. **데이터 준비 (생성)** — 이 TC에 쓰이는 데이터 파일의 정확한 경로/내용과, 필요한 경우
   `00_COMMON_SETUP.md` 0.4 레지스트리를 참조해 만드는 Dataset의 이름/포함 경로/
   Authorized User
3. **테스트 수행 절차** — Helios/Gaia AI Assistant UI에서 클릭 단위로 따라 할 수 있는 단계
4. **예상 결과 / 합격 기준** — PASS/FAIL을 판정할 수 있는 구체적 기준
5. **결과 기록 템플릿** — 결과와 근거를 남길 수 있는 표

## 결과 취합

각 문서에서 얻은 TC별 결과는 하나의 결과표(TC 코드, 담당자, 수행일, PASS/FAIL, 비고 열을
가진 스프레드시트 등)에 취합하는 것을 권장합니다. API 제공 및 RAG 범위 포함 결정 이후에는
이 문서 세트의 결과와 나머지 17개 TC(RAG 전체 7개, TC-FUNC-02, TC-DATA-08, TC-PERF-06,
TC-API-01~07) 결과를 합쳐 50개 전체 결과표를 완성하면 됩니다.
