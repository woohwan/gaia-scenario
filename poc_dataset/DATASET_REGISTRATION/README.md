# Gaia Dataset 등록 계획

`cohesity_gaia_poc_testcases.md`의 50개 TC를 실행하려면 Gaia에 총 **10개**의 Dataset을
등록해야 합니다(선택 사항 1개 포함 시 11개). 아래 표가 "무엇을" 등록할지의 최종안이고,
각 항목의 근거는 표 아래 상세 섹션에 있습니다. "어떻게"(Helios UI 단계별 클릭 순서)는
[`REGISTRATION_STEPS.md`](REGISTRATION_STEPS.md) 참고.

이 폴더의 `.txt` 파일은 각 Dataset에 포함시킬 회사/폴더 목록입니다. `PERF/tier_1gb_companies.txt`,
`PERF/tier_10gb_companies.txt`는 기존 파일을 그대로 재사용합니다.

## 요약 표

| # | Dataset 이름(제안) | Object Type | 소스 | 크기 | Authorized User | 관련 TC |
|---|---|---|---|---|---|---|
| 1 | **Finance-Core** | NAS | `finance_core_companies.txt`의 4개사 (`$GAIA_DATASET_DIR` 기준) | 6.5GB | User A | FUNC-01,03~07 / RAG-01~07 / RBAC-01~08 / SEC-03,04,05 / API-01~07 / PERF-01,02,06 |
| 2 | **HR** | NAS | `../TC-RBAC/dataset_hr_synthetic/` | 수십 KB | User C (User A 미지정) | RBAC-06, SEC-05 |
| 3 | **Mailbox** | M365 Mailbox | 별도 M365 테넌트 백업 필요 (poc_dataset 범위 밖) | — | — | FUNC-02, DATA-08 |
| 4 | **OneDrive** | M365 OneDrive | 별도 M365 테넌트 백업 필요 (poc_dataset 범위 밖) | — | — | FUNC-02, DATA-08 |
| 5 | **Perf-1GB** | NAS | `../PERF/tier_1gb_companies.txt`의 37개사 | 1.02GB | — | DATA-06 |
| 6 | **Perf-10GB** | NAS | `../PERF/tier_10gb_companies.txt`의 130개사 | 10.00GB | — | DATA-06 |
| 7 | **Perf-100GB** | NAS | `$GAIA_DATASET_DIR` 전체(275개사) | 109.94GB | — | DATA-06, PERF-03, PERF-07(대용량 인덱싱 중 질의 대상) |
| 8 | **Perf-200GB** | NAS + NAS | `$GAIA_DATASET_DIR` 전체 + `$GAIA_WEB_DATASET_DIR` 전체 | ≈170GB | — | DATA-06, PERF-03, **DATA-01(대규모 포맷 커버리지 재사용)**, **RAG-07(다국어 재사용)** |
| 9 | **Corrupt-files** | NAS | `../TC-DATA-07_corrupt_files/` (5개 파일) | <1MB | — | DATA-07 |
| 10 | **Freshness** | NAS (Continuous Indexing 활성) | `../TC-DATA-03_05_freshness/` (3개 파일) | <1MB | — | DATA-02,03,04,05 |
| 11 (선택) | **Format-fixture** | NAS | `../TC-DATA-01_format_coverage/content.*` (8개 파일, 동일내용) | <1MB | — | DATA-01 (엄격 비교용) |

> 11번은 굳이 별도로 만들지 않고 Finance-Core에 8개 파일을 얹어도 무방합니다(내용이 작고
> "동일 질문 → 동일 답변" 비교만 하면 되므로 다른 Dataset과 섞여도 문제없음). 분리하는
> 이유는 순수하게 "포맷 자체만 다른, 완전히 통제된 비교군"을 유지하기 위함입니다.

## 지난 답변 대비 달라진 점

1. **Finance-Core를 "전체 103GB"가 아니라 4개사(6.5GB)로 축소했습니다.** RAG golden set이
   실제로 채점에 쓰는 회사는 교보증권/삼성전자/현대자동차 3곳뿐이고(`TC-RAG/golden_set_*.json`,
   `numeric_accuracy_subset.json`의 `company_code` 실측: `030610`/`005930`/`005380`),
   FUNC은 삼양식품(`003230`) 1곳만 씁니다. RBAC/SEC/API/PERF-01,02,06은 회사가 무엇이든
   상관없습니다. "전체 275개사"는 DATA-06/PERF-03(대용량 처리량 측정)에만 필요하므로
   Perf-100GB/Perf-200GB로 따로 뒀습니다. 이렇게 하면 FUNC/RAG/RBAC/SEC/API를 매번
   103GB Dataset의 인덱싱을 기다리지 않고 6.5GB로 빠르게 반복 테스트할 수 있습니다.
