# TC-RAG-01~07 — RAG 품질 골든셋

원본(`$GAIA_DATASET_DIR`, `$GAIA_WEB_DATASET_DIR` — 기본값은 `../paths_config.py` 참고)은
그대로 두고, 이미 존재하던 LLM 생성 QA 산출물(`$GAIA_RAGAS_EVAL_DIR/qa_pairs_mixed.json`,
기본값 `/data/richard/cohesity-poc/gaia_ragas/eval/qa_pairs_mixed.json`, 200개,
교보증권/삼성전자/현대자동차 혼합)에서 PoC 규모에 맞게 재추출했습니다. 신규 LLM 호출 없이
기존 산출물만 샘플링/가공했습니다.

**주의**: 아래 golden set의 JSON 파일 자체(질문/정답/근거문단)는 원본이 없어도 읽을 수
있지만, 실제로 Cohesity Gaia에 질의해서 채점하려면 근거 문서(교보증권/삼성전자/현대자동차
공시)가 `$GAIA_DATASET_DIR`에 실제로 존재하고 Dataset으로 인덱싱되어 있어야 합니다.

| 파일 | 용도 | 개수 |
|---|---|---|
| `golden_set_faithfulness_relevancy.json` | TC-RAG-01 (Faithfulness), TC-RAG-02 (Response Relevancy) | 30 (3사×10, 균형 샘플링) |
| `golden_set_context_precision_recall.json` | TC-RAG-03 (Context Precision/Recall) — `ground_truth_context`가 정답 근거 문서 태깅 역할 | 20 |
| `numeric_accuracy_subset.json` | TC-RAG-05 (수치 정확도) — question_type=financial만 필터링 | 15 |
| `no_answer_questions.json` | TC-RAG-04 (No-answer correctness) — Dataset 범위 밖 질문 10개 직접 작성 | 10 |
| `ambiguous_vs_specific_pairs.json` | TC-RAG-06 (모호성에 따른 답변 품질) — 동일 주제 구체/모호 질문 쌍 | 5 |

각 항목 필드: `question`(질의), `ground_truth_answer`(정답), `ground_truth_context`(근거
원문), `company`/`company_code`/`doc_id`/`filing_date`(출처), `question_type`.
GaiaAPIClient.ask()로 실제 `answer`/`contexts`를 수집한 뒤 이 골든셋의 `ground_truth_*`와
비교해 RAGAS 지표(faithfulness, relevancy, context_precision, context_recall)를 계산하면
됩니다 (`collector/eval/gaia_evaluator.py`, `gaia_ragas/gaia_evaluator.py` 로직 재사용 가능).

## TC-RAG-07 (다국어 질의응답)
- **영어**: 원본에 이미 존재 — `$GAIA_WEB_DATASET_DIR/english_reference/`(1,332개),
  `$GAIA_WEB_DATASET_DIR/kostat_eng/`(3,307개), `$GAIA_WEB_DATASET_DIR/kdischool_eng/`
  (966개) 등에서 20~30개 샘플링해 영어 질의응답 테스트 가능.
- **네덜란드어**: 원본에 전혀 없음. 이번 PoC 범위에서는 **제외**하기로 결정함(사용자 확인,
  2026-08-11). 추후 필요 시 영어 문서 일부를 LLM으로 번역해 합성해야 함.

## TC-DATA-01 관련
포맷별 golden set은 `../TC-DATA-01_format_coverage/README.md` 참고 (`$COLLECTOR_EVAL_OUTPUT_DIR`
의 기존 pdf/docx_doc/xlsx_xls_csv/ppt_pptx QA 200개씩 재사용).
