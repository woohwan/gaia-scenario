# Gaia PoC 전체 실행 순서

`gaia_scenario`(50개 TC 시나리오)와 `gaia_eval`(RAGAS 자동 평가 도구)을 어떤 순서/방법으로
엮어서 실행하는지 정리한 통합 문서입니다. `gaia_scenario`가 뼈대(진행 순서를 결정)이고,
`gaia_eval`은 RAG-01/02/03, PERF-06(일부), API-07 — 이 4곳에서만 "부품"으로 호출됩니다.
그 외 자세한 원본 데이터 위치/환경변수는 [`migration.md`](migration.md)(`migration.txt`와
동일 내용), Dataset 등록 자체는
[`poc_dataset/DATASET_REGISTRATION/README.md`](poc_dataset/DATASET_REGISTRATION/README.md)
를 참고하세요. 이 문서는 그 둘을 전제로 "무엇을 몇 번째로 하는가"만 다룹니다.

## 0단계 — 사전 준비 (한 번만)

1. Gaia Dataset 등록 — `poc_dataset/DATASET_REGISTRATION/README.md`대로 최소 Finance-Core는
   필수 (없으면 아래 전부 의미 없음)
2. `gaia_eval` conda 환경 + API 키 설정 — `migration.txt` 5절
     ```bash
     cd gaia_eval && ./setup_env.sh && conda activate gaia-eval
     export ANTHROPIC_API_KEY=sk-ant-...
     export COHESITY_CLUSTER_URL=https://<helios-fqdn>
     export COHESITY_API_KEY=<api-key>
     export COHESITY_DATASET_NAME=<Finance-Core Dataset 이름>
     ```

## 1단계 — FUNC (사람이 진행, 항상 최우선)

TC-FUNC-01~07. Dataset 생성/기본 QA가 안 되면 이후 전부 무의미하므로 반드시 먼저.

## 2단계 — RAG (7개 중 3개만 `gaia_eval` 자동 호출)

| TC | 방식 | 실행 |
|---|---|---|
| RAG-04 (무응답) | 수동 | `poc_dataset/TC-RAG/no_answer_questions.json` 질문을 UI/curl로 직접 질의 |
| RAG-05 (수치정확도) | 수동 | `numeric_accuracy_subset.json` 질문 직접 질의, 수치 비교 |
| RAG-06 (모호성) | 수동 | `ambiguous_vs_specific_pairs.json` 질문 쌍 직접 질의 후 비교 (RAGAS 자동 채점 대상 아님) |
| RAG-07 (다국어) | 수동 | `gaia_web_dataset`의 `english_reference`/`kostat_eng`/`kdischool_eng` 대상 UI 질의 |
| **RAG-01, RAG-02** | **자동** | 아래 명령 1 (Faithfulness=RAG-01, AnswerRelevancy=RAG-02 동시 산출) |
| **RAG-03** | **자동** | 아래 명령 2 (Context Precision/Recall) |

```bash
cd gaia_eval/gaia_dataset

# 명령 1 — RAG-01/02: POST /ask 기반, Faithfulness + AnswerRelevancy
python convert_scenario_golden_set.py \
    ../../gaia_scenario/poc_dataset/TC-RAG/golden_set_faithfulness_relevancy.json \
    --mode ask
# → output/ragas_eval_results_golden_set_faithfulness_relevancy.csv

# 명령 2 — RAG-03: PUT /ask/exhaustive 기반, Context Precision/Recall
python convert_scenario_golden_set.py \
    ../../gaia_scenario/poc_dataset/TC-RAG/golden_set_context_precision_recall.json \
    --mode exhaustive
# → output/ragas_context_eval_results_golden_set_context_precision_recall.csv
```

먼저 `--max-samples 3` 정도로 소규모 리허설 후 전체 실행을 권장합니다(API 키/Dataset
연결 문제를 30~200회 호출 전에 미리 걸러내기 위함 — `gaia_eval/README.txt` 3절과 같은 이유).

## 3단계 — DATA / RBAC / SEC (전부 수동, `gaia_eval`과 무관)

FUNC 이후라면 순서는 크게 안 중요합니다. `cohesity_gaia_poc_testcases.md` 번호 순서대로
진행하면 무난합니다. TC-DATA-03/04/05는 `poc_dataset/TC-DATA-03_05_freshness/`의 문서를
직접 교체/삭제하는 절차가 있으니 다른 TC와 순서가 꼬이지 않게 이 3개는 묶어서 진행하세요.

## 4단계 — PERF (대부분 수동, PERF-06만 `gaia_eval` 일부 재사용)

PERF-01~05, 07은 인프라 모니터링/부하테스트로 데이터 준비와 무관합니다(`DATASET_REGISTRATION/README.md`
의 Perf-1GB~200GB Dataset만 그때그때 등록). PERF-06(API 오류율/Timeout)은 RAGAS 없이
`gaia_evaluator.query_gaia()`만 반복 호출하면 됩니다:

```python
from gaia_evaluator import query_gaia
import time

for i in range(N):  # 목표 호출 횟수만큼
    try:
        query_gaia("아무 질문")
    except Exception as e:
        print(f"[{i}] error: {e}")
    time.sleep(간격)
```

## 5단계 — API (대부분 수동, API-07은 2단계의 "리허설 재확인")

API-01~06은 curl로 직접 (`cohesity_gaia_api_developer_guide_v1.2.md` 참고). **API-07**
("골든셋→질의→RAGAS→리포트"를 사람 개입 없이 E2E 자동 실행)은 2단계에서 이미 검증한
`convert_scenario_golden_set.py --mode ask`(또는 `--convert-only` 뺀 전체 실행)를 다시
한 번 처음부터 끝까지 무개입으로 돌려서, 중간에 에러 없이 리포트(CSV)까지 생성되는지
확인하는 것으로 충분합니다. 사실상 RAG-01~03의 통합 리허설입니다.

## `gaia_eval`의 자체 파이프라인은 이 순서에 안 낍니다

`gaia_eval`의 원래 기능(`run.sh` / `run_pipeline.py`의 `--step sample/qa/testset/evaluate`
— 자체 랜덤 샘플링으로 새 QA를 만드는 것)은 50개 TC 체크리스트와 별개로, "이 데이터셋
전반의 RAGAS 품질을 더 넓게 보고 싶을 때" 아무 때나 독립적으로 돌리는 보조 도구입니다.
순서상 이 문서의 앞/뒤/중간 어디에 둬도 상관없습니다.

## 전체 순서 요약

```
0. 사전 준비 (Dataset 등록 + gaia_eval 환경/키)
      │
1. FUNC (수동)
      │
2. RAG ──┬─ RAG-04/05/06/07 (수동)
         └─ RAG-01/02, RAG-03 (gaia_eval 자동 호출) ★
      │
3. DATA / RBAC / SEC (수동, 순서 자유)
      │
4. PERF ──┬─ PERF-01~05/07 (수동/인프라)
          └─ PERF-06 (gaia_eval query_gaia() 재사용)
      │
5. API ──┬─ API-01~06 (수동 curl)
         └─ API-07 (gaia_eval E2E 재실행으로 검증) ★

  ★ = gaia_eval 개입 지점 (2군데: RAG 섹션의 golden set 평가, API-07의 E2E 리허설)
```