2. **"Format/다국어용 별도 Dataset"을 없앴습니다.** TC-DATA-01 대규모 포맷 QA 샘플
   (`qa_pairs_*.json` 100건)이 참조하는 `gaia_web_dataset` 하위 폴더 18개(합계 약 53GB:
   `web_format_coverage_reference_folders.txt` 참고)와, TC-RAG-07 다국어 폴더 3개
   (`english_reference`/`kostat_eng`/`kdischool_eng`, 합계 8.3GB)가 전부 Perf-200GB
   Dataset(`$GAIA_WEB_DATASET_DIR` 전체)에 이미 포함됩니다. 새 Dataset을 만들 필요 없이
   Perf-200GB를 그대로 재사용하면 됩니다.

## Dataset별 상세

### 1. Finance-Core
- **포함 경로**: `finance_core_companies.txt`에 나열된 4개 폴더를
  `$GAIA_DATASET_DIR/<회사명>/` 형태로 Cohesity NAS 소스에 등록 후 Dataset 생성
- **Authorized User**: User A만
- **비고**: TC-RBAC-04/05는 이 Dataset을 "Dataset A"로 사용. TC-SEC-03/04는 이 Dataset에
  `../TC-SEC/injection_docs/`의 3개 인젝션 문서를 추가 인덱싱.

### 2. HR
- **포함 경로**: `../TC-RBAC/dataset_hr_synthetic/` 전체
- **Authorized User**: User C 등 별도 사용자만 (User A 미지정 — TC-RBAC-05/06의 차단 대상)
- **비고**: TC-SEC-05에서 "Dataset B"로 사용

### 3~4. Mailbox / OneDrive
- poc_dataset에 준비된 데이터가 없습니다. 실제 M365 테넌트(Mailbox 1개 이상, OneDrive 1개
  이상)를 Cohesity로 백업한 뒤 그 소스로 Dataset을 생성해야 합니다. TC-FUNC-02, TC-DATA-08
  진행 전 M365 테넌트 연동 여부를 먼저 확인하세요.

### 5~8. Perf-1GB / 10GB / 100GB / 200GB
- 경로는 `../PERF/volume_tiers.md` 그대로 사용 (`../paths_config.py`의
  `GAIA_DATASET_DIR`/`GAIA_WEB_DATASET_DIR` 기준)
- 4개를 동시에 유지할 필요는 없습니다. 다만 **TC-PERF-07**(대용량 Dataset이 인덱싱되는
  동안 다른 기존 Dataset에 질의)을 수행하는 시점에는 Perf-100GB(또는 200GB)와
  Finance-Core가 **동시에** 등록되어 있어야 합니다.
- Perf-200GB는 Perf-100GB(`$GAIA_DATASET_DIR`)에 `$GAIA_WEB_DATASET_DIR` NAS 소스를
  추가로 더해 하나의 Dataset으로 구성하면 됩니다(완전히 새로 만들 필요 없음).

### 9. Corrupt-files
- **포함 경로**: `../TC-DATA-07_corrupt_files/` 5개 파일 전부
- **비고**: 다른 Dataset과 분리하는 이유는 이 Dataset의 Index Status가 의도적으로
  Warning이 되기 때문 — Finance-Core 등 정상 Dataset의 상태 판정과 섞이지 않도록 격리

### 10. Freshness
- **포함 경로**: `../TC-DATA-03_05_freshness/`의 3개 파일
- **사전조건**: Continuous Indexing 활성화 (Cohesity Support 확인 필요, TC-DATA-02 참고)
- **비고**: TC-DATA-04에서 `living_policy_v1_90days.docx` → `living_policy_v2_60days.docx`로
  교체하고, TC-DATA-05에서 `deletion_candidate_falcon7.docx`를 삭제하는 등 이 Dataset의
  소스 파일을 실제로 변경/삭제하는 절차가 있으므로 반드시 별도 격리

### 11. Format-fixture (선택)
- **포함 경로**: `../TC-DATA-01_format_coverage/content.*` 8개 파일
